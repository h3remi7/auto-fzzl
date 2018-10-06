import logging
import smtplib
import time
import win32api
import win32gui
import win32ui
from ctypes import windll
import win32con
from PIL import ImageGrab
from pytesseract import *

import aircv
import os
import random


hWin = win32gui.FindWindow(None, '雷电模拟器')
ch = win32gui.FindWindowEx(hWin, 0, None, 'TheRender')
b = win32ui.CreateWindowFromHandle(ch)
x=0
y=38
rect = win32gui.GetWindowRect(hWin)
w = rect[2] - rect[0] - 38
h = rect[3] - rect[1] - 38
hwndDC = win32gui.GetWindowDC(hWin)  # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
mfcDC = win32ui.CreateDCFromHandle(hwndDC)  # 根据窗口的DC获取mfcDC
saveDC = mfcDC.CreateCompatibleDC()  # mfcDC创建可兼容的DC
saveBitMap = win32ui.CreateBitmap()  # 创建bigmap准备保存图片

saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)  # 为bitmap开辟空间


state_map = [
    ['battle_complete', 'touch.png'],
    ['get_new_pm', 'state_newpm.png'],
    ['get_pm', 'state_getpm.png'],
    ['battle_pre', 'do_attack.png'],
    ['sel_support', 'sel_support.png'],
    ['sel_team', 'sel_team.png'],
    ['do_attack_pre', 'team_attack.png'],
    ['battle_map', 'auto_walk.png'],
    ['sel_ch', '3-4.png'],
    ['sel_eve', 'event_3-10.png'],
    ['go_event', 'go_event.png'],
    ['add_friend', 'friend_no.png'],

    ['in_battle_start_auto', 'in_battle_start_auto.png'],
    ['jjc_start', 'jjc_start.png'],
    ['jjc_sel', 'jjc_sel.png'],


]
newpm_no = aircv.imread('new_pm_no.png')


for k,s in enumerate(state_map):
    state_map[k][1] = aircv.imread(s[1])

def main():
    while(True):
        state, pos = check_state()
        if state:
            if state == 'sel_ch':
                tap(b, pos['result'])
                print('进入挂机关卡！')
            if state == 'sel_eve':
                tap(b, pos['result'])
                print('进入event挂机关卡！')
            if state == 'go_event':
                tap(b, pos['result'])
                print('进入副本！')
            if state == 'battle_complete':
                #战斗结束随便点一下！
                tap(b, pos['result'])
                print('战斗结束随便点一下！')
            if state == 'get_new_pm':
                #获得新pm
                aim_pos = get_img_pos(newpm_no)
                tap(b, aim_pos['result'])
                print('获得新pm不锁定！')
            if state == 'get_pm':
                #获得新pm随便点一下！
                tap(b, (500,500))
                print('获得pm随便点一下！')
            if state == 'battle_pre':
                #点击进入战斗！
                tap(b, pos['result'])
                print('点击进入战斗！')
            if state == 'sel_support':
                #选择助战队友！
                tap(b, pos['result'])
                print('选择助战队友！')
            if state == 'sel_team':
                #点击选择队伍！
                tap(b, pos['result'])
                print('点击选择队伍！')
            if state == 'do_attack_pre':
                #队伍出鸡！
                tap(b, pos['result'])
                print('队伍出鸡！')
            if state == 'battle_map':
                #自动搜怪 on！
                tap(b, pos['result'])
                print('自动搜怪 on！')
            if state == 'add_friend':
                tap(b, pos['result'])
                print('不加好友,滚！！')
            if state == 'in_battle_start_auto':
                tap(b, pos['result'])
                print('开启自动战斗')
            if state == 'jjc_start':
                tap(b, pos['result'])
                print('开始jjc战斗')
            if state == 'jjc_sel':
                tap(b, pos['result'])
                print('选择jjc目标')
        
        time.sleep(2)



def tap(handle, xy, t=2.0):
    x, y = xy
    x = int(x) + random.randint(-10, 10)
    y = int(y) + random.randint(-10, 10)
    print(f'tap: ({x}, {y})')
    pos = win32api.MAKELONG(x, y)
    handle.PostMessage(win32con.WM_LBUTTONDOWN, 0x1, pos)
    time.sleep(.5)
    handle.PostMessage(win32con.WM_LBUTTONUP, 0x0, pos)


def get_pic():
    print(1)
    #tap(b, pos['result'])


def check_state():
    saveDC.SelectObject(saveBitMap)  # 高度saveDC，将截图保存到saveBitmap中
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (x, y),
                win32con.SRCCOPY)  # 截取从左上角（0，0）长宽为（w，h）的图片
    saveBitMap.SaveBitmapFile(saveDC, 'frame.jpg')
    src = aircv.imread('frame.jpg')
    for state in state_map:
        pos = aircv.find_template(src, state[1])
        #print(state[0], pos)
        if pos and pos['confidence'] > 0.8:
            return (state[0], pos)
    return (None, None)

def get_img_pos(img):
    src = aircv.imread('frame.jpg')
    pos = aircv.find_template(src, img)
    #print('check pos', pos)
    if pos and pos['confidence'] > 0.8:
        return pos
    return None

    


if '__main__' == __name__:
    main()
