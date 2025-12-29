# Инструкция по настройке интерпретатора в PyCharm

## Проблема
PyCharm показывает предупреждение: "No Python interpreter configured for the project"

## Решение

### Способ 1: Через настройки проекта (рекомендуется)

1. **Откройте настройки проекта:**
   - Нажмите `File` → `Settings` (или `Ctrl+Alt+S`)
   - Или кликните на предупреждение "No Python interpreter configured" и выберите "Interpreter settings"

2. **Выберите интерпретатор:**
   - В левом меню выберите `Project: Task_3` → `Python Interpreter`
   - В правой части нажмите на выпадающий список рядом с "Python Interpreter"
   - Выберите `Add Interpreter...` → `Add Local Interpreter...`

3. **Настройте виртуальное окружение:**
   - Выберите `Virtualenv Environment`
   - Выберите `Existing environment`
   - В поле "Interpreter" укажите путь к интерпретатору:
     ```
     C:\Users\vikharev-d\work\Task_3\venv\Scripts\python.exe
     ```
   - Нажмите `OK`

4. **Проверьте установленные пакеты:**
   - В окне настроек интерпретатора должны отображаться все установленные пакеты:
     - selenium
     - pytest
     - allure-pytest
     - webdriver-manager
     - и другие из requirements.txt

### Способ 2: Через предупреждение в редакторе

1. Кликните на желтое предупреждение "No Python interpreter configured for the project"
2. Выберите "Interpreter settings"
3. Следуйте инструкциям из Способа 1, начиная с пункта 3

### Способ 3: Автоматическое определение

1. Откройте любой Python файл в проекте (например, `tests/conftest.py`)
2. PyCharm может автоматически предложить настроить интерпретатор
3. Если появится предложение, выберите существующий интерпретатор из `venv`

## Проверка настройки

После настройки интерпретатора:

1. **Проверьте в статус-баре:**
   - В правом нижнем углу PyCharm должен отображаться Python интерпретатор
   - Должен быть виден путь: `Python 3.10 (venv)`

2. **Проверьте импорты:**
   - Откройте файл `tests/conftest.py`
   - Все импорты должны быть распознаны (без красных подчеркиваний)

3. **Проверьте запуск тестов:**
   - Правой кнопкой мыши на файл `tests/test_password_recovery.py`
   - Выберите `Run 'pytest in test_password_recovery.py'`
   - Тесты должны запуститься без ошибок

## Путь к интерпретатору

**Полный путь к интерпретатору:**
```
C:\Users\vikharev-d\work\Task_3\venv\Scripts\python.exe
```

**Альтернативный путь (для проверки):**
```
C:\Users\vikharev-d\work\Task_3\venv\Scripts\pythonw.exe
```

## Дополнительная информация

### Версия Python
- **Версия:** Python 3.10.11
- **Расположение базового Python:** `C:\Users\vikharev-d\AppData\Local\Programs\Python\Python310`

### Установленные зависимости
Все зависимости из `requirements.txt` уже установлены в виртуальное окружение:
- ✅ selenium==4.15.0
- ✅ pytest==7.4.3
- ✅ webdriver-manager==4.0.1
- ✅ allure-pytest==2.13.2
- ✅ python-dotenv==1.0.0
- ✅ requests==2.31.0
- ✅ pytest-xdist==3.5.0

## Если проблема не решена

1. **Перезапустите PyCharm** после настройки интерпретатора
2. **Инвалидируйте кеш:** `File` → `Invalidate Caches...` → `Invalidate and Restart`
3. **Проверьте путь к интерпретатору** в терминале:
   ```powershell
   C:\Users\vikharev-d\work\Task_3\venv\Scripts\python.exe --version
   ```
   Должно вывести: `Python 3.10.11`

## Настройка для запуска тестов

После настройки интерпретатора можно настроить конфигурацию запуска тестов:

1. `Run` → `Edit Configurations...`
2. Нажмите `+` → `Python tests` → `pytest`
3. Укажите:
   - **Name:** `pytest tests`
   - **Target:** `Custom`
   - **Custom:** `tests/`
   - **Python interpreter:** выберите `venv` интерпретатор
   - **Additional arguments:** `--browser=chrome -v`


