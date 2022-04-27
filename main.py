from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

chrome_driver_path = "C:/Selenium/chromedriver.exe"
URL = "https://orteil.dashnet.org/cookieclicker/"
driver = webdriver.Chrome(service=Service(chrome_driver_path))

driver.get(URL)

cookie = driver.find_element(By.ID, "bigCookie")
reserve_tags = driver.find_element(By.ID, "cookies")


def scrap_price_list():
    """
    The products available to user changes depending on the amount of cookies owned. This function first
    tries to write down all the prices. At the start of the game, it won't succeed because it tries to write
    down 6 prices where there are only two available. It will then try and write down 5 prices. If failed, try 4 prices.
    Then 3 and so on.
    """
    product_number = 5
    while True:
        try:
            price_list = [int(driver.find_element(By.ID, f"productPrice{i}").text.replace(",", "")) for i in range(product_number+1)]

        except ValueError:
            product_number -= 1

        else:
            return price_list


def get_product_list():
    """
       The products available to user changes depending on the amount of cookies owned. This function first
       tries to grab all the products. At the start of the game, it won't succeed because it tries to grab
       down all 6 prodcuts where there are only two available. It will then try and get 5 products. If failed, try 4 products.
       Then 3 and so on.
       """
    product_number = 5
    while True:
        try:
            product_list = [driver.find_element(By.ID, f"product{i}") for i in range(product_number+1)]
        except ValueError:
            product_number -= 1
        else:
            return product_list


def get_reserve(var):
    """
    this function grabs your cookie reserve and turns it into a interger

    """
    try:
        cookies = int(var.text.split(" ")[0])
    except ValueError:
        cookies = int(var.text.split(" ")[0].replace(",", ""))
        return cookies
    else:
        return cookies


time_the_program_starts = time.time() # the time you click "run main.py"
time_to_end_the_programme = time_the_program_starts + 60 # 60 seconds after you clicked "run main.py"


def cookie_manager():

    is_on = True
    timeout = time.time() + 15
    print("new loop")
    while is_on:
        cookie.click()
        if time.time() > timeout:

            is_on = False
            print("it's been 5 seconds")
            reserve = get_reserve(reserve_tags)
            price_list = scrap_price_list()
            product_list = get_product_list()

            for price in price_list[::-1]: # start from the most expensive item
                if reserve > price:  # keep buying the item while reserve of cookies is higher than the most expensive
                    print(price)
                    index = price_list.index(price)  # find the index of the price_list
                    times_able_buy = reserve // price
                    for _ in range(times_able_buy):
                        product_list[index].click()  # click the button responding to that index

            if time.time() < time_to_end_the_programme: #keep running the loop until it's been 60 secs since you clicked "run main.py"
                cookie_manager() # restart the loop
            else:
                break # stop the loop and end the bot


cookie_manager()


# 1650990586.3867166
# driver.quit()
