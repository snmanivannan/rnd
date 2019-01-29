#! python3
# scrapMM.py - scrapping data from MM

import requests, sys, webbrowser, bs4
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Export the results to text file
def WriteLog(arr):
    with open('scrappedData.txt', 'a',encoding='utf-8') as file:
        for x in arr:
            for y in x:
                file.write(y + ";")
            file.write("\n")

#Open website with firefox #Headless for production
browser = webdriver.Firefox()
browser.get('http://www.sitename.com/regularsearch.php')
arr = []
try:    
    #Select the filtered options
    browser.find_element_by_xpath("//select[@id='from_age']/option[text()='23']").click()
    browser.find_element_by_xpath("//select[@id='to_age']/option[text()='28']").click()
    elements = browser.find_elements_by_name('R1')
    elements[1].click()
    elements[1].submit()

    # Wait for the search results to appear
    element = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.ID, "search_reg"))
        )

    #Get the total pages found
    totalMatch = browser.find_element_by_xpath("//p[@class='text-center']")
    iTotal = int(totalMatch.text[totalMatch.text.find('/')+1::])
    
    for i in range(iTotal):
        #Get the user details
        names = browser.find_elements_by_class_name('text-warning')
        details = browser.find_elements_by_xpath("//div[contains(@class,'col-xs-6')]")
        j = 0
        for a in names:
            name = a.text.split('/')
            row = name[0].strip(),name[1].strip(),details[j].text,details[j+1].text,details[j+2].text,details[j+3].text,details[j+4].text,details[j+5].text
            print(row)
            arr.append(row)
            j = j + 6

        #Go to next page
        i+=1
        browser.find_element_by_link_text(str(i+1)).click()
        
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "search_reg"))
        )
except TimeoutException:
    print("Page timed out")
finally:
    WriteLog(arr)
