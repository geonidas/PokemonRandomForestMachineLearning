# Group Members:
    # Natalie Downing
    # John Flores
    # Ellis Johnson
    # Giovanni Mueco

# Imported Libraries
import ast
import numpy
import pandas
from prettytable import PrettyTable
import random
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
import sys
import time

# -------------------------------------------------------------------------------- Introduction --------------------------------------------------------------------------------
# A balanced team of Pokemon is essential when battling trainers in the world of Pokemon. Having a balanced team of Pokemon ensures that the members of the team can be effective 
# against each others' weaknesses, be a good combination of offense and defense, and have supporting diverse attributes such as stats and moves. The purpose of our project is to 
# create a Machine Learning Model that can create a balanced team of Pokemon.
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# interaction functions ------------------------------------------------------------------
# The purpose of the following function is to ask the user for their choice of pokemon
def choose_your_pokemon(user_options):
    print("\nChoose your fighter from the following list!\n")

    # While loop that continues until the user has selected a pokemon or decided to exit
    while(True):
        print("* * * * * * * * * * * * * * * * * * * * * * * *\n")

        # iterate through the dictionary of options and display the options
        for choice in user_options.keys(): 
            print("""\t\t{0}. {1}\t""".format(list(user_options.keys()).index(choice)+1, choice))
        print("\n* * * * * * * * * * * * * * * * * * * * * * * *")

        # receive input from the user
        your_pokemon = input("\nEnter the name of your fighter: ")

        # capitalize the input given so that, if it is valid input, it matches the dictionary key
        your_pokemon = your_pokemon.title()

        # if the input exists in the list of keys, the input is valid so the function will be exited.
        if your_pokemon in user_options.keys():
            break
        
        # if the input is invalid, ask user if they would like to input again or not
        # question to send to yes_or_no function
        question = your_pokemon + " is not a valid selection. Would you like to try again? [Yes, No] "

        # ask user if they want to continue or not
        yes_or_no(question)

    # display chosen pokemon
    print("You have chosen " + your_pokemon)

    # return chosen pokemon
    return your_pokemon

# The purpose of this function is to determine if the user wants try entering a valid input
# after giving an invalid input
def yes_or_no(question):
    # ask user for input
    answer = input(question)

    # while input being determined, continue
    while(True):
        if answer.lower() == "yes":
            return
        elif answer.lower() == "no":
            sys.exit("Terminating program!")
        else:
            answer = input(question)

