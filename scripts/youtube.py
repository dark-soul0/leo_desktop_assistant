import time

import pyautogui
from pytube import YouTube
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)


def youtube():
    driver.get('https://www.youtube.com/')
    driver.implicitly_wait(10)


def search_song(n):
    search = driver.find_element(By.NAME, 'search_query')
    search.send_keys(n)
    button = driver.find_element(By.ID, "search-icon-legacy")
    button.click()
    # pyautogui.press('enter')
    driver.implicitly_wait(5)
    first_result = driver.find_element(By.XPATH, '//*[@id="video-title"]/yt-formatted-string')
    first_result.click()


def skip_ad():
    try:
        time.sleep(5)
        skip_button = driver.find_element(By.CLASS_NAME, 'ytp-skip-ad-button__icon')
        skip_button.click()
        print("ad skipped")
    except:
        time.sleep(2)
        print("ad not skippeble")


# Function to open history
def open_history():
    try:
        # Open YouTube history
        driver.get('https://www.youtube.com/feed/history')
        time.sleep(5)
        print("Opened YouTube history.")
    except Exception as e:
        print(f"Error opening history: {e}")


# play next song
def play_next_song():
    try:
        next_button = driver.find_element(By.CLASS_NAME, 'ytp-next-button')
        next_button.click()
        print("Playing next song.")
    except Exception as e:
        print(f"Error playing next song: {e}")


def stop_song():
    pyautogui.press('k')
    print("song has been stoped")


def play_back_speed_i():
    pyautogui.hotkey("shift + >")


def play_back_speed_d():
    pyautogui.hotkey("shift + <")


def download_song():
    current_url = driver.current_url
    print(current_url)

    try:
        yt = YouTube(current_url)
    except Exception as e:
        print(f"Error initializing YouTube object: {e}")
        return

    try:
        length = yt.length
        title = yt.title
        # Remove characters that are not allowed in filenames
        safe_title = "".join(x for x in title if x.isalnum() or x in "._- ")

        # Check for progressive streams (which contain both audio and video)
        stream = yt.streams.filter(progressive=True, res="480p").first()

        if stream:
            stream.download(output_path="", filename=f'{safe_title}.mp4')
            print(f"Downloaded: {safe_title}.mp4")
        else:
            print("Stream with the required resolution not found")
    except Exception as e:
        print(f"Error downloading video: {e}")


if __name__ == "__main__":
    youtube()
    driver.implicitly_wait(2)
    s = "blue eyes"
    search_song(s)
    skip_ad()
    # time.sleep(10)
    # stop_song()
    # play_next_song()
    # open_history()
    # download_song()
