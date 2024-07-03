import pygame


class Settings:
    """设置选项内容"""

    def __init__(self, alien_game):
        """初始化游戏设置"""
        self.screen = alien_game.screen
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.fullscreen = False
        self.ship_speed = 12
        self._bulletset()
        self.alien_speed = 2
        self.ship_limit = 3
        self.speedup_scale = 1.3
        self.bulletup_scale = 1.3
        self.alienup_scale = 1.3

    def Yfullscreenmode(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width = self.screen.get_rect().width
        self.screen_height = self.screen.get_rect().height

    def Ffullscreenmode(self):
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

    def _bulletset(self):
        self.bullet_speed = 7
        self.bullet_width = 10
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 10
        self.keepfire = False

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed = 12
        self.alien_speed = 2
        self.bullet_speed = 7
        self.alien_points = 20

    def increase_speed(self):
        """提高速度设置的值"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.bulletup_scale
        self.alien_speed *= self.alienup_scale
