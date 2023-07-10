from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

import undetected_chromedriver as uc

from twilio.rest import Client

import time
import keys
import random

# Fill in your info here
# Dont add the dashes - for license
DRIVERS_LICENSE = "LXXXXXXXXXXXXXX"
# Dont add the slashes / for license
EXPIRY = "202XXXXX"
# You can add more than one centre, enter it as an array entry
CENTRES = [ "Toronto Etobicoke Centennial Park Plaza 5555 Eglinton Ave. W., Unit E120-124", ]

while True:
    # SMS Client
    sms_client = Client(keys.account_sid, keys.auth_token)

    # Fetch the driver test, pass the cloudflare security
    browser = uc.Chrome()
    browser.get('https://drivetest.ca/dtbookingngapp/registration/confirmRegistration')
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@href='/dtbookingngapp/registration/confirmRegistration']")))

    time.sleep(random.uniform(1, 15))

    action = ActionChains(browser)

    # Locate and navigate to sign in page
    sign_in_button = browser.find_element(By.XPATH, "//a[@href='/dtbookingngapp/registration/confirmRegistration']")
    sign_in_button.click()

    time.sleep(random.uniform(1, 10))

    # Locate and fill drivers license input
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "driverLicenceNumber")))
    license_input = browser.find_element(By.ID, "driverLicenceNumber")
    license_input.send_keys(DRIVERS_LICENSE)

    time.sleep(random.uniform(1, 10))

    # Locate and fill expireday date input
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "driverLicenceExpiry")))
    license_input = browser.find_element(By.ID, "driverLicenceExpiry")
    license_input.send_keys(EXPIRY)

    time.sleep(random.uniform(1, 10))

    # Locate and press submit
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".mat-focus-indicator.mat-raised-button.mat-button-base.mat-primary.drivetest-landf.mt-2.mb-2")))
    submit_button = browser.find_element(By.CSS_SELECTOR, ".mat-focus-indicator.mat-raised-button.mat-button-base.mat-primary.drivetest-landf.mt-2.mb-2")
    submit_button.click()

    time.sleep(random.uniform(1, 10))

    # Locate the reschedule button and click
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".btn.btn-quaternary.buttonRescheduleTest.w-100")))
    reschedule_button = browser.find_element(By.CSS_SELECTOR, ".btn.btn-quaternary.buttonRescheduleTest.w-100")
    reschedule_button.click()

    time.sleep(random.uniform(1, 3))

    # At this point, there should be a confirmation popup. Click through to reschedule page
    reschedule_button = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//button[.//span[contains(text(), "Reschedule")]]')))
    reschedule_button.click()

    time.sleep(random.uniform(1, 10))

    # Now we are at the juicy part. A session timer starts with 45 minutes. 
    # Lets use 35 minutes to leave some margin for actually signing up. 
    # First intially load the calendar
    # During the 35 minutes, we will scan through all the desired centres for updates at a minimum of 1-3 minutes per load
    # Should a time be discovered, notify user

    # Start 35 minute timer
    start_time = time.time()
    current_time = time.time()
    set_prev_month = False

    while (current_time - start_time) / 60 < 35:
        
        for centre in CENTRES:
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".mat-focus-indicator.mat-raised-button.mat-button-base.mat-primary.drivetest-landf.mt-2.mb-2")))

            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, f"//button[@aria-label='{centre}']")))
            centre_button = browser.find_element(By.XPATH, f"//button[@aria-label='{centre}']")
            
            ActionChains(browser)\
            .scroll_to_element(centre_button)\
            .perform()

            time.sleep(random.uniform(1, 3))

            centre_button.click()

            continue_button = browser.find_element(By.CSS_SELECTOR, ".mat-focus-indicator.mat-raised-button.mat-button-base.mat-primary.drivetest-landf.mt-2.mb-2")
            continue_button.click()

            time.sleep(random.uniform(1, 5))

            if(set_prev_month == False):
                WebDriverWait(browser, 50).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-labelledby='previous-label']")))
                prev_month_button = browser.find_element(By.XPATH, "//button[@aria-labelledby='previous-label']")
                prev_month_button.click()
                set_prev_month = True

            time.sleep(random.uniform(1, 10))

            # Search through available date tiles in current month
            available_dates_buttons = browser.find_elements(By.CSS_SELECTOR, ".date-selection-coontainer.custom-date-selection-button.date-available")
            
            location_spot_flag = False
            for date_button in available_dates_buttons:
                date_button.click()

                time.sleep(random.uniform(1, 5))

                continue_buttons = browser.find_elements(By.CSS_SELECTOR, ".mat-focus-indicator.mat-raised-button.mat-button-base.mat-primary.drivetest-landf.mt-2.mb-2")
                continue_buttons[1].click()

                time.sleep(2)

                # Once we hit a time widget, a spot is open
                times_available = browser.find_elements(By.CSS_SELECTOR, "app-time-widget")
                if (len(times_available) > 0):
                    location_spot_flag = True
                    break
        
            if location_spot_flag:
                message = sms_client.messages.create(
                    body="Spot has opened for Drivetest Location: " + centre,
                    from_=keys.twilio_number,
                    to=keys.target_number
                )
                call = sms_client.calls.create(
                    url='http://demo.twilio.com/docs/voice.xml',
                    from_=keys.twilio_number,
                    to=keys.target_number
                )
                time.sleep(500)
        current_time = time.time()
    browser.quit()
