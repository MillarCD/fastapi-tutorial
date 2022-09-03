from player import Player
from game import Game

def main():
    name1 = 'diego'
    name2 = 'juanito'

    print('--> create players')
    player1 = Player(name1)
    player2 = Player(name2)

    print(player1)
    print()

    print('--> add money')
    player1.addMoney(1000)
    print('money: ',player1.money)
    
    print('--> rest money')
    res = player1.restMoney(500)
    print('res(true): ',res)
    res = player1.restMoney(500)

    res = player2.restMoney(500)
    print('res(false): ',res)
    

    print('--> create game')
    game = Game(123)
    print('id: ',game.id_)

    print('--> add players')
    game.addPlayer(player1)
    game.addPlayer(player2)

    for i in game.players:
        print('playername: ', i.name)

    print('--> give money')
    game.giveMoney(name1, 2100)
    game.giveMoney(name2, 1500)

    print('money player1(2100): ', player1.money)

    print('--> transfer money')
    res = game.transfer(name1, name2, 123)
    print('res(true): ',res)
    res = game.transfer(name1, name2, 12300)
    print('res(false): ',res)
    

    print('money player1(1977): ', player1.money)
    print('money player2(1623(: ', player2.money)




if __name__=='__main__':
    main()
