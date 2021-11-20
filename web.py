from selenium import webdriver
import re
from utils import open_file

# Constants
URL = "https://www.recepty.cz/recept/jednoducha-rajska-omacka-155495"
PATH = "C:\Program Files (x86)\chromedriver.exe"

# Set up driver
driver = webdriver.Chrome(PATH)
driver.get(URL)

# Load resource list (json file)
RESOURCE_LIST = open_file('data/resource.json')


# Format split text with resource


def format(list):
    num = list[0]

    if not re.search(r'\d+', num):
        ing = num
        num = "10"

    elif len(list) == 3:
        ing = list[-1]

    elif len(list) >= 4:
        ing = list[2:]
        ing = ' '.join([str(elem) for elem in ing])

    if "," in num:
        num = num.replace(",", ".")
    num = float(num)

    if len(list) > 1:
        many = list[1]
        if many == "kg":
            num = num * 1000

        elif many == 'l':
            num = num * 1000

        elif many == "dl":
            num = num * 100

        elif "lž" in many:
            num = num * 15

        elif "šp" in many:
            num = num * 5

        elif "ks" in many:
            pass

    return float(num), ing

# Find correct text for resource


def get_resource(item):
    text = item.text
    try:
        child = item.find_element_by_xpath(".//em").text
        text = text.replace(child, "")
    except Exception as e:
        pass

    t = text.split()
    return t


# Click on button (allow cokkies)
button = driver.find_element_by_xpath(
    "/html/body/div[1]/div/div/div/div/div/div[3]/button[2]")
button.click()

# Find classes
title = driver.find_elements_by_class_name("recipe-title-box__title")[0].text
resource = driver.find_elements_by_class_name('ingredient-assignment__desc')
procedure = driver.find_elements_by_class_name("cooking-process__item-wrapper")

# Format procedure (list to string)
for paragraph in procedure:
    proces = paragraph.text

# Add resources to dictionary
res_dict = dict()
for i in resource:
    num, ing = format(get_resource(i))
    res_dict.update({ing: num})


img = driver.find_element_by_xpath(
    "/html/body/div[3]/div/div[2]/div[5]/div[2]/div[1]/div[1]/div[2]/a/img").get_attribute('src')


# Create final dictioary
RESOURCE = {"name": title,
            "resource": res_dict,
            "procedure": proces,
            "img": img,
            "url": URL}


# Display new resource
print(RESOURCE)

# Update and save resource list
RESOURCE_LIST.append(RESOURCE)
open_file('data/resource.json', "w", RESOURCE_LIST)

driver.close()
