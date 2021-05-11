#!/usr/bin/env python

import os
from time import sleep

from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests
import random
from appium.webdriver.common.touch_action import TouchAction
import sys, getopt
import uuid


################## argv #########################


################## argv #########################

argv = sys.argv[1:]
deviceName = ""
province = ""
local_province = ""
androidVersion = ""
info = ""
ifd_print = False
isTEST = True

try:
    opts, args = getopt.getopt(argv, "hdti:a:")

    for opt, arg in opts:
        if opt == '-h':
            print('Ex.ppw.py -i emulator-5554 -a 10')
            print("\t-d open debug\n\t-i device udid\n\t-a Android version (Default 10.0)\n\t")
            sys.exit()

        elif opt in ("-i", "--i"):
            deviceName = arg
        elif opt in ("-a", "--a"):
            androidVersion = arg
        elif opt in ("-d", "--d"):
            ifd_print = True
        elif opt in ("-t", "--t"):
            isTEST = False

    if isTEST == True:
        deviceName = "emulator-5554"
        androidVersion = '7.0'
        ifd_print = True
    else:

        if (androidVersion is None) or (str(androidVersion).strip() == ""):
            androidVersion = '7.0'

except getopt.GetoptError:
    print('Ex.ppw.py -i emulator-5554 -a 10')
    print("\t-d open debug\n\t-i device udid\n\t-a Android version (Default 10.0)\n\t")
    sys.exit()


################## End argv #########################

def clickButton(op, byOp):

    i = 0
    while True:

        try:

            if op == By.ID :
                button = driver.find_element_by_id(byOp)
            else:
                button = driver.find_element_by_xpath(byOp)

            button.click()

            break
        except NoSuchElementException:
            d_print("%s Error clickButton %s" % (i, byOp))
            sleep(1)
            i = i+1
            if i > 100:
                return 1
    return 0

def getText(op, byOp):

    i = 0
    while True:
        try:
            d_print("%s try getText %s" % (i, byOp))
            if op == By.ID:
                val = driver.find_element_by_id(byOp)
            else:
                val = driver.find_element_by_xpath(byOp)

            break
        except NoSuchElementException:
            d_print("%s Error getText %s" % (i, byOp))
            #sleep(1)
            i = i + 1
            if i > 100:
                return 1
    return val.text

def getTextOneTime(op, byOp):

    try:
        if op == By.ID:
            val = driver.find_element_by_id(byOp)
        else:
            val = driver.find_element_by_xpath(byOp)

    except NoSuchElementException:
        return '-'
    return val.text

def d_print(message):
    if ifd_print == True:
        print("debug : %s" % message)

sleep(2)
message = ('Test nPerf from ANDROID EMU.(%s)' % deviceName)
path_file = '/home/phongphawits/Phongohawit@True/my_app/log-test/screenshot.png'

ran_uuid = ""'%s'"" % uuid.uuid4() #Random UUID

#print(ran_uuid)
desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = androidVersion
desired_caps['deviceName'] = deviceName
desired_caps['udid'] = deviceName
desired_caps['autoGrantPermissions'] = 'true'
desired_caps['appPackage'] = 'com.android.chrome'
desired_caps['appActivity'] = 'com.google.android.apps.chrome.Main'
desired_caps['newCommandTimeout'] = 1000
desired_caps['appWaitDuration'] = 10 # Timeout in milliseconds used to wait for the appWaitActivity to launch (default 20000)
#desired_caps['uuid'] = 'ac003cc1-4321-5555-a71d-cc25280521ab'
desired_caps['uuid'] = ran_uuid
desired_caps['autoGrantPermissions'] = 'true'
desired_caps['autoAcceptAlerts'] = 'true'

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
wait = WebDriverWait(driver, 30)
Device = 'PRIMO'

ifERROR = False

isp = ''

try:

    retVal = clickButton(By.ID, 'com.android.chrome:id/terms_accept')
    if retVal == 1 :
        d_print("Error App close")
        ifERROR = True
        exit()
    sleep(1)
    # next_button
    clickButton(By.ID, 'com.android.chrome:id/next_button')
    sleep(1)
    # negative_button
    clickButton(By.ID, 'com.android.chrome:id/negative_button')
    sleep(1)
    #driver.get("http://speedtest.adslthailand.com")
    #sleep(5)
    # Select search_box_text
    goto = "speedtest-html5.trueinternet.co.th/"
    clickButton(By.ID, 'com.android.chrome:id/search_box_text')
    sleep(1)
    val = driver.find_element_by_id('com.android.chrome:id/url_bar')
    val.send_keys(goto)
    #https://developer.android.com/reference/android/view/KeyEvent
    driver.press_keycode(66);
    sleep(5)
    # Start Test
    clickButton(By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.webkit.WebView/android.view.View[2]/android.view.View[1]')

    d_print("waiting 30 s.")
    for x in range(1, 30):
        d_print("%s" % x)
        sleep(1)

    ####################### Get Result ###############################
    # ip
    ip = getText(By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.webkit.WebView/android.view.View[2]/android.view.View[2]/android.view.View[3]/android.view.View[2]')

    ####################### END Result ###############################

except NoSuchElementException:
    d_print("Error: %s" % NoSuchElementException)
    ifERROR = True

finally:

    if ifERROR == True :
        d_print("CLOSE THE SESSION WHIT ERROR.")
    else:
        d_print("CLOSE THE SESSION.")

        path_file = 'speedtest-html5-screenshot.png'

        driver.save_screenshot(path_file)

        print("IP ADDRESS: %s" % ip)


    ####################### Close APP ###############################
    d_print("Waiting close app.")
    sleep(2)
    driver.terminate_app('com.android.chrome')
    sleep(1)
    #driver.close_app()
    #sleep(1)
    # end the session
    driver.quit()
    ####################### End  Close APP ###############################


