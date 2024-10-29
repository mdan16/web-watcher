import os
import requests
from bs4 import BeautifulSoup
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
target_text = driver.find_element(by=By.XPATH, value=xpath).get_attribute("innerHTML")
print(f"target_text: {target_text}")
target_soup = BeautifulSoup(target_text, 'html.parser')

driver.quit()

target_expected_text = os.environ.get('TARGET_EXPECTED_TEXT')
expected_soup = BeautifulSoup(target_expected_text, 'html.parser')
is_expected = (target_soup.prettify().split() == expected_soup.prettify().split())

target_current_text = os.environ.get('TARGET_CURRENT_TEXT') or target_current_text
current_soup = BeautifulSoup(target_current_text, 'html.parser')
is_changed = (target_soup.prettify().split() != current_soup.prettify().split())

if is_expected or is_changed:
    url = os.environ.get('SLACK_WEBHOOK_URL')
    notify_text = os.environ.get('SLACK_NOTIFY_TEXT')
    headers = {"Content-type": "application/json"}
    r = requests.post(url, headers=headers, data=f'{{"text": "{notify_text}"}}'.encode("utf-8"))
