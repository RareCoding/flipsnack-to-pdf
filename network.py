import json
import pprint

from selenium import webdriver

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

capabilities = DesiredCapabilities.CHROME
# capabilities["loggingPrefs"] = {"performance": "ALL"}  # chromedriver < ~75
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # chromedriver 75+

chrome_options = Options()
chrome_options.binary_location = "/usr/bin/brave-browser"
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(chrome_options=chrome_options, desired_capabilities=capabilities)
driver.get("https://www.flipsnack.com/7B76FA77C6F/guide-du-rapport-de-stage-pour-les-coles-d-ing-nieurs-en-in.html")


# myElem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'wrapper')))
# elem = driver.find_element_by_class_name("wrapper")
#
# elem.click()
def process_browser_logs_for_network_events(logs):
    """
    Return only logs which have a method that start with "Network.response", "Network.request", or "Network.webSocket"
    since we're interested in the network events specifically.
    """
    for entry in logs:
        log = json.loads(entry["message"])["message"]
        if (
                "Network.response" in log["method"] and "params" in log and "headers" in log[
            "params"] and "content-type" in log["params"]["headers"] and "image" in
                log["params"]["headers"]["content-type"]
        ):
            yield log


logs = driver.get_log("performance")
events = process_browser_logs_for_network_events(logs)
with open("log_entries.json", "wt") as out:
    for event in events:
        pprint.pprint(event, stream=out)
