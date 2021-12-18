#  MIT License
#
#  Copyright (c) 2021 Obaydah BOUIFADENE
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import json
import time
import validators
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


link = input("please enter the link of the book : ")
if not validators.url(link):
    raise RuntimeError("not a url")


def initialize_selenium():
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # chromedriver 75+

    chrome_options = Options()

    chrome_options.binary_location = input("please enter the path of the chromium based driver /version 92 - for more assistance "
                                           "on that regard please open an issue in the github repo ")
    # "/usr/bin/brave-browser "
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    return webdriver.Chrome(chrome_options=chrome_options, desired_capabilities=capabilities)


def flip_pages(driver):
    driver.get(link)
    frame = driver.find_element_by_tag_name('iframe')
    driver.switch_to.frame(frame)
    try:
        fullscreen_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'clickToRead')))
        print("fullscreen_button is ready!")
    except TimeoutException:
        print("Loading took too much time!")
    # noinspection PyUnboundLocalVariable
    fullscreen_button.click()
    for i in range(20):
        try:
            next_slide_button = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'flip-next-page')))
            print("next_slide_button is ready!")
        except TimeoutException:
            print("Loading took too much time!")
        # noinspection PyUnboundLocalVariable
        driver.execute_script("arguments[0].click();", next_slide_button[1])
        time.sleep(2)


def get_number_of_pages():
    # i still need a more accurate way
    #      return counter*2 #give or take
    pass


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


def generate_logs():
    driver = initialize_selenium()
    flip_pages(driver)
    process_browser_logs_for_network_events(driver.get_log("performance"))
