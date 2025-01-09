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

def fast_fill_input(driver, element_id, value):
    js_code = f'document.getElementById("{element_id}").value = "{value}";'
    driver.execute_script(js_code)

def solve_captcha(captcha_url):
    response = requests.post(
        "https://api.apitruecaptcha.org/one/gettext",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "userid": USER_ID,
            "apikey": API_KEY,
            "data": captcha_url
        })
    )

    json_response = response.json()
    if json_response.get('success') and json_response.get('result'):
        return json_response['result']
    else:
        raise Exception(f"Failed to solve CAPTCHA: {json_response}")

def Time_dif():
    return datetime.now()-datetime.now().replace(hour=22, minute=54, second=10, microsecond=0)

def wait_until_4am():
    now = datetime.now()
    target_time = now.replace(hour=22, minute=54, second=10, microsecond=0)
    if now.time() >= target_time.time():
        target_time += timedelta(days=1)
    wait_seconds = (target_time - now).total_seconds()
    print(f"Waiting until exactly 4:00:00 AM. Sleeping for {wait_seconds} seconds...")
    time.sleep(wait_seconds)

# Open the target webpage
driver.get("https://service2.diplo.de/rktermin/extern/appointment_showDay.do?locationCode=kara&realmId=967&categoryId=2801&dateStr=10.01.2025")
wait = WebDriverWait(driver, 10)

captcha_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'captcha div')))
background_image_style = captcha_div.get_attribute("style")
base64_match = re.search(r'url\(["\']?(data:image\/[a-zA-Z]+;base64,[^"\']*)["\']?\)', background_image_style)

if base64_match:
    base64_image = base64_match.group(1)
    cap = solve_captcha(base64_image)
    
    try:
        # Fill first captcha using JavaScript
        fast_fill_input(driver, 'appointment_captcha_day_captchaText', cap)
        
        # Submit the form
        driver.execute_script("document.getElementById('appointment_captcha_day_appointment_showDay').click();")
        
        target_url = "https://service2.diplo.de/rktermin/extern/appointment_showForm.do?locationCode=kara&realmId=967&categoryId=2801&dateStr=10.01.2025&openingPeriodId=68494"
        wait_until_4am()
        driver.get(target_url)
        
        print("URL get in = ", Time_dif())
        
        # Fast fill all form fields using JavaScript
        form_data = {
            'appointment_newAppointmentForm_lastname': 'KHAN',
            'appointment_newAppointmentForm_firstname': 'AIMON',
            'appointment_newAppointmentForm_email': 'aimonkhan24@gmail.com',
            'appointment_newAppointmentForm_emailrepeat': 'aimonkhan24@gmail.com',
            'appointment_newAppointmentForm_fields_0__content': 'KN4145152',
            'appointment_newAppointmentForm_fields_1__content': 'Sindh',
            'appointment_newAppointmentForm_fields_2__content': 'Paksitan'
        }
        
        # Fill all fields at once
        js_code = ""
        for element_id, value in form_data.items():
            js_code += f'document.getElementById("{element_id}").value = "{value}";'
        driver.execute_script(js_code)

        captcha_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'captcha div')))
        background_image_style = captcha_div.get_attribute("style")
        base64_match = re.search(r'url\(["\']?(data:image\/[a-zA-Z]+;base64,[^"\']*)["\']?\)', background_image_style)
        
        if base64_match:
            base64_image = base64_match.group(1)
            cap = solve_captcha(base64_image)
            try:
                # Fill second captcha using JavaScript
                fast_fill_input(driver, 'appointment_newAppointmentForm_captchaText', cap)
                
                print("completed form = ", Time_dif())
                time.sleep(3)
                
                # Submit final form using JavaScript
                driver.execute_script("document.getElementById('appointment_newAppointmentForm_appointment_addAppointment').click();")
                
                print("completed in = ", Time_dif())
                input("Press Enter to exit and close the browser...")
            except Exception as e:
                sys.exit(e)
    except Exception as e:
        sys.exit(e)