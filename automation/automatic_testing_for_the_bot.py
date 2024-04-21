import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
import pyautogui

BOT_ID = 'Image_Hash_1Bot'

real_files = ["download.jpg", "pass.txt", "images.png", "images21.jpg"]
abs_file = [os.path.abspath(os.getcwd()) + "\\automation" +"\\files_for_testing\\" + file for file in real_files]
for i in range(len(abs_file)):
    abs_file[i] = abs_file[i].replace("\\\\", "\\")
    
IMAGE_PATH = abs_file[0]
INVALID_FILE_PATH_LIST = [abs_file[1] , abs_file[2]]
JPG_FILE_PATH = abs_file[3]

TEXT_RESULT_EXPECTAION = 'ERRO: can only handle image messages.'
JPG_IMAGE_RESULT_EXPECTAION = 'Hash of the photo:'
FILE_RESULT_EXPECTAION = "ERROR: send me a JPG or JPEG image."

def main():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://web.telegram.org/a/')

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'sign_in_button')))
        time.sleep(2)
    except TimeoutException:
        print("Logging in. Proceeding with bot interaction.\n")

    try:
        time.sleep(5)
        search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Search"]')))
        search_input.send_keys(BOT_ID)
        time.sleep(2)
        
        first_result = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="LeftColumn-main"]/div[2]/div[2]/div/div[2]/div/div[1]/div/div')))
        time.sleep(2)
        first_result.click()

        start_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="MiddleColumn"]/div[4]/div[1]/div[2]/div/button[1]/div')))
        start_button.click()

        time.sleep(3)
        
        test_send_jpg_image(driver)
        test_send_text_instead_of_image(driver)
        test_send_invalid_files(driver)
        test_send_jpg_files(driver)
    except TimeoutException:
        print("Timed out waiting for elements.")

    driver.quit()
    
    
def send_text(driver):
    text_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="editable-message-text"]')))
    text_input.send_keys("testing result" + "\n")
    time.sleep(3)
    message_elements = driver.find_elements(By.CLASS_NAME, 'message-content')
    time.sleep(1)
    return message_elements[-1].text.strip().split("\n")
     
    
def send_image(driver, image_path):
    attachment_button = driver.find_element(By.XPATH, '//*[@id="MiddleColumn"]/div[4]/div[2]/div/div[2]/div[1]/div[2]/div/div[3]')
    attachment_button.click()
    time.sleep(1)
    
    send_image_option = driver.find_element(By.XPATH, '//*[@id="attach-menu-controls"]/div/div[1]')
    send_image_option.click()
    time.sleep(1)

    time.sleep(2)
    pyautogui.write(image_path)
    pyautogui.press('enter')

    time.sleep(1)
    send_button = driver.find_element(By.XPATH,'//*[@id="portals"]/div[2]/div/div/div[2]/div[2]/div/div[2]/div[3]/div[2]/button')
    send_button.click()
    
    time.sleep(3)
    message_elements = driver.find_elements(By.CLASS_NAME, 'message-content')
    time.sleep(1)
    return message_elements[-1].text.strip().split("\n")
     

def send_file(driver, file_path):
    attachment_button = driver.find_element(By.XPATH, '//*[@id="MiddleColumn"]/div[4]/div[2]/div/div[2]/div[1]/div[2]/div/div[3]')
    attachment_button.click()

    send_file_option = driver.find_element(By.XPATH, '//*[@id="attach-menu-controls"]/div/div[2]')
    send_file_option.click()
    time.sleep(1)
    
    pyautogui.write(file_path)
    pyautogui.press('enter')

    time.sleep(2)

    send_button = driver.find_element(By.XPATH, '//*[@id="portals"]/div[2]/div/div/div[2]/div[2]/div/div[2]/div[3]/div[2]/button')
    send_button.click()
    
    time.sleep(5)
    message_elements = driver.find_elements(By.CLASS_NAME, 'message-content')
    time.sleep(1)
    return message_elements[-1].text.strip().split("\n")
    
     

def test_send_jpg_image(driver):
    result = send_image(driver, IMAGE_PATH)
    if JPG_IMAGE_RESULT_EXPECTAION in result[0]:
        print("Test Passed: Sending a *.jpg image passed successfully.\n")
    else:
        print("Test Failed: Sending a *.jpg image failed.\n")

def test_send_text_instead_of_image(driver):
    result = send_text(driver)
    if TEXT_RESULT_EXPECTAION == result[0]:
        print("Test Passed: Sending text instead of an image resulted in an error message.\n")
    else:
        print("Test Failed: Sending text instead of an image did not result in an error message.\n")

def test_send_invalid_files(driver):
    for file_path in INVALID_FILE_PATH_LIST:
        result = send_file(driver, file_path)
        if FILE_RESULT_EXPECTAION == result[0]:
            print(f"Test Passed: Sending {file_path} resulted in an error message.\n")
        else:
            print(f"Test Failed: Sending {file_path} did not result in an error message.\n")
            
def test_send_jpg_files(driver):
    result = send_file(driver, JPG_FILE_PATH)
    if JPG_IMAGE_RESULT_EXPECTAION in result[0]:
        print(f"Test Passed: Sending {JPG_FILE_PATH} Passed the test.\n")
    else:
        print(f"Test Failed: Sending {JPG_FILE_PATH} result in an error message or unexpected message.\n")

if __name__ == "__main__":
    main()