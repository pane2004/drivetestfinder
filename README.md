# Ontario Drivetest Spot Finder
A Selenium-based webscraper for the Ontario Drivetest spots.
This script is intended to search for spots in the current month which are usually booked out. While running, it will detect any spots that open up from cancellations, etc.
If a spot appears, it will send you a text with the specific location and give you a call via the Twilio API.

# Usage
1. You must already have an Ontario Drivetest account, and have a test pre-booked. The script will only attempt to reschedule should anything earlier become available.
2. Make sure you have chrome installed
3. Install the packages. The code assumes that Python 3.9+ and Pip are installed.
```
pip install selenium
pip install twilio
pip install undetected-chromedriver
```
3. Create a [Twilio](https://www.twilio.com/try-twilio) account and fill in ```keys.py```. Your target number can only be your own if you are using the trial account for Twilio.
4. Fill in the strings in ```main.py``` for the driver's license and expiry date.
5. For the centres, add the name as you see it in the centre selection.
For example, add the string "Nipisong" for the Nipisong location, or "Toronto Etobicoke" for the Etobicoke location.

![Image of the centre select](https://i.ibb.co/TL2kJdW/Screen-Shot-2023-07-10-at-12-19-22-AM.png "Location Select List")

7. Now, the script is ready. Let's run it!
```
python main.py
```
8. If everything was done currently, a new browser window should be open. Let it run in the background and do not touch it.

Note: The script is dependent on the UC module to pass the Cloudflare captcha. Should the module or captcha be updated, it may not work. 

# Disclaimer
1. The provided code herein is intended strictly for academic and research-related purposes. The user is responsible for complying with this usage policy.
2. The Drivetest website employs a layer of Cloudflare security, which limits its operation exclusively to the user's local computer or environment. Any attempts to deploy, distribute, or use this script for commercial purposes are highly likely to encounter blocking or other restrictive measures. The user is responsible for understanding and abiding by these constraints.
3. By opting to use any portion of this code, the user agrees to abide by the terms stipulated in the LICENSE. In doing so, the user accepts all responsibilities and potential consequences arising from misuse, which may include but are not limited to: IP address banning from the concerned website, suspension or revocation of driver's license, legal action from any relevant parties, being flagged by Cloudflare, or any other related punitive actions.
4. This disclaimer is not exhaustive and does not cover all potential risks and liabilities. It is the user's responsibility to fully understand the legal and ethical implications of using this code and to ensure their actions align with local, national, and international laws and regulations.
5. By using this code, the user acknowledges that the developers, contributors, and associated entities are not responsible for any harm or legal trouble that results from code misuse. The user assumes all liabilities resulting from their actions.
6. The user acknowledges and agrees that the code may contain certain vulnerabilities, errors, or other potential risks. The user assumes all risk for any damages, losses, or other consequences that may result from these vulnerabilities.
7. The developer reserves the right to modify this disclaimer at any time. The user is responsible for regularly reviewing and adhering to the most recent version of the disclaimer.
8. The continued use of this code signifies your acceptance of these terms.
