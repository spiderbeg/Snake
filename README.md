# Python 使用 Pygame 实现贪吃蛇小游戏
## 目录部分
1. Pygame 上手
   1. 创建方格，并移动方格位置
   2. 绘制格子，写字
2. 创建主要角色 蛇、食物
   1. 创建蛇，使用方向键控制移动方向（如何移动）
   2. 碰撞检测（撞墙、撞自己、吃食物），以及长身体
3. 其他注意事项，速率控制，
   1. 速率控制
   2. 得分显示
   3. 创建类，分类方法，游戏完成
## 项目思路
1. 如何控制移动
## Pygame 上手
### 创建方格，并移动方格位置
* 熟悉一个新库的方式就是直接看例子，所以下面直接贴 Pygame 创建位置随机方格的代码，后面再详细讲解每一句的含义。
      
      #encoding: utf8
      import pygame
      from pygame.locals import *
      import random
      pygame.init() # 初始化 pygame 各模块

      edge = 20 # 格子大小
      screenColor = 230,230,250 # 屏幕颜色淡紫色
      width,height = 400,400 # 窗口尺寸，后面的例子中，我们格子、窗口屏幕都设置为正方形
      screen = pygame.display.set_mode((width,height)) # 初始化一个窗口, 为 Surface 对象
      pygame.display.set_caption('Snake') # 设置标题名

      # 格子 
      # surface 对象表示图片 rect对象 表示坐标，
      grid = pygame.Surface((edge, edge)) # 创建一个 20 * 20 大小的 Surface 对象
      gridColor = (0,0,255) # 蓝色
      grid.fill(gridColor) # 格子 Surface 对象填充颜色
      gr = grid.get_rect() # Rect 对象
      gr.left, gr.top = random.randrange(0,width,edge),random.randrange(0,height,edge) # 在屏幕范围内产生随机坐标

      going = True # 控制是否退出循环
      clock = pygame.time.Clock()
      while going:
          clock.tick(10) # 游戏帧率为 10，每秒刷新 10 次
          for event in pygame.event.get():
              if event.type == pygame.QUIT: # 监听游戏退出
                  going = False
          screen.fill(screenColor) # 添加屏幕颜色
          screen.blit(grid, gr) # 将格子画到 gr 的位置 
          pygame.display.flip() # 使我们刚刚画到屏幕上的 格子 可见
      pygame.quit() # 退出游戏
* 通过这个例子你可以在淡紫色屏幕上获取一个每次启动更新位置的蓝色方形格子。首先我们需要导入相关的包。然后调用 pygame.init() 初始化相应的模块。方法 pygame.display.set_mode() 会创建一个图形化窗口。正如在代码注释中所写，在 Pygame 中 Surface 对象表示了图像。display.set_mode() 函数创建一个新的 Surface 对象来表示实际要显示的图像，任何你画到这个 Surface 对象的图像，都会在显示器上变得可见。pygame.display.set_caption('Snake') 会给创建的窗口命名为 Snake。这就是对于窗口的配置。
* pygame.Surface() 是生成一个相应大小、颜色的格子。grid.get_rect() 方法根据grid（Surface 对象），获取一个矩形区域 Rect 对象。在 Pygame 中可以认为 Surface 对象就像是图片，Rect 对象就是图片的一个坐标位置，只有将图片放在对应的坐标位置，图像才会出现在对应的位置。screen.blit(grid, gr) 就是将 格子 画到 screen(Surface 对象)上 gr 的位置的函数。
* 接下来我们就要通过改变 gr（Rect 对象）的坐标来改变位置。修改矩形位置的左上角坐标(gr.left, gr.top),就完成了修改 gr 位置。
最后，再强调一次，对于你要显示的图像，都要使用 screen.blit() 方法将图像（Surface 对象）画到相应的坐标（Rect 对象）。在图像画好之后调用 pygame.display.flip() 就可以把我们画到屏幕上的图像变得可见。
* 在上面的代码中我们已经实现了每次变换位置的格子。接下来我们就要根据键盘的上下左右控制格子的移动。下面代码加入 pygame.event.get() 获取键盘事件，get_nextRect() 来控制格子移动.
   * pygame.event.get() 会获取键盘的响应信息。在代码中是这样的。
         
         for event in pygame.event.get():
              if event.type == pygame.QUIT: # 退出
                  going = False
              elif event.type == KEYDOWN: # 按下按键
                  if event.key == K_UP and direct != 0:direct = 1 # 按了向上 1 并且当前方向不是向下 0 ，则向上
                  elif event.key == K_DOWN and direct != 1:direct = 0 # 向上 1 ，向下 0
                  elif event.key == K_LEFT and direct != 2:direct = 3 # 向左 3， 向右 2
                  elif event.key == K_RIGHT and direct != 3:direct = 2 
                  elif event.key == K_0:
                          going = False # 退出游戏
   * 简单理解就是，这一段代码可以获取键盘中你按下的方向键，然后更改 direct 值，这里 direct 代表方格运动的方向。按键含义KEYDOWN：按下按键、K_UP：方向键上、K_DOWN：方向键下、K_LEFT：方向键左、K_RIGHT：方向键右，K_0：数字 0 键。
   * get_nextRect() 作用为将传入的 Rect 对象即坐标根据 方向（speed）,移动 sWidth 距离。意为每调用一次就将坐标向响应方向移动sWidth长度。
   
         def get_nextRect(rect,speed,sWidth):
          """根据方向移动格子
          ：param rect：格子的坐标对象；
          ：param swidth：每次移动的距离
          ：param speed：方向
          ：return rect：返回新的坐标对象
          """
          if speed == 0: # 向下
              rect.top += sWidth
          elif speed == 1: # 向上
              rect.top -= sWidth
          elif speed == 2: # 向右
              rect.left += sWidth
          elif speed == 3: # 向左
              rect.left -= sWidth
          return rect
   * 最后为了不让格子跑到界面外，添加了一下代码，格子到边界就朝相反方向移动。Rect 对象有自身的坐标信息，我们就依赖坐标信息与屏幕尺寸判断是否出界。
   
          # 判断是否出界，出界就将方向改为相反。
         if gr.left < 0: direct = 2
         if gr.right > width: direct = 3
         if gr.top < 0: direct = 0
         if gr.bottom > height: direct = 1 
   * 注意动画是由一系列的图片序列组成的，所以当我们移动了格子后，之前的格子不会自动消失，为了保证之前的格子会被擦除，我们会使用screen.fill(screenColor) 来覆盖原有的格子，然后再把格子画到 screen 上新的位置上，这样就可以保证我们每次都只看到一个格子。
