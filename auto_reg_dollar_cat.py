import random
import threading

import cv2
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

from read_outlook_mail import OutLook
from data.user import User
import data.managedatabase

user_agent_list = User.user_agent_list


class DollarCat:
    t1 = True

    def __init__(self, username, pwd, ssh_session):  # username, pwd

        self.username = username
        self.pwd = pwd
        self.ssh_session = ssh_session

        self.count = 0
        self.ERROR = 0

        user_agent = random.choice(user_agent_list)

        # Chrome options
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("--start-maximized")
        options.add_argument("--incognito")
        # Driver
        self.driver = webdriver.Chrome('D:\\Project\\PythonScript\\drivers\\chromedriver.exe', options=options)

    # def load_url(self):
    #     user_agent = self.driver.execute_script("return navigator.userAgent;")
    #     print(str(user_agent))
    #     self.driver.get("https://mobile.dollarcat.net")
    #     return user_agent

    def start(self):

        user_agent = self.driver.execute_script("return navigator.userAgent;")
        print(str(user_agent))
        self.driver.get("https://mobile.dollarcat.net")

        timeout1 = 20
        try:
            element_present = EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div[1]/div/i"))
            element = WebDriverWait(self.driver, timeout1).until(element_present)
            element.click()

            # wait for a signup button present
            signup_present = EC.presence_of_element_located((By.CSS_SELECTOR, ".register-btn.flex-level-center"))
            element = WebDriverWait(self.driver, timeout1).until(signup_present)
            element.click()
            time.sleep(1)

            # email button
            email_present = EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div[2]"))
            element = WebDriverWait(self.driver, timeout1).until(email_present)
            element.click()
            time.sleep(1)

            # enter email
            element_present = EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div[1]/div[3]/div[1]/div/div[1]/input"))
            element = WebDriverWait(self.driver, timeout1).until(element_present)
            element.send_keys(self.username)
            time.sleep(3)

            # enter password
            element_present = EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div[1]/div[3]/div[2]/div/div/input"))
            element = WebDriverWait(self.driver, timeout1).until(element_present)
            element.send_keys(self.pwd)
            time.sleep(3)

            # confirm password
            element_present = EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div[1]/div[3]/div[3]/div/div/input"))
            element = WebDriverWait(self.driver, timeout1).until(element_present)

            element.send_keys(self.pwd)
            time.sleep(3)

            # send button
            send_present = EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[3]/div[4]/div/div/div"))
            element = WebDriverWait(self.driver, timeout1).until(send_present)
            element.click()

            # switch to iframe
            element_present = EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/iframe"))
            iframe = WebDriverWait(self.driver, timeout1).until(element_present)
            self.driver.switch_to.frame(iframe)
            print("Switch to iframe")
            time.sleep(2)

            return user_agent

        except TimeoutException:
            self.ERROR = 3
            print("Timed out waiting for page to load")
            self.end_session_dollar_cat()

    def download_image(self):
        timeout1 = 30
        try:

            # download a piece
            element_present = EC.presence_of_element_located(
                (By.ID, "slideBlock"))
            element = WebDriverWait(self.driver, 30).until(element_present)
            # sliderBlock = self.driver.find_element_by_id("slideBlock").get_attribute("src")
            sliderBlock = element.get_attribute("src")
            print(sliderBlock)
            self.download(sliderBlock, "sliderBlock")

            # download a background img
            bg_present = EC.presence_of_element_located((By.ID, "slideBg"))
            element = WebDriverWait(self.driver, timeout1).until(bg_present)
            background = element.get_attribute("src")
            print(background)
            self.download(background, "background")

        except TimeoutException:
            print("Timed out waiting for downloading an image")
            self.end_session_dollar_cat()

    def download(self, url, filename):

        myfile = requests.get(url)

        open('D:\Project\PythonScript\captcha\{}.png'.format(filename), 'wb').write(myfile.content)

    def automate_slider(self):
        timeout = 30
        print('sliding count: ' + str(self.count))
        self.count += 1

        distance = self.distance()
        try:
            # sliding
            element_present = EC.presence_of_element_located((By.XPATH, "/html/body/div/div[3]/div[2]/div[2]/div[2]"))
            element = WebDriverWait(self.driver, timeout).until(element_present)
            ActionChains(self.driver).click_and_hold(element).move_by_offset(distance, 0).release().perform()
            time.sleep(1)
            element.click()

            time.sleep(3)

            if self.t1 is True:
                thresh = threading.Thread(self.refresh())
                thresh.start()


        except TimeoutException:
            # self.end_session_dollar_cat()
            print("Timed out waiting for sliding")

    def enter_code(self):
        timeout1 = 60
        # switch to default content
        self.driver.switch_to.default_content()

        outlook = OutLook(self.username, self.pwd)
        outlook.read_email()

        verification_code = outlook.read_verification_code()
        print(verification_code)

        try:
            # enter verification code
            element_present = EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div[1]/div[3]/div[4]/div/div/input"))
            element = WebDriverWait(self.driver, timeout1).until(element_present)
            element.send_keys(verification_code)

        except TimeoutException:
            print("get_code time out")
            self.end_session_dollar_cat()

    def register_now_button(self):
        timeout1 = 15
        try:
            self.driver.switch_to.default_content()
            # press register button
            element_present = EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div[1]/button"))
            element = WebDriverWait(self.driver, timeout1).until(element_present)
            element.click()
            print("Clicked register")

            time.sleep(5)


        except TimeoutException:
            self.end_session_dollar_cat()
            print("Timed out")

    def register_status(self):
        timeout1 = 5
        try:
            # press register button
            element_present = EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div[1]/div[5]"))
            element = WebDriverWait(self.driver, timeout1).until(element_present)
            if element.text == 'User Already Exists':
                return 1
            elif element.text == 'Network error, please refresh':
                return 3
            else:
                return 0
        except TimeoutException:
            print("No register status")
            return 0

    def distance(self):
        small_image = cv2.imread('captcha/sliderBlock.png')
        large_image = cv2.imread('captcha/background.png')
        result = cv2.matchTemplate(small_image, large_image, cv2.TM_CCOEFF_NORMED)
        mn, _, mnLoc, _ = cv2.minMaxLoc(result)
        MPx, MPy = mnLoc
        # print(MPx)
        # print(MPy)
        trows, tcols = small_image.shape[:2]

        distant = (MPx + tcols / 2) * (303.5 / 694)  # laptop
        # distant = (MPx + tcols / 2) * (300.5 / 694)  # miA1
        # distant = (MPx + tcols / 2) * (263.5 / 694) # vinSmart
        print(distant)
        return distant

    def refresh(self):
        timeout = 10
        if self.count == 5:
            self.t1 = False
            self.end_session_dollar_cat()

        try:
            element_present = EC.presence_of_element_located((By.ID, "reload"))
            WebDriverWait(self.driver, timeout).until(element_present)
            refresh = self.driver.find_element(By.ID, "reload")

            while refresh is not None:
                refresh.click()
                time.sleep(3)
                self.download_image()
                self.automate_slider()
            self.t1 = False

        except:
            self.t1 = False


    def end_session_dollar_cat(self):
        self.driver.close()
        self.driver.quit()
        data.managedatabase.kill(self.ssh_session)
