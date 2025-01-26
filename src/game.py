import pygame
from pygame.locals import *
from const import *
from player import *
from ball import *
from level import *
from block import *

class Game(object):
    def __init__(self, surface):
        pygame.mixer.init()
        self.surface = surface
        self.Load(1)
        self.isGameStart = True
    
    def Load(self, lv):
        self.level = Level(lv)
        self.isGameOver = False
        self.balls = []
        self.loadPlayer()
        self.loadBlockImages()
        self.initialBallDirection = 0
    
    def loadPlayer(self):
        self.player = Player(
            PLAYER_RES, 
            (GAME_SIZE[0] - PLAYER_SIZE_W)/2, GAME_SIZE[1] - PLAYER_SIZE_H, 
            SPRITE_SIZE_W, GAME_SIZE[0] - PLAYER_SIZE_W - SPRITE_SIZE_W)
    
    def loadOneBall(self, x, y, dirX, dirY):
        ball = Ball(BALL_RES, x, y, dirX, dirY)
        ball.SetSpeed(0.5)
        self.balls.append(ball)

    def loadBlockImages(self):
        self.blocks = []
        for block in self.level.GetBlocks():
            sp = Block(block[2], block[0], block[1], (0, 0))
            self.blocks.append(sp)
    
    def update(self):
        if self.isGameOver:
            keys = pygame.key.get_pressed()
            if keys[K_SPACE]:
                self.Load(1)
                self.isGameOver = False
            return
            
        keys = pygame.key.get_pressed()
        if self.initialBallDirection == 0:
            if keys[K_LEFT]:
                self.initialBallDirection = -1
                self.loadOneBall(self.player.GetRect().x, self.player.GetRect().y - SPRITE_SIZE_H - 5, -0.5, -0.5)
            elif keys[K_RIGHT]:
                self.initialBallDirection = 1
                self.loadOneBall(self.player.GetRect().x, self.player.GetRect().y - SPRITE_SIZE_H - 5, 0.5, -0.5)
            return
                
        self.player.update()
        [ball.update() for ball in self.balls]
        self.checkCollide()
        if self.isGameWin():
            if self.level.level < MAX_LEVEL:
                self.showWinMessage()
                self.Load(self.level.level + 1)
            else:
                self.showGameComplete()
                self.isGameOver = True

    def draw(self):
        if self.isGameOver:
            gameOverImg = pygame.image.load(GAME_OVER_RES)
            gameOverImg = pygame.transform.scale(gameOverImg, GAME_SIZE)
            self.surface.blit(gameOverImg, (0, 0))
            
            font = pygame.font.SysFont("simhei", 36)
            text = font.render("按空格键重新开始", True, (255, 255, 255))
            text_rect = text.get_rect(center=(GAME_SIZE[0]/2, GAME_SIZE[1] - 50))
            self.surface.blit(text, text_rect)
            return 
            
        self.player.draw(self.surface)
        [block.draw(self.surface) for block in self.blocks]
        [ball.draw(self.surface) for ball in self.balls]

    def showWinMessage(self):
        start_time = pygame.time.get_ticks()
        player_img = pygame.image.load(PLAYER_RES[0])
        player_img = pygame.transform.scale(player_img, (SPRITE_SIZE_W * 2, SPRITE_SIZE_H * 2))
        x = 0
        direction = 1
        
        while pygame.time.get_ticks() - start_time < 2000:
            self.surface.fill((0, 0, 0))
            
            # 绘制移动的玩家图片
            x += direction * 2
            if x > GAME_SIZE[0] - SPRITE_SIZE_W or x < 0:
                direction *= -1
            self.surface.blit(player_img, (x, GAME_SIZE[1]/2 - SPRITE_SIZE_H/2))
            
            # 绘制文字
            font = pygame.font.SysFont("simhei", 48)
            text = font.render("恭喜过关！", True, (255, 255, 0))
            text_rect = text.get_rect(center=(GAME_SIZE[0]/2, GAME_SIZE[1]/2 - 100))
            self.surface.blit(text, text_rect)
            
            font = pygame.font.SysFont("simhei", 36)
            text = font.render(f"即将进入第 {self.level.level + 1} 关", True, (255, 255, 255))
            text_rect = text.get_rect(center=(GAME_SIZE[0]/2, GAME_SIZE[1]/2 + 60))
            self.surface.blit(text, text_rect)
            
            pygame.display.update()

    def showGameComplete(self):
        self.surface.fill((0, 0, 0))
        
        font = pygame.font.SysFont("simhei", 48)
        text = font.render("游戏通关！", True, (255, 255, 0))
        text_rect = text.get_rect(center=(GAME_SIZE[0]/2, GAME_SIZE[1]/2 - 50))
        self.surface.blit(text, text_rect)
        
        font = pygame.font.SysFont("simhei", 36)
        text = font.render("按空格键从第一关重新开始", True, (255, 255, 255))
        text_rect = text.get_rect(center=(GAME_SIZE[0]/2, GAME_SIZE[1]/2 + 50))
        self.surface.blit(text, text_rect)
        
        pygame.display.update()
        pygame.time.wait(2000)

    def checkBallBlockCollide(self):
        for ball in self.balls:
            for block in self.blocks:
                if ball.GetRect().colliderect(block.GetRect()):
                    ball.changeDirection(block.GetRect())
                    self.processBlock(ball, block)
                    break

    def processBlock(self, ball, block):
        if block.GetBlockType() == BlockType.COPY:
            self.copyBalls()
        if block.GetBlockType() == BlockType.SPEED_UP:
            ball.SetSpeed(1.0)
        if block.GetBlockType() == BlockType.SPEED_DOWN:
            ball.SetSpeed(0.3)
        if block.GetBlockType() == BlockType.WALL:
            return
        self.blocks.remove(block)
 
    def checkBallPlayerCollide(self):
        for ball in self.balls:
            if ball.GetRect().colliderect(self.player.GetRect()):
                ball.changeYDirection(self.player.GetRect())
                break

    def checkCollide(self):
        self.checkBallBlockCollide()
        self.checkBallPlayerCollide()

        flag = True
        while flag:
            flag = False
            for ball in self.balls:
                if ball.GetRect().y > GAME_SIZE[1]:
                    self.balls.remove(ball)
                    flag = True
                    break
        if len(self.balls) == 0:
            self.isGameOver = True
    
    def copyBalls(self):
        balls = [ball for ball in self.balls]
        for ball in balls:
            self.loadOneBall(ball.GetRect().x, ball.GetRect().y, 0.5, -0.5)
 
    def isGameWin(self):
        for block in self.blocks:
            if block.GetBlockType() != BlockType.WALL:
                return False
        return True