import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument('--headless')

driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=options
)


url = os.environ.get('TARGET_URL')
driver.get(url)

xpath = os.environ.get('TARGET_XPATH')

element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, xpath))
)
target_text = driver.find_element(by=By.XPATH, value=xpath).text
print(f"target_text: {target_text}")

driver.quit()

target_expected_text = os.environ.get('TARGET_EXPECTED_TEXT')
is_expected = (target_text == target_expected_text)

target_current_text = os.environ.get('TARGET_CURRENT_TEXT') or target_text
is_changed = (target_text != target_current_text)

if is_expected or is_changed:
    url = os.environ.get('SLACK_WEBHOOK_URL')
    notify_text = os.environ.get('SLACK_NOTIFY_TEXT')
    headers = {"Content-type": "application/json"}
    r = requests.post(url, headers=headers, data=f'{{"text": "{notify_text}"}}'.encode("utf-8"))
