# Инструкция по запуску автоматических тестов

## Требования

- Браузер Chrome (желательно последней версии)
- `chromedriver` для взаимодействия Selenium с Chrome
- Python 3
- Библиотека `selenium` для Python

## Шаги для запуска тестов

1. Клонируйте этот репозиторий:
```bash
git clone <URL-репозитория>
cd <имя-папки-репозитория>
```

2. Подготовьте Chrome и ChromeDriver:
	- Скачайте подходящую версию ChromeDriver с сайта: [ChromeDriver для тестирования](https://googlechromelabs.github.io/chrome-for-testing/)
	- Поместите файл `chromedriver.exe` (или `chromedriver` для Linux/macOS) в ту же папку, где находится файл `autotests.py`.

3. Установите Python 3:  
    Если еще не установлен, скачайте и установите его с официального сайта: [python.org](https://www.python.org/downloads/).

4. Установите необходимые библиотеки:
```bash
pip install selenium
```

5. Запуск автоматических тестов:
```bash
python3 autotests.py
```