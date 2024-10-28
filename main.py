import time

if __name__ == '__main__':
    from Preprocessing import *
    from BotProcessing import *

    listener = waitKeys()
    if listener is None:
        print("Can't init listener!")
        exit(0)

    OPEN_BROSWER, OPEN_TAB, SELECT_TAB = 1, 1, 1
    if preprocessTab(OPEN_BROSWER, OPEN_TAB, SELECT_TAB) == 1:
        print("Can't preprocessing tab")
        exit(0)

    # GameMode: 0 - REALGAME, (any) - VsFRIEND or yourshelf
    gameMode = 0
    if gameMode != 0:
        gameMode = 2
    myBot = gomokuBot(gameMode)
    if gameMode != 0:
        if preprocessGameMode(gameMode) == 1:
            print(f"Can't preprocessing gameMode {gameMode}")
            exit(0)
    myBot.start()

    while listener.is_alive():
        if not checkInGame(gameMode):
            print("You've outed the game")
            break
        # print("still in game")
    myBot.stop()
    print("GomokuBot finished duty!")
