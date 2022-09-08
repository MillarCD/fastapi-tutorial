from .player import Player

class Game:
    def __init__(self):
        self.players: list[Player] = []

    def getPlayer(self, name: str):
        p = list( filter(lambda player: player.name==name, self.players) )
        if len(p) == 0:
            return None
        return p[0]

    def addPlayer(self, newPlayer: Player):
        if self.getPlayer(newPlayer.name):
            return False, self.getPlayer(newPlayer.name)
        self.players.append(newPlayer)
        return True, newPlayer

    def transfer(self, name_from: str, name_to: str, monto: int):
        player_1 = self.getPlayer(name_from)
        player_2 = self.getPlayer(name_to)

        if (not player_1.restMoney(monto)):
            return [ player_1 ]

        player_2.addMoney(monto)

        return [ player_1, player_2 ]

    def getPlayersNames(self):
        return list(map(lambda player: player.name, self.players))

