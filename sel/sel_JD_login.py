"""
sel_JD_login - 模拟京东登录

Author: hanayo
Date： 2024/1/18
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import ddddocr
import base64
from selenium.webdriver import ActionChains
import random
from PIL import Image
import requests


def sel_main():
    browser = webdriver.Chrome()
    # browser.maximize_window()
    browser.get('https://passport.jd.com/uc/login')

    # 点击账户密码登录
    up_btn = browser.find_element(By.ID, 'pwd-login')
    up_btn.click()

    # 通过元素ID获取用户名和密码框
    username_input = browser.find_element(By.ID, 'loginname')
    pw_input = browser.find_element(By.ID, 'nloginpwd')
    # 模拟输入
    username_input.send_keys('18xxxxxxx93')
    pw_input.send_keys('1234567')
    # 选取登录按钮
    submit_btn = browser.find_element(By.ID, 'loginsubmit')
    # su_button = browser.find_element(By.CSS_SELECTOR, '#su')
    # 模拟用户点击行为
    submit_btn.click()

    time.sleep(2)
    is_login = False
    while not is_login:
        try:
            # 获取验证码图片背景大图
            captcha = browser.find_element(By.XPATH, '//div[@class="JDJRV-bigimg"]/img')
            captcha_img = captcha.get_attribute('src')
            captcha_size = (captcha.size['width'], captcha.size['height'])
            handle_img(captcha_img, 'bg', captcha_size, 'bg_sized')
            # 获取滑块小图
            wrap = browser.find_element(By.XPATH, '//div[@class="JDJRV-smallimg"]/img')
            wrap_img = wrap.get_attribute('src')
            wrap_size = (wrap.size['width'], wrap.size['height'])
            handle_img(wrap_img, 'sm', wrap_size, 'sm_sized')

            # 计算滑动距离
            distance = get_distance("sm_sized", "bg_sized")
            print(distance)
            # 进行滑动
            # do_moves(browser, distance, wrap)
            move_mouse(browser, distance, wrap)
            time.sleep(0.5)
        except NoSuchElementException as msg:
            print("无法获取该元素:", msg)
            is_login = True

    cookies = browser.get_cookies()
    with open("cookies.json", "w") as c:
        c.write(f"{cookies}")

    input("请输入回车结束")


def handle_img(img_src: str, name: str, size: tuple, name_sized: str):
    """
    对下载的验证码图片进行处理
    :param img_src: 原图片编码
    :param name: 保存名称
    :param size: 调整的大小，元组(width, height)
    :param name_sized: 调整后的图片名
    :return: 无
    """
    s_img = img_src.replace('data:image/png;base64,', '')
    img_byte = base64.b64decode(s_img)
    with open(f"images/{name}.png", "wb") as f:
        f.write(img_byte)
    img = Image.open(f"images/{name}.png")
    res_img = img.resize(size)
    res_img.save(f"images/{name_sized}.png")


def get_distance(tg_img, bg_img):
    """
    获取滑动距离
    :param bg_img: 底层大图片
    :param tg_img: 滑块小图片
    :return: 返回距离
    """
    # 读取图片
    with open(f"images/{tg_img}.png", "rb") as f:
        tg = f.read()
    with open(f"images/{bg_img}.png", "rb") as f:
        bg = f.read()

    det = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
    # 目标图无多余背景，需要加入simple_target参数
    res = det.slide_match(tg, bg, simple_target=True)
    return res['target'][0]


def do_moves(browser, distance, btn):
    """
    加速度滑动法，计算生成轨迹然后滑动
    :param browser: 浏览器对象
    :param distance: 滑动距离
    :param btn: 滑动对象
    :return:无
    """
    # 生成运动轨迹
    track = []
    current = 0
    mid = distance * 4 / 5
    t = 0.2
    v = 1
    while current < distance:
        if current < mid:
            a = 4
        else:
            a = -3
        v0 = v
        v = v0 + a*t
        move = v0*t + 0.5*a*t*t
        current += move
        track.append(round(move))
    ActionChains(browser).click_and_hold(btn).perform()
    for x in track:
        ActionChains(browser).move_by_offset(xoffset=x, yoffset=random.randint(-5, 5)).perform()
        # 重置滑动值，否则多次滑动会超出范围
        ActionChains(browser).reset_actions()
    time.sleep(0.5)

    ActionChains(browser).release(on_element=btn).perform()


def use_cookies():
    # 我的订单页面，需要登录才能访问
    test_url = "https://order.jd.com/center/list.action"

    # 从本地读取cookie文件，
    with open("cookies.json", 'r') as c:
        cookies = eval(c.read())

    cookie = [item["name"] + "=" + item["value"] for item in cookies]
    # 拼接成字符串
    cookie_str = '; '.join(item for item in cookie)
    print(cookie_str)

    # 将cookie放入header中
    header = {
        'cookie': cookie_str,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    html = requests.get(test_url, headers=header)
    print(html.text)


def move_mouse(browser, distance, element):
    """
    轨迹模拟方法（三段随机速度）成功几率高
    :param browser: 浏览器driver对象
    :param distance: 移动距离
    :param element: 移动的元素
    :return: 无返回值
    """
    has_gone_dist = 0
    remaining_dist = distance
    ActionChains(browser).click_and_hold(element).perform()
    time.sleep(0.5)
    while remaining_dist > 0:
        ratio = remaining_dist / distance
        if ratio < 0.1:
            span = random.randint(3, 5)
        elif ratio > 0.9:
            span = random.randint(5, 8)
        else:
            span = random.randint(15, 20)
        ActionChains(browser).move_by_offset(span, random.randint(-5, 5)).perform()
        remaining_dist -= span
        has_gone_dist += span
        time.sleep(random.randint(5, 20) / 100)
    ActionChains(browser).move_by_offset(remaining_dist, random.randint(-5, 5)).perform()
    ActionChains(browser).release(on_element=element).perform()


if __name__ == '__main__':
    sel_main()
    # use_cookies()
