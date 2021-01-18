from selenium import webdriver
import time as TIME

from datetime import *

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

from datetime import datetime
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
baseUrl = "https://campaign.aliexpress.com/wow/gcp/ae/channel/ae/accelerate/tupr?spm=a2g0o.best.15027.6.23a12c25Tg01R2&wh_pid=ae/mega/ae/2020_global_shopping_festival_v2/Computers_Office_v2&wh_weex=true&_immersiveMode=true&wx_navbar_hidden=true&wx_navbar_transparent=true&ignoreNavigationBar=true&wx_statusbar_hidden=true&gps-id=300000000422666&productIds=4001042186695"
driver=webdriver.Chrome(chrome_options=chrome_options)
hrefs = []
ProductList = []
today = datetime.today()

driver.get(baseUrl)

print('ready')
prevN = 0

strt = TIME.time()
while(True):
    
    driver.execute_script("window.scrollTo(0, (document.body.scrollHeight))")
    TIME.sleep(2)
    newN = len(driver.find_elements_by_css_selector("a[href]"))
    if(prevN == newN):
        for product in driver.find_elements_by_css_selector("a[href]"):
            if(product.get_property('href').startswith('https://www.aliexpress.com/item/')):
                hrefs.append(product.get_property('href'))
        break
    else:
        prevN = newN

print("found ",len(hrefs)," products")
nd = TIME.time()
######################################
print("the search took : ",nd - strt)

def ScrapProductDetails(href):
    dates=[]
    driver.get(href)
    driver.execute_script("window.scrollTo(0, (document.body.scrollHeight)*0.8)")

    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li[ae_object_type="feedback"]'))).click()




    driver.switch_to.frame(WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[class="product-evaluation"]'))))
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[class="rate-score-number"]')))

    list = driver.find_elements_by_css_selector('span[class="r-time-new"]')
    for i in list:
        
        d = datetime.strptime(i.text, '%d %b %Y %H:%M')
        if(today - timedelta(days = 7) < d):
            dates.append(d)
############################### sort by latest
        




    for i in range(2):
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[id="complex-pager"]')))
        # goto = driver.find_elements_by_css_selector('a[class="ui-goto-page"]')[i]
        driver.execute_script("arguments[0].click();", driver.find_elements_by_css_selector('a[class="ui-goto-page"]')[i])
        # goto[i].click()
        prevN = 0
        while(True):
            TIME.sleep(1)
            newN = len(driver.find_elements_by_css_selector('span[class="r-time-new"]'))
            if(prevN == newN):
                for i in driver.find_elements_by_css_selector('span[class="r-time-new"]'):
                    dates.append(datetime.strptime(i.text, '%d %b %Y %H:%M'))
                    
                
                break
            else:
                prevN = newN
    a = sorted(dates,reverse=True)
    for date in a:
        print(date)
    print(len(dates))


hreftest = 'https://www.aliexpress.com/item/4001042186695.html?spm=a2g0o.tm537881.1700847540.1.7bc2iYHniYHn6E&&scm=1007.25281.150765.0&scm_id=1007.25281.150765.0&scm-url=1007.25281.150765.0&pvid=6cf7071b-9a41-4c4d-b9c0-ca4f22fca8e5&utparam=%7B"process_id":"1","x_object_type":"product","pvid":"6cf7071b-9a41-4c4d-b9c0-ca4f22fca8e5","belongs":[%7B"floor_id":"13663333","id":"375021","type":"dataset"%7D,%7B"id_list":["3626290","3317577"],"type":"gbrain"%7D],"scm":"1007.25281.150765.0","tpp_buckets":"21669%230%23186385%230_21669%234190%2319161%23349_15281%230%23150765%230","x_object_id":"4001042186695"%7D'
driver.get(hreftest)
TIME.sleep(2)
driver.refresh()

a=0
card = ""

l=len(hrefs)
for i in range(len(hrefs)):
    canDo=True
    card = ""
    while(canDo):
        if(card==""):
            try:
                ScrapProductDetails(hrefs[i])
                a=a+1
                print("product number :",a,"/",l)
                canDo=False
            except:
                card="yellow"
                print("failed")
        elif(card=="yellow"):
            try:
                ScrapProductDetails(hrefs[i])
                a=a+1
                print("product number :",a,"/",l)
                card = ""
                canDo=False
            except:
                card="red"
                canDo=False
                l=l-1
                print("failed")