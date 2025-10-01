from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time

# Настройка браузера
driver = webdriver.Chrome()
driver.get("https://slutsk-minsk-marshrutka.by/")
wait = WebDriverWait(driver, 15)

# Выбор направления
direction_select = Select(wait.until(EC.element_to_be_clickable((By.ID, "order-direction"))))
direction_select.select_by_value("2")  # 1 = Слуцк–Минск, 2 = Минск–Слуцк

# Установка даты напрямую (обход календаря)
date_input = wait.until(EC.element_to_be_clickable((By.ID, "order-date")))
date_input.click()

# Ждём появления календаря
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "datepicker-days")))

# Выбираем дату — например, 2 октября
target_day = "2"
day_cell = wait.until(EC.element_to_be_clickable((By.XPATH, f"//td[contains(@class, 'day') and text()='{target_day}']")))
day_cell.click()

# Выбор количества мест
seats_select = Select(wait.until(EC.element_to_be_clickable((By.ID, "order-seats"))))
seats_select.select_by_value("1")

submit_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.searchForm_submit"))
)
submit_button.click()




desired_time_str = "17:40"
desired_time = datetime.strptime(desired_time_str, "%H:%M").time()

# Получаем все строки рейсов
rows = WebDriverWait(driver, 15).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.ordered"))
)

selected_row = None
closest_time = None

for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    if len(cells) < 1:
        continue

    time_text = cells[0].text.strip()
    try:
        dep_time = datetime.strptime(time_text, "%H:%M").time()

        if dep_time == desired_time:
            selected_row = row
            print(f"🎯 Найден точный рейс: {time_text}")
            break
        elif dep_time > desired_time and (closest_time is None or dep_time < closest_time):
            selected_row = row
            closest_time = dep_time
    except:
        continue

# Нажимаем кнопку «Забронировать» (.visible-xs)
if selected_row:
    try:
        book_button = selected_row.find_element(By.CSS_SELECTOR, "form button.visible-xs")
        driver.execute_script("arguments[0].scrollIntoView(true);", book_button)
        driver.execute_script("arguments[0].click();", book_button)
        print("✅ Бронирование отправлено на рейс:", selected_row.find_element(By.TAG_NAME, "td").text.strip())
    except Exception as e:
        print(f"Ошибка при нажатии кнопки: {e}")
else:
    print("Нет подходящего рейса после", desired_time_str)




phone_input = wait.until(EC.presence_of_element_located((By.ID, "order-phone")))
phone_input.send_keys("7416000")  # ← сюда подставь нужный номер





# Заполнение дополнительных полей
try:
    name_input = wait.until(EC.presence_of_element_located((By.NAME, "Order[name]")))
    name_input.send_keys("Иван")

    surname_input = driver.find_element(By.NAME, "Order[surname]")
    surname_input.send_keys("Иванов")

    phone_input = driver.find_element(By.NAME, "Order[phone]")
    phone_input.send_keys("7416000")

    agree_checkbox = driver.find_element(By.NAME, "Order[agree]")
    agree_checkbox.click()
except:
    print("Дополнительные поля не найдены — возможно, они появляются позже или по событию.")

# Отправка формы
submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.searchForm_submit")))
submit_button.click()

print("Бронирование отправлено!")
time.sleep(5)