# battle functions ------------------------------------------------------------------
# The purpose of this function is to simulate a pokemon battle
def battle_simulator(your_pokemon, mystery_pokemon):

    # comment these out for testing so it doesnt take long
    # below is to add animation to the program
    # print("...")
    # time.sleep(1)
    # print("......")
    # time.sleep(1)
    # print("A wild pokemon appears!")
    # time.sleep(1)
    # print("But who's that pokemon?!\n")
    # time.sleep(1)
    # print(your_pokemon["Name"] + " go, let the battle begin!")
    # time.sleep(1)

    while(True):
        print("Your Pokemon : " + your_pokemon["Name"])
        print("Your Pokemon's HP(Health): " + str(your_pokemon["HP"]))
        #time.sleep(1)
        print()
        print("Mystery Pokemon : ?")
        print("Mystery Pokemon's HP(Health): " + str(mystery_pokemon["HP"]))
        print()

        # obtain a random move from the user's pokemon and the mystery pokemon
            # the random move will be obtained using the select_random() function
        opponent_move_name, opponent_move = select_random(mystery_pokemon["Moves"])
        your_move_name, your_move = select_random(your_pokemon["Moves"])

        # obtain your pokemon's HP, PP and Power
        your_HP, your_move_PP, your_move_Power = obtain_battle_stats(your_move_name, your_move, your_pokemon)

        # to record your pokemon's damage taken
        your_damage_taken = 0

        
        # obtain Mystery pokemon's HP, PP and Power
        opponent_HP, opponent_move_PP, opponent_move_Power = obtain_battle_stats(opponent_move_name, opponent_move, mystery_pokemon)

        # to record mystery pokemon's damage taken
        opponent_damage_taken = 0

        # boolean to determine whose turn it is
        your_turn = random.choice([True, False])

        # boolean to determine who won the battle
        you_win = False

        if (your_turn):
            print(your_pokemon["Name"] + " will go first!")
        else:
            print("? will go first!")

        # calculate damage taken
        while(True):
            # when it is your/user's turn
            if(your_turn):
                # subract from health, update PP left and calculate total damage taken
                opponent_HP = opponent_HP - your_move_Power
                your_move_PP = your_move_PP - 1
                opponent_damage_taken = opponent_damage_taken + your_move_Power

                # if your opponent does not have health left, end battle calculation loop
                if opponent_HP <= 0:
                    you_win = True
                    break

                # obtain new move if uses run out
                elif your_move_PP <= 0:
                    # obtain new move
                    your_move_name, your_move = select_random(your_pokemon["Moves"])      
                    # obtain your pokemon's HP, PP and Power
                    your_HP, your_move_PP, your_move_Power = obtain_battle_stats(your_move_name, your_move, your_pokemon)

                else:
                    continue

                # switch turns
                your_turn = False

            # when it is the opponent's turn
            else:
                # subract from health, update PP left and calculate total damage taken
                your_HP = your_HP - opponent_move_Power
                opponent_move_PP = opponent_move_PP - 1
                your_damage_taken = your_damage_taken + opponent_move_Power

                # if your opponent does not have health left, end battle calculation loop
                if your_HP <= 0:
                    break
                # obtain new move if uses run out
                elif opponent_move_PP <= 0:
                    # obtain new move
                    opponent_move_name, opponent_move = select_random(mystery_pokemon["Moves"])        
                    # obtain Mystery pokemon's HP, PP and Power
                    opponent_HP, opponent_move_PP, opponent_move_Power = obtain_battle_stats(opponent_move_name, opponent_move, mystery_pokemon)
                else:
                    continue

                # switch turns
                your_turn = True

        # Display the battle results
        print("Battle Results!!")
        print("Your pokemon's health = " + str(your_HP))
        print("Mystery Pokemon's health = " + str(opponent_HP))

        # Display winner
        if(you_win):
            print("\n" + your_pokemon["Name"] + " won the battle!\n")
        else:
            print("\n? won the battle!\n")

        # end outer loop (might not need outer loop so might remove that)
        break

# obtain pokemon's stats needed to calculate the battle outcome of battle such as:
    # HP, PP, Power, etc.
def obtain_battle_stats(move_name, move, pokemon):
    # start with obtaining power
    Power = (move["Power"])

    # some of the entries for Power are "--" and "??" so if that happens we get a new move until is does not
    while(Power == "--" or Power == "??"):
        move_name, move = select_random(pokemon["Moves"])
        Power = (move["Power"])

    # convert strings into ints
    Power = int(Power)
    HP = int(pokemon["HP"])
    PP = int(move["PP"])

    # return
    return HP, PP, Power

# The purpose of the following function is to randomly select from a dictionary
def select_random(dictionary):
    keys = dictionary.keys()
    random_key = random.choice(list(keys))
    return random_key, dictionary[random_key]    


#-----------------------------------------------------------------------------------------------------
# Step 1: Obtain data from CSV files as pandas DataFrames.
#-----------------------------------------------------------------------------------------------------
# Obtain Pokemon-data from the CSV file. 
pokemon_data = pandas.read_csv('pkmn_training_data.csv')
pokemon_data = pokemon_data.iloc[:, :]

#-----------------------------------------------------------------------------------------------------
# Step 2: Ask user which pokemon they would like to use.
#-----------------------------------------------------------------------------------------------------

# Create 3 separate lists that all consist of dictionaries
    # each dictionary contains a set of all the different "Natures" of that same pokemon
        # for example: the Charizard list contains all Charizards that were in the pokemon data but they will have different Natures and other stats
Charizards = [pokemon_data.iloc[i, :].to_dict() for i in range(len(pokemon_data)) if pokemon_data.loc[i, "Name"] == "Charizard"]
Mewtwos = [pokemon_data.iloc[i, :].to_dict() for i in range(len(pokemon_data)) if pokemon_data.loc[i, "Name"] == "Mewtwo"]
Pikachus = [pokemon_data.iloc[i, :].to_dict() for i in range(len(pokemon_data)) if pokemon_data.loc[i, "Name"] == "Pikachu"]

# Create a dictionary that will be composed of the different lists of pokemon
user_options = {
    "Charizard" : Charizards,
    "Mewtwo"    : Mewtwos,
    "Pikachu"   : Pikachus
}

