import math
import pyautogui
import time
from Preprocessing import getCenterPos, click, reloadPage
from threading import Thread
from Interface import *


# me = 1
# foe = 2
# mynode color (green): [24, 188, 156] - foenode color (black): [44, 62, 80]
# grid color: [206, 212, 218]
class gomokuBot:
    #board = []
    namePos = None
    stopped = None
    node = 0
    gameMode = 0
    currentTab = 'edge'
    firstPer = 0.83

    def __init__(self, gameMode=0):
        self.resetGame()
        self.gameMode = gameMode
        self.currentTab = 'edge'
        self.newGame = 1
        if self.gameMode == 2:
            self.firstPer = 0.77
        self.nodePos = None
        self.color = None
        self.stuckCount = 0

    def switchTabAndWait(self, toEdge):
        if toEdge:
            while (pos := pyautogui.locateOnScreen(r'.\Images\edgeopen.bmp', grayscale=False, confidence=0.85)) is None:
                pass
            click(getCenterPos(pos))
            pyautogui.moveTo(1450, 725)
            self.currentTab = 'edge'
        time.sleep(0.5)
        while pyautogui.locateOnScreen(r'.\Images\myturn.bmp', grayscale=False, confidence=0.85) is None:
            if pyautogui.locateOnScreen(r'.\Images\playbutton.bmp', region=(1035, 255, 155, 55), grayscale=True,
                                        confidence=0.95) is not None:
                return 2
            if pyautogui.locateOnScreen(r'.\Images\leaveroom.bmp', region=(700, 410, 600, 490), grayscale=True,
                                        confidence=0.95) is not None:
                return 2
            if pyautogui.locateOnScreen(r'.\Images\wait.bmp', grayscale=True, confidence=0.9) is not None:
                return 2
        while (
                pos := pyautogui.locateOnScreen(r'.\Images\brosweropened.bmp', grayscale=True,
                                                confidence=0.999)) is None:
            pass
        click(getCenterPos(pos))
        pyautogui.moveTo(1450, 725)
        self.currentTab = 'chrome'
        return 0

    def preGameMode2(self):
        print('in pre2')
        while True:
            if (pyautogui.locateOnScreen(r'.\Images\myturn.bmp', grayscale=False, confidence=0.83) is not None) and (
                    self.currentTab == 'edge'):
                while (pos := pyautogui.locateOnScreen(r'.\Images\brosweropened.bmp', grayscale=True,
                                                       confidence=0.999)) is None:
                    pass
                click(getCenterPos(pos))
                pyautogui.moveTo(1450, 725)
                self.currentTab = 'chrome'
                return
            elif pyautogui.locateOnScreen(r'.\Images\myturn.bmp', grayscale=False, confidence=0.85) is not None:
                return
            if (pyautogui.locateOnScreen(r'.\Images\friendturn.bmp', grayscale=False, confidence=0.8) is not None) and (
                    self.currentTab == 'chrome'):
                self.switchTabAndWait(True)
                return
            if (pyautogui.locateOnScreen(r'.\Images\friendturn.bmp', grayscale=False, confidence=0.8) is not None) and (
                    self.currentTab != 'chrome'):
                self.switchTabAndWait(False)
                return

    def waitLeave(self, notfine, fine):
        time.sleep(1.2)
        if pyautogui.locateOnScreen(r'.\Images\leaveroom.bmp', region=(820, 400, 240, 550), grayscale=True,
                                    confidence=0.97) is not None:
            return notfine
        return fine

    def checkStuck(self, fine, notfine, stuckMax):
        if self.stuckCount > stuckMax:
            if pyautogui.locateOnScreen(r'.\Images\finding.bmp', region=(650, 120, 620, 105), grayscale=True,confidence=0.95) is not None:
                self.stuckCount = 0
                return fine
            if (pos := pyautogui.locateOnScreen(r'.\Images\leaveroom.bmp', region=(300, 300, 880, 750), grayscale=True,confidence=0.9)) is not None:
                self.stuckCount = 0
                click(getCenterPos(pos))
                time.sleep(0.5)
                reloadPage(1)
                return notfine
            print('out at', self.stuckCount)
            reloadPage()
            time.sleep(0.5)
            self.stuckCount = 0
            return notfine
        return fine

    def waitTillNextTurn(self):
        if self.gameMode == 2:
            return 0
        self.stuckCount = 0
        while True:
            if pyautogui.pixel(*self.nodePos) == (24, 188, 156):
                return 0
            if pyautogui.locateOnScreen(r'.\Images\playbutton.bmp', region=(1035, 255, 155, 95), grayscale=True,
                                        confidence=0.9) is not None:
                return 2
            if pyautogui.locateOnScreen(r'.\Images\gotogame.bmp', region=(1050, 620, 215, 95), grayscale=True,
                                        confidence=0.9) is not None:
                print("wait see goto")
                return 2
            if (pyautogui.locateOnScreen(r'.\Images\leaveroom.bmp', region=(820, 400, 240, 550), grayscale=True,
                                         confidence=0.97)) is not None:
                if self.newGame:
                    if self.waitLeave(2, 0) == 2:
                        return 2
                else:
                    return 2
            self.stuckCount += 1
            if self.checkStuck(0, 2, 350) == 2:
                print('time out wait')
                return 2

    def resetGame(self):
        game.board = [[0 for _ in range(15)] for _ in range(15)]
        game.reset()
        self.newGame = 1
        self.stuckCount = 0

    def updateNamePosNode(self):
        self.stuckCount = 0
        while True:
            namePos = getCenterPos(
                pyautogui.locateOnScreen(r'.\Images\myname.bmp', region=(770, 105, 395, 55), grayscale=True,
                                         confidence=0.95))
            #print('yoo?')
            if namePos is not None:
                break
            if pyautogui.locateOnScreen(r'.\Images\playbutton.bmp', region=(1035, 255, 155, 95), grayscale=True,
                                        confidence=0.9) is not None:
                return 0
            if pyautogui.locateOnScreen(r'.\Images\gotogame.bmp', region=(1050, 620, 225, 115), grayscale=True,
                                        confidence=0.95) is not None:
                print("name see goto")
                return 0
            if (pyautogui.locateOnScreen(r'.\Images\leaveroom.bmp', region=(820, 400, 240, 550), grayscale=True,
                                         confidence=0.97)) is not None:
                print("name see leaveroom")
                if self.newGame:
                    if self.waitLeave(0, 1) == 0:
                        return 0
                else:
                    return 0
            self.stuckCount += 1
            if self.checkStuck(1, 0 ,80) == 0:
                print('time out name')
                return 0


        d2, d1 = math.dist(namePos, (1460, 154)), math.dist(namePos, (460, 153))
        if d1 < 400:
            node = 0 if pyautogui.pixel(460, 153) == (24, 188, 156) else 1
        else:
            node = 0 if pyautogui.pixel(1460, 154) == (24, 188, 156) else 1
        self.namePos = namePos
        self.node = node
        self.nodePos = (1014, 173) if (self.namePos[0] > 950) else (905, 173)
        self.color = (24, 188, 156) if self.node else (44, 62, 80)
        return 1

    def start(self):
        self.stopped = False
        t = Thread(target=self.run, daemon=True)
        t.start()
        self.newGame = 1

    def stop(self):
        self.stopped = True

    def getFoePos(self, step=306 / 7):
        #(675,277) init pos for searching
        cur_x = 675
        cur_y = 277
        screen = pyautogui.screenshot()
        for y in range(15):
            for x in range(15):
                # print(cur_x,cur_y)
                if game.board[y][x] != 0:
                    cur_x += step
                    continue
                if screen.getpixel((round(cur_x), round(cur_y))) == self.color:
                    return x, y
                cur_x += step
            cur_y += step
            cur_x = 675
        return None

    def updateBoardInfo(self, step=306 / 7):
        foePos = None
        pos = None
        self.stuckCount = 0
        while foePos is None:
            if self.node:
                nodepath = r'.\Images\greenNode.bmp'
            else:
                nodepath = r'.\Images\blackNode.bmp'

            foePos = getCenterPos(
                pyautogui.locateOnScreen(nodepath, region=(650, 260, 660, 660), grayscale=False, confidence=0.9999))
            if self.newGame:
                foePos = getCenterPos(
                    pyautogui.locateOnScreen(nodepath, region=(650, 260, 660, 660), grayscale=False, confidence=0.9))
            if pyautogui.locateOnScreen(r'.\Images\firstMove.bmp', region=(615, 230, 725, 720), grayscale=False,
                                        confidence=self.firstPer):
                return 1

            if pyautogui.locateOnScreen(r'.\Images\playbutton.bmp', region=(1035, 255, 155, 55), grayscale=True,
                                        confidence=0.85) is not None:
                return 0
            if (pyautogui.locateOnScreen(r'.\Images\leaveroom.bmp', region=(820, 400, 240, 550), grayscale=True,
                                         confidence=0.97)) is not None:
                return 0
            if pyautogui.locateOnScreen(r'.\Images\gotogame.bmp', region=(1060, 630, 195, 75), grayscale=True,
                                        confidence=0.9) is not None:
                return 0
            if foePos is not None:
                pos = (round((foePos[0] - 676) / step), round((foePos[1] - 280) / step))
                if game.board[pos[1]][pos[0]] != 0:
                    foePos = None
                elif self.newGame:
                    self.newGame = 0
            self.stuckCount += 1
            if self.checkStuck(1, 0, 80) == 0:
                return 0

        #print('see foe at: ', pos[0], ', ', pos[1])
        game.board[pos[1]][pos[0]] = 2
        enemyMove(pos[0], pos[1])
        return 1

    def updateBoardInfo2(self, step=306 / 7):
        foePos = None
        self.stuckCount = 0
        while True:
            foePos = self.getFoePos()
            if foePos is None:
                if pyautogui.locateOnScreen(r'.\Images\playbutton.bmp', region=(1035, 255, 155, 95), grayscale=True,
                                            confidence=0.9) is not None:
                    return 0
                if (pyautogui.locateOnScreen(r'.\Images\leaveroom.bmp', region=(820, 400, 240, 550), grayscale=True,
                                             confidence=0.97)) is not None:
                    return 0
                if pyautogui.locateOnScreen(r'.\Images\gotogame.bmp', region=(1050, 620, 215, 95), grayscale=True,
                                            confidence=0.9) is not None:
                    return 0
                if self.newGame:
                    return 1
            else:
                if self.newGame:
                    self.newGame = 0
                break
            self.stuckCount += 1
            if self.checkStuck(1, 0, 350) == 0:
                print('time out game')
                return 0

        # print('see foe at: ', pos[0], ', ', pos[1])
        game.board[foePos[1]][foePos[0]] = 2
        enemyMove(foePos[0], foePos[1])
        return 1

    def getNextMove(self):
        return getAIMove()

    def inGame(self):
        #print('new game')
        time.sleep(0.05)
        if not self.updateNamePosNode():
            self.resetGame()
            return
        #print('done name pos')
        while not game.done():
            while (res := self.waitTillNextTurn()) != 0:
                if res == 2:
                    self.resetGame()
                    return
            #    self.updateNamePosNode()
            if not self.updateBoardInfo2():
                break
            if game.done(): break
            x, y = self.getNextMove()
            pyautogui.moveTo(round(676 + (x * 306 / 7)), round(280 + (y * 306 / 7)))
            time.sleep(0.02)
            pyautogui.click()
            game.board[y][x] = 1
            if self.newGame:
                self.newGame = 0
            #print("i played at Pos: ", x, ', ', y)
            #for row in game.board:
            #print(row)
            if self.gameMode == 2:
                res = self.switchTabAndWait(1)
                if res != 0:
                    break
            else:
                time.sleep(0.05)
        self.resetGame()

    def postGame(self):
        #print('in pos game')
        time.sleep(0.5)
        if self.gameMode == 2:
            while True:
                if pyautogui.locateOnScreen(r'.\Images\wait.bmp', grayscale=True, confidence=0.9) is not None:
                    while (pos := pyautogui.locateOnScreen(r'.\Images\brosweropened.bmp', grayscale=True,
                                                           confidence=0.999)) is None:
                        pass
                    click(getCenterPos(pos))
                    while (pos := pyautogui.locateOnScreen(r'.\Images\playagain.bmp', grayscale=True,
                                                           confidence=0.9)) is None:
                        pass
                    click(getCenterPos(pos))
                    pyautogui.moveTo(1450, 725)
                    self.currentTab = 'chrome'
                    return 1
                if pyautogui.locateOnScreen(r'.\Images\friendout.bmp', grayscale=True, confidence=0.9) is not None:
                    return 0
        self.stuckCount = 0
        while True:
            if (pos := pyautogui.locateOnScreen(r'.\Images\leaveroom.bmp', region=(300, 300, 880, 750), grayscale=True,
                                                confidence=0.85)) is not None:
                click(getCenterPos(pos))
                time.sleep(0.75)
                continue
            if (pos := pyautogui.locateOnScreen(r'.\Images\playbutton.bmp', region=(1035, 255, 155, 95), grayscale=True,
                                                confidence=0.9)) is not None:
                click(getCenterPos(pos))
                time.sleep(0.05)
                pyautogui.moveTo(460, 253)
                time.sleep(0.5)
                return 1

            if pyautogui.locateOnScreen(r'.\Images\ingame.bmp', region=(930, 125, 60, 45), grayscale=True,confidence=0.95) is not None:
                return 1
            if (pos := pyautogui.locateOnScreen(r'.\Images\gotogame.bmp', region=(1050, 620, 225, 115), grayscale=True,
                                                confidence=0.9)) is not None:
                click(getCenterPos(pos))
                pyautogui.moveTo(460, 253)
                time.sleep(1)
                return 1
            self.stuckCount += 1
            if self.checkStuck(1, 0, 80) == 0:
                print('time out post')
                time.sleep(1)
                continue

    def run(self):
        while not self.stopped:
            if self.gameMode == 2:
                self.preGameMode2()
            self.inGame()
            res = self.postGame()
            #print('done post')
            if res == 0:
                pyautogui.press('esc')
                return
