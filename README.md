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
* 代码如下 

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

          gr = get_nextRect(gr,direct,edge) # 生成新的坐标位置
          screen.fill(screenColor) # 添加屏幕颜色
          screen.blit(grid, gr) # 将格子画到 gr 的位置 
          pygame.display.flip() # 使我们刚刚画到屏幕上的 格子 可见
      pygame.quit() # 退出游戏
这就完成了控制方块移动的功能。
### 画格子、显示字体内容
* 
 
 

      


