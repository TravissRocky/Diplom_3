# Автоматизация тестирования Stellar Burgers

Проект содержит UI-автотесты на Python + Selenium для веб‑приложения [Stellar Burgers](https://stellarburgers.education-services.ru/). Покрыты сценарии восстановления пароля, работы личного кабинета, конструктора бургеров и раздела «Лента заказов».

## Стек
- Python 3.11+
- pytest
- Selenium 4 (Chrome и Firefox через Selenium Manager)
- Allure
- requests (API-подготовка тестовых данных)

## Подготовка окружения
```bash
pip install -r requirements.txt
```

## Запуск тестов
Гонка всего набора сразу в двух браузерах:
```bash
pytest --alluredir=allure-results
```

Только Chrome или Firefox:
```bash
pytest --browser=chrome --alluredir=allure-results
pytest --browser=firefox --alluredir=allure-results


## Allure-отчёт
```bash
allure serve allure-results
```

## Структура
- `pages/` — Page Object классы
- `locators/` — все локаторы
- `tests/` — pytest-сuites по функционалу
- `helpers/` — API-клиент и генератор данных
- `data/` — константы и URL’ы
