# run_tests.ps1
$ErrorActionPreference = 'Stop'

# 1) Clean previous results
if (Test-Path 'allure-results') { Remove-Item 'allure-results' -Recurse -Force }
if (Test-Path 'allure-report')  { Remove-Item 'allure-report'  -Recurse -Force }

# 1.1) Ensure categories.json exists (for severity widget on Overview)
$categoriesPath = 'categories.json'
if (-not (Test-Path $categoriesPath)) {
@'
[
  { "name": "Blocker",  "matchedStatuses": ["failed","broken"], "messageRegex": ".*", "traceRegex": ".*", "severity": "blocker"  },
  { "name": "Critical", "matchedStatuses": ["failed","broken"], "messageRegex": ".*", "traceRegex": ".*", "severity": "critical" },
  { "name": "Normal",   "matchedStatuses": ["failed","broken"], "messageRegex": ".*", "traceRegex": ".*", "severity": "normal"   },
  { "name": "Minor",    "matchedStatuses": ["failed","broken"], "messageRegex": ".*", "traceRegex": ".*", "severity": "minor"    },
  { "name": "Trivial",  "matchedStatuses": ["failed","broken"], "messageRegex": ".*", "traceRegex": ".*", "severity": "trivial"  }
]
'@ | Set-Content -LiteralPath $categoriesPath -Encoding UTF8
}

# 2) Run pytest and write results to allure-results
pytest --alluredir=allure-results -v

# 3) Copy categories.json into allure-results
Copy-Item $categoriesPath 'allure-results/categories.json' -Force

# 4) Generate and open Allure report
allure generate 'allure-results' --clean -o 'allure-report'
allure open 'allure-report'