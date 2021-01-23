import ctypes
import functools
import concurrent.futures
from ctypes import windll

import numpy as np
import win32ui
import win32gui
import win32con

from rimo_utils import cv0


def 可疑(hWnd):
    title = win32gui.GetWindowText(hWnd)
    if not win32gui.IsWindowVisible(hWnd):
        return
    if title == 'Program Manager':
        return
    if not title:
        return
    left, top, right, bottom = win32gui.GetWindowRect(hWnd)
    if (right-left)*(bottom-top) <= 400:
        return
    if max([left, top, right, bottom]) <= 0:
        return
    return True


def 可疑窗口组():
    hWndList = []
    win32gui.EnumWindows(lambda hWnd, _: hWndList.append(hWnd), None)
    hWndList = list(filter(可疑, hWndList))
    return hWndList


def 顶层窗口():
    return win32gui.GetForegroundWindow()


@functools.lru_cache(maxsize=64)
def 我不知道什么DC反正一看就是邪法(hWnd, width, height):
    hWndDC = win32gui.GetWindowDC(hWnd)
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
    safeHdc = saveDC.GetSafeHdc()
    return hWndDC, mfcDC, saveDC, saveBitMap, safeHdc


def 窗口截图(hWnd):
    left, top, right, bot = win32gui.GetClientRect(hWnd)
    width = right - left
    height = bot - top
    if width == 0 or height == 0:
        return None
    hWndDC, mfcDC, saveDC, saveBitMap, safeHdc = 我不知道什么DC反正一看就是邪法(hWnd, width, height)
    result = windll.user32.PrintWindow(hWnd, safeHdc, 3)
    signedIntsArray = saveBitMap.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype='uint8')
    img.shape = (height, width, 4)
    cv0.cvtColor(img, cv0.COLOR_RGBA2BGR)
    return img[:, :, :3].copy()


def 全部扫描(h_list):
    def f(hWnd):
        if hWnd == 0:
            return None
        try:
            title = win32gui.GetWindowText(hWnd)
            位置 = win32gui.GetWindowRect(hWnd)
        except Exception as e:
            print('句柄坏了。')
            return None
        return title, 窗口截图(hWnd), 位置
    if len(h_list) > 1:
        q = concurrent.futures.ThreadPoolExecutor(max_workers=8)
        return list(filter(lambda x: x, q.map(f, h_list)))
    else:
        return list(filter(lambda x: x, map(f, h_list)))
