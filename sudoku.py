import  pygame
import requests
import numpy as np
import time
 
WIDTH=550
background_color=(251,247,245)
original_grid_element_color=(52,31,151)

responce= requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
grid = responce.json()['board']
board=np.array(grid)
#creating a copy of grid  to be used later
board_original=board.copy()
board_original2=board.copy()
buffer=6

def ScoreWindow(win,score):
    myfont=pygame.font.SysFont('Comic Sans MS',35)
    pygame.draw.rect(win,background_color,(0,0,600,600))
    pygame.display.update()
    pygame.draw.rect(win,background_color,(200,200,150,50))
    value=myfont.render("your score is "+str(score),True,(0,0,0))
    win.blit(value,(125,250))
    pygame.display.update()


def insert(win,position):
    myfont=pygame.font.SysFont('Comic Sans MS',35)
    i,j=position[1],position[0]
    if(position[0]==4 or position[0]==5 or  position[0]==6):
        if(position[1]==11):
            pygame.draw.rect(win,(251,131,131),(200,550,150,50))
            value=myfont.render(str("Solve"),True,(0,0,0))
            win.blit(value,(225,550))
            pygame.display.update()

            solve(board_original2)
            for i in range(0,len(board_original2)):
                for j in range(0,len(board_original2[0])):
                    if(0<board_original2[i][j]<10):
                        
                        value= myfont.render(str(board_original2[i][j]),True,original_grid_element_color)
                        win.blit(value,((j+1)*50+15,(i+1)*50))#value to be blitted , place where the value is to blitted
                        pygame.display.update()
            return

    
    if(position[0]==0 or position[1]==0):
        return
    if(position[0]>9 or position[1]>9):
        return

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type==pygame.KEYDOWN:
                #1. edit the original file
                #2. edit
                #3. adding the digits
                if(board_original[i-1][j-1]!=0):
                    return
                if(event.key == 48): #checking if 0 is pressed # we will superimpose a rectangle on the existing one
                    board[i-1][j-1]=event.key-48
                    pygame.draw.rect(win,background_color,(position[0]*50+buffer,position[1]*50+buffer,50-2*buffer,50-2*buffer))
                    pygame.display.update() 
                    return
                if(0< event.key- 48<10):
                    pygame.draw.rect(win,background_color,(position[0]*50+buffer,position[1]*50+buffer,50-2*buffer,50-2*buffer))
                    value=myfont.render(str(event.key -48),True,(0,0,0))
                    win.blit(value,(position[0]*50+15,position[1]*50))
                    board[i-1][j-1]=event.key-48
                    pygame.display.update()
                    return

def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col

    return None

def isValid(bo,tup, num):
    # row
    for i in range(len(bo[0])):
        if bo[tup[0]][i] == num and tup[1] != i:
            return False

    # column
    for i in range(len(bo)):
        if bo[i][tup[1]] == num and tup[0] != i:
            return False

    # box
    box_x = tup[1] // 3
    box_y = tup[0] // 3
    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != tup:
                return False

    return True


def solve(bo):

    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1,10):
        if isValid(bo, (row, col),i):
            bo[row][col] = i

            if solve(bo):
                return True

            bo[row][col] = 0

    return False

def main(board):
    ti=time.time()
    pygame.init()
    win = pygame.display.set_mode((WIDTH,WIDTH+100))
    pygame.display.set_caption("Sudoku")
    win.fill(background_color)#to fill the background color
    myfont=pygame.font.SysFont('Comic Sans MS',35)

    for i in range(0,10):
        if(i%3==0):
            pygame.draw.line(win, (0,0,0),(50+50*i,50),(50+50*i,500),4)# to display vertical thicker lines 
            pygame.draw.line(win,(0,0,0),(50,50+50*i),(500,50+50*i),4)# to display horizontal thicker lines
        pygame.draw.line(win, (0,0,0),(50+50*i,50),(50+50*i,500),2)# to display vertical lines 
        pygame.draw.line(win,(0,0,0),(50,50+50*i),(500,50+50*i),2)# to display horizontal lines
    pygame.display.update()    
    
    for i in range(0,len(board)):
        for j in range(0,len(board[0])):
            if(0<board[i][j]<10):
                value= myfont.render(str(board[i][j]),True,original_grid_element_color)
                win.blit(value,((j+1)*50+15,(i+1)*50))#value to be blitted , place where the value is to blitted
    pygame.display.update()    

    pygame.draw.rect(win,(251,247,131),(200,550,150,50))
    value=myfont.render(str("Solve"),True,(0,0,0))
    win.blit(value,(225,550))
    pygame.display.update()

    while(True):#to check  for quit
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:#checking for left click
                pos=pygame.mouse.get_pos()
                insert(win,(pos[0]//50,pos[1]//50))
                if (board==board_original2).all():
                    ti2=time.time()
                    timeTaken=(ti2-ti)
                    score=(3050-(timeTaken))
                    if(score<0):
                        score=0
                    score=round(score)
                    ScoreWindow(win,score)
                    pygame.time.delay(1500)
                    return score
            if event.type ==pygame.QUIT:
                pygame.quit()
                return

solve(board_original2)
print(board_original2)

if __name__=="__main__":
    main(board)