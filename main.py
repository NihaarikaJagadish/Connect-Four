from minimaxAlphaBeta import *
import datetime
RED     = '\033[1;31;40m'
YELLOW  = '\033[1;33;40m'
WHITE   = '\033[1;37;40m'

dir_path = os.getcwd()
os.chdir(dir_path)


def saveParser(board, filename):
    def parseRow(row):
        return str(row).strip(']').strip('[').replace("' '",'.').replace(',','').replace("'",'')
    if os.name == 'nt':
        slash = '\\'
    else:
        slash = '/'
    with open(dir_path +slash + "saved-games" + slash +filename + '.txt', 'w') as f:
        for row in board:
            f.write(parseRow(row)+'\n')

    return True

def playerTurn(board):
    Col = input(WHITE + 'Choose a Column between 1 and 7: ' + WHITE)
    if not(Col.isdigit()):
        print(YELLO + "Input must be integer!" + WHITE)
        return playerTurn(board)

    playerMove = int(Col) - 1

    if playerMove < 0 or playerMove > 6:
        print(YELLOW + "Column must be between 1 and 7!" + WHITE)
        return playerTurn(board)

    if not(isColumnValid(board, playerMove)):
        print(YELLOW + "The Column you select is full!" + WHITE)
        return playerTurn(board)


    board = makeMove(board, playerMove, HUMAN_PLAYER)[0]
    playerFourInRow  = findFours(board)
    return board, playerFourInRow

def playerWins(board):
    printBoard(board)
    print('                    '+YELLOW+"HUMAN WINS !!\n" +WHITE)
    global aiTimeArray
    totalTime = datetime.timedelta(seconds=0)
    for each in aiTimeArray:
        totalTime = each + totalTime
    print('                     '+YELLOW+"On an average the AI took \n" +WHITE)
    print(totalTime/len(aiTimeArray))
    playagain = True if input(WHITE +'DO YOU WANT TO PLAY AGAIN(y/n)?'+WHITE).lower() == 'y' else False
    if playagain:
        mainFucntion()
    return 0

aiTimeArray = []
def aiTurn(board,depth, abAlgorithm):
    startTime = datetime.datetime.now()
    aiMove  = MiniMaxAlphaBeta(board, depth, AI_PLAYER, abAlgorithm)
    board = makeMove(board, aiMove, AI_PLAYER)[0]
    aiFourInRow  = findFours(board)
    endTime = datetime.datetime.now()
    print(endTime - startTime)
    global aiTimeArray
    aiTimeArray.append(endTime - startTime)
    return  board, aiFourInRow

def aiWins(board):
    printBoard(board)
    print('                     '+RED+"AI WINS !!!!\n" +'\033[1;37;40m')
    global aiTimeArray
    totalTime = datetime.timedelta(seconds=0)
    for each in aiTimeArray:
        totalTime = each + totalTime
    print('                     '+RED+"On an average the AI took  \n" +'\033[1;37;40m')
    print(totalTime/len(aiTimeArray))
    playagain = True if input(WHITE+'DO YOU WANT TO PLAY AGAIN(y/n)?'+WHITE).lower() == 'y' else False
    if playagain:
        mainFucntion()
    return 0

def mainFucntion():
    board = initializeBoard()
    os.system('cls' if os.name == 'nt' else 'clear')
    printBoard(board)
    depth = 3
    whileCondition = 1
    abAlgorithm = True if input(WHITE + 'DO YOU WANT TO USE ALPHA-BETA PRUNING(y/n)? ' + WHITE).lower() == 'y' else False
    whomStart = True if input(WHITE + 'DO YOU WANT TO START(y/n)? ' + WHITE).lower() == 'y' else False
    if board == None:
        board = initializeBoard()

    while(whileCondition):
        if isBoardFilled(board) :
            print("GAME OVER\n")
            break

        if whomStart:

            board, playerFourInRow = playerTurn(board)
            if playerFourInRow:
                whileCondition = playerWins(board)
                if whileCondition ==0:
                    break

            #AI
            board, aiFourInRow = aiTurn(board,depth, abAlgorithm)
            if aiFourInRow:
                whileCondition = aiWins(board)
                if whileCondition ==0:
                    break
            printBoard(board)
  
        else:
            #AI
            board, aiFourInRow = aiTurn(board,depth, abAlgorithm)
            if aiFourInRow:
                whileCondition = aiWins(board)
                if whileCondition ==0:
                    break
            printBoard(board)

            #Human
            board, playerFourInRow = playerTurn(board)
            if playerFourInRow:
                whileCondition = playerWins(board)

                if whileCondition ==0:
                    break

            printBoard(board)

mainFucntion()