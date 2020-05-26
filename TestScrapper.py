from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd
import time
from time import sleep

startTime = time.time()

#SAVE COMPANIES LIST AS DATAFRAME
data = pd.read_csv("Select.csv")['Security Code']
print("Indices Loaded")

download_dir = "D:/BSEDailyData/"

counter = 0
def downloadData():
    global counter
    
    # SET FIREFOX PREFERENCES
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", download_dir)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.ms-excel")
    
    ffOptions = Options()
    #ffOptions.headless = True
    
    driver = webdriver.Firefox(firefox_profile = profile, options=ffOptions,executable_path = 'D:/Softwares/geckodriver.exe')
    
    scripCode = data[0]
    urlpage = 'https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=6&scripcode='+str(scripCode)+'&flag=sp&Submit=G'
    driver.get(urlpage)
    driver.execute_script("document.getElementById('ContentPlaceHolder1_txtFromDate').value = '01/01/2010'")
    #print("From Set")
    driver.execute_script("document.getElementById('ContentPlaceHolder1_txtToDate').value = '14/02/2020'")
    driver.execute_script("document.getElementById('ContentPlaceHolder1_hidDMY').value = 'D'")
    driver.execute_script("document.getElementById('ContentPlaceHolder1_hidDMY').value = 'D'")
    #driver.execute_script("onbtnSubmit_Click()")
    driver.execute_script("__doPostBack('ctl00$ContentPlaceHolder1$btnDownload','')")
    sleep(0.5)
    print("Downloaded :",scripCode)
    
    input("Press Enter to Exit...")
    driver.quit()


downloadData()

endTime = time.time()
print("Total Execution Time :",endTime-startTime)
