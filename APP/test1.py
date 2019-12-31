from appium import webdriver

caps = {
  "platformName": "Android",
  "platformVersion": "4.4.4",
  "deviceName": "30293128",
  "appPackage": "com.tencent.mobileqq",
  "appActivity": ".activity.SplashActivity",
  "noReset": "true"
}
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub',caps)
driver.implicitly_wait(10)

el1 = driver.find_element_by_accessibility_id("请输入QQ号码或手机或邮箱")
el1.clear()
el1.send_keys("506135307")
el2 = driver.find_element_by_accessibility_id("密码 安全")
el2.clear()
el2.send_keys("RainQAQ999?")
el3 = driver.find_element_by_accessibility_id("登 录")
el3.click()
el4 = driver.find_element_by_id("com.tencent.mobileqq:id/conversation_head")
el4.click()
el5 = driver.find_element_by_xpath("//android.widget.LinearLayout[@content-desc=\"设置\"]/android.widget.RelativeLayout/android.widget.ImageView")
el5.click()
el6 = driver.find_element_by_id("com.tencent.mobileqq:id/account_switch")
el6.click()
el7 = driver.find_element_by_accessibility_id("退出当前帐号按钮")
el7.click()
el8 = driver.find_element_by_id("com.tencent.mobileqq:id/dialogRightBtn")
el8.click()
driver.quit()