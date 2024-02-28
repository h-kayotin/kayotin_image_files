"""
wjx_job - 提交问卷星

https://github.com/zzmvp-1/wjx-auto-fill

Author: hanayo
Date： 2024/2/28
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import selenium
from selenium.common.exceptions import NoSuchElementException

# 题目总数
question_num = 15

# 题目种类，1表示单选，2表示多选
ques_types = [1] * question_num
ques_types[2] = 0

# 题目选项, 也就是所有的都选A，第三题选AB
choices: list[int | list[int]] = [0] * question_num
choices[2] = [0, 1]

print(choices)


def write_wjx(url):
    driver = webdriver.Chrome()

    # 设置浏览器定位
    (longitude, latitude) = fun.random_position()
    # print(longitude, latitude)
    driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
        "latitude": latitude,
        "longitude": longitude,
        "accuracy": 100
    })
    # 将webdriver属性置为undefined
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                        {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    })

    # 打开问卷星网址
    driver.get(url)
    for i in range(0, question_num):
        # 题目的题目类型
        ques_type = ques_types[i]
        if ques_type == 1:  # 单选
            q_option = choices[i]
            q_select = driver.find_element(By.XPATH, f'//*[@id="div{i + 1}"]/div[2]/div[{q_option}]')
            q_select.click()
        elif ques_type == 0:  # 多选
            q_selects = choices[i]
            for j in q_selects:
                q_select = driver.find_element(By.XPATH, f'//*[@id="div{i+1}"]/div[2]/div[{j}]')
                q_select.click()
    submit_button = driver.find_element(By.XPATH, '//*[@id="ctlNext"]')
    submit_button.click()
    time.sleep(0.2)

    # 点按验证（新）
    confirm = driver.find_element(By.XPATH, '//*[@id="layui-layer1"]/div[3]/a')
    confirm.click()
    validation = driver.find_element(By.XPATH, '//*[@id="SM_BTN_WRAPPER_1"]')
    validation.click()
    time.sleep(2.5)

    res = driver.find_element(By.XPATH, '//*[@id="SM_TXT_1"]')

    # 滑块验证
    try:
        slider = driver.find_element(By.XPATH, '//*[@id="nc_1__scale_text"]/span')

        print('[' + eval(head) + f']: ', slider.text, cnt)
        if str(slider.text).startswith("请按住滑块"):
            width = slider.size.get('width')
            ActionChains(driver).drag_and_drop_by_offset(slider, width, 0).perform()

    except NoSuchElementException:
        pass

    time.sleep(1)
    print('[' + eval(head) + f']: ', res.text, cnt)
    driver.close()
