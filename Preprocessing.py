import pyautogui
import time
# import random
import webbrowser
import win32api, win32con
from threading import Thread, Lock
from pynput.keyboard import Key, Listener


def checkKeys(key):
    if key == Key.esc:
        print("You pressed esc")
        # for bot in allBots:
        # bot.stop()
        return False
    if key == Key.f2:
        pass


def waitKeys():
    def wait():
        nonlocal listener
        with Listener(
                on_press=checkKeys,
                on_release=lambda x: None) as mlistener:
            listener = mlistener
            mlistener.join()

    listener = None
    t1 = Thread(target=wait, daemon=True)
    t1.start()
    time.sleep(0.05)
    return listener


def click(pos: tuple):
    x, y = pos
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def getCenterPos(box):
    if box is None:
        return None
    if len(box) != 4:
        return None
    return box[0] + (box[2] // 2), box[1] + (box[3] // 2)


chromePath = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
edgePath = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chromePath))
webbrowser.register('edge', None, webbrowser.BackgroundBrowser(edgePath))

reloadLock = Lock()


def reloadPage(option=0):
    global reloadLock
    reloadLock.acquire()
    if option != 0:
        pyautogui.press('f5')
        time.sleep(0.5)
        pyautogui.moveTo(460, 253)
        while pyautogui.locateOnScreen(r'.\Images\tabselected.bmp', grayscale=False, confidence=0.95) is None:
            continue
        reloadLock.release()
        return
    while True:
        pos = pyautogui.locateOnScreen(r'.\Images\tabselected.bmp', region=(25, 0, 1775, 60), grayscale=False,
                                       confidence=0.9)
        if pos is not None:
            click(getCenterPos(pos))
            break
        else:
            pos = pyautogui.locateOnScreen(r'.\Images\tabnotselected.bmp', region=(25, 0, 1775, 60), grayscale=False,
                                           confidence=0.9)
            if pos is not None:
                click(getCenterPos(pos))
                break

    pyautogui.hotkey('ctrl', 'w')
    time.sleep(0.5)
    webbrowser.get('chrome').open_new_tab('https://papergames.io/en/gomoku')
    pyautogui.moveTo(460, 253)
    while pyautogui.locateOnScreen(r'.\Images\tabselected.bmp', grayscale=False, confidence=0.95) is None:
        continue
    reloadLock.release()


def preprocessTab(openbroswer=1, openTab=1, selectTab=1):
    if pyautogui.locateOnScreen(r'.\Images\broswerselected.bmp', grayscale=True, confidence=0.999) is None:
        broswerPos = pyautogui.locateOnScreen(r'.\Images\brosweropened.bmp', grayscale=True, confidence=0.999)
        if broswerPos is not None:
            click(getCenterPos(broswerPos))
            time.sleep(0.2)
        elif openbroswer:
            webbrowser.get('chrome').open_new_tab('https://papergames.io/en/gomoku')
            while not pyautogui.locateOnScreen(r'.\Images\tabselected.bmp', grayscale=False, confidence=0.95):
                continue
            time.sleep(0.5)
        else:
            print("Webbroswer is not opened")
            return 1
    tabPos = pyautogui.locateOnScreen(r'.\Images\tabselected.bmp', grayscale=True, confidence=0.85)
    if tabPos is None:
        tabPos = pyautogui.locateOnScreen(r'.\Images\tabnotselected.bmp', grayscale=True, confidence=0.99)
    # print(tabPos)
    if tabPos is None:
        if openTab:
            webbrowser.get('chrome').open_new_tab('https://papergames.io/en/gomoku')
            while not pyautogui.locateOnScreen(r'.\Images\tabselected.bmp', grayscale=False, confidence=0.95):
                continue
            time.sleep(0.5)
            return 0
        else:
            print("Tab is not opened")
            return 1

    if selectTab:
        click(getCenterPos(tabPos))
        time.sleep(0.2)
    else:
        print("Tab is not selected")
        return 1
    return 0


def preprocessGameMode(gameMode=0):
    if gameMode == 0:
        if (pos := pyautogui.locateOnScreen(r'.\Images\playbutton.bmp', grayscale=True, confidence=0.95)) is not None:
            click(getCenterPos(pos))
            pyautogui.moveTo(460, 253)
        else:
            print("Can't find the play button in gameMode 0")
            return 1
    else:
        if (pos := pyautogui.locateOnScreen(r'.\Images\playwfriend.bmp', grayscale=True, confidence=0.9)) is not None:
            click(getCenterPos(pos))
            time.sleep(0.5)
            while (
                    pos := pyautogui.locateOnScreen(r'.\Images\continuebutton.bmp', grayscale=True,
                                                    confidence=0.95)) is None:
                pass
            click(getCenterPos(pos))
            time.sleep(0.8)
            while pyautogui.pixel(1250, 285) != (255, 232, 199): pass
            click((1250, 285))
        else:
            print("Can't find the play button in gameMode 2")
            return 1
        pos = None
        if (pos := pyautogui.locateOnScreen(r'.\Images\edgeopen.bmp', grayscale=False, confidence=0.95)) is None:
            webbrowser.get('edge').open_new_tab('https://papergames.io/en/gomoku')
            time.sleep(0.8)
            while pyautogui.locateOnScreen(r'.\Images\edgetabopened.bmp', grayscale=False, confidence=0.9) is None:
                pass
        else:
            click(getCenterPos(pos))
        pos = None
        if (pos := pyautogui.locateOnScreen(r'.\Images\edgetabopened.bmp', grayscale=False, confidence=0.9)) is None:
            webbrowser.get('edge').open_new_tab('https://papergames.io/en/gomoku')
            time.sleep(0.8)
            while pyautogui.locateOnScreen(r'.\Images\edgetabopened.bmp', grayscale=False, confidence=0.9) is None:
                pass
        else:
            click(getCenterPos(pos))
        time.sleep(0.3)
        click((520, 60))
        time.sleep(0.5)
        pyautogui.keyDown('ctrl')
        pyautogui.press('v')
        pyautogui.keyUp('ctrl')
        pyautogui.press('enter')
        time.sleep(0.5)
        while (pos := pyautogui.locateOnScreen(r'.\Images\play.bmp', grayscale=True, confidence=0.9)) is None:
            pass
        click(getCenterPos(pos))
    time.sleep(1)
    return 0


def reselectTab():
    pos = pyautogui.locateOnScreen(r'.\Images\tabnotselected.bmp', region=(25, 0, 1775, 60), grayscale=False,
                                   confidence=0.9)
    if pos is None:
        pos = pyautogui.locateOnScreen(r'.\Images\tabselected.bmp', region=(25, 0, 1775, 60), grayscale=False,
                                       confidence=0.9)
    if pos is not None:
        click(getCenterPos(pos))
        return True
    return False


def checkInGame(gameMode):
    if gameMode == 2:
        time.sleep(2)
        return True
    global reloadLock
    #print('can i go')
    reloadLock.acquire()
    #print('yeah')
    if pyautogui.locateOnScreen(r'.\Images\tabselected.bmp', grayscale=False, confidence=0.95) is None:
        if not reselectTab():
            return False
    reloadLock.release()
    time.sleep(1.5)
    return True
