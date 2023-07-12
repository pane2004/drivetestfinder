from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

import undetected_chromedriver as uc

from twilio.rest import Client

import time
import keys
import locations
import random

# Fill in your info here
# Dont add the dashes - for license
DRIVERS_LICENSE = ""
# Dont add the slashes / for license
EXPIRY = ""
# Enter the centre location as you see it on the website
CENTRES = [ "Brampton", ]

def click_element(browser, identifier, method=By.ID, wait_time=10):
    WebDriverWait(browser, wait_time).until(EC.presence_of_element_located((method, identifier)))
    button = browser.find_element(method, identifier)
    button.click()

def send_keys_to_element(browser, identifier, keys, method=By.ID, wait_time=10):
    WebDriverWait(browser, wait_time).until(EC.presence_of_element_located((method, identifier)))
    input_field = browser.find_element(method, identifier)
    input_field.send_keys(keys)

# SMS Client
sms_client = Client(keys.account_sid, keys.auth_token)

run_program = True
error_count = 0

while run_program:
    try:
        # Fetch the driver test, pass the cloudflare security
        options = uc.ChromeOptions()
        options.add_argument('--auto-open-devtools-for-tabs')
        options.add_argument("--start-fullscreen")
        browser = uc.Chrome(options=options)
        browser.get('https://drivetest.ca/dtbookingngapp/registration/confirmRegistration')
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@href='/dtbookingngapp/registration/confirmRegistration']")))

        time.sleep(random.uniform(1, 15))

        action = ActionChains(browser)

        # Locate and navigate to sign in page
        click_element(browser, "//a[@href='/dtbookingngapp/registration/confirmRegistration']", By.XPATH)

        time.sleep(random.uniform(1, 5))

        # Locate and fill drivers license input
        send_keys_to_element(browser, "driverLicenceNumber", DRIVERS_LICENSE)

        time.sleep(random.uniform(1, 2))

        # Locate and fill expireday date input
        send_keys_to_element(browser, "driverLicenceExpiry", EXPIRY)

        time.sleep(random.uniform(1, 2))

        # Locate and press submit
        click_element(browser, ".mat-focus-indicator.mat-raised-button.mat-button-base.mat-primary.drivetest-landf.mt-2.mb-2", By.CSS_SELECTOR)

        time.sleep(random.uniform(1, 2))
        
        # Locate the reschedule button and click
        click_element(browser, ".btn.btn-quaternary.buttonRescheduleTest.w-100", By.CSS_SELECTOR, 50)

        time.sleep(random.uniform(3, 5))

        # At this point, there should be a confirmation popup. Click through to reschedule page
        click_element(browser, '//button[.//span[contains(text(), "Reschedule")]]', By.XPATH, 50)

        time.sleep(random.uniform(1, 3))

        # Now we are at the juicy part. A session timer starts with 45 minutes. 
        # Lets use 35 minutes to leave some margin for actually signing up. 
        # First intially load the calendar
        # During the 35 minutes, we will scan through all the desired centres for updates at a minimum of 1-3 minutes per load
        # Should a time be discovered, notify user

        # Start 35 minute timer
        start_time = time.time()
        current_time = time.time()
        set_prev_month = False

        # TODO: send notification when program stops runnning due to error, etc
        while (current_time - start_time) / 60 < 35:
            for centre in CENTRES:
                # find the id of centre
                centre_id=locations.LOCATIONS_HASHMAP[centre]

                # scroll and click the centre button
                WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.ID, f"{centre_id}")))
                centre_button = browser.find_element(By.ID, f"{centre_id}")
                ActionChains(browser)\
                .scroll_to_element(centre_button)\
                .perform()
                time.sleep(random.uniform(1, 3))
                centre_button.click()

                click_element(browser, ".mat-focus-indicator.mat-raised-button.mat-button-base.mat-primary.drivetest-landf.mt-2.mb-2", By.CSS_SELECTOR, 50)

                time.sleep(random.uniform(1, 3))

                if(set_prev_month == False):
                    click_element(browser, "//button[@aria-labelledby='previous-label']", By.XPATH, 100)
                    set_prev_month = True

                time.sleep(random.uniform(1, 2))

                # Search through available date tiles in current month
                try:
                    available_dates_buttons = WebDriverWait(browser, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".date-selection-coontainer.custom-date-selection-button.date-available"))
                    )
                except:
                    available_dates_buttons = []
                
                location_spot_flag = False
                for date_button in available_dates_buttons:
                    time.sleep(random.uniform(1, 3))

                    date_button.click()

                    time.sleep(random.uniform(1, 2))

                    continue_buttons = WebDriverWait(browser, 50).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".mat-focus-indicator.mat-raised-button.mat-button-base.mat-primary.drivetest-landf.mt-2.mb-2"))
                    )
                    continue_buttons[1].click()

                    time.sleep(random.uniform(1, 2))

                    # Once we hit a time widget, a spot is open
                    try:
                        times_available = WebDriverWait(browser, 10).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "app-time-widget"))
                        )
                    except:
                        times_available = []
                    
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
                    # this will give you time to go to the scraper browser and book it
                    time.sleep(1000)
            current_time = time.time()
        browser.quit()
    except:
        error_count+=1
        error_msg = sms_client.messages.create(
                        body="An error has occured with the program",
                        from_=keys.twilio_number,
                        to=keys.target_number
                    )
        if (error_count > 10):
            run_program = False
            close_msg = sms_client.messages.create(
                        body="More than 10 errors have occured, aborting program",
                        from_=keys.twilio_number,
                        to=keys.target_number
                    )
