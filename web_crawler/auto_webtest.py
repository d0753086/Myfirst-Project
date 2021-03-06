w# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 15:29:13 2020

@author: Joe
"""

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os,datetime,time
import json
import selenium.webdriver.support.ui as ui
from selenium.webdriver.chrome.options import Options
from array import *
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchFrameException
#==================================================================================
start_time = time.time()
#程式執行時間起點
#==================================================================================
try:
    file = open("filename.txt",mode='r',encoding="utf-8-sig")
except:
    print("檔案毀損或不存在")
Filename = file.readline().replace("\n"," ")
print("執行檔案為",Filename)
#==================================================================================
with open(Filename,'r',encoding="utf-8-sig", errors='ignore') as load_f:
    load = json.load(load_f, strict=False)
    #print(load)
    for step in load:
        if step.get('restart_time') != " ":
            restart_time = step.get('restart_time')
#==================================================================================
restart_num = int(restart_time)
print("重複執行次數為",restart_num)
print(type(restart_num))
#==================================================================================
#網頁動作執行
# 使用 Chrome 的 WebDriver,chrome建議升級到.84版本

chromeOpitons = Options()
    
prefs= {
    "profile.managed_default_content_settings.images":1,
    "profile.content_settings.plugin_whitelist.adobe-flash-player":1,
    "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player":1,

}
#Adobe Flash Player封鎖解除
#==================================================================================
chromeOpitons.add_experimental_option('prefs', prefs)
#開啟一個瀏覽器的driver


#==================================================================================

'''for i in range(0,len(load)):
    for y in range(0,len(load)-1):
        if load[y].get('Id') > load[y+1].get('Id'):
            tmp = load[y]
            load[y] = load[y+1]
            load[y+1] = tmp'''
#==================================================================================
while(restart_num >= 0):
    
    browser = webdriver.Chrome('./chromedriver', chrome_options=chromeOpitons)
    for step in load:
        
        if step.get('time_interval') == " ":
            num = 0
        elif step.get('time_interval') == None:
            num = 0
        else:
            num = int (step.get('time_interval'))
        print("與上一動作間隔",num,"秒")
        time.sleep(num)
        interval_start = time.time()
        
        if step.get('step') == "點擊":
            count = 0
            print("步驟為點擊")
            time.sleep(1)
            if step.get('xpath') != " ":
                 windows = browser.window_handles
                 #讓控制代碼抓到新跳出的視窗
                 browser.switch_to.window(windows[-1]) 
                 
                
                 try:           
                    #先試試能不能點，不能的話，走下面
                    elementclick = browser.find_element_by_xpath(step.get('xpath'))
                    elementclick.click()
                 except:
                     while(1):
                         try:
                             browser.switch_to_frame(count)
                             elementclick = browser.find_element_by_xpath(step.get('xpath'))
                             elementclick.click()                                                     
                             break                        
                         except NoSuchFrameException:
                             count = count+1
                             browser.switch_to.parent_frame()
                         except:
                             continue                                                       
                                                     
            else:
                #exception
                print("your xpath is null!\nPlease check your xpath in action.json")
               
        elif step.get('step') == "login":
            print("步驟為login")
            if step.get('account_xpath') != " ":
                if step.get('iframe') == " ":
                    inputElement_account = browser.find_element_by_xpath(step.get('account_xpath'))
                        
                    if step.get('passwd_xpath')!=" ":
                        inputElement_passwd = browser.find_element_by_xpath(step.get('passwd_xpath'))
                    else:
                         #exception
                        print("your passwd_xpath has some problems,please check your action.json")
                else:
                    browser.switch_to_frame(step.get('iframe'))
                    if step.get('account_xpath')!=" ":
                        inputElement_account = browser.find_element_by_xpath(step.get('account_xpath'))
                        
                    if step.get('passwd_xpath')!=" ":
                        inputElement_passwd = browser.find_element_by_xpath(step.get('passwd_xpath'))
                    else:
                         #exception
                        print("your passwd_xpath has some problems,please check your action.json")
               
                    browser.switch_to_default_content()
            else:
                print("your account_xpath is null,please check your xpath!")
                
            inputElement_account.send_keys(step.get('account'))
            inputElement_passwd.send_keys(step.get('passwd'))
                        
            go = browser.find_element_by_xpath(step.get('account_xpath'))
            go.submit()
        elif step.get('step') == "網頁搜尋":
            print("步驟為網頁搜尋")
            browser.get(step.get('search'))
        elif step.get('step') == "網頁起始位址":
            print("步驟為開啟網頁")
            browser.get(step.get('start'))
        elif step.get('step') == "Text_Input":
            print("步驟為文字輸入")
            if  step.get('iframe') == " ":
                inputElement = browser.find_element_by_xpath(step.get('xpath'))
                inputElement.click()
                inputElement.send_keys(step.get('search'))
                if(step.get('IsSend') == "true"):
                    inputElement.submit()
            else:
                browser.switch_to_frame(step.get('iframe'))
                inputElement = browser.find_element_by_xpath(step.get('xpath'))
                inputElement.click()
                inputElement.send_keys(step.get('search'))
                if(step.get('IsSend') == "true"):
                    inputElement.submit()
                browser.switch_to_default_content()
                
        interval_end = time.time()
        print("此步驟執行了",interval_end-interval_start,"秒\n")            
    restart_num = restart_num-1
    time.sleep(3)
    browser.close()

end_time = time.time()
print("專案執行完成，共花費",end_time-start_time,"秒")
#==================================================================================

