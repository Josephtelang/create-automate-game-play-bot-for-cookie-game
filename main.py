from selenium import webdriver
from selenium.webdriver.common.by import By
import time

option_chrome = webdriver.ChromeOptions()
option_chrome.add_experimental_option("detach",True)

driver = webdriver.Chrome(options=option_chrome)
driver.get("https://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element(By.ID,value="cookie")

items = driver.find_elements(By.CSS_SELECTOR,"#store div")
item_ids = [item.get_attribute("id") for item in items]

timeout = time.time() + 5
five_min = time.time() + 1*60 # adds 5 minutes

while True:
    cookie.click()

    if time.time() > timeout :

        all_prices = driver.find_elements(By.CSS_SELECTOR,value="#store b")
        items_prices = []

        for price in all_prices:
            element_text = price.text
            if element_text != "":
                costs = int(element_text.split("-")[1].strip().replace(",",""))
                items_prices.append(costs)

        # Create an dictionary to store items and prices
        cookie_upgrades = {}
        for n in range(len(items_prices)):
            cookie_upgrades [items_prices[n] ] = item_ids[n]
        

        money_element = driver.find_element(By.ID,value="money").text
        if "," in money_element:
            money_element = money_element.replace(",","")
        cookie_count = int(money_element)

        affordable_upgraders = {}
        for cost,id in cookie_upgrades.items():
            if cookie_count > cost:
                affordable_upgraders[cost] = id

        highest_price_of_affordable_upgrades = max(affordable_upgraders)
        highest_price_of_affordable_upgrades_id = affordable_upgraders[highest_price_of_affordable_upgrades]

        driver.find_element(By.ID,value=highest_price_of_affordable_upgrades_id).click()

        # add more 5 seconds until the next check
        timeout = time.time() + 5

    # After 5 min stops the bot and check cookies per seconds counts
    if time.time() > five_min:
        cookie_per_sec = driver.find_element(By.ID,value="cps").text
        print(cookie_per_sec)
        break

driver.quit()




