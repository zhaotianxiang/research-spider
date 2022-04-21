import datetime
import time
import pdfkit
import pymongo
import urllib
import pdfcrowd

from selenium import webdriver
import json
import time

def google_download(url, filename):
    options = webdriver.ChromeOptions()
    # options.add_argument("start-maximized")
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option("useAutomationExtension", False)

    settings = {
        "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local",
            "account": ""
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2,
        "isHeaderFooterEnabled": False,

        # "customMargins": {},
        # "marginsType": 2,
        # "scaling": 100,
        # "scalingType": 3,
        # "scalingTypePdf": 3,
        "isLandscapeEnabled": True,  # landscape横向，portrait 纵向，若不设置该参数，默认纵向
        "isCssBackgroundEnabled": True,
        "mediaSize": {
            "height_microns": 297000,
            "name": "ISO_A4",
            "width_microns": 210000,
            "custom_display_name": "A4 210 x 297 mm"
        },
    }

    options.add_argument('--enable-print-browser')
    # options.add_argument('--headless') #headless模式下，浏览器窗口不可见，可提高效率

    prefs = {
        'printing.print_preview_sticky_settings.appState': json.dumps(settings),
        'savefile.default_directory': 'C:\\draft'  # 此处填写你希望文件保存的路径
    }
    options.add_argument('--kiosk-printing')  # 静默打印，无需用户点击打印页面的确定按钮
    options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.maximize_window()

    # 定义一个初始值
    temp_height = 0
    # driver.find_element(By.XPATH, "//button[@aria-label='收起谷歌翻译导航栏']").click()

    while True:
        # 循环将滚动条下拉
        driver.execute_script("window.scrollBy(0,1000)")
        # sleep一下让滚动条反应一下
        time.sleep(1)
        # 获取当前滚动条距离顶部的距离
        # check_he