* 控制格子移动代码如下 

      # encoding: utf8
      import pygame
      from pygame.locals import *
      import random
      pygame.init()

      edge = 20 # 格子大小
      screenColor = 0, 0, 0 # 黑色
      width,height = 400,400 # 窗口尺寸，后面的例子中，我们格子、窗口屏幕都设置为正方形
      screen = pygame.display.set_mode((width,height)) # 初始化一个窗口, 为 Surface 对象
      pygame.display.set_caption('Snake') # 设置标题名
      

      # 格子 
      # surface 对象表示图片 rect对象 表示坐标，
      grid = pygame.Surface((edge, edge)) # 创建一个 20 * 20 大小的 Surface 对象
      gridColor = (0,0,255) # 蓝色
      grid.fill(gridColor) # 格子 Surface 对象填充颜色
      gr = grid.get_rect() # Rect 对象
      gr.left, gr.top = random.randrange(10,width,10),random.randrange(10,height,10) # 在屏幕范围内产生随机坐标

      def get_nextRect(rect,speed,sWidth):
          """根据方向移动格子
          ：param rect：格子的坐标对象；
          ：param swidth：每次移动的距离
          ：param speed：方向
          ：return rect：返回新的坐标对象
          """
          if speed == 0: # 向下
              rect.top += sWidth
          elif speed == 1: # 向上
              rect.top -= sWidth
          elif speed == 2: # 向右
              rect.left += sWidth
          elif speed == 3: # 向左
              rect.left -= sWidth
          return rect

      direct  = 2 # 默认方向向右
      going = True # 控制是否退出循环
      clock = pygame.time.Clock()
      while going:
          clock.tick(10) # 游戏帧率为 10
          for event in pygame.event.get():
              if event.type == pygame.QUIT:
                  going = False
              elif event.type == KEYDOWN:
                  if event.key == K_UP and direct != 0:direct = 1 # 按了向上 1 并且当前方向不是向下 0 ，则向上
                  elif event.key == K_DOWN and direct != 1:direct = 0 # 向上 1 ，向下 0
                  elif event.key == K_LEFT and direct != 2:direct = 3 # 向左 3， 向右 2
                  elif event.key == K_RIGHT and direct != 3:direct = 2 
                  elif event.key == K_0:
                          going = False # 退出游戏
          # 判断是否出界
          if gr.left < 0: direct = 2
          if gr.right > width: direct = 3
          if gr.top < 0: direct = 0
          if gr.bottom > height: direct = 1 
          screen.fill(screenColor) # 添加屏幕颜色，覆盖之前格子留下的印记。
          gr = get_nextRect(gr,direct,edge) # 生成新的坐标位置
          screen.blit(grid, gr) # 将格子画到 gr 的位置 
          pygame.display.flip() # 使我们刚刚画到屏幕上的 格子 可见
      pygame.quit() # 退出游戏
