import random
import time

class Battleship:
    def __init__(self):
        # Initializes the fleet by creating ships.
        self.ships = {
            "Carrier": self.createships("Carrier"),
            "Battleship": self.createships("Battleship"),
            "Cruiser": self.createships("Cruiser"),
            "Submarine": self.createships("Submarine"),
            "Destroyer": self.createships("Destroyer")
        }
        self.opponent_ships = {}  # To store the enemy’s ships
        self.shot_history = []  # Track each shot made for undo functionality
        self.redo_stack = []  # For redoing undone shots

    def createships(self, name):
        # Creates a dictionary representing a ship.
        return {
            
            "name": name,
            "shipsType": name,  
            "coords": [],
            "sunk": False  
        }
            
    def setOpponentShips(self, opponent_fleet):
        #Assigns an opponent's fleet.
        self.opponent_ships = opponent_fleet
    
    def placeShipRandom(self, name, boardType):
        ship = self.ships.get(name)
        if not ship:
            print(f"Ship {name} not found!")
            return False

       # Determine the ship's length based on its name
        if name == "Carrier":
           ships_length = 5
        elif name == "Battleship":
           ships_length = 4
        elif name in ["Cruiser", "Submarine"]:
           ships_length = 3
        elif name == "Destroyer":
            ships_length = 2 
    
    # Set board size based on the board type
        if boardType == 'Square':
            maxWidth = 10
            maxHeight = 10
        elif boardType == 'Rectangle':
            maxWidth = 5
            maxHeight = 20
    
        # Randomly pick orientation (H = Horizontal, V = Vertical)
        randomOrientation = random.choice("HV")  # Horizontal or Vertical

        # Try placing the ship until a valid position is found
        for _ in range(100):  # Try 100 times before giving up (to avoid infinite loop)
            start_col = random.choice("ABCDEFGHIJ")  # Random starting column
            start_col_index = ord(start_col.upper()) - ord('A')
            start_row = random.randint(0, maxHeight - 1)  # Random starting row
        
            ships_coords = []  # List to store the coordinates of the ship
        
        # Check if placing the ship horizontally
            if randomOrientation.upper() == 'H':
                if start_col_index + ships_length > maxWidth:  # Ship goes out of bounds horizontally
                    continue  # Try again with a new starting position
            
                # Check if any of the coordinates are already occupied
                overlap = False
                for i in range(ships_length):
                    coord = f"{chr(65 + start_col_index + i)}{start_row}"
                    if any(coord in [s["coord"] for s in ship["coords"]] for ship in self.ships.values()):  # Check for overlap
                        overlap = True
                        break
                    ships_coords.append({"coord": coord, "hit": False})
            
                if overlap:
                    continue  # Try placing the ship at a new random position
                else:
                    break  # Successfully placed the ship
        
        # Check if placing the ship vertically
            elif randomOrientation.upper() == 'V':
                if start_row + ships_length > maxHeight:  # Ship goes out of bounds vertically
                    continue  # Try again with a new starting position
            
            # Check if any of the coordinates are already occupied
                overlap = False
                for i in range(ships_length):
                    coord = f"{start_col}{start_row + i}"
                    if any(coord in [s["coord"] for s in ship["coords"]] for ship in self.ships.values()):  # Check for overlap
                        overlap = True
                        break
                    ships_coords.append({"coord": coord, "hit": False})
            
                if overlap:
                    continue  # Try placing the ship at a new random position
                else:
                    break  # Successfully placed the ship

        ship["coords"] = ships_coords
        #print(f"Placed ship {name} at {ships_coords}")
        return True
            
    def addToBoard(self, name, start, direction, boardType):
        ship = self.ships.get(name)
        if not ship:
            print(f"ships {name} not found!")
            return False
        if name == "Carrier":
            ships_length = 5
        elif name == "Battleship":
            ships_length = 4
        elif name in ["Cruiser", "Submarine"]:
            ships_length = 3
        elif name == "Destroyer":
            ships_length = 2
        # Example: start = 'A1', direction = 'H' (Horizontal), direction = 'V' (Vertical)
        start_col, start_row = start[0], int(start[1:])
        start_col_index = ord(start_col.upper()) - ord('A')
        
        #code to validate the ship will fit on the board for each shape (boardType)
        if boardType == 'Square':
            maxWidth = 10
        elif boardType == 'Rectangle':
            maxWidth = 5 #shorter on the width (row = 12345...)
            
        if boardType == 'Square':
            maxHeight = 10
        elif boardType == 'Rectangle':
            maxHeight = 20 #longer on the length/height (column = ABCDEF...)
            
            
        # List to store the coordinates of the ship with hit status
        ships_coords = []
        # Check if placing the ship horizontally
        if direction.upper() == 'H':
            if start_col_index + ships_length > maxWidth:  # ship goes out of bounds horizontally (falls of the right)
                print("Ship does not fit horizontally!")
                return False

            if start_row + ships_length > maxHeight:  # ship goes out of bounds vertically (falls off the bottom)
                print("Ship does not fit vertically! \ncheck that the number is within the bounds")
                return False 
               
            for i in range(ships_length):
                coord = f"{chr(65 + start_col_index + i)}{start_row}"
                ships_coords.append({"coord": coord, "hit": False})
        
        # Check if placing the ship vertically
        elif direction.upper() == 'V':
            if start_row + ships_length > maxHeight:  # ship goes out of bounds vertically (falls off the bottom)
                print("ship does not fit vertically!")
                return False
            if start_col_index + ships_length > maxWidth:  # ship goes out of bounds horizontally (falls of the right)
                print("ship does not fit horizontally! \ncheck that the letter is within the bounds")
                return False
            for i in range(ships_length):
                coord = f"{start_col}{start_row + i}"
                ships_coords.append({"coord": coord, "hit": False})       
        ship["coords"] = ships_coords
        
        print(name, " placed at ", ships_coords)
        return True
    
    def shoot(self, coord):
        #fire a shot at a specific coordinate, search for it in all ships.
        #includes ships names just for my information, will delete later as it gives information away to the player.
        for name, ships in self.opponent_ships.items():
            for pos in ships["coords"]:
                if pos["coord"] == coord:
                    if pos["hit"]:
                        print(f"Already hit at {coord} on {name}.")
                        return False  # Already hit
                    else:
                        pos["hit"] = True
                        print(f"Hit at {coord} on {name}.")
                        self.checkSinkShip(name)
                        self.redo_stack.clear()
                        self.shot_history.append({
                        "coord": coord,
                        "target": name,
                        "was_hit": True
                        })
                        return True  # Successfully hit

        print(f"Miss at {coord}")
        self.shot_history.append({
        "coord": coord,
        "target": None,
        "was_hit": False
    })
        return False  # No ships at this coordinate

    def undoLastShot(self):
        if not self.shot_history:
            print("No shots to undo.")
            return False

        last_shot = self.shot_history.pop()
        coord = last_shot["coord"]
        target = last_shot["target"]
        was_hit = last_shot["was_hit"]

        if was_hit and target:
            ship = self.opponent_ships.get(target)
            if ship:
                for pos in ship["coords"]:
                    if pos["coord"] == coord:
                        pos["hit"] = False
                # Recalculate sunk status
                ship["sunk"] = False
                print(f"Undo: Reverted hit on {target} at {coord}")
        else:
            print(f"Undo: Reverted miss at {coord}")

        self.redo_stack.append(last_shot)  # Store it for redo
        return True

    def redoLastShot(self):
        if not self.redo_stack:
            print("No shots to redo.")
            return False

        shot = self.redo_stack.pop()
        coord = shot["coord"]
        target = shot["target"]
        was_hit = shot["was_hit"]

        if was_hit and target:
            ship = self.opponent_ships.get(target)
            if ship:
                for pos in ship["coords"]:
                    if pos["coord"] == coord:
                        pos["hit"] = True
                ship["sunk"] = all(p["hit"] for p in ship["coords"])
                print(f"Redo: Reapplied hit on {target} at {coord}")
        else:
            print(f"Redo: Reapplied miss at {coord}")

        self.shot_history.append(shot)  # Put it back in history
        return True

    def checkSinkShip(self, name):
        ship = self.opponent_ships.get(name)
        if ship:  # Ensure the ship exists
            if all(coord["hit"] for coord in ship["coords"]):  # Check if all positions are hit
                ship["sunk"] = True
                print(f"{name} has been sunk!")
                self.gameEndCheck()
        
    def computerShoot(self, boardtype):
        if boardtype == 'Square':
            coord = random.choice("ABCDEFGHIJ") + str(random.randint(0, 9))
            self.shoot(coord)        
        elif boardtype == 'Rectangle':
            coord = random.choice("ABCEFGHIJKLMNOPRST") + str(random.randint(0,4))
            self.shoot(coord)        
                        
    def gameEndCheck(self):
        #Check if all ships are sunk and end the game.
        if all(ship["sunk"] for ship in self.ships.values()):  # Check if all ships are sunk
            print("Game over!")
            return True  # Indicates the game is over
        else:
          # print("Don't give up yet!.")
            return False



