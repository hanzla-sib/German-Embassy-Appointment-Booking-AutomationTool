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

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
options = webdriver.ChromeOptions()

options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options)
# Configuration
API_KEY = 'lHj6eDPmIAuMz14ymqsj'
USER_ID = 'hanzlasib@gmail.com'
def solve_captcha(captcha_url):
    # Make API call to TrueCaptcha
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

def wait_until_4am():
    """
    Wait until exactly 4:00:00 AM before executing the submit action
    """
    # Get current time
    now = datetime.now()
    
    # Calculate time to 4:00:00 AM
    target_time = now.replace(hour=23, minute=59, second=54, microsecond=0)

    # If we've already passed 4 AM today, target tomorrow's 4 AM
    if now.time() >= target_time.time():
        target_time += timedelta(days=1)
    
    # Calculate seconds to wait
    wait_seconds = (target_time - now).total_seconds()
    
    print(f"Waiting until exactly 4:00:00 AM. Sleeping for {wait_seconds} seconds...")
    # Precise waiting
    time.sleep(wait_seconds)


    # Open the target webpage
driver.get("https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=kara&realmId=967&categoryId=1988")
# Use WebDriverWait for dynamic content
wait = WebDriverWait(driver, 10)

captcha_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'captcha div')))

# Extract the background-image style attribute
background_image_style = captcha_div.get_attribute("style")

# Use regular expression to extract the base64 data from the style attribute
base64_match = re.search(r'url\(["\']?(data:image\/[a-zA-Z]+;base64,[^"\']*)["\']?\)', background_image_style)


# If a base64 image is found, extract it
if base64_match:
    base64_image = base64_match.group(1)
    cap=solve_captcha(base64_image)
    
    try:
        # result = solver.normal(base64_image)
       
        captcha_input = driver.find_element(By.ID, 'appointment_captcha_month_captchaText')
       
        # captcha_code = result['code']  # Assuming this is from the previous 2Captcha result
        captcha_input.send_keys(cap)
       
        
        # Submit the form
        submit_button = driver.find_element(By.ID, 'appointment_captcha_month_appointment_showMonth')

        wait_until_4am()
        submit_button.click()
        target_url = "https://service2.diplo.de/rktermin/extern/appointment_showForm.do?locationCode=kara&realmId=967&categoryId=1988&dateStr=27.01.2025&openingPeriodId=43852"

# Load the target URL
        driver.get(target_url)
       
        
        
        #--------------------------------Correct till here--------------------------------
        # Click the "Appointments are available" link
        
        while True:
            try:
                # Wait for the "Appointments are available" link
                element = WebDriverWait(driver,0.5).until(EC.presence_of_element_located((By.ID, "wwlbl_appointment_newAppointmentForm_lastname")))
                
                # If link is found, print success and click
                print("Appointments are available!")
                
                
                break
            
            except TimeoutException:
                # If link not found, reload the page
                print("No available appointments. Reloading...")
                
                driver.refresh()
                
        
       
        
        print("cehcking div")
        element = WebDriverWait(driver,100).until(EC.presence_of_element_located((By.ID, "wwlbl_appointment_newAppointmentForm_lastname")))
        
        print("form entered")
        lastname_input = driver.find_element(By.ID, 'appointment_newAppointmentForm_lastname')
        last_name = "ANSARI"  # Assuming this is from the previous 2Captcha result
        lastname_input.send_keys(last_name)


        firstname_input = driver.find_element(By.ID, 'appointment_newAppointmentForm_firstname')
        first_name = "FAHAD AHMED"  # Assuming this is from the previous 2Captcha result
        firstname_input.send_keys(first_name)


        email_input = driver.find_element(By.ID, 'appointment_newAppointmentForm_email')
        email = "fahadahmadd2025@gmail.com"  # Assuming this is from the previous 2Captcha result
        email_input.send_keys(email)


        email_input_repeat = driver.find_element(By.ID, 'appointment_newAppointmentForm_emailrepeat')
        emailrepeat = "fahadahmadd2025@gmail.com"  # Assuming this is from the previous 2Captcha result
        email_input_repeat.send_keys(emailrepeat)

        
        passportNumber_input = driver.find_element(By.ID, 'appointment_newAppointmentForm_fields_0__content')
        passportnumber = "EC1719191"  # Assuming this is from the previous 2Captcha result
        passportNumber_input.send_keys(passportnumber)

        Province_input = driver.find_element(By.ID, 'appointment_newAppointmentForm_fields_1__content')
        province = "Sindh"  # Assuming this is from the previous 2Captcha result
        Province_input.send_keys(province)


        Nationality_input = driver.find_element(By.ID, 'appointment_newAppointmentForm_fields_2__content')
        nationality = "Paksitan"  
        Nationality_input.send_keys(nationality)

        captcha_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'captcha div')))

        background_image_style = captcha_div.get_attribute("style")

        base64_match = re.search(r'url\(["\']?(data:image\/[a-zA-Z]+;base64,[^"\']*)["\']?\)', background_image_style)
        
        if base64_match:
            base64_image = base64_match.group(1)
            cap=solve_captcha(base64_image)
            try:
                captcha_input = driver.find_element(By.ID, 'appointment_newAppointmentForm_captchaText')
                captcha_input.send_keys(cap)
                # Submit the form
                submit_button = driver.find_element(By.ID, 'appointment_newAppointmentForm_appointment_addAppointment')
                current_url = driver.current_url
                print(f"Current URL BAchelors by direct form before submission: {current_url}")
                time.sleep(3)
                submit_button.click()
                input("Press Enter to exit and close the browser...")
            except Exception as e:
                sys.exit(e)
    except Exception as e:
        sys.exit(e)