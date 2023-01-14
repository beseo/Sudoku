import pygame as pg
import time

WIDTH = 650
BACKGROUND = (251, 234, 235) #pink-ish background
LINE_COLOR = (0, 0, 0)       #black lines
NUM_COLOR = (47, 60, 126)    #blue numbers
FILL_COLOR = (119, 237, 160) #when number is filled

EMPTY_COLOR = (240, 108, 123)#when space is cleared
board = [
    [8, 0, 0, 0, 5, 2, 0, 4, 0],
    [7, 0, 0, 0, 0, 0, 0, 8, 1],
    [0, 4, 5, 0, 7, 8, 0, 9, 6],
    [0, 0, 0, 0, 6, 0, 1, 0, 0],
    [0, 6, 2, 8, 9, 5, 3, 7, 0],
    [4, 7, 0, 0, 3, 1, 0, 0, 0],
    [9, 1, 3, 7, 0, 4, 0, 5, 8],
    [0, 0, 7, 0, 0, 0, 0, 3, 2],
    [0, 0, 0, 0, 8, 6, 0, 0, 0]
]

'''
Helper method to declutter main() loop
Draws Sudoku board lines
@param window Pygame display window and surface
'''
def draw_board_lines(window):
    #draw boxes
    for i in range(0, 10):
        #bolded separators
        if i % 3 == 0:
            pg.draw.line(window, LINE_COLOR, (100 + 50 * i, 100), (100 + 50 * i, 550), 3)
            pg.draw.line(window, LINE_COLOR, (100, 100 + 50 * i), (550, 100 + 50 * i), 3)

        pg.draw.line(window, LINE_COLOR, (100 + 50 * i, 100), (100 + 50 * i, 550))
        pg.draw.line(window, LINE_COLOR, (100, 100 + 50 * i), (550, 100 + 50 * i))
    pg.display.update()

'''
Draws in all the numbers in the Sudoku board onto the display. 
Prints all elements in a single row of the board, for every row.
Does not print zeros.
@param window Pygame display window and surface
@param font PyGame font object
@param board 2-d array representation of a Sudoku board
'''
def fill_board(window, font, board, finish = False):
    if not finish:
        for i in range(len(board)):   #A.K.A. for row in board:
            for j in range(len(board[i])): #A.K.A. for number in row:
                if board[i][j] == 0:
                    continue #do not print zeros.
                fill_space(window, board, j, i, BACKGROUND)
                pg.display.update()
                fill_space(window, board, j, i, FILL_COLOR)
                text = font.render(str(board[i][j]), True, NUM_COLOR)
                window.blit(text, (117 + 50*j, 110+50*i)) 
                pg.display.update()
    else:
        flower(window, font, board)
'''
EXTRA METHOD FOR FINAL ANIMATION: not required, remove for efficiency
Assumes no zeros.
'''
def flower(window, font, board):
    fill_space(window, board, 4, 4, BACKGROUND)
    for i in range(1,5):  

        for j in range(1,5): 
            fill_space(window, board, 4+i, 4+j, BACKGROUND)
            fill_space(window, board, 4+i, 4-j, BACKGROUND)
            fill_space(window, board, 4-i, 4+j, BACKGROUND)
            fill_space(window, board, 4-i, 4-j, BACKGROUND)

            fill_space(window, board, 4+j, 4+i, BACKGROUND)
            fill_space(window, board, 4+j, 4-i, BACKGROUND)
            fill_space(window, board, 4-j, 4+i, BACKGROUND)
            fill_space(window, board, 4-j, 4-i, BACKGROUND)

            fill_space(window, board, 4+i, 4, BACKGROUND)
            fill_space(window, board, 4-i, 4, BACKGROUND)
            fill_space(window, board, 4, 4+i, BACKGROUND)
            fill_space(window, board, 4, 4-i, BACKGROUND)
            time.sleep(0.01)
            pg.display.update()
            # text = font.render(str(board[i][j]), True, NUM_COLOR)
            # window.blit(text, (117 + 50*j, 110+50*i)) 
            # pg.display.update()
    time.sleep(0.5)
    fill_board(window, font, board)
'''
@param clear boolean value of whether we are clearing or filling in a value
'''

def fill_space(window, board, row, col, color):
    rect = pg.Rect(102 + 50 * row, 102 + 50 * col, 47,47)
    pg.draw.rect(window, color, rect)

    
#------------------------------- SOLVER SECTION -------------------------
def safe(board, row, column, num):
    row_clear = num not in board[row]
    col_clear = not in_col(board, column, num)
    box_clear = not in_box(board, row, column, num)
    return row_clear and col_clear and box_clear

'''
Helper method for safe()
@return True if the number provided is in the column, False otherwise
@param column to check
@param num number to check for
'''
def in_col(board, column, num):
    for i in range(9):
        if board[i][column] == num:
            return True
    return False
'''
Helper method for safe()
@return True if the number provided is in the respective 3x3 box, False otherwise
@param row to check
@param column to check
@param num number to check for
'''
def in_box(board, row, column, num):
    for i in range(row// 3*3, row//3*3+3):
        for j in range(column//3*3, column//3*3+3):
            if board[i][j] == num:
                return True
    return False

''''''
def solve(window, font, board, row = 0, col = 0):
    
    if row == 9:
        return True #found solution
    elif col == 9:
        #move to next row, and start on column 0
        
        return solve(window, font, board, row + 1, 0)
    elif board[row][col] != 0:
        #space taken, move to next position (col + 1)
        return solve(window, font, board, row, col+1)
    else: #empty space, and not out of bounds
        for num in range(1,10): #valid sudoku numbers
            fill_space(window, board, row, col, EMPTY_COLOR)
            pg.display.update()
            time.sleep(0.0015)
            if safe(board, row, col, num):
                board[row][col] = num
                fill_board(window, font, board)
                if solve(window, font, board, row, col+1): #if solution found
                    return True #stop recursion
                board[row][col] = 0 #solution not found, reset space
                
        return False #no valid solution, move on
#---------------------------- END OF SOLVER SECTION -------------------------
#main loop
def main():
    pg.init()

    #make sure font package is loaded
    if not pg.font.get_init(): 
        pg.font.init()
    font = pg.font.SysFont('Roboto', 50) #choose fonts
    
    window = pg.display.set_mode((WIDTH, WIDTH))
    pg.display.set_caption("Sudoku")
    window.fill(BACKGROUND)

    draw_board_lines(window)

    fill_board(window, font, board)
    solve(window, font, board, 0, 0)
    time.sleep(1)
    fill_board(window, font, board, finish = True)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return 

main()