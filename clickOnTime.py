# -*- coding: utf-8 -*-
import time
import sys
from pymouse import PyMouse

def setShoppingTime():
    # TODO(parth):后续时间应该由GUI录入
    print('本次外观开售时间，请使用如下格式\"2019-05-21 18:02:49\"')
    t = input()
    if t == '' :
        print('你必须指定一个北京时间')
        sys.exit()
    print('''
预期将在北京时间 %s 模拟鼠标点击''' % (t))
    timeArray = time.strptime(t, "%Y-%m-%d %H:%M:%S")
    return time.mktime(timeArray)

def setBuyButtonPosition(mouse):
    print('''/-------------------------------------------/
/请将鼠标放置与购买按钮位置，3s后记录鼠标位置/
/-------------------------------------------/''')
    time.sleep(2)
    x,y = mouse.position()
    return x,y

def main():
    print('这只是一个简单的定时点击鼠标的脚本，仅考虑该脚本在Win32下的表现。')

    clickTimeStamp = setShoppingTime()
    # print('clickTime=%s' % (clickTimeStamp))

    mouse = PyMouse()
    x,y = setBuyButtonPosition(mouse)
    print('购买按钮位置记录完毕，x=%s, y=%s' % (x,y))

    # 休眠到开始点击前1s
    sleepTime = clickTimeStamp - time.time() - 1
    if (sleepTime > 0):
        print('休眠%sms至购买开放前夕' % ((int)(sleepTime)))
        time.sleep(sleepTime)

    # 开始循环查询时间等待点击
    print('开始等待购买开放')
    while(time.time() < clickTimeStamp):
        pass
    # Just Buy It!
    mouse.click(x,y,1,1)
    nowTimeStamp = time.time()
    localTime = time.localtime(nowTimeStamp)
    endTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
    print('%s 点击购买完毕' % (endTime))

if __name__ == '__main__':
    main()