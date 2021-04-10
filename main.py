import random

count = 0
bankroll = 0

######################################
#returns an integer with ceiling of 10
#param x: integer to take ceiling of
######################################
def ceiling_10(x) :
    if x > 10 or x == 0:
        return 10
    else : 
        return x

######################################
#returns a randomly shuffled shoe of 8
#playing card decks(466 cards) value
#only
######################################
def generate_shoe() :
    temp = []
    for y in range(0, 7) :
        for x in range(1, 52) :
            temp.append(ceiling_10(x % 13)) 

    random.shuffle(temp)
    return temp

#######################################
#determines if the banker should hit,
#given the player and bankers current
#number
#Param: player - players card value
#Param: banker - bankers card value
########################################
def should_banker_hit(player, banker) :      #banker value
    chart = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], #0
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], #1
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], #2
             [1, 1, 1, 1, 1, 1, 1, 1, 0, 1], #3
             [0, 0, 1, 1, 1, 1, 1, 1, 0, 0], #4
             [0, 0, 0, 0, 1, 1, 1, 1, 0, 0], #5
             [0, 0, 0, 0, 0, 0, 1, 1, 0, 0]] #6... 
#player val   0, 1, 2, 3, 4, 5, 6, 7, 8, 9

    if banker % 10 > 6 :
        return False
    return chart[banker % 10][player % 10] == 1

#############################################
#pop card from shoe, and adjust count based
#on value
#############################################
def pop_and_count(shoe) :
    global count
    card = shoe.pop()
    if card <= 4 :
        count += 1
    elif card <= 8 :
        count -= 1
    
    return card

#############################################
#runs a specified number of baccarat hand
#simulations 
#Param: num_sims - number of simulations to run
#Param: banker_commission - % value of bankers 
#                                   commission
##############################################
def run_sims(num_sims, banker_commission) :
    global count
    global bankroll

    shoe = generate_shoe()
    PLAYER_WINS = 0
    BANKER_WINS = 0
    TIES = 0

    count = 0
    bankroll = 0
    gambler_bet_banker = True

    for n in range(0, num_sims) :
        if len(shoe) < 233 : 
            shoe = generate_shoe()
            count = 0

        #deal two cards each to player and banker
        player = pop_and_count(shoe) + pop_and_count(shoe)
        banker = pop_and_count(shoe) + pop_and_count(shoe)
        player_hit = 0

        if player % 10 < 6 : # if player has less than 6 player hits
            player_hit = pop_and_count(shoe)
            player += player_hit
        elif banker % 10 < 6 : # if player does not hit and banker has less than 6 banker hits
            banker += pop_and_count(shoe)

        if player_hit != 0 and should_banker_hit(player, banker) : # if player hits, banker may or may not hit based on ez bac rules
            banker += pop_and_count(shoe)
    
        if player % 10 > banker % 10 :
            PLAYER_WINS += 1
            bankroll += 1 if not gambler_bet_banker else -1
        elif banker % 10 > player % 10 :
            BANKER_WINS += 1
            bankroll += 1 if gambler_bet_banker else -1
        else :
            TIES += 1

        gambler_bet_banker = count > 4

    return (PLAYER_WINS, BANKER_WINS, TIES)

def main() :
    global count
    global bankroll
    while True : 
        num_sims = int(input("number of simulations to run: "))
        while num_sims <= 0 :
            num_sims = input("please input number of simulations > 0: ")

        banker_commission = int(input("house commission for banker win (%): "))
        while banker_commission < 0 :
            banker_commision = input("please input banker commission >= 0 (%): ")

        results = run_sims(num_sims, banker_commission)

        print("Banker Wins: ", results[1])
        print("Player Wins: ", results[0])
        print("Ties: ", results[2])
        print("Count: ", count)
        print("Bankroll with card counting: ", bankroll)

if __name__ == "__main__":
    main()