# -*- coding: utf-8 -*-
import time
import sys
from pynput.mouse import Controller, Button
from datetime import datetime
import pytz

def setShoppingTime():
    # TODO(parth): 后续时间应该由GUI录入
    print('本次外观开售时间，请使用如下格式"2019-05-21 18:02:49"')
    t = input()
    if t == '':
        print('你必须指定一个北京时间')
        sys.exit()
    print('''
预期将在北京时间 %s 模拟鼠标点击''' % t)
    timeArray = time.strptime(t, "%Y-%m-%d %H:%M:%S")
    return time.mktime(timeArray)

def setBuyButtonPosition(mouse):
    print('''
/-------------------------------------------/
/请将鼠标放置与购买按钮位置，3s后记录鼠标位置/
/-------------------------------------------/
''')
    time.sleep(3)
    x, y = mouse.position
    return x, y

def checkTimeZone():
    print('检查您系统的时间是否正确。')
    # 获取中国时区
    china_tz = pytz.timezone('Asia/Shanghai')

    # 获取当前系统时间
    local_time = datetime.now()
    local_ftime = local_time.strftime('%Y-%m-%d %H:%M:%S')

    # 获取当前北京时间
    beijing_time = datetime.now(china_tz)
    beijing_ftime = beijing_time.strftime('%Y-%m-%d %H:%M:%S')

    # 打印当前系统时间和北京时间
    print("当前系统时间：", local_ftime)
    print("标准北京时间：", beijing_ftime)
    # 比较两者是否相同
    if local_ftime == beijing_ftime:
        print("当前系统时间与北京时间相同，你可以正常使用该脚本。")
        return True
    else:
        print("当前系统时间与北京时间不同，请调整您的系统设置。")
        return False

def main():
    clickTimeStamp = setShoppingTime()
    # print('clickTime=%s' % (clickTimeStamp))

    mouse = Controller()
    x, y = setBuyButtonPosition(mouse)
    print('购买按钮位置记录完毕，x=%s, y=%s' % (x, y))

    # 休眠到开始点击前1s
    sleepTime = clickTimeStamp - time.time() - 1
    if sleepTime > 0:
        print('休眠%s秒至购买开放前夕' % int())
        time.sleep(sleepTime)

    # 开始循环查询时间等待点击
    print('开始等待购买开放')
    while time.time() < clickTimeStamp:
        pass

    # Just Buy It!
    mouse.position = (x, y)
    mouse.click(Button.left, 3)
    nowTimeStamp = time.time()
    localTime = time.localtime(nowTimeStamp)
    endTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
    print('%s 点击购买完毕' % endTime)

if __name__ == '__main__':
    if (not checkTimeZone()):
        input("按任意键关闭程序...")
    else:
        main()