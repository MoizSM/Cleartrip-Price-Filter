from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime

flyFrom = input("Where do you want to fly from? ")
flyTo = input("Where do you want to fly to ?")
dandt = input("When do you want to fly ? Please enter in format DD/MM/YYYY: ")

options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")

chrome = webdriver.Chrome( options=options , executable_path = r"webdrivers\chromedriver.exe")
print("The name of the browser is " + chrome.name)

chrome.get("https://www.cleartrip.ae/")

source = chrome.find_element_by_id("FromTag")
source.send_keys(flyFrom)
time.sleep(5)
source.send_keys(u'\ue007')

destination = chrome.find_element_by_id("ToTag")
destination.send_keys(flyTo)
time.sleep(5)
destination.send_keys(u'\ue007')

date = chrome.find_element_by_id("DepartDate")
date.send_keys(dandt)
time.sleep(3)
source.send_keys(u'\ue007')

# Only for one stop trips (continous trips)
time.sleep(10)
stop = chrome.find_element_by_xpath("//label[@for='1_1_0']")
ActionChains(chrome).move_to_element(stop).click().perform()

time = str(datetime.datetime.now())

f = open("price logs.txt" , "a")
f.write("\n" + time + " "+ flyFrom + " to " + flyTo + "\n************************")
f.close()

for x in range(1,4):

    counter = 2
     
    flightName = chrome.find_element_by_xpath("//*[@id='flightForm']/section[2]/div[4]/div/nav/ul/li[%d]/table/tbody/tr[1]/th[1]/small[1]" %x)
    fname = flightName.get_attribute('innerHTML').strip()
    

    f = open("price logs.txt" , "a")
    f.write("\n" + fname )
    f.close()
    
    while counter < 4:

        departTime = chrome.find_element_by_xpath("//*[@id='flightForm']/section[2]/div[4]/div/nav/ul/li[%d]/table/tbody/tr[1]/th[%d]" %(x , counter))
        dTime = departTime.get_attribute("innerHTML").strip()

        f = open("price logs.txt" , "a")
        if counter == 2:
            f.write("\nDeparture Time: " + dTime )
        else: 
            f.write("\nArrival Time: " + dTime)
        f.close()

        counter = counter + 1
    
    
    price = chrome.find_element_by_xpath("//*[@id='flightForm']/section[2]/div[4]/div/nav/ul/li[%d]//*[@id='withCabinBaggage']/span[1]" %x)
    
    p = price.get_attribute("innerText").strip()
    f = open("price logs.txt" , "a")
    f.write("\nPrice: " + p + "\n-------------------------------------")

print("Prices have been saved")