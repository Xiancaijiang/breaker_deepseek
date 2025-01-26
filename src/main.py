import pygame, sys
from pygame.locals import *
from game import *
from const import *

def show_start_screen(surface):
    font = pygame.font.Font(None, 74)
    text = font.render('Press SPACE to Start', True, (0, 0, 0))
    text_rect = text.get_rect(center=(GAME_SIZE[0]/2, GAME_SIZE[1]/2))
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return
        
        surface.fill((255, 255, 255))
        surface.blit(text, text_rect)
        pygame.display.update()

def main():
    pygame.init()
    # 初始化音效系统，设置适当音量
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.5)
    
    DISPLAYSURF = pygame.display.set_mode(GAME_SIZE)
    pygame.display.set_caption('Breaker')
    
    # 加载字体
    font = pygame.font.Font(None, 36)
    
    # Show start screen
    show_start_screen(DISPLAYSURF)
    
    # Initialize game
    game = Game(DISPLAYSURF)
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        game.update()
        DISPLAYSURF.fill((255, 255, 255))
        game.draw()
        
        # 显示关卡信息
        level_text = font.render(f'Level: {game.level.level}', True, (0, 0, 0))
        DISPLAYSURF.blit(level_text, (10, 10))
        
        # 处理R键重启
        keys = pygame.key.get_pressed()
        if keys[K_r] and game.isGameOver:
            game.Load(1)
            
        pygame.display.update()

if __name__ == '__main__':
    main()