这就完成了控制方块移动的功能。
### 画格子、显示字体内容
* 画格子，这里是指在屏幕上画线就成了我们看起来的格子，下面就是画线条的方法。我们是在屏幕上画线形成格子。所以第一个 Surface 对象就是 screen，然后再传入 edge: 线条间隔，width: 窗口尺寸（我们使用正方形）。然后一条条画线格子就出来。

      def drawGrid(surface,edge,width):
          """根据间隔和屏幕大小画全屏幕格子
          surface: screen 
          """
          rows = width // edge
          sizeBtwn = edge
          x,y = 0,0
          for i in range(rows):
              x += sizeBtwn
              y += sizeBtwn
              pygame.draw.line(surface,(219,112,147),(x,0),(x,width)) # (219,112,147) 表示线条颜色
              pygame.draw.line(surface, (219,112,147),(0,y),(width,y))

 
* 写字，代码见下。

      f=pygame.font.SysFont('Arial', 30) # 选则字体及大小
      t=f.render('Score: %s'%str(score), True, (255, 255, 255)) # 在新的 Surface 对象上画上文本
      screen.blit(t, (20, 260)) # 将文本放置到对应的坐标
* 以上就是 pygame 中的基本操作，我们接下来的贪吃蛇游戏，用到的方法就是上面介绍的。 
## 创建主要角色 蛇、食物
* 考虑一下，在我们要自己写贪吃蛇这个游戏时。我们应该想到，在这个游戏中有蛇、食物、背景（画格子，以及显示字体）三个对象，当然你可以认为主要是蛇和食物两个对象也没关系。这里以三个对象来描述游戏。那么我们就来分析一下，各个对象都有哪些方法。
* 蛇
   0. 蛇的格子 Surface 对象，如红色的格子
   1. 产生一条蛇；
   2. 能够移动；
   3. 蛇的撞击检测，蛇 1 撞墙、2 撞自己、3 吃食物
   4. 获取头部位置
   5. 长身体，即加尾巴
* 食物
   0. 食物的 Surface 对象，如蓝色的格子
   1. 生成食物
   2. 更新食物位置
* 背景
   0. 与屏幕颜色相同的 Surface 对象，如黑色的格子（大小与蛇的大小相同）
   1. 画全屏的线条形成格子
   2. 画单个格子的线条，如 pygame 的基本操作中所讲，蛇移动后 1 需要将原先蛇尾部的格子颜色如红色更新成屏幕格子颜色如黑色； 2 蛇吃果实，尾部就不变；3 食物移动后，将原先食物格子还原为屏幕的样子。步骤为，在原来的位置更新为屏幕颜色，然后画上相应的线条。就完成了单个格子大小的复原。
### 创建蛇，使用方向键控制移动方向（如何移动）
* 在不考虑食物的情况下，创建 SnakeNibble 类。实现以下方法：
   1. makeSnake() 创建三个格子大小的蛇
   2. move() 根据方向移动
   3. \_get_nextRect() 获取头部的新位置
