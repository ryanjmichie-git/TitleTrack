# Builds data/raw/top40_titles.json from files already in data/raw/.
# Fully offline - no network calls. Re-run after refreshing data/raw/.
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$raw  = Join-Path $root 'data\raw'
$AS_OF = [datetime]'2026-08-07'

# --- Employers that run civil-service exams but do NOT appear in the citywide
# --- payroll file (k397-673e). Derived from k397_agencies_2025.json: no agency
# --- matching HOSPITAL / H+H / TRANSIT exists in FY2025 payroll.
# --- NOTE: HOUSING AUTHORITY *is* present (NYC HOUSING AUTHORITY, 14,297 rows),
# --- so it is deliberately NOT in this list.
$FOREIGN_EMPLOYER = @('NYC H+H', 'H+H', 'HOSPITALS', 'TRANSIT AUTHORITY')

# open_competitive_promotion conflates ELIGIBILITY with STATUS. Map only the
# eligibility values; statuses (Canceled/Postponed) yield a null eligibility.
$ELIGIBILITY = @{
  'OPEN COMPETITIVE'          = 'Open Competitive'
  'PROMOTION'                 = 'Promotion'
  'QIE'                       = 'Qualified Incumbent Exam'
  'QUALIFIED INCUMBENT EXAM'  = 'Qualified Incumbent Exam'
}
$STATUS_ONLY = @('CANCELED', 'POSTPONED')

function Norm([string]$s) {
  if (-not $s) { return '' }
  (($s -replace '\([^)]*\)', '') -replace '\s+', ' ').ToUpper().Trim()
}

function Median([double[]]$v) {
  if ($v.Count -eq 0) { return $null }
  $s = [double[]]($v | Sort-Object)
  $n = $s.Count
  if ($n % 2 -eq 1) { return $s[[int](($n - 1) / 2)] }
  return ($s[$n / 2 - 1] + $s[$n / 2]) / 2
}

# ---- 1. top 40 titles by FY2025 headcount (all pay bases) ----
$top = Get-Content (Join-Path $raw 'k397_top40_headcount_2025.json') -Raw | ConvertFrom-Json

# ---- 2. per Annum salaries, bucketed by title ----
$byTitle = @{}
Get-ChildItem $raw -Filter 'k397_perannum_2025_chunk*.csv' | Sort-Object Name | ForEach-Object {
  Import-Csv $_.FullName | ForEach-Object {
    $t = $_.title_description
    if (-not $t) { return }
    if (-not $byTitle.ContainsKey($t)) { $byTitle[$t] = [System.Collections.Generic.List[double]]::new() }
    $byTitle[$t].Add([double]$_.base_salary)
  }
}

# ---- 3. exams, normalized and indexed by normalized title ----
$exams = Get-Content (Join-Path $raw '4ptz-hmtc_full.json') -Raw | ConvertFrom-Json
$examIdx = @{}
foreach ($e in $exams) {
  if (-not $e.exam_title) { continue }
  $k = Norm $e.exam_title
  if (-not $examIdx.ContainsKey($k)) { $examIdx[$k] = [System.Collections.ArrayList]::new() }
  $null = $examIdx[$k].Add($e)
}

function Get-OpenExams([string]$titleDesc) {
  $k = Norm $titleDesc
  $hits = $examIdx[$k]
  $result = [System.Collections.ArrayList]::new()
  if (-not $hits) { return $result }
  foreach ($e in $hits) {
    $rawVal = $e.open_competitive_promotion
    $up = if ($rawVal) { $rawVal.ToUpper().Trim() } else { '' }
    if ($up -eq 'CANCELED') { continue }   # cancelled exams are not open

    $start = if ($e.application_period_start)    { [datetime]$e.application_period_start }    else { $null }
    $end   = if ($e.application_period_end_date) { [datetime]$e.application_period_end_date } else { $null }
    # "open" = window still open, or window entirely in the future
    $isOpen = ($end -ne $null -and $end -ge $AS_OF) -or ($end -eq $null -and $start -ne $null -and $start -gt $AS_OF)
    if (-not $isOpen) { continue }

    $elig = $null
    if ($ELIGIBILITY.ContainsKey($up)) { $elig = $ELIGIBILITY[$up] }

    $upTitle = $e.exam_title.ToUpper()
    $same = $true
    foreach ($m in $FOREIGN_EMPLOYER) { if ($upTitle -match [regex]::Escape("($m)")) { $same = $false } }

    $null = $result.Add([ordered]@{
      exam_number               = $e.exam_number
      exam_title                = $e.exam_title
      application_period_start  = if ($start) { $start.ToString('yyyy-MM-dd') } else { $null }
      application_period_end    = if ($end)   { $end.ToString('yyyy-MM-dd') }   else { $null }
      eligibility               = $elig
      eligibility_source_value  = $rawVal
      same_employer             = $same
    })
  }
  return $result
}

