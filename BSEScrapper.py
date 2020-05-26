from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd
import numpy as np
import time
from time import sleep
from datetime import date
from threading import Thread,Barrier
import os
from os import path

#SAVE COMPANIES LIST AS DATAFRAME
data = pd.read_csv("Select.csv")
data = data[data['Status'] == 'Active']['Security Code']
currDate = date.today().strftime("%d/%m/%y")
nThreads = 8
minSize = 0

'''
class myThread (threading.Thread):
    def __init__(self, threadID, compList):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.compList = compList
        
    def run(self):
        print("Starting",self.threadID)
        threadLock.acquire()
        self.downloadData(self.compList)
'''   
   
def downloadData(n,barrier,compList):
    # SET FIREFOX PREFERENCES
    #counter = 0
    download_dir = "D:\\BSEDailyData\\Data"
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", download_dir)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.ms-excel")
    
    ffOptions = Options()
    ffOptions.headless = True
    
    driver = webdriver.Firefox(firefox_profile = profile, options=ffOptions,executable_path = 'D:/Softwares/geckodriver.exe')
    
    ##While Loop
    for scripCode in compList:
        #if(counter >= 16):
        #    break
        fPath = f"Data/{scripCode}.csv"
        if(path.exists(fPath+".part")):
            os.remove(fPath+".part")
        urlpage = f"https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=6&scripcode={scripCode}&flag=sp&Submit=G"
        #print(urlpage)
        driver.get(urlpage)
        driver.execute_script("document.getElementById('ContentPlaceHolder1_txtFromDate').value = '01/01/2010'")
        #print("From Set")
        driver.execute_script("document.getElementById('ContentPlaceHolder1_txtToDate').value = '"+currDate+"'")
        driver.execute_script("document.getElementById('ContentPlaceHolder1_hidDMY').value = 'D'")
        #driver.execute_script("onbtnSubmit_Click()")
        driver.execute_script("__doPostBack('ctl00$ContentPlaceHolder1$btnDownload','')")
        t1 = time.time()
        t2 = t1
        while(t2 - t1 < 3):
            if(path.exists(fPath)):# and not path.exists(fPath+".part")):
                break
            t2 = time.time()
            
        print("Thread",n,"Downloaded :",scripCode)
        #counter += 1
    while(True):
        if((path.exists(fPath)) and (not path.exists(fPath+".part"))):
            break
    print("Thread",n,"Downloads Complete")
    for scripCode in compList:
        fPath = "Data/"+str(scripCode)+".csv"
        if(path.exists(fPath) and os.stat(fPath).st_size < minSize):
            os.remove(fPath)
    print("Thread Complete",n)
    barrier.wait()
    driver.quit()
        
data = np.array_split(data,nThreads)
threads = []
barrier = Barrier(nThreads)
print("Indices Loaded")

startTime = time.time()

for i in range(nThreads):
    t = Thread(target=downloadData, args=(i+1,barrier,data[i],)) 
    t.start()
    threads.append(t)
    
for thread in threads:
    thread.join()

endTime = time.time()
print("Total Execution Time :",endTime-startTime)
#input("Press Enter to Exit...")