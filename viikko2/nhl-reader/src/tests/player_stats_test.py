import unittest
from player_stats import PlayerStats
from player import Player

def create_player(name, team, goals, assists, nationality):
    return Player({
        "name": name,
        "team": team,
        "goals": goals,
        "assists": assists,
        "nationality": nationality
    })

class PlayerReaderStub:
    def get_players(self):
        return [
            create_player("Semenko", "EDM", 4, 12, "CAN"),  #  4+12 = 16
            create_player("Lemieux", "PIT", 45, 54, "CAN"), # 45+54 = 99
            create_player("Kurri",   "EDM", 37, 53, "FIN"), # 37+53 = 90
            create_player("Selanne", "WPG", 40, 20, "FIN"), # 40+20 = 60
            create_player("Gretzky", "EDM", 35, 89, "CAN")  # 35+89 = 124
        ]

class TestPlayerStats(unittest.TestCase):
    def setUp(self):
        self.stats = PlayerStats(PlayerReaderStub())

    def test_top_goal_scorers_returns_players_in_order_of_goals(self):
        names = [player.name for player in self.stats.top_goal_scorers(3)]

        self.assertEqual(names, ["Lemieux", "Selanne", "Kurri"])

    def test_top_goal_scorers_returns_all_players_if_how_many_is_too_large(self):
        self.assertEqual(len(self.stats.top_goal_scorers(10)), 5)

    def test_top_goal_scorers_returns_empty_list_for_zero(self):
        self.assertEqual(self.stats.top_goal_scorers(0), [])

    def test_top_scorers_by_nationality_returns_only_given_nationality(self):
        players = self.stats.top_scorers_by_nationality("FIN")

        self.assertEqual({player.nationality for player in players}, {"FIN"})
        self.assertEqual(len(players), 2)

    def test_top_scorers_by_nationality_returns_players_in_order_of_points(self):
        names = [player.name for player in self.stats.top_scorers_by_nationality("CAN")]

        self.assertEqual(names, ["Gretzky", "Lemieux", "Semenko"])

    def test_top_scorers_by_nationality_returns_empty_list_for_unknown_nationality(self):
        self.assertEqual(self.stats.top_scorers_by_nationality("SWE"), [])
