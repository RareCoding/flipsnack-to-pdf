import json
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

capabilities = DesiredCapabilities.CHROME
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # chromedriver 75+

chrome_options = Options()
chrome_options.binary_location = "/usr/bin/brave-browser"
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(chrome_options=chrome_options, desired_capabilities=capabilities)
driver.get("link")
frame = driver.find_element_by_tag_name('iframe')

driver.switch_to.frame(frame)
try:
    fullscreen_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'clickToRead')))
    print("fullscreen_button is ready!")
except TimeoutException:
    print("Loading took too much time!")
fullscreen_button.click()
counter = 0
for i in range(20):
    try:
        next_slide_button = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'flip-next-page')))
        print("next_slide_button is ready!")
    except TimeoutException:
        print("Loading took too much time!")

    counter += 1
    driver.execute_script("arguments[0].click();", next_slide_button[1])
    time.sleep(2)

    # for j in next_slide_button.find_elements_by_css_selector("*"):
    #     print(j.tag_name)

def get_number_of_pages():
    # i still need a more accurate way
         return counter*2 #give or take

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
        ):
            result.append(log)
    new_dict = {}
    counter = 0
    for item in result:
        new_dict[str(counter)] = item
        counter += 1
    with open("log_entries.json", "wt") as out:
        json.dump(new_dict, out)


process_browser_logs_for_network_events(driver.get_log("performance")
)