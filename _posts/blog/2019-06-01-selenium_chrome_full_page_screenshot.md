---
layout: post
title: selenium + chrome 全页面截图
category: 技术
tags: 
    - selenium
    - chrome
keywords: 
description: 
---

# selenium + chrome 全页面截图

完整代码：

```
__author__ = 'rk.feng'

import base64
import json

from selenium import webdriver


def chrome_take_full_screenshot(driver: webdriver.Chrome):
    """
        copy from https://stackoverflow.com/questions/45199076/take-full-page-screenshot-in-chrome-with-selenium
        author: Florent B.

    :param driver:
    :return:
    """
    def send(cmd, params):
        resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
        url = driver.command_executor._url + resource
        body = json.dumps({'cmd': cmd, 'params': params})
        response = driver.command_executor._request('POST', url, body)
        return response.get('value')

    def evaluate(script):
        response = send('Runtime.evaluate', {'returnByValue': True, 'expression': script})
        return response['result']['value']

    metrics = evaluate(
        "({" + \
        "width: Math.max(window.innerWidth, document.body.scrollWidth, document.documentElement.scrollWidth)|0," + \
        "height: Math.max(innerHeight, document.body.scrollHeight, document.documentElement.scrollHeight)|0," + \
        "deviceScaleFactor: window.devicePixelRatio || 1," + \
        "mobile: typeof window.orientation !== 'undefined'" + \
        "})")
    send('Emulation.setDeviceMetricsOverride', metrics)
    screenshot = send('Page.captureScreenshot', {'format': 'png', 'fromSurface': True})
    send('Emulation.clearDeviceMetricsOverride', {})

    return base64.b64decode(screenshot['data'])


def get_driver(headless: bool = False) -> webdriver.Chrome:
    capabilities = {
        'browserName': 'chrome',
        'chromeOptions': {
            'useAutomationExtension': False,
            'args': ['--disable-infobars']
        }
    }

    chrome_options = webdriver.ChromeOptions()
    if headless:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(
        executable_path="/Users/pzzh/Work/bin/chromedriver",
        chrome_options=chrome_options,
        desired_capabilities=capabilities
    )

    return driver


def full_page_screenshot(driver: webdriver.Chrome, url: str, png_file: str = "screenshot.png"):
    driver.get(url)

    png = chrome_take_full_screenshot(driver)

    with open(png_file, 'wb') as f:
        f.write(png)


if __name__ == '__main__':
    _driver = get_driver(headless=False)
    try:
        # 商务部
        target_url = "http://www.mofcom.gov.cn/article/b/c/?"

        full_page_screenshot(driver=_driver, url=target_url, png_file="mofcom_full.png")

        # 非整页
        _driver.get(url=target_url)
        _driver.save_screenshot("mofcom.png")

    finally:
        if _driver:
            _driver.close()
            _driver.quit()

```

结果：

普通截图

![普通截图结果](../../../public/img/selenium_chrome/mofcom.png)

全页面截图

![全页面截图结果](../../../public/img/selenium_chrome/mofcom_full.png)

