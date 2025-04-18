# -*- coding: utf-8 -*-
import time
import sys
from pynput.mouse import Controller, Button
from datetime import datetime
import pytz
import ntplib


def setShoppingTime():
    print('输入本次外观开售时间，请使用如下格式"2019-05-21 18:02:49"')
    t = input()
    if t == "":
        print("你必须指定一个北京时间")
        sys.exit()
    print(
        """
预期将在北京时间 %s 模拟鼠标点击"""
        % t
    )
    timeArray = time.strptime(t, "%Y-%m-%d %H:%M:%S")
    return time.mktime(timeArray)


def setBuyButtonPosition(mouse):
    print(
        """
/-------------------------------------------/
/请将鼠标放置与购买按钮位置，3s后记录鼠标位置/
/-------------------------------------------/
"""
    )
    time.sleep(3)
    x, y = mouse.position
    return x, y


def tryGetTimeBurden():
    print("检查您系统的时间是否正确……")
    # Get Beijing time
    china_tz = pytz.timezone("Asia/Shanghai")
    ntp_client = ntplib.NTPClient()
    for _ in range(5):  # 尝试5次
        try:
            # try get standard UTC time
            ntp_response = ntp_client.request("pool.ntp.org")
            utc_time = datetime.fromtimestamp(ntp_response.tx_time, tz=pytz.utc)
            beijing_time = utc_time.astimezone(china_tz)
            beijing_ftime = beijing_time.strftime("%Y-%m-%d %H:%M:%S")
            # Get Local system time
            local_time = datetime.now(china_tz)
            local_ftime = local_time.strftime("%Y-%m-%d %H:%M:%S")

            # logger current time
            print("当前系统时间：", local_ftime)
            print("标准北京时间：", beijing_ftime)
            # diff time
            if local_ftime == beijing_ftime:
                print("当前系统时间与北京时间相同，脚本将基于本地时间运行。")
                return 0
            else:
                print("当前系统时间与北京时间不同，脚本将基于标准北京时间运行。")
                return local_time.timestamp() - beijing_time.timestamp()
        except ntplib.NTPException as ex:
            print("校准时间失败，即将重试。" + str(ex))
            time.sleep(1)
    else:
        print(
            "无法获取标准北京时间，脚本将基于本地时间运行，请自行确定本地时间是否准确。"
        )
        return 0


def main():
    # Use the UTC time to verify the local time and update the burden value
    time_burden = tryGetTimeBurden()
    # get target click time
    clickTimeStamp = setShoppingTime() + time_burden

    # record target click position
    mouse = Controller()
    x, y = setBuyButtonPosition(mouse)
    print("购买按钮位置记录完毕，x=%s, y=%s" % (x, y))

    # update sleep duration
    print("准备休眠至开始购买前夕……")
    sleepTime = clickTimeStamp - time.time() - 1
    if sleepTime > 0:
        print("休眠%s秒至购买开放1s" % int(sleepTime))
        time.sleep(sleepTime)

    # ready to click
    print("开始等待购买开放")
    while time.time() < clickTimeStamp:
        pass

    # Just Buy It!
    mouse.position = (x, y)
    mouse.click(Button.left, 3)
    nowTimeStamp = time.time() - time_burden
    localTime = time.localtime(nowTimeStamp)
    endTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
    print("北京时间 %s 点击购买完毕" % endTime)

    # waiting
    input("按回车键退出...")


if __name__ == "__main__":
    main()