# Call the function that will ask the user what pokemon they will like to use
# your_pokemon_name = choose_your_pokemon(user_options)

# comment line above and uncomment line below when testing so you don't have to go through interaction everytime
your_pokemon_name = "Charizard" 

# Obtain the list of the user's chosen pokemon from the user_options dictionary
your_pokemon_list = user_options[your_pokemon_name]

# initialize the your_pokemon variable that will hold the pokemon that the user will have in battle
your_pokemon = None

# Select the "Docile" natured version of the selected pokemon
for pokemon in your_pokemon_list:
    if pokemon['Nature'] == "Docile":
        your_pokemon = pokemon

# randomly select a pokemon from the dataset to be the mystery pokemon and make it a dictionary
mystery_pokemon = dict(pokemon_data.iloc[(random.randint(0, len(pokemon_data))), :])

# must convert the moves into a dictionary because it comes as a string from the CSV file
mystery_pokemon["Moves"] = ast.literal_eval(mystery_pokemon["Moves"])
your_pokemon["Moves"] = ast.literal_eval(your_pokemon["Moves"])

#-----------------------------------------------------------------------------------------------------
# Step 3: Begin battle
#-----------------------------------------------------------------------------------------------------
# commence battle in battles_simulator function
battle_simulator(your_pokemon, mystery_pokemon)

#-----------------------------------------------------------------------------------------------------
# Step 4: Build tree
#-----------------------------------------------------------------------------------------------------

# # initialize Random Forest Classifier that will
#     # consist of 100 trees
#     # use Gini Impurity to calculate the split
#     # uses bootstrapping method to train the model
random_forest = RandomForestClassifier(n_estimators=100, criterion="gini", bootstrap=True, random_state=random.randint(0, len(pokemon_data)))

# next step: use random_forest.fit(X, y) to train model (most likely do this with cross fold validation) where X is dataset of pokemon (without pokemon names/labels) and Y is target values (pokemon names)

# COMMENTS --------------------------------------------------------------------------------------------------------------------
# The following is psuedocode that is subject to change. (feel free to correct/change anything!)
# Build Random Forest Tree to determine what the mystery pokemon is
    # Determine number of trees, n, in forest
    # Build and save n trees
        # for each tree use bagging 
            # at each node use gini impurity to determine how to split
    # Use majority vote of trees to decide which pokemon to put in slot/how team layout should be (depending on what is decided on how random forest tree is built)

# To-do list/More Information:
    # Train Random Forest Tree model
        # Random Forest Tree --------------------------------------------------------------------------------------
            # It is a "forest" of decision trees where the decision that will be made is based on majority vote
            # of what each decision tree resulted in. The purpose of this is too avoid making overfitting. Overfitting 
            # can occur if we use only one tree that has too many decisions to make to where it overfits the data.

                # Individual Decision Tree -------------------------------------------------------------------------
                    # 1. Each decision tree will use "bootstrap aggregation" or "bagging"
                        # Bagging is a method of random sampling where a dataset is created by randomly selected data 
                        # points from the dataset, with replacement, that creates a dataset to train a decision tree.
                        # This will be done for each individual decision tree in the Random Forest Tree model.
                        # The elements that were not in the bagging set, called the "Out-of-the-bag" set, will be used for testing.

                    # 2. Select a random number of features to choose from as a decision maker at each node.
                        # At each node, the data will be split depending on the decision that the is determined for the node
                        # to make. The decision is based on a question asked about a feature of the dataset.
                        # The features are types, moves, etc. For example: We decide to select between 2 random 
                        # features for the first node and the 2 random features are moves and types. When we select which of
                        # these 2 would be the more ideal decision maker at this node, we select that feature and discard the
                        # other one for this specific tree and not use it for the following nodes as a feature to make decisions
                        # with. This makes it to where each individual decision tree will not have too many decisions to make
                        # and cause overfitting.
                            # Example: --  
                            # Pokemon Decision Tree structure example
                            #
                            #                                         root node -> all training data
                            #                                   how much damage can this pokemon take?
                            #                                         /        \
                            #                                       5         100

                    # 2. Use the Gini Impurity of the data set at each node, starting at the root, to decide how to split.
                        # The Gini Impurity is the probability of making an incorrect classification if an element or data
                        # point in the set were randomly selected and randomly labeled. I believe the split with the lowest impurity 
                        # is chosen.

    # K-fold validation