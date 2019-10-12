# encoding: utf8
import pygame
from pygame.locals import *
import random
import tkinter as tk
import tkinter.messagebox as tkmb

# 游戏对象的类 surface:表示图片 rect: 坐标属性，
class SnakeNibble:
    """移动蛇，当蛇吃果子时，身体会变大，撞墙或者撞到自己时游戏结束"""
    def __init__(self,width=400,edge=20):
        self.width = self.height = 400 # 屏幕尺寸
        self.edge = edge # 身体边长
        self.ball = pygame.Surface((edge, edge)) # Surface对象
    
    def makeSnake(self):
        '''创建蛇 初始方向 右'''
        self.ball.fill((220,20,60)) # 红色
        ballrect = self.ball.get_rect() # 获取 rect 对象
        a = self.edge * 5
        snake = []
        for _ in range(3):
            ballrect2 = ballrect.copy() 
            ballrect2.left += a
            ballrect2.top = 100
            a -= self.edge
            snake.append(ballrect2)
        return snake

    def move(self,snake,direct):
        """按照方向移动 并返回更新之前 snake 的尾巴"""
        for i in range(len(snake)):
            if i==0: # 每次只更新队列第一个的方向，其他方向照旧
                rect = snake[0].copy()
                temp = self._get_nextRect(rect,direct)
        snake.insert(0,temp) # 加入头部的新位置
        endPop = snake.pop() # 删除末尾
        return endPop

    def strike(self,snake,food):
        '''蛇的撞击检测
        ：param snake：蛇的 Rect 对象序列
        ：param food：食物的 Rect 对像
        ：return ：撞墙，撞自己返回 0,代表游戏结束,吃果子返回 1，无碰撞返回 3
        '''
        # 撞墙
        if snake[0].left < 0 or snake[0].right > self.width: return 0
        if snake[0].top < 0 or snake[0].bottom > self.height: return 0
        # 撞自己
        for sr in snake[1:]:
            if sr.colliderect(snake[0]):
                return 0
        # 吃食物
        if food.colliderect(snake[0]):
            return 1
        return 2 

    def _get_nextRect(self,rect,direct):
        """蛇 获取头部的新位置"""
        if direct == 0: rect.top += self.edge # 向下
        elif direct == 1: rect.top -= self.edge # 向上
        elif direct == 2: rect.left += self.edge # 向右
        elif direct == 3: rect.left -= self.edge # 向左
        return rect
        
 
class Food:
    """位置随机生成的食物"""
    def __init__(self,width=400,edge=20):
        self.width = self.height = 400
        self.edge = edge
        self.food = pygame.Surface((self.edge, self.edge)) # surface 对象

    def get_food(self):
        """生成食物 rect 对象"""
        self.food.fill((0,0,255)) # 蓝色
        fr = self.food.get_rect() 
        return fr
    
    def get_foodpos(self,food,snake):
        '''获取食物新位置'''
        while True:
            food.left, food.top = random.randrange(self.edge,self.height,self.edge),random.randrange(self.edge,self.height,self.edge) # 更新 fr 的位置
            foodpos = True
            for sn in snake: # 食物更新位置不能在蛇的身体内部
                if food.colliderect(sn):
                    foodpos = False
                    break
            if foodpos == True:
                break
        if foodpos == True: # 有位置
            return True

class Background:
    def __init__(self,width=400,edge=20):
        self.width = self.height = 400
        self.edge = edge
        self.grid = pygame.Surface((self.edge,self.edge)) # Surface 对象
        self.scoref = pygame.font.SysFont('Arial', 20)

    def userScore(self,screen,score): # 游戏结束显示文本
        """游戏结束 时的得分显示"""
        f=pygame.font.SysFont('Arial', 30)
        t=f.render('Score: %s'%str(score), True, (255, 255, 255))
        screen.blit(t, (20, 260))
        pygame.display.update()
        pygame.time.wait(1000)

    def drawGrid(self,surface):
        # 画全屏幕格子线条
        rows = self.width // self.edge
        sizeBtwn = self.edge
        x,y = 0,0
        for _ in range(rows):
            x += sizeBtwn
            y += sizeBtwn
            pygame.draw.line(surface,(219,112,147),(x,0),(x,self.width))
            pygame.draw.line(surface, (219,112,147),(0,y),(self.width,y))

    def drawSgrid(self,surface,rect):
        # 画单个小格子线条
        left = rect.left
        right = rect.right
        top = rect.top
        bottom = rect.bottom
        pygame.draw.line(surface,(219,112,147),(left,top),(right,top))
        pygame.draw.line(surface,(219,112,147),(left,bottom),(right,bottom))
        pygame.draw.line(surface, (219,112,147),(left,top),(left,bottom))
        pygame.draw.line(surface, (219,112,147),(right,top),(right,bottom))

