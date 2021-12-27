#------------------------------------------------------------------------------------------------------------------------------------------
#file(s) needed: words_list.txt
#------------------------------------------------------------------------------------------------------------------------------------------
#imports
import random
#------------------------------------------------------------------------------------------------------------------------------------------
#Functions
def choose_words(filename,num_rounds):
    word=[]
    word_list=open(filename).readlines()
    temp_his=set()
    for i in range(0,num_rounds): #Randomly choosing the 3 words that we'll use in this game
        while True:
            temp=random.choice(word_list)
            if temp in temp_his:
                continue
            else:
                break
        temp_his.add(temp)
        temp=temp[:-1] #Removes the /n in word
        word.append(temp)
    return word
def display_word(word,guess_his):
    display=""
    for i in range(0,len(word)):
        if word[i] in guess_his:
            display+=word[i]+" "
        else:
            display+="_ "
    print(display)
def y_n_input(prompt):
    while True:
        y_n_input=input(prompt).upper()
        if y_n_input == "Y":
            return True
        elif y_n_input == "N":
            return False
        else:
            print("Error:\nInvalid Response")
def consonant_input(guess_his):
    consonant=("b","c","d","f","g","h","j","k","l","m","n","p","q","r","s","t","v","w","x","y","z")
    while True:
        guess=input("Guess a consonant: ").lower()
        if guess not in consonant:
            print("That is not a consonant...")
        elif guess in guess_his:
            print("You're lucky we're kind here in the studio! That letter has been guessed before; try again.")
        else:
            break
    return guess
def vowel_input(guess_his):
    vowel=("a","e","i","o","u")
    while True:
        guess=input("Guess a vowel?: ").lower()
        if guess not in vowel:
            print("That is not a vowel...")
        elif guess in guess_his:
            print("You're lucky we're kind here in the studio! That letter has been guessed before; try again.")
        else:
            break
    return guess
def letter_check(word,guess,guess_his):
    num_letters=0
    if guess in set(word):
        for i in range(0,len(word)):
            if guess==word[i]:
                num_letters+=1
    if num_letters==0:
        print("Sorry, there is no {0}.".format(guess.upper()))
    elif num_letters==1:
        print('There is {0} {1}!'.format(num_letters,guess.upper()))
    else:
        print('There are {0} {1}s!'.format(num_letters,guess.upper()))
    return num_letters
def vowels_left(word,guess_his):
    remainder=set(word)-guess_his
    vowel={"a","e","i","o","u"}
    return not remainder.isdisjoint(vowel)
#------------------------------------------------------------------------------------------------------------------------------------------
#Initialization
wheel=[600,500,300,500,800,550,400,300,900,500,300,900,"Bankrupt",600,400,300,"Lose A Turn",800,350,450,700,"Mystery",600,"One Million"]
final_prize=100000 #Stretch Goal: Change to be randomly chosen from a list
num_players=3
num_rounds=3 #Including the final round
min_round_prize=1000 #The minimum prize won in a round is $1000
round=0 #Tracks round number, starting from 0
guess_his=set()
player=[] #Player list of dictionaries
for i in range(0,num_players):
    player.append({"name":"", "bank":0, "round_bank":0, "round_prize":0, "prize":0})
active=random.randint(0,2) #Tracks the active player, randomizes who the first player will be
word=choose_words("words_list.txt",num_rounds) #This decides what the three words are going to be this game! Stretch Goal: Import in real prompts
#------------------------------------------------------------------------------------------------------------------------------------------
print("(To make it easier on the graders when they are testing the game)") #DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=
print(word) #DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=
#------------------------------------------------------------------------------------------------------------------------------------------
#The Game itself
print("\nWelcome to Wheel of Fortune!\n")
for i in  range(0,num_players): #Inputs player names
    player[i].update({"name":input("What is the name of Player {0}?: ".format(i+1))})
