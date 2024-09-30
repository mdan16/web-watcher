import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument('--headless')

print("aaaaaaaaaaaaaaaa")
driver = webdriver.Remote(
    command_executor='http://172.17.0.2:4444/wd/hub',
    options=options
)

print("aaaaaaaaaaaaaaaa")

url = os.environ.get('TARGET_URL')
driver.get(url)
print("aaaaaaaaaaaaaaaa")

xpath = os.environ.get('TARGET_XPATH')
target_text = driver.find_element(by=By.XPATH, value=xpath).text
print(f'target_text: {target_text} ({url} {xpath})')

driver.quit()

target_expected_text = os.environ.get('TARGET_EXPECTED_TEXT')
is_expected = (target_text == target_expected_text)
print(f'is_expected: {is_expected} ({target_expected_text})')

target_current_text = os.environ.get('TARGET_CURRENT_TEXT') or target_text
is_changed = (target_text != target_current_text)
print(f'is_changed: {is_changed} ({target_current_text})')

if is_expected or is_changed:
    url = os.environ.get('SLACK_WEBHOOK_URL')
    notify_text = os.environ.get('SLACK_NOTIFY_TEXT')
    headers = {"Content-type": "application/json"}
    r = requests.post(url, headers=headers, data=f'{{"text": "{notify_text}"}}'.encode("utf-8"))
