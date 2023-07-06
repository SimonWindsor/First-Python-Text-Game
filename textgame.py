import backend
import sys

def y_or_n(prompt):
    sys.stdout.write(prompt)
    answer = sys.stdin.readline().strip().lower()
    while answer != "y" and answer != "n":
        sys.stdout.write("\nInvalid answer- must be 'y' or 'n'.\n")
        answer = sys.stdin.readline().strip().lower()
    return answer

def show_save_menu():
    menu = "\nChoose a Save Slot:\n"
    for e in range(1, 6):
        save_slot = open("gamefiles\slot" + str(e) + ".gwm", "r")
        if save_slot.readline().strip() != "empty":
            menu += str(e) + ". Slot " + str(e) + "\n"
        else:
            menu += str(e) + ". ---empty---\n"
        save_slot.close()
    menu += "6. Go Back\n"
    sys.stdout.write(menu)

def check_empty(slot):
    is_empty = False
    check_file = open("gamefiles\slot" + str(slot) + ".gwm", "r")
    if check_file.readline().strip() == "empty":
        is_empty = True
    return is_empty

def get_menu_item(first, last):
    chosen = False
    while chosen == False:
        try:
            choice = int(sys.stdin.readline().strip())
        except ValueError:
            sys.stdout.write("\nNot a valid number. Re-enter:\n")
        else:
            if choice < first or choice > last:
                sys.stdout.write("\nNot a valid choice\n")
            else:
                chosen = True
    return choice

# Required so that an 'else' statement under while prog_running doesn't output
# 'I don't understand that' when program is quit
exiting_program = False

prog_running = True

# Initiates main menu on program run
open_main_menu = True

player = None

while prog_running:

    while open_main_menu:
        menu = "\n---Main Menu---\n"
        menu += "1. New Game\n"
        menu += "2. Load Game\n"
        menu += "3. Delete Game\n"
        menu += "4. Exit\n"

        get_game = ""
        sys.stdout.write(menu)
        option = get_menu_item(1, 4)

        if option == 1:
            # Create fresh instance of backend.BackEnd() upon load
            # This prevents duplicating game data upon saves
            player = backend.BackEnd()
            player.load_game("gamefiles\startnew.gwm")
            open_main_menu = False
            sys.stdout.write(player.show_story())

        elif option == 2:
            loading = True
            while loading:
                show_save_menu()
                selection = get_menu_item(1, 6)
                if selection != 6 and check_empty(selection):
                    sys.stdout.write("\n That slot is empty.\n")
                elif selection != 6 and check_empty(selection) == False:
                    # Create fresh instance of backend.BackEnd() upon load
                    # This prevents duplicating game data upon saves
                    player = backend.BackEnd()
                    player.load_game("gamefiles\slot" + str(selection) + ".gwm")
                    loading = False
                    open_main_menu = False
                    sys.stdout.write(player.show_story())
                else:
                    loading = False
        
        elif option == 3:
            deleting = True
            while deleting:
                show_save_menu()
                selection = get_menu_item(1, 6)
                if selection != 6 and check_empty(selection):
                    sys.stdout.write("\n That slot is empty.\n")
                elif selection != 6 and check_empty(selection) == False:
                    choice = y_or_n("\nAre you sure you would like to " +
                        "delete this file? y/n \n")
                    if choice == "y":
                        erase = open ("gamefiles\slot" + str(selection) + 
                        ".gwm", "w")
                        erase.write("empty")
                        erase.close()
                else:
                    deleting = False

        else:
            choice = y_or_n("\nAre you sure you want to exit? y/n \n")
            if choice == "y":
                sys.stdout.write("\nExiting program... [press ENTER]\n")
                exiting_program = True
                prog_running = False
                open_main_menu = False

    # Outside of the main menu: Code below is for program to take input from
    # user and return game information on-screen accoringly

    # Must check if user has finished game or if their character has died
    if player.check_end() and exiting_program == False:
        sys.stdout.write("\nGame Over [press ENTER]\n")
        #no readline required as user_input below will take input
        open_main_menu = True

    user_input = sys.stdin.readline().strip().lower()


    if (user_input == "north" or user_input == "south" or user_input == "west"
        or user_input == "east" or user_input == "n" or user_input == "s"
        or user_input == "w" or user_input == "e"):
        sys.stdout.write(player.go_direction(user_input))

    elif user_input[0:4] == "take":
        remain = user_input[5:len(user_input)]
        sys.stdout.write(player.take_item(remain))

    elif user_input[0:3] == "use":
        remain = user_input[4:len(user_input)]
        sys.stdout.write(player.use_item(remain))

    elif user_input[0:8] == "interact":
        remain = user_input[9:len(user_input)]
        sys.stdout.write(player.use_item(remain))

    elif user_input == "story":
        sys.stdout.write(player.show_story())

    elif user_input == "inventory":
        sys.stdout.write(player.inventory())

    elif user_input == "fight":
        sys.stdout.write(player.fight())

    elif user_input[0:7] == "talk to":
        remain = user_input[8:len(user_input)]
        sys.stdout.write(player.talk(remain))

    elif user_input == "save":
        show_save_menu()
        selection = get_menu_item(1, 6)
        if selection != 6 and check_empty(selection):
            player.save_game("gamefiles\slot" + str(selection) + ".gwm")
            sys.stdout.write("\nGame Saved.\n")
        elif selection != 6 and check_empty(selection) == False:
            choice = y_or_n("\nDo you want to overwrite this game? y/n\n")
            if choice == "y":
                player.save_game("gamefiles\slot" + str(selection) + ".gwm")
                sys.stdout.write("\nGame Saved.\n")
        sys.stdout.write(player.show_story())
                
    elif user_input == "help":
        pass

    elif user_input == "exit":
        choice = y_or_n("\nAre you sure you would like to exit to the main " +
        "menu? Unsaved data will be lost y/n \n")
        if choice == "y":
            sys.stdout.write("\nLeaving game... (press ENTER)\n")
            sys.stdin.readline()
            open_main_menu = True
        else:
            sys.stdout.write(player.show_story())

    else:
        if exiting_program == False and player.check_end() == False:
            sys.stdout.write("\nI do not understand that\n")


