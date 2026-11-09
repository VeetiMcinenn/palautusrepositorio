class PlayerStats:
    def __init__(self, reader):
        self.reader = reader

    def top_goal_scorers(self, how_many):
        players = sorted(
            self.reader.get_players(),
            key=lambda player: player.goals,
            reverse=True
        )

        return players[:how_many]

    def top_scorers_by_nationality(self, nationality):
        players = [
            player for player in self.reader.get_players()
            if player.nationality == nationality
        ]

        return sorted(players, key=lambda player: player.points, reverse=True)
