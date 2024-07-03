import pygame


class Ship:
    """飞船管理"""

    def __init__(self, ai_game):
        """初始化，设置初始位置"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        #         加载飞船凸显，获取外接矩形
        self.image = pygame.image.load('images/战机1形态.bmp')
        self.rect = self.image.get_rect()
        # 放在屏幕底部中央
        self.rect.midbottom = self.screen_rect.midbottom
        # 在飞船的属性 x 中存储一个浮点数
        self.x = float(self.rect.x)
        #     移动标志
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """指定位置画飞船"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """根据标志调整飞船位置  """
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        #         根据 self.x 更新 rect 对象
        self.rect.x = self.x

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
