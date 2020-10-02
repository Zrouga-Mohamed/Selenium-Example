
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
import time 
import os 
import glob 



def is_root():
    """ 
    Check if user is root or Not 
    """
    print("Your UID is : ",os.geteuid())
    return os.geteuid() == 0


def wait_loading():
    """ 
    Wait for selenium page to be ready 
    """
    return driver.execute_script('return document.readyState;') != 'complete' 





""" 
    Initial Step : define the driver
"""

# Create the downloads dir and make sure it's writable for every user
cwd = os.getcwd()
if not os.path.exists('downloads'):
    os.makedirs('downloads')
    os.system('chmod 777 -R downloads/')

# Add a download folder in chrome prefs for files to be saved in 
prefs = {'download.default_directory': cwd+'/downloads/'}
options = webdriver.ChromeOptions()

# whoami ?
if is_root():
    print("Hey , chrome is headless as Root! follow prints !!")
    options.set_headless()

# Options for driver
options.add_experimental_option("prefs",prefs)
options.add_argument("--no-sandbox") 
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")


driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)

# get the url
driver.get("https://opensource-demo.orangehrmlive.com/")




#================= Wait for Load 
while not(wait_loading):
    print("Loading ...")
print("Loaded index > Login now ....")
#================= End Waiting
print(driver.title)

#===================== Login

Login=driver.find_element_by_id("txtUsername")
Password=driver.find_element_by_id("txtPassword")
Login.send_keys("Admin")
Password.send_keys("admin123")
Password.send_keys(Keys.RETURN)
#===================== END Login 


#================= Wait for Load 
while not(wait_loading):
    print("Loading ...")
print("Loaded : Logged in  > Go to some menu with hover now  ....")
#================= End Waiting



#===================== Get Items

actions_menu = driver.find_element_by_id("menu_maintenance_purgeEmployee")
child = driver.find_element_by_id("menu_maintenance_accessEmployeeData")

actions = ActionChains(driver)
actions.move_to_element(actions_menu).click(child).perform()


#======== Verify Password
Password=driver.find_element_by_xpath('//*[@id="confirm_password"]')
Password.send_keys("admin123")
Password.send_keys(Keys.RETURN)


#================= Wait for Load 
while not(wait_loading):
    print("Loading ...")
print("Loaded : List of requests  > Verify password now ....")
#================= End Waiting

search=driver.find_element_by_id('employee_empName')
search.send_keys("Dibyesh123456 Dash")
search.send_keys(Keys.RETURN)

#================= Wait for Load 
while not(wait_loading):
    print("Loading ...")
print("Loaded : Got list  > Download now ....")
#================= End Waiting

search.send_keys(Keys.RETURN)


#================= Wait for Load 
while not(wait_loading):
    print("Loading ...")
print("Loaded : Downloaded  > Check file content  ....")
#================= End Waiting


# Downloaded file location  

print(cwd)
time.sleep(2)


print("Getting the file from the creation date time....")
list_of_files = glob.glob(cwd+"/downloads/*") # you can filter for specific file types *.json or *.xlsx

file_name = max(list_of_files, key=os.path.getctime)

f = open(file_name)
Res = f.readlines()
print(Res)  

time.sleep(3)
driver.quit()
#==================== End Items