while round<num_rounds-1:
    if round>0: #Adding jackpot segment and replacing the mystery wedges after round 1
        wheel[22]=5000
        wheel[21]="Mystery"
    input("\nIt is currently {0}'s turn! (Enter to continue) ".format(player[active]["name"]))
    display_word(word[round],guess_his)
    while True: #Player's Turn
        #Guess Word
        if y_n_input("Would you like to guess the word? (y/n): "):
            guess=input("Guess the word: ").lower()
            if guess==word[round]: #Round ending!
                print("That is correct! The round is over!\n")
                if player[active]["round_bank"]>min_round_prize:
                    player[active]["bank"]+=player[active]["round_bank"]
                else:
                    player[active]["bank"]+=min_round_prize #Minimum price won is $1000
                player[active]["prize"]+=player[active]["round_prize"]
                round+=1
                guess_his=set()
                for i in range(0,num_players):
                    player[i].update({"round_bank":0, "round_prize":0})
                    print("{0} has ${1} (with ${2} in prizes)!".format(player[i]["name"],player[i]["bank"],player[i]["prize"]))
                print("\nWe will return for round {0} after THIS commercial break...\n".format(round+1))
                break
            else:
                print("That is not correct.")
                break
        #Spin Wheel
        else: 
            input("\nSPIN THE WHEEL!\n") #This is to give a better user experience to enter something to spin the wheel.
            wheel_active=wheel[random.randint(0,len(wheel)-1)]
            if wheel_active=="One Million": #Changes the "One Million" wedge into a one-third change of landing on Bankrupt
                if random.randint(0,2)!=1:
                    wheel_active="Bankrupt"
            print("The wheel landed on: {0}".format(wheel_active))
            if wheel_active=="Bankrupt":
                print("Oh No!")
                player[active].update({"round_bank":0,"round_prize":0})
                break
            elif wheel_active=="Lose A Turn":
                print("Tough luck!")
                break
            else: #Guess a consonant
                guess=consonant_input(guess_his)
                guess_his.add(guess)
                num_letters=letter_check(word[round],guess,guess_his)
                if num_letters!=0:
                    if wheel_active=="One Million":
                        player[active].update({"round_prize":1000000})
                    elif wheel_active=="Mystery": #It seems like they only get to go bankrupt or get the cash prize after they guess a letter correct.
                        if y_n_input("Would you like to take the 50/50 for $10,000 instead of $1000 per letter? (y/n): "):
                            if random.randint(0,1)==0:
                                print("It's $10,000!")
                                player[active]["round_bank"]+=10000 #Not sure if they can use this money to buy vowels or not... assuming they can for now
                            else:
                                print("It's Bankrupt!")
                                player[active].update({"round_bank":0,"round_prize":0})
                                break
                            wheel[21]=600 #Now that the mystery wedge has been picked up, it is replaced with a $600 wedge
                        else:
                            player[active]["round_bank"]+=num_letters*1000
                    elif wheel_active>=5000: #If they hit the jackpot!
                        player[active]["round_bank"]+=wheel_active
                    else:
                        player[active]["round_bank"]+=num_letters*wheel_active
                    display_word(word[round],guess_his)
                    while True: #Buy a vowel loop
                        print("You currently have ${0} this round (with ${1} in prizes)!".format(player[active]["round_bank"],player[active]["round_prize"]))         
                        if vowels_left(word[round],guess_his):
                            if player[active]["round_bank"]>=250:
                                if y_n_input("Would you like to buy a vowel? (y/n): "):
                                    player[active]["round_bank"]-=250
                                    guess=vowel_input(guess_his)
                                    guess_his.add(guess)
                                    if letter_check(word[round],guess,guess_his)==0: #Do you lose your turn if there are no vowels, or just are unable to buy another vowel without spinning again? I assumed the latter. Rubric/assignment unclear
                                        break
                                    else:
                                        display_word(word[round],guess_his)   
                                else:
                                    break
                            else:
                                break
                        else:
                            print("There are no vowels remaining!")
                            break
                else:
                    break
    #Player Turn ended
    if active<2:
        active+=1 
    else:
        active=0
else: #Final Round
    print("\nWelcome to the Final Round!")  

    #Determine Final Player
    max_bank=0
    top_players=[]
    for i in range(0,len(player)):
        if player[i]["bank"]>max_bank:
            max_bank=player[i]["bank"]
            tie=False
            top_players.clear()
            top_players.append(i)
        elif player[i]["bank"]==max_bank:
            tie=True
            top_players.append(i)
    if tie:
        active=random.choice(top_players)
        input("Because they tied for the most money (and were more fortunate), it is {0}'s turn! (Enter to continue) ".format(player[active]["name"]))
    else:
        active=top_players[0]
        input("Because they had the most money, it is {0}'s turn! (Enter to continue) ".format(player[active]["name"]))

    #Final Round Mechanics
    display_word(word[round],guess_his)
    print("\nAnd R, S, T, L, N, E")
    guess_his.update('r','s','t','l','n','e')
    display_word(word[round],guess_his)
    print('\nAnd we now need 3 consonants and 1 vowel from you:')
    guess_his.add(consonant_input(guess_his))
    guess_his.add(consonant_input(guess_his))
    guess_his.add(consonant_input(guess_his))
    guess_his.add(vowel_input(guess_his))
    display_word(word[round],guess_his)
    guess=input("You get one guess!: ").lower()
    if guess==word[round]:
        print("That is correct! You won an additional...\n${0}!\n".format(final_prize))
        player[active]["bank"]+=final_prize
    else:
        print("That is not correct. You, unfortunately, missed out on ${0}.\n".format(final_prize))
    player[active]["bank"]+=player[active]["prize"] #If they got the million dollar wedge and finished "as a champion". I'm not sure if that means they had to get the final round correct or not... if so, this should be 0within the previous if statement instead
for i in range(0,num_players):
    print("{0} has ended with ${1}".format(player[i]["name"],player[i]["bank"]))
print("Thanks for playing!")