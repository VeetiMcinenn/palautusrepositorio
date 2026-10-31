import unittest
from statistics_service import StatisticsService, SortBy
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        self.stats = StatisticsService(PlayerReaderStub())

    def test_search_finds_existing_player(self):
        player = self.stats.search("Kurri")

        self.assertEqual(player.name, "Kurri")
        self.assertEqual(player.team, "EDM")
        self.assertEqual(player.points, 90)

    def test_search_returns_none_for_missing_player(self):
        self.assertIsNone(self.stats.search("Selanne"))

    def test_team_returns_players_of_team(self):
        names = [player.name for player in self.stats.team("EDM")]

        self.assertEqual(names, ["Semenko", "Kurri", "Gretzky"])

    def test_team_returns_empty_list_for_unknown_team(self):
        self.assertEqual(self.stats.team("PHI"), [])

    def test_top_returns_players_in_order_of_points(self):
        names = [player.name for player in self.stats.top(2)]

        self.assertEqual(names[:3], ["Gretzky", "Lemieux", "Yzerman"])

    def test_top_by_points_explicitly(self):
        names = [player.name for player in self.stats.top(2, SortBy.POINTS)]

        self.assertEqual(names[:3], ["Gretzky", "Lemieux", "Yzerman"])

    def test_top_by_goals(self):
        names = [player.name for player in self.stats.top(2, SortBy.GOALS)]

        self.assertEqual(names[:3], ["Lemieux", "Yzerman", "Kurri"])

    def test_top_by_assists(self):
        names = [player.name for player in self.stats.top(2, SortBy.ASSISTS)]

        self.assertEqual(names[:3], ["Gretzky", "Yzerman", "Lemieux"])
