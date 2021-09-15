from selenium import webdriver

from data.user import User
import random

user_agent_list = User.user_agent_list


def setDriver():
    user_agent = random.choice(user_agent_list)
    print(user_agent)
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--start-maximized")
    options.add_argument("--incognito")
    # Driver
    driver = webdriver.Chrome('D:\\Project\\PythonScript\\drivers\\chromedriver.exe', options=options)
    return driver


driver = setDriver()
