import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """表示单个外星人的类"""

    def __init__(self, ai_game):
        """初始化外星人并设置其起始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # 加载外星人图像并设置其 rect 属性
        self.image = pygame.image.load('images/敌人1.bmp')
        self.rect = self.image.get_rect()
        self.rect.y = -1 * self.rect.height
        # 每个外星人最初都在屏幕的左上角附近
        # self.rect.x = self.rect.width
        # self.rect.y = self.rect.height
        # 存储外星人的精确水平位置
        self.y = float(self.rect.y)

    def update(self):
        """向下移动外星人"""
        if self.y <= self.settings.screen_height:
            self.y += self.settings.alien_speed
            self.rect.y = self.y
