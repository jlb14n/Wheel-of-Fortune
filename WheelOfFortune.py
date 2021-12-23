#------------------------------------------------------------------------------------------------------------------------------------------
#imports
import random
#------------------------------------------------------------------------------------------------------------------------------------------
#Functions
def choose_words():
    word=[]
    word_list=open("words_alpha.txt").readlines()
    temp_his=set()
    for i in range(0,3): #Randomly choosing the 3 words that we'll use in this game
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
wheel=[600,500,300,500,800,550,400,300,900,500,300,900,"Bankrupt",600,400,300,"Lose A Turn",800,350,450,700,300,600,600]
final_prize=100000 #Stretch Goal: Change to be randomly chosen from a list
bank=[0,0,0] #Player 1, 2, 3 permanent bank
temp_bank=[0,0,0] #Player 1, 2, 3 round bank
guess_his=set()
active=random.randint(0,2) #Tracks the active player
word=choose_words() #This decides what the three words are going to be this game!
round=0 #Tracks round number
print("(To make it easier on the graders when they are testing the game)") #DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=
print(word) #DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=DELETEME=
#------------------------------------------------------------------------------------------------------------------------------------------
print("\nWelcome to Wheel of Fortune!")
while round<2:
    input("\nIt is currently Player {0}'s turn! (Enter to continue) ".format(active+1))
    display_word(word[round],guess_his)
    while True: #Player's Gameplay
        if y_n_input("Would you like to guess the word? (y/n): "): #Guess word
            guess=input("Guess the word: ").lower()
            if guess==word[round]: #Round ending!
                print("That is correct! The round is over!")
                bank[active]+=temp_bank[active] #Only the winner of the round gets to keep the money they earned during the round (as per the rules stated during standup 12/23/21)
                round+=1
                guess_his=set()
                temp_bank=[0,0,0]
                print("\nPlayer 1 has ${0}, Player 2 has ${1}, and Player 3 has ${2}".format(bank[0],bank[1],bank[2]))
                print("We will return for round {0} after THIS commercial break...\n".format(round+1))
                break
            else:
                print("That is not correct.")
                break
        else: #Spin wheel
            input("\nSPIN THE WHEEL!\n") 
            wheel_active=wheel[random.randint(0,len(wheel)-1)]
            print("The wheel landed on: {0}".format(wheel_active))
            if wheel_active=="Bankrupt":
                print("Oh No!")
                temp_bank[active]=0
                break
            elif wheel_active=="Lose A Turn":
                print("Tough luck!")
                break
            else: #Guess a consonant
                guess=consonant_input(guess_his)
                guess_his.add(guess)
                num_letters=letter_check(word[round],guess,guess_his)
                if num_letters!=0:
                    temp_bank[active]+=num_letters*wheel_active
                    display_word(word[round],guess_his)
                    while True: #Buy a vowel loop
                        print("You currently have ${0} (this round)!".format(temp_bank[active]))         
                        if vowels_left(word[round],guess_his):
                            if temp_bank[active]>=250:
                                if y_n_input("Would you like to buy a vowel? (y/n): "):
                                    temp_bank[active]-=250
                                    guess=vowel_input(guess_his)
                                    guess_his.add(guess)
                                    if letter_check(word[round],guess,guess_his)==0: #Do you lose your turn if there are no vowels, or just are unable to buy another vowel? I assumed the latter. Rubric/assignment unclear
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
    #Turn ended
    if active<2:
        active+=1
    else:
        active=0
else: #Final Round
    if len(set(bank))==len(bank): #There is no tie
        active=bank.index(max(bank))
    else: #There is a tie
        winners=[]
        for i in range(0,len(bank)):
            if bank[i]==max(bank):
                winners.append(i)
        active=random.choice(winners)
    print("\nWelcome to the Final Round!")
    input("Because they had the most money, it is Player {0}'s turn! (Enter to continue) ".format(active+1))
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
        print("That is correct! You won an additional...\n${0}!".format(final_prize))
        bank[active]+=final_prize
    else:
        print("That is not correct. You, unfortunately, missed out on ${0}".format(final_prize))
print("\nPlayer 1 ended with ${0}, Player 2 ended with ${1}, and Player 3 ended with ${2}".format(bank[0],bank[1],bank[2]))
print("Thanks for playing!")