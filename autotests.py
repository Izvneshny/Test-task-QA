from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from pathlib import Path

base_dir = Path(__file__).parent
driver_path = base_dir / 'chromedriver'
service = Service(executable_path=str(driver_path))

def log_and_assert(condition, message, driver=None):
    if not condition:
        print(f"FAIL: {message}")
        if driver:
            driver.quit()
        raise AssertionError(message)
    else:
        print(f"PASS: {message}")

def run_test(test_func, *args, **kwargs):
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 15)
    try:
        test_func(driver, wait, *args, **kwargs)
    except AssertionError as e:
        print(f"Тест {test_func.__name__} не прошел: {e}")
    except Exception as e:
        print(f"Произошла ошибка в тесте {test_func.__name__}: {e}")
    finally:
        driver.quit()

def test_price_range_filter(driver, wait):
    driver.set_window_size(1920, 1080)
    driver.get("https://cerulean-praline-8e5aa6.netlify.app/")
    try:
        min_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='От' and @type='number']")))
        max_input = driver.find_element(By.XPATH, "//input[@placeholder='До' and @type='number']")
        min_input.clear(); min_input.send_keys("1000")
        max_input.clear(); max_input.send_keys("5000")
        wait.until(EC.presence_of_element_located((By.XPATH, "//main[@class='_main_imlvm_118']")))
        prices = driver.find_elements(By.CSS_SELECTOR, ".ad-item .price")
        for p in prices:
            price_value = int(p.text.replace("₽", "").replace(" ", ""))
            log_and_assert(1000 <= price_value <= 5000, f"Объявление с ценой {price_value} вне диапазона.")
        print("Диапазон цен — PASS\n")
    except Exception as e:
        print(f"Ошибка при тесте цены: {e}")
        driver.quit()
        raise

def test_sort_by_price(driver, wait, order='asc'):
    driver.set_window_size(1920, 1080)
    driver.get("https://cerulean-praline-8e5aa6.netlify.app/")
    try:
        sort_select = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@class='_filters__select_1iunh_21']")))
        sort_select.click()
        option_value = 'price_asc' if order == 'asc' else 'price_desc'
        option = driver.find_element(By.XPATH, "//select[@class='_filters__select_1iunh_21']")
        option.click()
        wait.until(lambda d: True)
        prices = driver.find_elements(By.CSS_SELECTOR, ".ad-item .price")
        prices = [int(p.text.replace("₽", "").replace(" ", "")) for p in driver.find_elements(By.CSS_SELECTOR, ".ad-item .price")]
        sorted_prices = sorted(prices)
        if order == 'desc':
            sorted_prices.reverse()
        log_and_assert(prices == sorted_prices, f"Объявления отсортированы должным образом ({order})")
        print("Сортировка — PASS\n")
    except Exception as e:
        print(f"Ошибка при тесте сортировки: {e}")
        driver.quit()
        raise

def test_category_filter(driver, wait):
    driver.set_window_size(1920, 1080)
    driver.get("https://cerulean-praline-8e5aa6.netlify.app/")
    try:
        select = Select(wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, '_filters__group_1iunh_1')][.//label[contains(text(), 'Категория')]]//select"))))
        select.select_by_value("0")
        wait.until(EC.presence_of_element_located((By.XPATH, "//main[@class='_main_imlvm_118']")))
        categories = driver.find_elements(By.CSS_SELECTOR, ".ad-item .category")
        for cat in categories:
            log_and_assert("электроника" in cat.text.lower(), f"Объявление категории: {cat.text}")
        print("Категория — PASS\n")
    except Exception as e:
        print(f"Ошибка при тесте категории: {e}")
        driver.quit()
        raise

def test_only_urgent_tag(driver, wait):
    driver.set_window_size(1920, 1080)
    driver.get("https://cerulean-praline-8e5aa6.netlify.app/")
    try:
        toggle = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Только срочные') or contains(@class, 'urgent')]")))
        toggle.click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//main[@class='_main_imlvm_118']")))
        urgent_labels = driver.find_elements(By.CSS_SELECTOR, ".ad-item .urgent-label")
        assert all(label.is_displayed() for label in urgent_labels), "Не все объявления срочные."
        print("Тогл срочности — PASS\n")
    except Exception as e:
        print(f"Ошибка при тесте тогла: {e}")
        driver.quit()
        raise

def test_statistics_timer_controls(driver, wait):
    driver.set_window_size(1920, 1080)
    driver.get("https://cerulean-praline-8e5aa6.netlify.app/stats/")
    try:
        error_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Page not found')]")
        if error_elements:
            raise AssertionError("Страница недоступна: 'Page not found'. Возможно, это баг сайта или временная проблема.\n")
        container = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='_container_ir5wu_1']")))        
        button_texts = {btn.text: btn for btn in container.find_elements(By.TAG_NAME, 'button')}
        log_and_assert('Обновить' in button_texts, "Кнопка 'Обновить' есть")
        button_texts['Обновить'].click()
        log_and_assert('Стоп' in button_texts, "Кнопка 'Стоп' есть")
        button_texts['Стоп'].click()
        log_and_assert('Старт' in button_texts, "Кнопка 'Старт' есть")
        button_texts['Старт'].click()
        print("Таймер — PASS\n")
    except AssertionError as e:
        print(f"Ошибка при тесте таймера: {e}")
        driver.quit()
        raise
    except Exception as e:
        print(f"Обнаружена проблема: {e}")
        driver.quit()
        raise

def test_theme_switch_mobile(driver, wait):
    driver.set_window_size(375, 667)
    driver.get("https://cerulean-praline-8e5aa6.netlify.app/")
    try:
        toggle_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, '_themeToggle')]")))
        theme_label = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(@class,\"_label_127us_35\")]")))
        initial_text = theme_label.text.strip()
        toggle_btn.click()
        def label_changed(driver):
            label_now = theme_label.text.strip()
            return label_now != initial_text
        wait.until(label_changed)
        new_text = theme_label.text.strip()
        log_and_assert(new_text != initial_text, "Тема успешно переключилась.")
        print("Переключение темы — PASS\n")
    except Exception as e:
        print(f"Ошибка при тесте смены темы на мобильном устройстве: {e}")
        driver.quit()
        raise

if __name__ == "__main__":
    print("Запуск независимых тестов...\n")
    run_test(test_price_range_filter)
    run_test(test_sort_by_price, 'asc')
    run_test(test_category_filter)
    run_test(test_only_urgent_tag)
    run_test(test_statistics_timer_controls)
    run_test(test_theme_switch_mobile)
    print("Все тесты завершены.")