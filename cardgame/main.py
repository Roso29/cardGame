import random

class InsufficientMana(Exception):
    """Raised when the player tries to use more mana points than they have."""
    pass

class IllegalCard(Exception):
    """Raised when player attacks with a card they dont have"""
    pass

class InvalidUserInput(Exception):
    """Raise when user inputs a bad card choice string"""
    pass

class Player():
    def __init__(self):
        self.health = 30
        self.mana = 0
        self.deck = [0,0,1,1,2,2,2,3,3,3,3,4,4,4,5,5,6,6,7,8]
        self.hand = []
        self.MakeInitialHand()

    def __repr__(self):
        return self.name

    def SetName(self,name):
        self.name = name

    def IncrementMana(self):
        self.mana=min(self.mana+1,10)

    def DrawFromDeck(self):
        if len(self.deck)==0:
            return
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

    def IsDead(self):
        return self.GetHealth() <= 0

    def GetHealth(self):
        return self.health

    def HasEmptyDeck(self):
        return len(self.hand + self.deck) == 0

    def IsValidHand(self,cardIDS):
        isValid = all([id<len(self.GetHand()) for id in cardIDS])
        return isValid

    def HasPlayableHand(self):
        playableHand= any([cardMana<self.mana for cardMana in self.hand])
        return playableHand

    def Attack(self,cardIDS):
        if not self.IsValidHand(cardIDS):
            raise IllegalCard
        damage = sum([self.hand[cardID] for cardID in cardIDS])
        if damage>self.mana:
            raise InsufficientMana
        else:
            self.RemoveCardsFromHand(cardIDS)
            self.DrawFromDeck()
            return damage

    def RemoveCardsFromHand(self,cardIDS):
        for index in sorted(cardIDS, reverse=True):
            self.hand.pop(index)

class Game():
    def __init__(self):
        self.player1 = Player()
        self.player2 = Player()
        self.activePlayer = self.player1
        self.otherPlayer = self.player2
        self.gameOver = False

    def SwapPlayers(self):
        self.activePlayer, self.otherPlayer = self.otherPlayer, self.activePlayer

    def Step(self,cardIDS):
        if self.activePlayer.HasEmptyDeck():
            self.activePlayer.LoseHealth(1)
        else:
            try:
                damage = self.activePlayer.Attack(cardIDS)
                self.otherPlayer.LoseHealth(damage)
            except InsufficientMana:
                print(f"Insufficient mana available to {self.activePlayer}")
                return
        self.activePlayer.IncrementMana()
        if self.otherPlayer.IsDead():
            self.gameOver=True
            return
        self.SwapPlayers()

    def ValidateUserInput(self,rawInput):
        input = rawInput.rstrip()
        if input =='':
            return []
        inputList = input.split(' ')
        #Check if every item in list is a digit 
        validInput = all([id.isnumeric() for id in inputList])
        if not validInput:
            raise InvalidUserInput
        intList = [int(id)-1 for id in inputList]
        return intList

    def OutputGameState(self):
        print(f"{self.activePlayer} (active player)")
        print(f"Health: {self.activePlayer.GetHealth()}")
        print(f"Mana:   {self.activePlayer.mana}")
        print('-'*10)
        print(f"{self.otherPlayer}")
        print(f"Health: {self.otherPlayer.GetHealth()}")
        print(f"Mana:   {self.otherPlayer.mana}")
        print('\n'*2)
        print(f"{self.activePlayer} cards")
        print(' '.join(['('+str(i+1)+'):' + str(mana) for i,mana in enumerate(self.activePlayer.GetHand())]))

    def Loop(self):
        player1Name = input("Enter player 1 name: ")
        player2Name = input("Enter player 2 name: ")
        print('\n')
        self.player1.SetName(player1Name)
        self.player2.SetName(player2Name)
        while not self.gameOver:
            self.OutputGameState()
            choiceRaw = input()
            try:
                ValidatedInput = self.ValidateUserInput(choiceRaw)
            except InvalidUserInput:
                print("Invalid card choice...")
                continue
            self.Step(ValidatedInput)
            print("\n")
        print(f"Winner is {self.activePlayer}")
        print("Final game stats")
        self.OutputGameState


game = Game()
game.Loop()


'''
Game Loop

1. Starting player (attacking player) uses a legal mana card 
2. Other player gets damage dealt to them equal to mana amount
3. If other player health drops below zero, attacking player wins
4. Increment attacking player mana by 1 (up to ten)
5. Swap players and repeat


'''