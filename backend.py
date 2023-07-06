# This class creates a "location" in the game. Each of these "locations" has an
# x and y coordinate. Each instance will be stored in a list in BackEnd as if
# to simulate a 2D map.
class GameSquare:

    def __init__(self, x, y, paths, story, items, blocked): #put altered here
        self.x = x
        self.y = y
        self.paths = paths
        self.story = story
        self.items = items
        self.blocked = blocked
        #self.altered = altered
        
    def show_paths(self):
        available = "\nAvailable paths are: "
        if len(self.paths) > 0:
            i = 0
            while(i < len(self.paths)):
                available += self.paths[i]
                if i != len(self.paths) - 1:
                    available += ", "
                i += 1
            available += "\n"
        else:
            available = "\nThere are no paths at the moment! You are stuck!\n"
        return available

    def show_items(self):
        items = "\nYou currently see: "
        if len(self.items) > 0:
            i = 0
            while(i < len(self.items)):
                items += self.items[i]
                if i != len(self.items) - 1:
                    items += ", "
                i += 1
            items += "\n"
        else:
            items = "\nThere are no items here\n"
        return items

    def check_item(self, take):
        available = False
        if take in self.items:
            self.items.remove(take)
            available = True
        return available

    def is_available(self, direction):
        available = False
        if direction in self.paths:
            available = True
        return available

    def is_blocked(self):
        return self.blocked