# ---- 4. assemble ----
$titles = [System.Collections.ArrayList]::new()
$rank = 0
foreach ($t in $top) {
  $rank++
  $name = $t.title_description
  $head = [int]$t.count_1
  $vals = if ($byTitle.ContainsKey($name)) { $byTitle[$name].ToArray() } else { @() }
  $nInc = $vals.Count
  $med  = Median $vals
  $null = $titles.Add([ordered]@{
    rank              = $rank
    title_description = $name
    headcount_fy2025  = $head
    salary            = [ordered]@{
      basis      = 'per Annum'
      median     = if ($med -ne $null) { [int][math]::Round($med, 0) } else { $null }
      n_included = $nInc
      n_excluded = $head - $nInc
    }
    open_exams        = @(Get-OpenExams $name)
  })
}

$doc = [ordered]@{
  generated_as_of = $AS_OF.ToString('yyyy-MM-dd')
  sources = [ordered]@{
    payroll = [ordered]@{
      dataset = 'k397-673e'; name = 'Citywide Payroll Data (Fiscal Year)'
      attribution = 'Office of Payroll Administration (OPA)'
      fiscal_year = 2025; rows_updated_at = '2026-04-16'
    }
    exams = [ordered]@{
      dataset = '4ptz-hmtc'; name = 'Annual Examination Schedule of Each Fiscal Year'
      attribution = 'Department of Citywide Administrative Services (DCAS)'
      rows_updated_at = '2026-07-22'
    }
  }
  definitions = [ordered]@{
    headcount_fy2025 = 'FY2025 payroll rows for this title_description, ALL pay bases. One row = one person-year per agency; a person in two agencies appears twice.'
    salary_median    = "Median base_salary over FY2025 rows with pay_basis='per Annum' and non-null base_salary. per Day / per Hour / Prorated Annual rows are EXCLUDED, not converted - base_salary means a different unit in each basis and the per Hour column is known to contain misfiled annual figures (FY2025 max 190941.71)."
    n_included       = 'per Annum rows contributing to the median.'
    n_excluded       = 'headcount_fy2025 minus n_included: rows dropped for non-annual pay basis or null base_salary.'
    open_exams       = "Exams from 4ptz-hmtc whose title matches this payroll title after uppercasing and stripping parentheticals, that are not Canceled, and whose application window is still open or entirely in the future as of generated_as_of."
    eligibility      = "Normalized from open_competitive_promotion. That column conflates eligibility with schedule status, so rows carrying only a status (Postponed) yield null. Raw value kept in eligibility_source_value."
    same_employer    = "False when the exam is for an employer absent from the citywide payroll file (NYC H+H, Hospitals, Transit Authority) - those hires can never appear in k397-673e. Verified against FY2025 agency_name list; NYC Housing Authority IS in payroll and is therefore true."
  }
  caveats = @(
    'A null salary.median means the title has zero per Annum rows - it is paid per Day, per Hour, or per Session. It is not missing data.',
    'Title matching is text-based: 4ptz-hmtc title_code is populated on only 367 of 2901 rows (12.7%), so it is unusable as a join key.',
    'CUNY community colleges ARE in payroll (19,863 FY2025 rows under COMMUNITY COLLEGE agency names), so their exams are correctly same_employer=true; senior colleges are state-funded and absent, so treat any senior-college CUNY exam as foreign despite the flag. An earlier version of this caveat keyed the check on CUNY CENTRAL OFFICE (217 rows) and wrongly called CUNY staff largely absent.',
    'work_location_borough is the agency location, not the employee location.'
  )
  titles = $titles
}

$dest = Join-Path $raw 'top40_titles.json'
$doc | ConvertTo-Json -Depth 8 | Out-File -Encoding utf8 $dest
"WROTE $dest ($((Get-Item $dest).Length) bytes)"
