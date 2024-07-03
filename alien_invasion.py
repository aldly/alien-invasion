import sys
import threading
import time
from random import randint
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """管理游戏资源和行为"""

    def __init__(self):
        """初始化游戏，创建资源"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.clock1 = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1200, 800))  # 默认窗口大小
        self.settings = Settings(self)
        self._fullscreen()
        self.screen = self.settings.screen
        pygame.display.set_caption("AlienInvasion")
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)  # self指向当前实例AlienInvasion
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.game_active = False
        self._timer()
        self.play_button = Button(self, "Play")

    def _run_every_alien(self):
        while True:
            if self.game_active:
                self._creat_alien()
            # self._fire_bullet()
            time.sleep(1)

    def _run_every_bullet(self):
        while True:
            # self._creat_alien()
            if self.game_active:
                self._fire_bullet()
            time.sleep(0.1)

    def _timer(self):
        # 创建一个线程来运行定时任务
        timer_creat_alien = threading.Thread(target=self._run_every_alien)
        timer_fire_bullet = threading.Thread(target=self._run_every_bullet)
        # 设置为守护线程，这样当主程序退出时，定时器线程也会退出
        timer_creat_alien.daemon = True
        timer_fire_bullet.daemon = True
        timer_creat_alien.start()
        timer_fire_bullet.start()

    def run_game(self):
        """游戏主循环"""
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(120)

    def _fullscreen(self):
        # 判断是否全屏
        if self.settings.fullscreen:
            self.settings.Yfullscreenmode()
        else:
            self.settings.Ffullscreenmode()

    def _check_events(self):
        """检测键盘和鼠标"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """在玩家单击 Play 按钮时开始新游戏"""
        if self.play_button.rect.collidepoint(mouse_pos) and not self.game_active:
            self.stats.reset_stats()
            self.settings.initialize_dynamic_settings()
            self.stats.gold = 0
            self.game_active = True
            #         清空
            self.bullets.empty()
            self.aliens.empty()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            # self._fire_bullet()
            self.settings.keepfire = True

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_SPACE:
            # self._fire_bullet()
            self.settings.keepfire = False
        elif event.key == pygame.K_q:
            sys.exit()

    def _ship_hit(self):
        """响应飞船和外星人的碰撞"""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.ship.center_ship()
            time.sleep(0.5)
        else:
            pygame.mouse.set_visible(True)

            self.game_active = False

    def _fire_bullet(self):
        """创建一颗子弹， 并将其加入编组 bullets """
        if self.settings.keepfire:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹的位置并删除已消失的子弹"""
        # 更新子弹的位置
        self.bullets.update()
        # 删除已消失子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # 检查是否有子弹击中了外星人
        # 如果是， 就删除相应的子弹和外星人
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.gold += len(aliens)
                self.sb.check_high_score()
            self.sb.prep_score()

            if self.stats.gold >= self.settings.alien_points:
                self.settings.increase_speed()
                self.settings.alien_points *= 2

            # print(self.stats.gold)

    def _update_aliens(self):
        """更新外星舰队中所有外星人的位置"""
        # self._check_fleet_edges()
        self.aliens.update()
        hit_alien = pygame.sprite.spritecollideany(self.ship, self.aliens)
        if hit_alien:
            self._ship_hit()
            self.aliens.remove(hit_alien)
        # 删除已消失外星人
        for alien in self.aliens.copy():
            if alien.rect.top >= self.settings.screen_height:
                self.aliens.remove(alien)

    def _creat_alien(self):
        new_alien = Alien(self)
        new_alien.rect.x = randint(0, self.settings.screen_width)
        self.aliens.add(new_alien)

    def _update_screen(self):
        """更新屏幕上的图像， 并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.game_active:
            self.play_button.draw_button()
        # 显示最近绘制的屏幕
        pygame.display.flip()


if __name__ == '__main__':
    # 创建示例，运行游戏
    ai = AlienInvasion()
    ai.run_game()
