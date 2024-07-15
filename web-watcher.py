import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument('--headless')

driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=options
)

url = os.environ.get('TARGET_URL')
driver.get(url)

xpath = os.environ.get('TARGET_XPATH')
target_text = driver.find_element(by=By.XPATH, value=xpath).text
print(target_text)

driver.quit()

if target_text == os.environ.get('TARGET_EXPECTED_TEXT'):
    url = os.environ.get('SLACK_WEBHOOK_URL')
    notify_text = os.environ.get('SLACK_NOTIFY_TEXT')
    headers = {"Content-type": "application/json"}
    r = requests.post(url, headers=headers, data=f'{{"text": "{notify_text}"}}'.encode("utf-8"))
