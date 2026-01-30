import pprint
theBoard = {
    'top-L': ' ',
    'top-M': ' ',
    'top-R': ' ',
    'mid-L': ' ',
    'mid-M': ' ',
    'mid-R': ' ',
    'low-L': ' ',
    'low-M': ' ',
    'low-R': ' '
}

theBoard['top-L'] = 'O'
theBoard['top-M'] = 'O'
theBoard['top-R'] = 'O'
theBoard['low-L'] = 'X'
theBoard['mid-R'] = 'X'

def printBoard(board: str):  # call this function with variable of type dict
    print(board['top-L'] + '|' + board['top-M'] + '|' + board['top-R'])
    print('-----')
    print(board['mid-L'] + '|' + board['mid-M'] + '|' + board['mid-R'])
    print('-----')
    print(board['low-L'] + '|' + board['low-M'] + '|' + board['low-R'])


printBoard(theBoard)
# pprint.pformat(theBoard)
# pprint.pprint(theBoard)