def message_box():
    """跳出信息框，决定退出还是重新开始游戏"""
    root  = tk.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    response = tkmb.askyesno('Snake', '是 退出，否 重新开始游戏')
    try:
        root.destroy()
    except:
        pass
    if response:
        return True
    else:
        return False

def main():
    """初始化并在循环中运行直到有返回"""
    # 初始化
    pygame.init()
    direct = 2
    oldDirect = direct # 有效速度
    edge = 20 # 格子大小
    width,height = 400,400 # 使用正方形
    screen = pygame.display.set_mode((width,height)) # 初始化一个窗口
    pygame.display.set_caption('Snake')
    
    # 对象准备
    # 蛇
    s = SnakeNibble(width,edge) # 身体尺寸=格子尺寸
    snake = s.makeSnake() # 创建蛇 生成 rect 序列
    # 食物
    f = Food(width,edge) # 身体尺寸=格子尺寸
    foodr = f.get_food() # 生成 rect 对象
    f.get_foodpos(foodr,snake) # 随机生成食物位置
    # 格子
    b = Background(width,edge)
    grid = b.grid 
    scoref = b.scoref
    b.drawGrid(screen)
    # 分数
    scorer = grid.get_rect()

    c = 0 # 计数
    dt = 0 # 计时
    score = 0 # 得分
    going = True # 状态
    endPop = None # snake 尾巴
    runSpeed = 300 # 每 runSpeed 毫秒移动 10 个像素位置。游戏速率越小游戏运行越快
    clock = pygame.time.Clock() # 创建帮助记录时间的对象
    while going:
        lastt = clock.tick(60) # 帧率 60
        dt += lastt # 控制显示效果
        c += 1
        print('循环次数 %d, 前一次的时间 %d，目前总时间 %d 单位毫秒'%(c,lastt,dt)) # 游戏帧率
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                going = False
            elif event.type == KEYDOWN:
                if event.key == K_UP and oldDirect != 0: direct = 1 # 按了向上 1 并且当前方向不是向下 0 ，则向上
                elif event.key == K_DOWN and oldDirect != 1: direct = 0 # 向上 1 ，向下 0
                elif event.key == K_LEFT and oldDirect != 2: direct = 3 # 向左 3， 向右 2
                elif event.key == K_RIGHT and oldDirect != 3: direct = 2 
                elif event.key == K_0: going = False # 退出或重新开始游戏
                
        if dt > runSpeed: # 控制速度
            oldDirect = direct
            dt = 0 # 初始化时间
            endPop = s.move(snake,direct)
            screen.blit(grid, endPop) # 画格子
            b.drawSgrid(screen,endPop) # 画线
        else:
            for i in range(len(snake)):
                screen.blit(s.ball, snake[i])
        # 分数更新
        screen.blit(grid, scorer) # 画图
        b.drawSgrid(screen,scorer)  # 画线
        scoret=scoref.render(str(score), True, (255, 255, 255)) # 得分记录
        screen.blit(scoret, (0, 0)) # 记录
        screen.blit(f.food, foodr) # 根据 fr(Rect 对象) 更新 food(Surface 对象) 位置 ，绘图
        pygame.display.flip() # 显示图形
        # 判断是否右撞击存在
        # 撞墙 撞自己
        clli = s.strike(snake,foodr)
        if clli == 0:
            b.userScore(screen,score)
            going = False
        elif clli == 1:
            snake.append(endPop) # 吃果实，长身体
            score += 1
            if not f.get_foodpos(foodr,snake): going = False # 生成 food 新位置, 如果占满全屏，则退出
                
if __name__ == '__main__':
    while True:
        main()
        if message_box():
            break






