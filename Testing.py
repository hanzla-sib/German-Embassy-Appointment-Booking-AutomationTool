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
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
options = webdriver.ChromeOptions()

options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options)
# Configuration
load_dotenv()
API_KEY = os.getenv('API_KEY')
USER_ID = os.getenv('USER_ID')
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
driver.get("https://appointment-booking-automation-tool.vercel.app/")
# Use WebDriverWait for dynamic content
wait = WebDriverWait(driver, 10)



# If a base64 image is found, extract it
if True:
    
    
    try:
        
        
       
        
        while True:
            try:
                # Wait for the "Appointments are available" link
                appointments_links = WebDriverWait(driver, 0.5).until(
                EC.presence_of_all_elements_located((By.XPATH, "//a[contains(text(), 'this')]"))
                )
            
            
            
                print("Appointments are available!")
                
                appointments_links[1].click()
                input("Press Enter to exit and close the browser...")
                break
            
            except TimeoutException:
                # If link not found, reload the page
                print("No available appointments. Reloading...")
                
                driver.refresh()
                
        
       
        

    except Exception as e:
        sys.exit(e)

# When filling forms, use dummy values like 'LASTNAME', 'FIRSTNAME', 'dummy@email.com', 'P1234567', etc.