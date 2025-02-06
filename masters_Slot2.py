from datetime import datetime, timedelta
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import requests
import json
import sys
import os
from selenium.common.exceptions import TimeoutException
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

options = webdriver.ChromeOptions()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options)

API_KEY = 'lHj6eDPmIAuMz14ymqsj'
USER_ID = 'hanzlasib@gmail.com'

# Pre-compile the regex pattern for better performance
BASE64_PATTERN = re.compile(r'url\(["\']?(data:image\/[a-zA-Z]+;base64,[^"\']*)["\']?\)')

# Optimize the captcha solving function with a session
session = requests.Session()
def solve_captcha(captcha_url):
    response = session.post(
        "https://api.apitruecaptcha.org/one/gettext",
        headers={"Content-Type": "application/json"},
        json={  # Using json parameter instead of manually dumping
            "userid": USER_ID,
            "apikey": API_KEY,
            "data": captcha_url
        }
    )
    json_response = response.json()
    if json_response.get('success') and json_response.get('result'):
        return json_response['result']
    raise Exception(f"Failed to solve CAPTCHA: {json_response}")

def fast_fill_input(driver, element_id, value):
    js_code = f'document.getElementById("{element_id}").value = "{value}";'
    driver.execute_script(js_code)

def Time_dif():
    return datetime.now()-datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

def wait_until_4am():
    now = datetime.now()
    target_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
    if now.time() >= target_time.time():
        target_time += timedelta(days=1)
    wait_seconds = (target_time - now).total_seconds()
    print(f"Waiting until exactly 4:00:00 AM. Sleeping for {wait_seconds} seconds...")
    time.sleep(wait_seconds)

# Optimize the main flow with better error handling and reduced DOM queries
driver.get("https://service2.diplo.de/rktermin/extern/appointment_showDay.do?locationCode=kara&realmId=967&categoryId=2801&dateStr=07.03.2025")
wait = WebDriverWait(driver, 10)

try:
    captcha_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'captcha div')))
    background_image_style = captcha_div.get_attribute("style")
    base64_match = BASE64_PATTERN.search(background_image_style)

    if not base64_match:
        raise Exception("Could not find CAPTCHA image")
        
    cap = solve_captcha(base64_match.group(1))
    fast_fill_input(driver, 'appointment_captcha_day_captchaText', cap)
    
    time.sleep(3)
    driver.execute_script("document.getElementById('appointment_captcha_day_appointment_showDay').click();")
    
    target_url = "https://service2.diplo.de/rktermin/extern/appointment_showForm.do?locationCode=kara&realmId=967&categoryId=2801&dateStr=07.03.2025&openingPeriodId=68489"
    wait_until_4am()
    driver.get(target_url)
    
    # Combine all form fields into a single JavaScript execution
    form_data = {
        'appointment_newAppointmentForm_lastname': 'MALIK',
        'appointment_newAppointmentForm_firstname': 'MUHAMMAD INSHAAL',
        'appointment_newAppointmentForm_email': 'germanyappointment8@gmail.com',
        'appointment_newAppointmentForm_emailrepeat': 'germanyappointment8@gmail.com',
        'appointment_newAppointmentForm_fields_0__content': 'FU0764442',
        'appointment_newAppointmentForm_fields_1__content': 'Sindh',
        'appointment_newAppointmentForm_fields_2__content': 'Pakistan'
    }
    
    js_code = ';'.join(f'document.getElementById("{id}").value="{value}"' for id, value in form_data.items())
    driver.execute_script(js_code)

    captcha_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'captcha div')))
    base64_match = BASE64_PATTERN.search(captcha_div.get_attribute("style"))
    
    if not base64_match:
        raise Exception("Could not find second CAPTCHA image")
        
    cap = solve_captcha(base64_match.group(1))
    fast_fill_input(driver, 'appointment_newAppointmentForm_captchaText', cap)
    
    print("completed form = ", Time_dif())
    time.sleep(3)
    
    driver.execute_script("document.getElementById('appointment_newAppointmentForm_appointment_addAppointment').click();")
    print("completed in = ", Time_dif())
    input("Press Enter to exit and close the browser...")

except Exception as e:
    print(f"Error occurred: {str(e)}")
    sys.exit(1)