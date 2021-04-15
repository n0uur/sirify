import selenium.webdriver as webdriver

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import os
import time
import requests

from dotenv import load_dotenv

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")

def changeStatus(word):
    print("[Log] Changing to :", word)

    status = str(word).strip(' ')

    requests.patch(
        'https://discord.com/api/v8/users/@me/settings',
        json = {
            "custom_status": {
                "text": status
            }
        },
        headers = {
            "origin": "https://discord.com",
            "referer": os.environ.get("PROFILE_REFERER"),
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
            "authorization": os.environ.get("PROFILE_TOKEN"),
            "Content-Type": "application/json"
        }
    )

    print("[Log] Changed! :", status)

def main():
    global PROJECT_ROOT, DRIVER_BIN

    load_dotenv()

    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=" + os.environ.get("PROFILE_NAME")) 

    browser = webdriver.Chrome(executable_path = DRIVER_BIN, options=chrome_options)
    browser.get('https://open.spotify.com/lyrics')

    time.sleep(2)

    # button = browser.find_element_by_xpath("//button[@data-testid='login-button']")
    # button.click()

    _ = input('Login and then press [Enter]')

    print("current lyrics...")

    lastLyric = None

    while True:

        try:

            currentLyric = None

            lyrics_windows = browser.find_element_by_class_name('main-view-container')

            # print(lyrics_windows.text)

            if ("These lyrics aren't time synced, yet." in lyrics_windows.text or
                "It looks like we don't have" in lyrics_windows.text):
                currentLyric = None
            else:
                # get current lyrics
                lyrics_element = lyrics_windows.find_element_by_xpath("//p[@style='--animation-index:1;']")
                # print(lyrics_element.text)
                currentLyric = lyrics_element.text

            # update status

            if currentLyric != lastLyric:
                lastLyric = currentLyric

                if(currentLyric == None):
                    # change to music name..
                    music_name = browser.find_element_by_xpath("//a[@data-testid='nowplaying-track-link']").text
                    artist_name = browser.find_element_by_xpath("//div[@data-testid='track-info-artists']").text
                    
                    changeStatus("%s - %s" % (music_name, artist_name))
                else:
                    changeStatus(currentLyric)

                # print(currentLyric)

            time.sleep(0.5)
        except:
            print("Something error... rest for 5 secs..")
            time.sleep(5)

if __name__ == "__main__":
    main()
