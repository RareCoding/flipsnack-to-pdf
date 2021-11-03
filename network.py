import json
import pprint
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

capabilities = DesiredCapabilities.CHROME
# capabilities["loggingPrefs"] = {"performance": "ALL"}  # chromedriver < ~75
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # chromedriver 75+

chrome_options = Options()
chrome_options.binary_location = "/usr/bin/brave-browser"
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(chrome_options=chrome_options, desired_capabilities=capabilities)
driver.get("https://www.flipsnack.com/7B76FA77C6F/guide-du-rapport-de-stage-pour-les-coles-d-ing-nieurs-en-in.html")
# driver.switch_to.default_content()
frame = driver.find_element_by_tag_name('iframe')

driver.switch_to.frame(frame)
try:
    fullscreen_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'clickToRead')))
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")
fullscreen_button.click()


# if next_button is None == 0:
#     time.sleep(3)
#     next_button = driver.find_element_by_id("clickToRead")
# if next_button is None == 0:
#     raise RuntimeError("couldn't find wrapper'")
# time.sleep(1)


# myElem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'wrapper')))
# elem = driver.find_element_by_class_name("wrapper")
#
# next_button.click()
def process_browser_logs_for_network_events(logs):
    """
    Return only logs which have a method that start with "Network.response", "Network.request", or "Network.webSocket"
    since we're interested in the network events specifically.
    """
    result = []
    for entry in logs:
        log = json.loads(entry["message"])["message"]
        if (
                "Network.request" in log["method"]
                #     and "params" in log
                #     and "headers" in log[
                # "params"] and "path" in log["params"]["headers"]
                # and "original" in log["params"]["headers"]["path"]
        ):
            result.append(log)
    new_dict = {}
    counter = 0
    for item in result:
        new_dict[str(counter)] = item
        counter += 1
    with open("log_entries.json", "wt") as out:
        json.dump(new_dict,out)


#
logs = driver.get_log("performance")
events = process_browser_logs_for_network_events(logs)
# with open("log_entries.json", "wt") as out:
#     json.dump(events, out)
#     # counter = 0
#     # for event in events:
#     #     pprint.pprint(event, stream=out)
#
# # document.querySelector('html > body > #fsw > [id^="fsw_widget"] > #mainLayout > #clickToRead > [class="wrapper"] > [class="click-to-read"]').click()
#
# # document.querySelector('html > body > [class="page-wrap"] > [class="auto-height"] > #myPlayer > iframe > html')
