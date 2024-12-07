# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import re
# import sys
# import os

# sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(_file_))))

# from twocaptcha import TwoCaptcha

# # Initialize the ChromeDriver
# service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service)


#     # Open the target webpage
# driver.get("https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=kara&realmId=967&categoryId=2801")

# # Use WebDriverWait for dynamic content
# wait = WebDriverWait(driver, 10)
# captcha_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'captcha div')))

# # Extract the background-image style attribute
# background_image_style = captcha_div.get_attribute("style")
# print(background_image_style)
# # Use regular expression to extract the base64 data from the style attribute
# base64_match = re.search(r'url\(["\']?(data:image\/[a-zA-Z]+;base64,[^"\']*)["\']?\)', background_image_style)
# print(base64_match)

# # If a base64 image is found, extract it
# if base64_match:
#     base64_image = base64_match.group(1)
#     print(base64_image)
#     api_key = os.getenv('APIKEY_2CAPTCHA', '80921b7e4175ef3a4721e75cc867f3cb')
#     solver = TwoCaptcha(api_key)
#     try:
#         result = solver.normal(base64_image)
#         captcha_input = driver.find_element(By.ID, 'appointment_captcha_month_captchaText')
#         captcha_code = result['code']  # Assuming this is from the previous 2Captcha result
#         captcha_input.send_keys(captcha_code)
        
#         # Submit the form
#         submit_button = driver.find_element(By.ID, 'appointment_captcha_month_appointment_showMonth')
#         submit_button.click()
        
#         #--------------------------------Correct till here--------------------------------
#         # Click the "Appointments are available" link
        
#         appointments_link=WebDriverWait(driver, 50).until(
#             EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'available')]"))
#         )

#         appointments_link.click()
        
#         # Click the "Book this appointment" button
    
#         appointments_link=WebDriverWait(driver, 50).until(
#             EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'this')]"))
#         )

#         appointments_link.click()
        
#         # Capture page HTML
#         page_html = driver.page_source
        
#         # Save HTML to file
#         with open('captured_page.html', 'w', encoding='utf-8') as f:
#             f.write(page_html)
        
#         print("Booking process completed. HTML saved to captured_page.html")
#     except Exception as e:
#         sys.exit(e)



# #appointment_newAppointmentForm_captchaText
# #appointment_newAppointmentForm_appointment_addAppointmen



from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(_file_))))

from twocaptcha import TwoCaptcha

# Initialize the ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


    # Open the target webpage
driver.get("https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=kara&realmId=967&categoryId=2801")

# Use WebDriverWait for dynamic content
wait = WebDriverWait(driver, 10)



lastname_input = driver.find_element(By.ID, 'appointment_captcha_month_captchaText')
last_name = "hanzla"  # Assuming this is from the previous 2Captcha result
lastname_input.send_keys(last_name)




# Capture page HTML
page_html = driver.page_source


print("Booking process completed. HTML saved to captured_page.html")


captcha_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'captcha div')))

# Extract the background-image style attribute
background_image_style = captcha_div.get_attribute("style")
print(background_image_style)
# Use regular expression to extract the base64 data from the style attribute
base64_match = re.search(r'url\(["\']?(data:image\/[a-zA-Z]+;base64,[^"\']*)["\']?\)', background_image_style)
print(base64_match)

# If a base64 image is found, extract it
if base64_match:
    base64_image = base64_match.group(1)
    print(base64_image)
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
        
    except Exception as e:
        sys.exit(e)



#appointment_newAppointmentForm_captchaText
#appointment_newAppointmentForm_appointment_addAppointmen