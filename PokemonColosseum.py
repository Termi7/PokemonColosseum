import csv
from pokemon import Pokemon
from moves import Moves
import random
import math
import sys

print("Welcome to pokemon Colosseum!")
print()
playerName = input("Enter a player Name: ")
print()
# playerName = 'VIP'
available = set()

pokemons = []  # used to populated all the pokemons and the descriptions and attributes
moves = []  # used to populated all the moves and the descriptions

with open("pokemon-data.csv", 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    for row in reader:
        pokemons.append(Pokemon(*row))
    csvfile.close()

with open("moves-data.csv", 'r') as csvfiles:
    reader1 = csv.reader(csvfiles, delimiter=',')
    next(reader1)
    for row in reader1:
        moves.append(Moves(*row))
    csvfiles.close()

rocket_queue = random.sample(pokemons, 3)
player_queue = random.sample(list(set(pokemons) - set(rocket_queue)), k=3)

# player_queue = random.sample(pokemons-rocket_queue,3)

for p in pokemons:
    for s in p.moves:
        if s in (' "Self\'Destruct"', ' "Baby\'Doll Eyes"', ' "Mud\'Slap"', '"Mud\'Slap"', '"Double\'Edge"'):
            p.moves.remove(s)

# for p in pokemons:
#     for s in p.moves:
#         print(p.moves)


# for p in moves:
#     print(p.name)

# for s in rocket_queue:
#     print(s)




def damage(mov, A, B, moves1):
    """This function calculate the damage when a Pokemon A makes a move mov on pokemon B
    arguments: mov string name of the move being selected, A and B are two pokemon respectively the attacking one
    and the defending one, moves1 is a move object
    This function return damage done  .
    """
    table = {
        'Normal': {'Normal': 1, 'Fire': 1, 'Water': 1, 'Electric': 1, 'Grass': 1},
        'Fire': {'Normal': 1, 'Fire': 0.5, 'Water': 0.5, 'Electric': 1, 'Grass': 2},
        'Water': {'Normal': 1, 'Fire': 2, 'Water': 0.5, 'Electric': 1, 'Grass': 0.5},
        'Electric': {'Normal': 1, 'Fire': 1, 'Water': 2, 'Electric': 0.5, 'Grass': 0.5},
        'Grass': {'Normal': 1, 'Fire': 0.5, 'Water': 2, 'Electric': 1, 'Grass': 0.5},
        'Other': {'Normal': 1, 'Fire': 1, 'Water': 1, 'Electric': 1, 'Grass': 1},
    }
    powerMove = 0

    for c in moves1:
        v = mov.replace("'", "")
        if c.name == v.strip():
            powerMove = c.power
            # print(powerMove)
            break
    AA = ""
    BB = ""
    attackPokemon = 0
    defencePokemon = 0

    for k in pokemons:
        if k.name == A:
            attackPokemon = k.attack
            break
    # this is to figure out the type of the move A  pokemon

    for o in moves:
        v = mov.replace("'", "")
        if o.name == v.strip():
            AA = o.typeMove
            # print("move", AA)
            break

    for n in pokemons:
        if n.name == B:
            defencePokemon = n.defence
            BB = n.typePokemon
            break

    stab = 1.5 if AA == BB else 1  # check if A.typePokemon==B.typePokemon
    if AA not in ("Water", "Fire", "Normal", "Electric", "Grass"):
        AA = "Other"

    typeEfficiency = table[AA][BB]  # table[o.typeMove][B.typePokemon]
    # print(AA, BB, table[AA][BB])
    # print(table[AA][BB])
    Random = random.uniform(0.5, 1)

    damageMade = int(powerMove) * (int(attackPokemon) / int(defencePokemon)) * stab * typeEfficiency * Random

    return math.ceil(damageMade)





def playerGame(moves, rocket_queue, player_queue, damage_pokemon):
    """This function execute the player game action , ask for input and display the outcome
    arguments : moves which is the a moves object , rocket_queue and player_queue are respectively the pokemon
    available for Team Rocket and the and the other team , damage_pokemon is the HP of the previous playing pokenon
    No return value
    """
    print("")
    if len(available) == len(player_queue[0].moves):
        available.clear()
    print(f"Choose the move for {player_queue[0].name}:")
    for i, move in enumerate(player_queue[0].moves, 1):
        move_without_quote = move.replace("'", "")
        if i in available:
            print(f"{i}. {move_without_quote.strip()} (N/A)")
            continue

        print(f"{i}. {move_without_quote.strip()}")
    print("")

    # print("Team Professor’s choice:")
    # p = int(input("Team Professor’s choice:"))
    p = input(f"Team {playerName}’s choice: ")
    while not (p.isdigit() and int(p) in range(len(player_queue[0].moves) + 1) and int(p) not in available):
        print("Invalid input. Please enter valid choice number between 1 and ", len(player_queue[0].moves))
        print(
            "You can't select the previous selected choice until you've used up all the options available. Then it will reset again.")
        p = input(f"Team {playerName}’s choice:")
    p = int(p)
    available.update({p})
    # print(available)
    m = player_queue[0].moves[p - 1]
    # print(m)
    damage_doneA = damage(m, player_queue[0].name, rocket_queue[0].name, moves)
    print(f"Team's {playerName} {player_queue[0].name} cast{m} to {rocket_queue[0].name}:")
    print(f"Damage to {rocket_queue[0].name} is {damage_doneA} points.")
    damage_pokemonAB = int(rocket_queue[0].HP) - int(damage_doneA)

    rocket_queue[0].setHP(damage_pokemonAB)

    if damage_pokemonAB <= 0:
        print(
            f"Now {rocket_queue[0].name} has faints to poke ball, and {player_queue[0].name} has {damage_pokemon} HP.")
        fainted = True
        return True
    print(f"Now {rocket_queue[0].name} has {damage_pokemonAB} HP, and {player_queue[0].name} has {damage_pokemon} HP.")
    return damage_pokemonAB





def rocketGame(moves, rocket_queue, player_queue, x):
    """This function execute the Rocket team game action , ask for input and display the outcome
    arguments : moves which is the a moves object , rocket_queue and player_queue are respectively the pokemon
    available for Team Rocket and the and the other team , x is the HP of the previous playing pokenon
    No return value
    """
    print("")
    m = random.choice(list(move for move in rocket_queue[0].moves))
    print(f"Team's Rocket {rocket_queue[0].name} cast{m} to {player_queue[0].name}: ")
    damage_done = damage(m, rocket_queue[0].name, player_queue[0].name, moves)
    print(f"Damage to {player_queue[0].name} is {damage_done} points.")
    damage_pokemon = int(player_queue[0].HP) - int(damage_done)
    player_queue[0].setHP(damage_pokemon)

    if damage_pokemon <= 0:
        print(f"Now {rocket_queue[0].name} has {x} HP, and {player_queue[0].name} has faints to poke ball.")
        fainted = True
        return fainted
    print(f"Now {rocket_queue[0].name} has {x} HP, and {player_queue[0].name} has {damage_pokemon} HP.")
    return damage_pokemon


print(f"Team Rocket enter with {rocket_queue[0].name}, {rocket_queue[1].name}, {rocket_queue[2].name}.")
print("")
print(f"Team {playerName} enter with {player_queue[0].name}, {player_queue[1].name}, {player_queue[2].name}.")
print("")
print("Let's begin the battle!")
x = random.randint(0, 1)
# print(x)

if x == 1:
    team = 'Rocket'
    print(f"Coin toss goes to ----- Team {team} to start the attack.")

    # damage_pokemon = rocketGame(moves, rocket_queue, player_queue)
    # for s in rocket_queue[0].moves:
    #     print(s)
    w = rocketGame(moves, rocket_queue, player_queue, rocket_queue[0].HP)
    # if w<0:
    if w == True:
        player_queue.pop(0)
        print("")
        print(f"Next for team {playerName}, {player_queue[0].name} enters the battle!")
        available.clear()
        # print(f"Next for team Rocket , {rocket_queue[0].name} enters the battle!")
        x = playerGame(moves, rocket_queue, player_queue, player_queue[0].HP)

    else:
        x = playerGame(moves, rocket_queue, player_queue, w)

    while True:
        if x == True:
            if len(rocket_queue) == 0:
                print("")
                print(f"All of Team Rocket’s Pokemon fainted, and Team {playerName} prevails!")
                sys.exit()
            rocket_queue.pop(0)
            if len(rocket_queue) == 0:
                print("")
                print(f"All of Team Rocket’s Pokemon fainted, and Team {playerName} prevails!")
                sys.exit()
            print("")
            print(f"Next for team Rocket, {rocket_queue[0].name} enters the battle!")
            y = rocketGame(moves, rocket_queue, player_queue, rocket_queue[0].HP)
        else:
            y = rocketGame(moves, rocket_queue, player_queue, x)
        if y == True:
            if len(player_queue) == 0:
                print("")
                print(f"All of Team {playerName}’s Pokemon fainted, and Team Rocket  prevails!")
                sys.exit()
            player_queue.pop(0)
            if len(player_queue) == 0:
                print("")
                print(f"All of Team {playerName}’s Pokemon fainted, and Team Rocket  prevails!")
                sys.exit()
            print("")
            print(f"Next for team {playerName}, {player_queue[0].name} enters the battle!")
            available.clear()
            x = playerGame(moves, rocket_queue, player_queue, player_queue[0].HP)
        else:
            x = playerGame(moves, rocket_queue, player_queue, y)

    # if x == True:
    #     if len(rocket_queue)==0:
    #         print(f"All of Team Rocket’s Pokemon fainted, and Team {playerName} prevails!")
    #         sys.exit()
    #     rocket_queue.pop(0)
    #     if len(rocket_queue)==0:
    #         print(f"All of Team Rocket’s Pokemon fainted, and Team {playerName} prevails!")
    #         sys.exit()
    #     print(f"Next for team Rocket , {rocket_queue[0].name} enters the battle!")
    #     y = rocketGame(moves, rocket_queue, player_queue, rocket_queue[0].HP)
    # else:
    #     y = rocketGame(moves, rocket_queue, player_queue, x)
    # if y == True:
    #     if len(player_queue)==0:
    #         print(f"All of Team {playerName}’s Pokemon fainted, and Team Rocket  prevails!")
    #         sys.exit()
    #     player_queue.pop(0)
    #     if len(player_queue) == 0:
    #         print(f"All of Team {playerName}’s Pokemon fainted, and Team Rocket  prevails!")
    #         sys.exit()
    #     print(f"Next for team {playerName} , {player_queue[0].name} enters the battle!")
    #     n = playerGame(moves, rocket_queue, player_queue, player_queue[0].HP)
    # else:
    #     n = playerGame(moves, rocket_queue, player_queue, y)
    #
    # if n == True:
    #     if len(rocket_queue)==0:
    #         print(f"All of Team Rocket’s Pokemon fainted, and Team {playerName} prevails!")
    #         sys.exit()
    #     rocket_queue.pop(0)
    #     if len(rocket_queue)==0:
    #         print(f"All of Team Rocket’s Pokemon fainted, and Team {playerName} prevails!")
    #         sys.exit()
    #     print(f"Next for team Rocket , {rocket_queue[0].name} enters the battle!")
    #     s = rocketGame(moves, rocket_queue, player_queue, rocket_queue[0].HP)
    # else:
    #     s = rocketGame(moves, rocket_queue, player_queue, n)
    #
    # if s == True:
    #     if len(player_queue)==0:
    #         print(f"All of Team {playerName}’s Pokemon fainted, and Team Rocket  prevails!")
    #         sys.exit()
    #     player_queue.pop(0)
    #     if len(player_queue)==0:
    #         print(f"All of Team {playerName}’s Pokemon fainted, and Team Rocket  prevails!")
    #         sys.exit()
    #     print(f"Next for team {playerName} , {player_queue[0].name} enters the battle!")
    #     y = playerGame(moves, rocket_queue, player_queue, player_queue[0].HP)
    # else:
    #     y = playerGame(moves, rocket_queue, player_queue, s)
    #
    # if y == True:
    #     if len(rocket_queue)==0:
    #         print(f"All of Team Rocket’s Pokemon fainted, and Team {playerName} prevails!")
    #         sys.exit()
    #     rocket_queue.pop(0)
    #     if len(rocket_queue)==0:
    #         print(f"All of Team Rocket’s Pokemon fainted, and Team {playerName} prevails!")
    #         sys.exit()
    #     print(f"Next for team Rocket , {rocket_queue[0].name} enters the battle!")
    #     t = rocketGame(moves, rocket_queue, player_queue, rocket_queue[0].HP)
    # else:
    #     t = rocketGame(moves, rocket_queue, player_queue, y)
    #
    # if t == True:
    #     if len(player_queue)==0:
    #         print(f"All of Team {playerName}’s Pokemon fainted, and Team Rocket  prevails!")
    #         sys.exit()
    #     player_queue.pop(0)
    #     if len(player_queue)==0:
    #         print(f"All of Team {playerName}’s Pokemon fainted, and Team Rocket  prevails!")
    #         sys.exit()
    #     print(f"Next for team {playerName} , {player_queue[0].name} enters the battle!")
    #     y = playerGame(moves, rocket_queue, player_queue, player_queue[0].HP)
    # else:
    #     y = playerGame(moves, rocket_queue, player_queue, t)


else:
    team = playerName
    print(f"Coin toss goes to ----- Team {team} to start the attack.")
    w = playerGame(moves, rocket_queue, player_queue, player_queue[0].HP)
    # damage_pokemon = playerGame(moves, rocket_queue, player_queue, )
    if w == True:
        rocket_queue.pop(0)
        print("")
        print(f"Next for team Rocket, {rocket_queue[0].name} enters the battle!")
        # print(f"Next for team Rocket , {rocket_queue[0].name} enters the battle!")
        x = rocketGame(moves, rocket_queue, player_queue, rocket_queue[0].HP)

    else:
        x = rocketGame(moves, rocket_queue, player_queue, w)

    while True:
        if x == True:
            if len(player_queue) == 0:
                print("")
                print(f"All of Team {playerName}’s Pokemon fainted, and Team Rocket prevails!")
                sys.exit()
            player_queue.pop(0)
            if len(player_queue) == 0:
                print("")
                print(f"All of Team {playerName}’s Pokemon fainted, and Team Rocket prevails!")
                sys.exit()
            print("")
            print(f"Next for team {playerName}, {player_queue[0].name} enters the battle!")
            available.clear()
            y = playerGame(moves, rocket_queue, player_queue, player_queue[0].HP)
        else:
            y = playerGame(moves, rocket_queue, player_queue, x)
        if y == True:
            if len(rocket_queue) == 0:
                print("")
                print(f"All of Team Rocket’s Pokemon fainted, and Team {playerName} prevails!")
                sys.exit()
            rocket_queue.pop(0)
            if len(rocket_queue) == 0:
                print("")
                print(f"All of Team Rocket’s Pokemon fainted, and Team {playerName} prevails!")
                sys.exit()
            print("")
            print(f"Next for team Rocket, {rocket_queue[0].name} enters the battle!")
            x = rocketGame(moves, rocket_queue, player_queue, rocket_queue[0].HP)
        else:
            x = rocketGame(moves, rocket_queue, player_queue, y)
