from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import sys
import os
from selenium.common.exceptions import TimeoutException
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from twocaptcha import TwoCaptcha

# Initialize the ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


    # Open the target webpage
driver.get("https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=kara&realmId=967&categoryId=2801")
# driver.get("https://appointment-booking-automation-tool.vercel.app/")
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

    api_key = os.getenv('APIKEY_2CAPTCHA', '80921b7e4175ef3a4721e75cc867f3cb')
    solver = TwoCaptcha(api_key)
    try:
        result = solver.normal(base64_image)
        captcha_input = driver.find_element(By.ID, 'appointment_captcha_month_captchaText')
        captcha_code = result['code']  # Assuming this is from the previous 2Captcha result
        captcha_input.send_keys(captcha_code)
        
        # Submit the form
        submit_button = driver.find_element(By.ID, 'appointment_captcha_month_appointment_showMonth')
        submit_button.click()
        
        #--------------------------------Correct till here--------------------------------
        # Click the "Appointments are available" link
        
        # appointments_link=WebDriverWait(driver, 50).until(
        #     EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'available')]"))
        # )

        # appointments_link.click()
        while True:
            try:
                appointments_link = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'available')]"))
                )
                print("Appointments are available!")
                appointments_link.click()
                break
            except TimeoutException:
                print("Appointments not available, refreshing the page...")
                driver.refresh()
        
        # Click the "Book this appointment" button
    
        appointments_link=WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'this')]"))
        )

        appointments_link.click()
        
        
        delay=WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'last')]"))
        )
        
    
        lastname_input = driver.find_element(By.ID, 'appointment_newAppointmentForm_lastname')
        last_name = "Hanzla"  # Assuming this is from the previous 2Captcha result
        lastname_input.send_keys(last_name)


        firstname_input = driver.find_element(By.ID, 'appointment_newAppointmentForm_firstname')
        first_name = "Hanzla"  # Assuming this is from the previous 2Captcha result
        firstname_input.send_keys(first_name)

        email_input = driver.find_element(By.ID, 'appointment_newAppointmentForm_email')
        email = "hanzlasib@gmail.com"  # Assuming this is from the previous 2Captcha result
        email_input.send_keys(email)

        email_input_repeat = driver.find_element(By.ID, 'appointment_newAppointmentForm_emailrepeat')
        emailrepeat = "hanzlasib@gmail.com"  # Assuming this is from the previous 2Captcha result
        email_input_repeat.send_keys(emailrepeat)

        passportNumber_input = driver.find_element(By.ID, 'appointment_newAppointmentForm_fields_0__content')
        passportnumber = "HN213123123"  # Assuming this is from the previous 2Captcha result
        passportNumber_input.send_keys(passportnumber)

        Province_input = driver.find_element(By.ID, 'appointment_newAppointmentForm_fields_1__content')
        province = "Sindh"  # Assuming this is from the previous 2Captcha result
        Province_input.send_keys(province)


        Nationality_input = driver.find_element(By.ID, 'appointment_newAppointmentForm_fields_2__content')
        nationality = "Paksitan"  # Assuming this is from the previous 2Captcha result
        Nationality_input.send_keys(nationality)

        



        captcha_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'captcha div')))

        # Extract the background-image style attribute
        background_image_style = captcha_div.get_attribute("style")

        # Use regular expression to extract the base64 data from the style attribute
        base64_match = re.search(r'url\(["\']?(data:image\/[a-zA-Z]+;base64,[^"\']*)["\']?\)', background_image_style)
        # print(base64_match)


        # # If a base64 image is found, extract it
        if base64_match:
            base64_image = base64_match.group(1)
            print(base64_image)
        
            api_key = os.getenv('APIKEY_2CAPTCHA', '80921b7e4175ef3a4721e75cc867f3cb')
            solver = TwoCaptcha(api_key)
            try:
                result = solver.normal(base64_image)
                captcha_input = driver.find_element(By.ID, 'appointment_newAppointmentForm_captchaText')
                captcha_code = result['code']  # Assuming this is from the previous 2Captcha result
                captcha_input.send_keys(captcha_code)
                
                # Submit the form
                submit_button = driver.find_element(By.ID, 'appointment_newAppointmentForm_appointment_addAppointment')
                # submit_button.click()
                page_html = driver.page_source
                with open('captured_page.html', 'w', encoding='utf-8') as f:
                    f.write(page_html)
                input("Press Enter to exit and close the browser...")
            except Exception as e:
                sys.exit(e)
    except Exception as e:
        sys.exit(e)



# #appointment_newAppointmentForm_captchaText
# #appointment_newAppointmentForm_appointment_addAppointmen





    # Open the target webpage








#appointment_newAppointmentForm_captchaText
#appointment_newAppointmentForm_appointment_addAppointmen