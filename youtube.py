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

from lxml import etree
from io import StringIO, BytesIO


## load webpage and waits until it's loaded 
def wait_loading():
    """ 
    Wait for selenium page to be ready 
    """
    return driver.execute_script('return document.readyState;') != 'complete' 



# chrome options for Root user
# options.add_experimental_option("prefs",prefs)
# options.add_argument("--no-sandbox") 
# options.add_argument("--disable-gpu")
# options.add_argument("--disable-dev-shm-usage")


#webdriver.chrome(chromedirer=/path/gecko)
#,chrome_options=options)

driver = webdriver.Chrome(ChromeDriverManager().install()) 
driver.get("https://www.youtube.com")




#================= Wait for Load 
while not(wait_loading):
    print("Loading ...")
print("Loaded index > ....")
#================= End Waiting
# printing title
print(driver.title)


# dumping html to a file 
output = open("youtube.html","w")
output.write(driver.page_source)

# creating tree  from HTMl Source
parser = etree.HTMLParser()
tree   = etree.parse(StringIO(driver.page_source), parser)


# creating the optimal XPATH for the video title
# '//yt-formatted-string[@id="video-title"]/text()'
#//Object[@id="id of the object"]/text() ==> local xpath 
# /html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-item-renderer[29]/div/ytd-rich-grid-media/div[1]/div/div[1]/h3/a/yt-formatted-string
titles = tree.xpath('//yt-formatted-string[@id="video-title"]/text()')
for title in titles:
    print("The vide title is : {}".format(title))