# This creates an object for a running game
class BackEnd:
    def __init__(self):
        self.x = None
        self.y = None
        self.items = []
        self.world = []
        self.finished = False

    def get_location(self, x, y):
        send_location = None
        i = 0
        while i < len(self.world):
            if x == self.world[i].x and y == self.world[i].y:
                send_location = self.world[i]
                break
            i += 1
        return send_location

    def unblock(self, x, y):
        self.get_location(x, y).blocked = False

    def alter(self, x, y, new_story):
        self.get_location(x, y).story = new_story
        #self.get_location(x, y).altered = True
    
    #Checks for shorthand input eg "n" for "north"
    def get_direction(self, direction):
        if direction == "n":
            direction = "north"
        elif direction == "s":
            direction = "south"
        elif direction == "w":
            direction = "west"
        elif direction == "e":
            direction = "east"
        return direction
    
    def go_direction(self, move_to):
        message = ""
        
        #Check for shorthand input eg "n" for "north" with get_direction()
        move_to = self.get_direction(move_to)
        
        if self.get_location(self.x, self.y).is_available(move_to):
            new_x = self.x
            new_y = self.y
            if move_to == "north":
                new_y -= 1
            elif move_to == "south":
                new_y += 1
            elif move_to == "west":
                new_x -= 1
            elif move_to == "east":
                new_x += 1

            if self.get_location(new_x, new_y).is_blocked():
                message = ("\nThere is a path in that direction not " +
                "available at this time\n")
            else:
                self.x = new_x
                self.y = new_y
                self.determine_end()
                message = self.show_story()
        else:
            message = "\nYou are unable to go " + move_to + "\n"
        return message
 

    def show_story(self):
        current = self.get_location(self.x, self.y)
        message = "\n" + current.story + "\n"
        # If entering a certain GameSquare ends the game, available directions
        # and items are not to be shown
        if self.finished == False:
            message += current.show_items() + current.show_paths()
        return message

    # Makes the game end if player enters specific GameSquares 
    def determine_end(self):
        if ((self.x == 18 and self.y == 6) or
            (self.x == 19 and self.y == 7)):
            self.finished = True

    # Checks to see if player has died or if player has finished game
    def check_end(self):
        return self.finished

    def take_item(self, get_item):
        message = ""
        if self.get_location(self.x, self.y).check_item(get_item):
            message = "\nYou have '" + get_item + "'\n"
            self.items.append(get_item)
        elif get_item == "":
            message = "\nTake what?\n"
        else:
            message = "\nThat item is not here\n"
        return message

    def inventory(self):
        message = "\nYou currently have these items: "
        i = 0
        while i < len(self.items):
            message += self.items[i]
            if i < len(self.items) - 1:
                message += ", "
            i += 1
        message += "\n"
        return message

    def talk(self):
        pass

    def use_item(self, item):
        message = ""
        if item in self.items:
            if item == "knife": #just testing for now
                if self.x == 18 and self.y == 8:
                    message = "You get stabbed through the eye to your brain!!!\n"
                    self.finished = True
                else:
                    message = "\nYou can't use that here.\n"
            if item == "oar":
                if self.x == 13 and self.y == 10:
                    self.x = 16
                    self.y = 7
                    message = ("\nYou are rowing to a nearby jetty to the " +
                        "north-east.\n")
                    message += self.show_story()
                elif self.x ==16 and self.y == 7:
                    self.x = 13
                    self.y = 10
                    message = ("\nYou are rowing to a nearby jetty to the " +
                        "south-west.\n")
                    message += self.show_story()
                else:
                    message = "\nYou can't use that here.\n"
            elif item == "rope":
                if self.x ==16 and self.y == 13:
                    self.unblock(16, 12)
                    self.items.remove("rope")
                    message = ("You used the rope. You no longer have it.")
                    self.alter(16, 13, "\nYou are now in the cave. " +
                        "You see stalactites and stalagmites. With a rope in " +
                        "place you can now move to the north.")
                    message += self.show_story()
                else:
                    message = "\nYou can't use that here.\n"
            elif item == "torch":
                if self.x ==16 and self.y == 14:
                    self.unblock(16, 13)
                    message = ("You used the torch.")
                    self.alter(16, 14, "\nNow that you have lit up the " +
                        "cave. You see a path north towards a very large " +
                        "rock")
                    message += self.show_story()
                else:
                    message = "\nYou can't use that here.\n"
        elif item == "":
            message = "\nUse what?\n"
        else:
            message = "\nYou do not have that.\n"
        return message

    # to interact with objects in environment that can't be picked up
    def interact(self, item):
        message = ""
        if item == "door":
            pass #this will be fleshed out later
            # need to put a location here
        elif item == "":
            message = "\Interact with what?\n"
        else:
            message = "\nThat is not here.\n"
        return message

    def save_game(self, slot):
        save_file = open(slot, "w")
        save_file.write(str(self.x) + "\n")
        save_file.write(str(self.y) + "\n")
        for e in self.items:
            save_file.write(e)
            save_file.write(",")
        save_file.write("\n")
        
        i = 0
        while i < len(self.world):
            save_file.write(str(self.world[i].x) + "\n")
            save_file.write(str(self.world[i].y) + "\n")
            for e in self.world[i].paths:
                save_file.write(e)
                save_file.write(",")
            save_file.write("\n")
            save_file.write(self.world[i].story.strip() + "\n")
            for e in self.world[i].items:
                save_file.write(e)
                save_file.write(",")
            save_file.write("\n")
            save_file.write(str(self.world[i].blocked) + "\n")
            i += 1

        save_file.write("end of data")
        save_file.close()

    def load_game(self, slot):
        load_file = open(slot, "r")
        
        self.x = int(load_file.readline().strip())
        self.y = int(load_file.readline().strip())
        # remove last comma
        get_items = load_file.readline().strip()[:-1]
        # Check line isn't empty as to avoid an empty item
        if get_items != "":    
            self.items = get_items.split(",")

        line = load_file.readline().strip()
        while line != "end of data":
            x = int(line)
            y = int(load_file.readline().strip())
            # remove last comma
            get_paths = load_file.readline().strip()[:-1]
            paths = get_paths.split(",")
            story = load_file.readline().strip()
            # remove last comma
            line = load_file.readline().strip()[:-1]
            items = []
            if line != "":
                items = line.split(",")
            line = load_file.readline().strip()
            blocked = False
            if line == "True":
                blocked = True
            #line = load_file.readline().strip()
            #altered = False
            #if line == "True":
                #altered = True
            self.world.append(GameSquare(x, y, paths, story, items, blocked)) #put altered in here
            line = load_file.readline().strip()
        load_file.close()

