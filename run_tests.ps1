# 1. Чистимо попередні результати
if (Test-Path "allure-results") {
    Remove-Item "allure-results" -Recurse -Force
}
if (Test-Path "allure-report") {
    Remove-Item "allure-report" -Recurse -Force
}

# 2. Запускаємо Pytest з Allure
pytest --alluredir=allure-results -v

# 3. Копіюємо categories.json (якщо існує)
if (Test-Path "categories.json") {
    Copy-Item "categories.json" "allure-results/categories.json" -Force
}

# 4. Генеруємо репорт
allure generate allure-results --clean -o allure-report

# 5. Відкриваємо репорт у браузері
allure open allure-report