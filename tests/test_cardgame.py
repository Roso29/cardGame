from cardgame.main import *

#Tests assume that the random shuffle of the deck uses seed: 0.

def test_player_lose_health():
    player1 = Player()
    player1.LoseHealth(10)
    assert player1.GetHealth() == 30-10

def test_set_up_deck():
    player1 = Player()
    assert len(player1.hand)+len(player1.deck) == 20

def test_player_draw_card():
    player1 = Player()
    player1.mana = 100
    numOfCards = len(player1.GetHand())
    player1.DrawFromDeck()
    newNumOfCards = len(player1.GetHand())
    assert newNumOfCards-numOfCards == 1

def test_overload_card():
    player1 = Player()
    player1.mana = 100
    numOfCards = len(player1.GetHand())
    player1.DrawFromDeck()
    player1.DrawFromDeck()
    player1.DrawFromDeck()
    newNumOfCards = len(player1.GetHand())
    assert newNumOfCards==5

def test_use_card():
    player1 = Player()
    player1.mana = 100
    numOfCards = len(player1.GetHand())
    player1.RemoveCardsFromHand(cardIDS=[0,1])
    newNumOfCards = len(player1.GetHand())
    assert numOfCards-newNumOfCards == 2

def test_damage_from_cards():
    player1 = Player()
    player1.mana = 100
    damage = player1.Attack([0,1])
    assert damage == 10

def test_player_receiving_damage():
    game = Game()
    game.player1.mana = 100
    player2Health = game.player2.GetHealth()
    game.Attack([0])
    assert player2Health - game.player2.GetHealth() == 3

def test_player_not_enough_mana():
    player1 = Player()
    player1.mana = 8
    try:
        player1.Attack([0,1])
        assert False
    except InsufficientMana:
        assert True

def test_player_attack_player():
    game = Game()
    game.player1.mana = 10
    startingHealth = game.player2.GetHealth()
    game.Attack([0,1])
    finishingHealth = game.player2.GetHealth()
    assert startingHealth-finishingHealth == 10

def test_player_call_isDead_health_drop_below_zero():
    player = Player()
    player.LoseHealth(32)
    isDead = player.IsDead()
    assert isDead == True

def test_player_call_isDead_health_drop_above_zero():
    player = Player()
    player.LoseHealth(29)
    isDead = player.IsDead()
    assert isDead == False

def test_increment_mana_below_ten():
    player = Player()
    player.mana = 5
    player.IncrementMana()
    assert player.mana == 6

def test_increment_mana_above_ten():
    player = Player()
    player.mana = 10
    player.IncrementMana()
    assert player.mana == 10

def test_IsValid_with_valid_deck():
    player=Player()
    cardIDs = [0,1,2]
    isValidHand = player.IsValidHand(cardIDs)
    assert isValidHand==True

def test_IsValid_with_invalid_deck():
    player=Player()
    cardIDs = [0,1,4]
    isValidHand = player.IsValidHand(cardIDs)
    assert isValidHand==False

def test_player_attack_with_out_of_bounds_card():
    player = Player()
    try:
        player.Attack([3])
        assert False
    except IllegalCard:
        assert True

def test_player_attack_with_legal_card():
    player = Player()
    player.mana = 10
    try:
        player.Attack([2])
        assert True
    except IllegalCard:
        assert False

def test_no_playable_cards():
    player = Player()
    player.mana = 2
    canPlayCard = player.HasPlayableHand()
    assert canPlayCard == False

def test_has_playable_cards():
    player = Player()
    player.mana = 10
    canPlayCard = player.HasPlayableHand()
    assert canPlayCard == True

def test_user_enters_invalid_input():
    game = Game()
    try:
        game.ValidateUserInput('0 1 2 a')
        assert False
    except InvalidUserInput:
        assert True

def test_user_enters_valid_input():
    game = Game()
    try:
        game.ValidateUserInput('0 1 2 4')
        assert True
    except InvalidUserInput:
        assert False
#Shuffled Deck
#[3, 7, 6, 5, 0, 6, 4, 1, 1, 3, 2, 3, 2, 8, 2, 5, 3, 0, 4, 4]
