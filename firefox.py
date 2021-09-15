
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from user_agent import generate_user_agent, generate_navigator
options = Options()


res = generate_user_agent(os='android')

# user_agent = random.choice(user_agent_list)
options.add_argument("--start-maximized")
options.add_argument(f'user-agent={res}')
# options.add_argument("window-size=1400,600")

driver = webdriver.Chrome('D:\\Project\\PythonScript\\drivers\\chromedriver.exe',options=options)
driver.get('https://mobile.dollarcat.net')
user_agent = driver.execute_script("return navigator.userAgent;")
print(user_agent)

