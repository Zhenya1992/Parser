from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

chrome_driver_path = 'chromedriver.exe'

options = webdriver.ChromeOptions()
options.add_argument('--headless')

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get('https://www.cbr.ru/currency_base/daily/')
    time.sleep(3)

    usd_element = driver.find_element(By.XPATH, "//td[contains(text(), 'USD')]/following-sibling::td[2]")
    usd_rate = usd_element.text

    eur_element = driver.find_element(By.XPATH, "//td[contains(text(), 'EUR')]/following-sibling::td[2]")
    eur_rate = eur_element.text

    print(f"Курс доллара: {usd_rate} руб.")
    print(f"Курс евро: {eur_rate} руб.")

finally:
    driver.quit()
