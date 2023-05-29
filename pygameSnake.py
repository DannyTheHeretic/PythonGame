'''
MIT License

Copyright (c) 2023 Daniel Schmitz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

#this was my Fall Semester First year project, kinda fun to go back and look where you came from :)

import random
import tkinter as tk
import math
import pygame as pyg
import csv
import os.path
from tkinter import *


pName = []
pScore = []
file_exists = os.path.exists('highscores.csv')
#check if the CSV exists already
if file_exists:
    fileInput = open('highscores.csv', 'r')
    data = fileInput.read().split('\n')
    fileInput.close()

    #parsing the CSV
    if len(data) > 3:
        for row in data:
            player = row.split(',')
            if ('' not in player and len(player) == 2):
                pName.append(player[0])
                pScore.append(int(player[1])) 

        #alert window popup
        def alert_popup(title, message):
            root = tk.Tk()
            root.title(title)
            w = 200
            h = 100
            sw = root.winfo_screenwidth()
            sh = root.winfo_screenheight()
            x = (sw - w)/2
            y = (sh - h)/2
            root.geometry('%dx%d+%d+%d' % (w, h, x, y))
            m = message
            w = Label(root, text=m, width=120, height=10)
            w.pack()
            b = Button(root, text="OK", command=root.destroy, width=10)
            b.pack()
            mainloop()
        y = pScore[0:len(pName)]
        pScore.sort(reverse=True)
        leadBor = []
        names = pName
        leadBor = []
        for i, score in enumerate(pScore):
            if i < 3:
                index = pScore.index(score)
                leadBor.append(pName[index])
            else:
                break
        alert_popup('LEADERBOARD',('LEADERBOARD'+'\n'+'1st Place is '+leadBor[0]+' with Score of '+str(pScore[0])+'\n'+'2nd Place is '+leadBor[1]+' with Score of '+str(pScore[1])+'\n'+'3rd Place is '+leadBor[2]+' with Score of '+str(pScore[2])))


#starts the game
pyg.init()

#defining the colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (215, 53, 81)
green = (0, 255, 0)
blue = (50, 153, 213)
apple = (174,0,1)
snake_green = (108, 187, 60)



root = tk.Tk()

screen_width = (root.winfo_screenwidth())
screen_height = (root.winfo_screenheight())

root.withdraw()


#define the window size, it will automatically be half the size of your monitor
dis_width = math.floor(screen_width/2)
dis_height = math.floor(screen_height/2)

dis = pyg.display.set_mode((dis_width, dis_height))
pyg.display.set_caption('Snake Game by Daniel')

#Start of 'Working Code'

clock = pyg.time.Clock()
snake_block = 10
font_style = pyg.font.Font(None, 25)
score_font = pyg.font.Font(None, 35)
#Score display
def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, blue)
    dis.blit(value, [0, 0])
snake_block = 10
#Snake drawing
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pyg.draw.rect(dis, snake_green, [x[0], x[1], snake_block, snake_block])
#Text Definition
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width*2 / 7, dis_height*2 / 5])

#start of "game"
def gameLoop():
    clock = pyg.time.Clock()
    screen = pyg.display.set_mode([dis_width,dis_height])
    base_font = pyg.font.SysFont(None,35)
    Name = ''
    input_rect = pyg.Rect((dis_width-70),0,140,50)
    active = True
    game_over = False
    game_close = False
    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0
    snake_List = []
    Length_of_snake = 1
    snake_speed = 15+(Length_of_snake*.2)
    foodX = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foodY = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
    while not game_over:
        while game_close:
            dis.fill(black)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            Your_score(Length_of_snake - 1)
            pyg.display.update()
            for event in pyg.event.get():
                if event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pyg.K_c:
                        data = [Name, Length_of_snake - 1]
                        with open('highscores.csv', 'a',encoding="UTF8", newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(data)
                        gameLoop()
        for event in pyg.event.get():
            if active:
                if event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_BACKSPACE:
                        Name = Name[:-1]
                    elif len(Name) != 3:
                        Name += event.unicode.upper()
                    if event.key == pyg.K_RETURN:
                        active = False
            if not active:
                if event.type == pyg.QUIT:
                    game_over = True
                if event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_UP or event.key == ord('w'):
                        y1_change = -snake_block
                        x1_change = 0
                    elif event.key == pyg.K_DOWN or event.key == ord('s'):
                        y1_change = snake_block
                        x1_change = 0
                    elif event.key == pyg.K_LEFT or event.key == ord('a'):
                        x1_change = -snake_block
                        y1_change = 0
                    elif event.key == pyg.K_RIGHT or event.key == ord('d'):
                        x1_change = snake_block
                        y1_change = 0
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(black)
        pyg.draw.rect(dis, apple, [foodX, foodY, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)

        text_surface = base_font.render(Name,True,blue,True)
        screen.blit(text_surface,(input_rect.x + 5,input_rect.y+7))
        
        pyg.display.update()
        if x1 == foodX and y1 == foodY:
            foodX = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foodY = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
        clock.tick(snake_speed)
                



    pyg.quit()

    data = [Name, Length_of_snake - 1]
    with open('highscores.csv', 'a',encoding="UTF8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)
    quit()

gameLoop()
