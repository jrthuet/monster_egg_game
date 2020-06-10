from random import choice
from random import randint

class Board:
    def __init___(self, width, length, mcount, ecount, tokens):
        Board.width = width
        Board.length = length
        Board.rooms = rooms
        Board.tlist = tlist
        Board.mcount = mcount
        Board.ecount = ecount
             
    def create_board(self):
        #creates a list of lists containing the coord and "_|" to create the room
        Board.rooms = []
        Board.width = int(input("How many rooms wide will your labyrith be? ")) #width of board (y vals for some reason)
        Board.length = int(input("How many rows long will your labyrith be? ")) #length of board (x vals)
        for x in range(0, Board.length):
            for y in range(0, Board.width):
                r = []
                cell=(x, y) 
                r.append(cell)
                r.append("_|")
                Board.rooms.append(r) #creates a list of lists containing the coord and "_|" to create the room
    
    def reset_board(self):
        Board.rooms = []
        for x in range(0, self.length):
            for y in range(0, self.width):
                r = []
                cell=(x, y) 
                r.append(cell)
                r.append("_|")
                Board.rooms.append(r) #creates a list of lists containing the coord and "_|" to create the room
                
        tokens = Board.tlist
        for t in tokens: #replaces the _ with the token letter
            for r in self.rooms:
                if t[0] == r[0]:
                    r[1] = f"{t[1]}" #for some reason - needed to drop the | for the board to print correctly.
        top = " _" * self.width
        print(top)
        for r in range(self.length):
            maps = list(map(lambda x: x[1], self.rooms[(((r+1) * self.width) - self.width):((r+1) *self.width)])) 
            combo = "".join(maps)
            print(f"|{combo}")

    def print_board(self):    
        tokens = Board.tlist
        for t in tokens: #replaces the _ with the token letter
            for r in self.rooms:
                if t[0] == r[0]:
                    r[1] = f"{t[1]}|"  #pulling the _| or token symbol out of our grid list and putting them into rows
        top = " _" * self.width
        print(top)
        for r in range(self.length):
            maps = list(map(lambda x: x[1], self.rooms[(((r+1) * self.width) - self.width):((r+1) *self.width)])) 
            combo = "".join(maps)
            print(f"|{combo}")  

class Token:
    def __init__(self, name, coordinates=[]):
        self.name = name
        self.coordinates = coordinates

    def __repr__(self):
         return f"<Token: {self.coordinates}>"

class Player(Token):     
    def __init__(self):
        Player.inventory = []
        Player.mlist = []
        Player.elist = []
        Player.end = False
        self.name = "Player"     

    def pmove(self):
        roomlist = []
        for r in range(len(Board.rooms)):
            roomlist.append(Board.rooms[r][0])

        while True:
            move = input("Which way do you want to move? ('u' for up, 'd' for down, 'r' for right, 'l' for left, 'i' to view inventory, or 'q' to quit) ")
            x = Player.coordinates[0][0]
            y = Player.coordinates[0][1]
            
            if move == 'u':
                if (x-1, y) in roomlist:
                    Player.coordinates[0] = (x-1, y)
                    break
                else:
                    print("You are not allowed to move that way. ")
            elif move == 'd':
                if (x+1, y) in roomlist:
                    Player.coordinates[0] = (x+1, y)
                    break
                else:
                    print("You are not allowed to move that way. ")
            elif move == 'r':
                if (x, y+1) in roomlist:
                    Player.coordinates[0] = (x, y+1)
                    break
                else:
                    print("You are not allowed to move that way. ")
            elif move == 'l':
                if (x, y-1) in roomlist:
                    Player.coordinates[0] = (x, y-1)
                    break
                else:
                    print("You are not allowed to move that way. ")
            elif move == 'q':
                Player.end = True
                break
            elif move == 'i':
                print("Current Inventory:")
                for i in Player.inventory:
                    print(f"{i.name}")
            else:
                print("You have pressed an incorrect key. ")

class Monsters(Token):
    monster_list = []

    def __init__(self):
        self.name = "Monster"
        self.monster_list.append(self)
    
    def mmove(self, board): #randomly moves monsters around the board
        Player.mlist = []
        for t in range(len(Board.tlist)): 
            if Board.tlist[t][1] == "M|":
                x = randint(0, Board.length-1) 
                y = randint(0, Board.width-1)
                Board.tlist[t][0] = (x, y)
                Player.mlist.append((x, y))       #works but only changes the coord in tlist not in M attributes. Also possible that the monsters exist on top of one another.
       
class Eggs(Token): 
    def __init__(self):
        self.name = "Egg"
class Basket(Token):
    def __init__(self):
        self.name = "Basket"
        self.inventory = []
class Door(Token):   
    def __init__(self):
        self.name = "Door"
def main():
    board = Board()
    player = Player()

    board.create_board()
   
    roomcopy = []
    roomcopy = Board.rooms.copy()
    randcoord = []
    Board.mcount = int(input("How many monsters do you want to face? "))
    Board.ecount = int(input("How many eggs do you want to find? ")) 
    for _ in range(3+Board.mcount+Board.ecount):
        token = choice(roomcopy)
        randcoord.append(token)
        roomcopy.remove(token)  
    
    Board.tlist = []       
    door = Door()        
    door.coordinates = randcoord.pop()
    door.coordinates[1] = "D"
    Board.tlist.append(door.coordinates)
   
    basket = Basket()
    basket.coordinates = randcoord.pop()
    basket.coordinates[1] = "B"
    Board.tlist.append(basket.coordinates)

    for _ in range(Board.ecount): 
        egg = Eggs()
        egg.coordinates = randcoord.pop()
        egg.coordinates[1] = "E"
        Board.tlist.append(egg.coordinates)
        Player.elist.append(egg.coordinates[0])
    
    Player.coordinates = randcoord.pop([0][0])
    player.coordinates[1] = "P"
    Board.tlist.append(Player.coordinates)
    
    for _ in range(Board.mcount):
        monster = Monsters()
        monster.coordinates = randcoord.pop()
        monster.coordinates[1] = "M"
        Board.tlist.append(monster.coordinates)

    board.print_board()
    
    while player.end != True:
        player.pmove()
        monster.mmove(board)
        board.reset_board() 
        if player.coordinates[0] in player.mlist:
            print("A monster got you. You lose. Better luck next time.")
            player.end = True
        elif basket not in player.inventory:
            if player.coordinates[0] == basket.coordinates[0]:
                print("You found the basket! Now you can look for eggs.")
                player.inventory.append(basket)
                Board.tlist.remove(basket.coordinates)
        elif basket in player.inventory:
            if player.coordinates[0] in player.elist:
                print(f"You found egg number {(board.ecount+1)-len(player.elist)}")
                player.elist.remove(player.coordinates[0])
                player.inventory.append(egg)#need a way to ID which egg to remove from tlist
                board.tlist.remove([player.coordinates[0], "E|"])
                if player.elist == []:
                    print("You have all of the eggs. Find the door.")
            elif player.elist == []:
                if player.coordinates[0] == door.coordinates[0]:
                    print("You win! Congratulations!")
                    break

main()