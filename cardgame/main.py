import random

class InsufficientMana(Exception):
    """Raised when the player tries to use more mana points than they have."""
    pass

class Player():
    def __init__(self):
        self.health = 30
        self.mana = 0
        self.deck = [0,0,1,1,2,2,2,3,3,3,3,4,4,4,5,5,6,6,7,8]
        self.hand = []
        self.MakeInitialHand()

    def IncrementMana(self):
        self.mana=max(self.mana+1,10)

    def DrawFromDeck(self):
        drawnCard = self.deck.pop()
        if len(self.hand) < 5:
            self.hand.append(drawnCard)

    def MakeInitialHand(self):
        random.seed(0)
        random.shuffle(self.deck)
        self.hand = self.deck[:3]
        self.deck = self.deck[3:]

    def GetHand(self):
        return self.hand

    def LoseHealth(self,hitPoints):
        self.health-=hitPoints

    def GetHealth(self):
        return self.health

    def HasEmptyDeck(self):
        return len(self.hand + self.deck) == 0


    def Attack(self,cardIDS):
        damage = sum([self.hand[cardID] for cardID in cardIDS])
        if damage>self.mana:
            raise InsufficientMana
        else:
            self.RemoveCardsFromDeck(cardIDS)
            return damage

    def RemoveCardsFromDeck(self,cardIDS):
        for index in sorted(cardIDS, reverse=True):
            del self.hand[index]

class Game():
    def __init__(self):
        self.player1 = Player()
        self.player2 = Player()
        self.activePlayer = self.player1
        self.otherPlayer = self.player2

    def Attack(self,cardIDS):
        damage = self.activePlayer.Attack(cardIDS)
        self.otherPlayer.LoseHealth(damage)


    def SwapPlayers(self):
        self.activePlayer, self.otherPlayer = self.otherPlayer, self.activePlayer

    def Step(self,cardIDS):
        if self.activePlayer.HasEmptyDeck():
            self.activePlayer.LoseHealth(1)
        else:
            self.Attack(cardIDS)

        self.SwapPlayers()
