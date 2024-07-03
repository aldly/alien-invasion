class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.gold = 0
        self.high_score = 5

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
