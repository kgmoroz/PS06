from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import csv

# Настройки Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Запуск браузера в фоновом режиме
#chrome_service = Service('/path/to/chromedriver')  # Убедитесь, что указали правильный путь к chromedriver

#driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
driver = webdriver.Chrome(options=chrome_options)

base_url = "https://www.divan.ru/category/svet/page-"
page_number = 1
product_info_list = []

while True:
    url = f"{base_url}{page_number}"
    driver.get(url)

    # Ожидание загрузки элементов на странице
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[itemprop='itemListElement']"))
        )
    except Exception as e:
        print(f"Ошибка при ожидании элементов: {e}")

    products = driver.find_elements(By.CSS_SELECTOR, "div[itemprop='itemListElement']")
    if not products:
        break  # Если элементов нет, выходим из цикла

    for product in products:
        try:
            # Поиск элемента с классом 'wYUX2'
            container = product.find_element(By.CLASS_NAME, "wYUX2")
            # Поиск вложенного элемента span с itemprop='name' внутри контейнера
            name = container.find_element(By.CSS_SELECTOR, "span[itemprop='name']").text
        except Exception as e:
            name = "N/A"
            print(f"Ошибка при получении наименования: {e}")
        try:
            price = product.find_element(By.CSS_SELECTOR, "meta[itemprop='price']").get_attribute("content")
        except Exception as e:
            price = "N/A"
            print(f"Ошибка при получении цены: {e}")
        try:
            link = product.find_element(By.CSS_SELECTOR, "a.ui-GPFV8").get_attribute("href")
        except Exception as e:
            link = "N/A"
            print(f"Ошибка при получении ссылки: {e}")
        product_info_list.append([name, price, link])

    page_number += 1

# Закрытие браузера
driver.quit()

# Сохранение данных в CSV-файл
csv_file = 'product_data.csv'
csv_columns = ['name', 'price', 'url']

try:
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_columns) # Создаём первый ряд
        writer.writerows(product_info_list) # Прописываем использование списка как источника для рядов таблицы
    print(f"Данные успешно сохранены в {csv_file}")
except IOError:
    print("Ошибка при записи в файл")