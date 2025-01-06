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
driver.get("https://service2.diplo.de/rktermin/extern/appointment_showDay.do?locationCode=kara&realmId=1116&categoryId=2339&dateStr=04.02.2025")
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
       
        captcha_input = driver.find_element(By.ID, 'appointment_captcha_day_captchaText')
       
        # captcha_code = result['code']  # Assuming this is from the previous 2Captcha result
        captcha_input.send_keys(cap)
       
        
        # Submit the form
        submit_button = driver.find_element(By.ID, 'appointment_captcha_day_appointment_showDay')

        wait_until_4am()
        
        submit_button.click()
        
        #--------------------------------Correct till here--------------------------------
        # Click the "Appointments are available" link
        
        while True:
            try:
                # Wait for the "Appointments are available" link
                appointments_links = WebDriverWait(driver, 0.5).until(
                EC.presence_of_all_elements_located((By.XPATH, "//a[contains(text(), 'this')]"))
                )
            
            
            
                print("Appointments are available!")
            
                for index, link in enumerate(appointments_links):
                    link_href = link.get_attribute('href')
                    print(f"{index + 1}: {link_href}")
           
               
                input("Press Enter to exit and close the browser...")
                
                
                
                break
            
            except TimeoutException:
                # If link not found, reload the page
                print("No available appointments. Reloading...")
                
                driver.refresh()
                
            except Exception as e:
                sys.exit(e)
    except Exception as e:
        sys.exit(e)