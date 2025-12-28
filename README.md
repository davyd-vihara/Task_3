# Тестирование веб-приложения Stellar Burgers

Проект автоматизированного тестирования веб-приложения Stellar Burgers с использованием Selenium WebDriver, Pytest и Allure.

## Структура проекта

```
Task_3/
├── tests/                    # Тесты
│   ├── __init__.py
│   ├── conftest.py          # Фикстуры Pytest
│   ├── test_login.py        # Тесты входа/выхода
│   ├── test_password_recovery.py
│   ├── test_constructor.py
│   ├── test_order_feed.py
│   └── test_user_profile.py
│
├── pages/                    # Page Object Model
│   ├── __init__.py
│   ├── base_page.py         # Базовый класс страницы
│   ├── login_page.py        # Страница входа
│   ├── main_page.py         # Главная страница
│   ├── password_recovery_page.py
│   ├── profile_page.py      # Личный кабинет
│   ├── constructor_page.py  # Конструктор бургеров
│   └── order_feed_page.py   # Лента заказов
│
├── locators/                 # Локаторы
│   ├── __init__.py
│   ├── base_locators.py
│   ├── login_locators.py
│   ├── main_locators.py
│   ├── profile_locators.py
│   ├── password_recovery_locators.py
│   ├── constructor_locators.py
│   └── order_feed_locators.py
│
├── utils/                    # Утилиты
│   ├── __init__.py
│   ├── driver_factory.py    # Фабрика драйверов
│   ├── api_client.py        # API для создания тестовых данных
│   └── config.py            # Конфигурация
│
├── requirements.txt
├── pytest.ini
└── README.md
```

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Установите Allure (опционально, для просмотра отчетов):
```bash
# Windows (через Chocolatey)
choco install allure-commandline

# Или скачайте с https://github.com/allure-framework/allure2/releases
```

## Запуск тестов

### Запуск в Chrome (по умолчанию):
```bash
pytest tests/ -v --browser=chrome
```

### Запуск в Firefox:
```bash
pytest tests/ -v --browser=firefox
```

### Запуск с Allure отчетом:
```bash
# Запуск тестов с генерацией отчета
pytest tests/ --alluredir=./allure-results

# Просмотр отчета
allure serve ./allure-results
```

### Параллельный запуск:
```bash
pytest tests/ -n 4
```

### Запуск конкретного теста:
```bash
pytest tests/test_password_recovery.py::TestPasswordRecovery::test_go_to_password_recovery -v
```

## Покрытие тестами

### Восстановление пароля
- ✅ Переход на страницу восстановления пароля
- ✅ Ввод почты и клик по кнопке «Восстановить»
- ✅ Клик по кнопке показать/скрыть пароль подсвечивает поле

### Личный кабинет
- ✅ Переход по клику на «Личный кабинет»
- ✅ Переход в раздел «История заказов»
- ✅ Выход из аккаунта

### Основной функционал
- ✅ Переход по клику на «Конструктор»
- ✅ Переход по клику на «Лента заказов»
- ✅ Всплывающее окно с деталями ингредиента
- ✅ Закрытие модального окна крестиком
- ✅ Увеличение счетчика ингредиента при добавлении
- ✅ Оформление заказа залогиненным пользователем

### Лента заказов
- ✅ Всплывающее окно с деталями заказа
- ✅ Заказы пользователя отображаются в ленте
- ✅ Увеличение счетчика «Выполнено за всё время»
- ✅ Увеличение счетчика «Выполнено за сегодня»
- ✅ Номер заказа появляется в разделе «В работе»

## Особенности реализации

- **Page Object Model**: Все элементы страниц описаны в отдельных классах
- **Кроссбраузерность**: Поддержка Chrome и Firefox через фабрику драйверов
- **Allure отчеты**: Детальные отчеты с шагами и скриншотами
- **API интеграция**: Создание и удаление тестовых пользователей через API
- **Независимые тесты**: Каждый тест создает свои данные и очищает их после выполнения

## Конфигурация

Настройки можно изменить в `utils/config.py` или через переменные окружения:

### Основные настройки:
- `BROWSER` - браузер для тестов (chrome/firefox), по умолчанию: `chrome`
- `FULLSCREEN` - полноэкранный режим (true/false), по умолчанию: `true`
- `TEST_EMAIL` - email для тестов
- `TEST_PASSWORD` - пароль для тестов

### Пути к драйверам:
- `CHROME_DRIVER_PATH` - путь к ChromeDriver (по умолчанию: `C:\WebDriver\chromedriver-win64\chromedriver.exe`)
- `FIREFOX_DRIVER_PATH` - путь к GeckoDriver (по умолчанию: пусто, используется webdriver-manager)

**Приоритет:** Если указан локальный путь и файл существует, используется он. Иначе используется webdriver-manager для автоматической загрузки.

### Пример настройки через переменные окружения (.env файл):
```env
BROWSER=chrome
FULLSCREEN=true
CHROME_DRIVER_PATH=C:\WebDriver\chromedriver-win64\chromedriver.exe
```

## Примечания

- Тесты используют реальный сайт https://stellarburgers.education-services.ru/
- Для работы тестов требуется стабильное интернет-соединение
- Некоторые тесты могут требовать дополнительной настройки локаторов в зависимости от актуальной структуры сайта