print("Welcome to Battleships!\n")        
difficulty = input("Would you like to play Easy (press 1), Medium (press 2) or Hard (press 3) difficulty:\n")
if difficulty == "1":
    gameLength = 300
elif difficulty == "2":
    gameLength = 240
elif difficulty == "3":
    gameLength  = 120
else:
    print("error wrong diffculty selected")
print("You will have", gameLength/60, "minutes to complete the game\n")
boardTypeInput = input("Please select the shape of board you would like\nFor the traditional 10x10 square press 1\nFor a 5x20 rectangle press 2\nEnter choice here: ")
if boardTypeInput == "1":
    boardType = "Square"
elif boardTypeInput == "2":
    boardType = "Rectangle"
    
    
player = Battleship()
cpu = Battleship()
player.setOpponentShips(cpu.ships)  # Player now stores CPU's ships
cpu.setOpponentShips(player.ships)  # CPU now stores Player's ships
cpu.placeShipRandom("Carrier", boardType)
cpu.placeShipRandom("Battleship", boardType)
cpu.placeShipRandom("Submarine", boardType)
cpu.placeShipRandom("Cruiser", boardType)
cpu.placeShipRandom("Destroyer", boardType)
#places the CPU's ships
print(cpu.ships)

shipsPlacedCounter = 0
autoplaceships = input("Would you like to place your own ships (press 1) or have them placed randomly (press 2): \n")
if autoplaceships == "1":
    while shipsPlacedCounter <= 4:
        print("Ships placed currently", shipsPlacedCounter)
        inputShipName = input("Type the name of the ship you would like to place: (e.g. Carrier) \n")
        inputStartCoord = input("Type the starting coordinate: (e.g. A1) \n")
        inputOrientation = input("Type the orientation: ('H' or 'V') \n")
        if player.addToBoard(inputShipName, inputStartCoord, inputOrientation, boardType):
            shipsPlacedCounter += 1
        
        
else:
    ship_names = ["Carrier", "Battleship", "Submarine", "Cruiser", "Destroyer"]
    shipsPlacedCounter = 0

    for name in ship_names:
        if player.placeShipRandom(name, boardType):
            shipsPlacedCounter += 1
        #randomly places the player's ships if they are too lazy to place them manually
  
print(player.ships)
print("Ships all placed\nStarting game now:")         
start_time = time.time()
time_limit = gameLength  # length of game is dependent on game difficulty selected    
        
while (Battleship.gameEndCheck(player) or Battleship.gameEndCheck(cpu)) == False:
    if time.time() - start_time > time_limit:
        print("Time's up! You lost.")
        break
    print("CPU shot:")
    cpu.computerShoot(boardType)
    print("-----------------------")
    playershoot = input("Your shot: ")
    player.shoot(playershoot)
    if difficulty == "1":
        undoInput = input("Type '1' if you would like to undo that shot: ")
        if undoInput == '1':
            player.undoLastShot()
            playerNewShoot = input("Your new shot: ")
            player.shoot(playerNewShoot)
            
    if cpu.gameEndCheck == True:
        print("You lost moron")
    elif player.gameEndCheck == True:
        print("You won!!! well done")
    