* 其中的难点为蛇的移动：move()。本文的实现方法为，用列表保存蛇的身体位置（Rect 对象），当蛇移动时，只需要根据方向更新头部位置，其余位置向前
移动一个元素。移动完后，更新蛇的身体列表。将蛇新的头部添加到列表头部，删除列表尾部元素，即原来蛇的尾部位置。如此便完成了一次移动。
* 实现蛇对象详细代码如下

      # encoding: utf8
      import pygame
      from pygame.locals import *

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

          def move(self,snake,speed):
              """按照方向移动 并返回更新之前 snake 的尾巴"""
              for i in range(len(snake)):
                  if i==0: # 每次只更新队列第一个的方向，其他方向照旧
                      rect = snake[0].copy()
                      temp = self._get_nextRect(rect,speed)
              snake.insert(0,temp) # 加入头部的新位置
              endPop = snake.pop() # 删除末尾
              return endPop

          def _get_nextRect(self,rect,speed):
              """蛇 获取头部的新位置"""
              if speed[1]<0: rect.top -= self.edge
              elif speed[1]>0: rect.top += self.edge
              elif speed[0]>0: rect.left += self.edge
              elif speed[0]<0: rect.left -= self.edge
              return rect


      def main():
          """初始化并在循环中运行直到有返回"""
          # 初始化
          pygame.init()
          speed = [2,0] # 速度
          oldSpeed = speed.copy() # 有效速度
          edge = 20 # 格子大小
          width,height = 400,400 # 使用正方形
          screen = pygame.display.set_mode((width,height)) # 初始化一个窗口
          pygame.display.set_caption('Snake')

          # 对象准备
          # 蛇
          s = SnakeNibble(width,edge) # 身体尺寸=格子尺寸
          snake = s.makeSnake() # 创建蛇 生成 rect 序列
          grid = pygame.Surface((edge,edge)) 

          c = 0 # 计数
          dt = 0 # 计时
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
                      if event.key == K_UP and oldSpeed[1] <= 0: speed = [0,-2] # 按了向上并且当前方向不是向下，则向上
                      elif event.key == K_DOWN and oldSpeed[1] >= 0: speed = [0,2]
                      elif event.key == K_LEFT and oldSpeed[0] <= 0: speed = [-2,0]
                      elif event.key == K_RIGHT and oldSpeed[0] >= 0: speed = [2,0]
                      elif event.key == K_0:
                          going = False # 退出或重新开始游戏

              if dt > runSpeed: # 控制速度，每过 runSpeed 毫秒，开始运动
                  oldSpeed = speed.copy()
                  dt = 0 # 初始化时间
                  endPop = s.move(snake,speed)
                  screen.blit(grid, endPop) # 画格子 
              else:
                  for i in range(len(snake)):
                      screen.blit(s.ball, snake[i])
              pygame.display.flip() # 显示图形
          pygame.quit() # 退出游戏

      if __name__ == '__main__':
          main()
### 创建食物
* 相对而言食物的实现就要简单一些，和上面实现一个变换位置的格子相同，具体步骤可参考上文。这里用类实现，类方法如下：
   1. get_food() # 获取食物的位置
   2. get_foodpos() # 获取食物新位置
   
* 食物类的详细代码

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
### 创建背景
* 上面实现一个变换位置的格子相同，具体步骤可参考上文。这里用类实现，类方法如下：
   1. userScore() 显示得分
   2. drawGrid() # 全屏画线，形成格子
   3. drawSgrid() # 画单个格子的线条，1 当蛇不吃果实移动后将蛇的原来尾部画线条 2 将果实更新后原来的位置画线条
* 背景代码如下：

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
## 最终完成代码
* 在上面我们实现了所有的类，接下来我们只需要添加，完善，我们最开时写的方法就大功告成了。这里先贴代码，当然建议直接看 mySnake.py。后面再讲一讲补充的方法实现原理。
* 增加的方法如下：
   1. 蛇：strike() 碰撞检测

* 贪吃蛇完成代码如下：

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

          def move(self,snake,speed):
              """按照方向移动 并返回更新之前 snake 的尾巴"""
              for i in range(len(snake)):
                  if i==0: # 每次只更新队列第一个的方向，其他方向照旧
                      rect = snake[0].copy()
                      temp = self._get_nextRect(rect,speed)
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

          def _get_nextRect(self,rect,speed):
              """蛇 获取头部的新位置"""
              if speed[1]<0: rect.top -= self.edge
              elif speed[1]>0: rect.top += self.edge
              elif speed[0]>0: rect.left += self.edge
              elif speed[0]<0: rect.left -= self.edge
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
          speed = [2,0] # 速度
          oldSpeed = speed.copy() # 有效速度
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
                      if event.key == K_UP and oldSpeed[1] <= 0: speed = [0,-2] # 按了向上并且当前方向不是向下，则向上
                      elif event.key == K_DOWN and oldSpeed[1] >= 0: speed = [0,2]
                      elif event.key == K_LEFT and oldSpeed[0] <= 0: speed = [-2,0]
                      elif event.key == K_RIGHT and oldSpeed[0] >= 0: speed = [2,0]
                      elif event.key == K_0:
                          going = False # 退出或重新开始游戏

              if dt > runSpeed: # 控制速度
                  oldSpeed = speed.copy()
                  dt = 0 # 初始化时间
                  endPop = s.move(snake,speed)
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
                  snake.append(endPop) # 吃果实
                  score += 1
                  if not f.get_foodpos(foodr,snake): going = False # # 生成 food 新位置

      if __name__ == '__main__':
          while True:
              main()
              if message_box():
                  break







              
     

    












