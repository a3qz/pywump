#Ryan Michalec
import random

class WumpController: 
	def __init__(self):
		self.num_arrows = 5
		self.playerLocation = 0
		self.wumpLocation = 0
		self.dead = False

		num_rooms = 20
		self.graph = {}
		self.graph = {
			1:[2,5,8],
			2:[1,3,10],
			3:[2,4,12],
			4:[3,5,14],
			5:[1,4,6],
			6:[5,7,15],
			7:[6,8,17],
			8:[1,7,11],
			9:[10,12,19],
			10:[1,9,11],
			11:[8,10,20],
			12:[3,9,13],
			13:[12,14,18],
			14:[4,13,15],
			15:[6,14,16],
			16:[15,17,18],
			17:[7,16,20],
			18:[13,16,19],
			19:[9,18,20],
			20:[11,17,19]
			}

		self.contains = {}
		hazards = ["B", "B", "H", "H"]
		for room in range(1,21):
			self.contains[room] = ""

		# make list to draw from
		tempList = list(range(1,21))
		random.shuffle(tempList)

		# choose unique starting locations for the fixed hazards 
		random.shuffle(tempList)
		locationlist = tempList[:4]
		for num in list(range(4)):
			self.contains[locationlist[num]] = hazards[num]
		
		# put the wumpus anywhere
		self.wumpLocation = random.choice(range(1,21))

		# put the player in an unoccupied space
		self.playerLocation = random.choice(range(1,21))
		while(self.contains[self.playerLocation] != "" or self.playerLocation == self.wumpLocation):
			self.playerLocation = random.choice(range(num_rooms))

		# create the transformations for randomizing room numbers
		self.CreateTranslation()


	
	def ReadAdjacentRooms(self, currentRoomNum):
		output = ""
		for adj in random.sample(self.graph[currentRoomNum], 3):
			if(adj == self.wumpLocation):
				output += "I SMELL A WUMPUS\n"
			if(self.contains[adj] == "B"):
				output += "BATS NEARBY\n"
			if(self.contains[adj] == "H"):
				output += "I FEEL A DRAFT\n"
		return output

	def CreateTranslation(self):
		temp = random.sample(range(1, 21), 20)
		self.InToSelfArray = {}
		self.SelfToOutArray = {}
		for index, value in enumerate(temp):
			self.InToSelfArray[value] = index+1
			self.SelfToOutArray[index+1] = value

	def TranslateIncomingToSelf(self,incomingnumber):
		return self.InToSelfArray[incomingnumber]
		
	
	def TranslateSelfToOut(self,outgoingnumber):
		return self.SelfToOutArray[outgoingnumber]

	def MovePlayer(self, newRoom):
		if self.dead:
			return "CANNOT MOVE WHEN DEAD"
		
		newRoom = self.TranslateIncomingToSelf(newRoom)
		output = ""
		if newRoom in self.graph[self.playerLocation]:
			self.playerLocation = newRoom
			output += self.CheckCurrentRoom()
		else:
			output = "NOT POSSIBLE\n"
		if not self.dead:
			output += self.ReadAdjacentRooms(self.playerLocation)
			output += "YOU ARE IN CAVE {}\n".format(self.TranslateSelfToOut(self.playerLocation))
			output += "TUNNELS LEAD TO CAVES "
			output += str(self.TranslateSelfToOut(self.graph[self.playerLocation][0])) + " "
			output += str(self.TranslateSelfToOut(self.graph[self.playerLocation][1])) + " "
			output += str(self.TranslateSelfToOut(self.graph[self.playerLocation][2]))
		else:
			output += "HA HA HA - YOU LOSE!"
		return output 

	def ShootArrow(self, roomArray):
		if self.dead:
			return "CANNOT SHOOT WHEN DEAD"
		elif self.num_arrows == 0:
			return "NO MORE ARROWS"
		output = ""
		self.num_arrows -= 1
		roomArray = [self.TranslateIncomingToSelf(i) for i in roomArray]
		arrowLocation = self.playerLocation
		shotWumpus = False
		shotSelf = False
		wokeWumpus = False
		arrowPossibilities = self.graph[arrowLocation]
		for room in roomArray:
			if room in arrowPossibilities or room == self.playerLocation:
				arrowLocation = room
			else:
				arrowLocation = random.choice(arrowPossibilities)
			if arrowLocation == self.playerLocation:
				shotSelf = True
			if arrowLocation == self.wumpLocation:
				shotWumpus = True
			arrowPossibilities = self.graph[arrowLocation]
			if self.wumpLocation in arrowPossibilities:
				wokeWumpus = True
		if shotSelf:
			output += "SHOT YOURSELF\n"
			self.dead = True
		elif shotWumpus:
			output += "AHA! YOU GOT THE WUMPUS!\n" 
			output += "HEE HEE HEE - THE WUMPUS'LL GETCHA NEXT TIME!!\n"
			return output
		elif wokeWumpus:
			output += self.WumpWake()
		if not self.dead:
			output += self.ReadAdjacentRooms(self.playerLocation)
			output += "YOU ARE IN CAVE {}\n".format(self.TranslateSelfToOut(self.playerLocation))
			output += "TUNNELS LEAD TO CAVES "
			output += str(self.TranslateSelfToOut(self.graph[self.playerLocation][0])) + " "
			output += str(self.TranslateSelfToOut(self.graph[self.playerLocation][1])) + " "
			output += str(self.TranslateSelfToOut(self.graph[self.playerLocation][2]))
		else:
			output += "HA HA HA - YOU LOSE!"
		return output
	def GetArrowCount(self):
		output = str(self.num_arrows) + " ARROWS REMAINING\n"
		output += self.ReadAdjacentRooms(self.playerLocation)
		output += "YOU ARE IN CAVE {}\n".format(self.TranslateSelfToOut(self.playerLocation))
		output += "TUNNELS LEAD TO CAVES "
		output += str(self.TranslateSelfToOut(self.graph[self.playerLocation][0])) + " "
		output += str(self.TranslateSelfToOut(self.graph[self.playerLocation][1])) + " "
		output += str(self.TranslateSelfToOut(self.graph[self.playerLocation][2]))
		return output
	def CheckCurrentRoom(self):
		output = ""
		if(self.playerLocation == self.wumpLocation):
			output += "...OOPS! BUMPED A WUMPUS!\n"
			output += self.WumpWake()
		if(self.contains[self.playerLocation] == 'H'):
			output += "YYYIIIIEEEE . . . FELL IN PIT\n"
			self.dead = True
		elif(self.contains[self.playerLocation] == 'B'):
			self.BatTravel()
			output += "ZAP--SUPER BAT SNATCH! ELSEWHEREVILLE FOR YOU!\n"
			self.CheckCurrentRoom()
		return output

	def BatTravel(self):
		self.playerLocation = random.choice(list(self.InToSelfArray.keys()))

	def WumpWake(self):
		output = ""
		result = random.choice([0,1,2,3])
		if(result != 3):
			self.WumpMove()
			output += "THE WUMPUS MOVED!\n"
		if self.wumpLocation == self.playerLocation:
			output += "TSK TSK TSK- WUMPUS GOT YOU!\n"
			self.dead = True
		return output

	def WumpMove(self):
		self.wumpLocation = random.choice(self.graph[self.wumpLocation])

	def Reset(self):
		self.__init__()
		output = ""
		output += """WELCOME TO 'HUNT THE WUMPUS'
  THE WUMPUS LIVES IN A CAVE OF 20 ROOMS. EACH ROOM
HAS 3 TUNNELS LEADING TO OTHER ROOMS. (LOOK AT A
DODECAHEDRON TO SEE HOW THIS WORKS-IF YOU DON'T KNOW
WHAT A DODECAHEDRON IS, ASK SOMEONE)

     HAZARDS:
 BOTTOMLESS PITS - TWO ROOMS HAVE BOTTOMLESS PITS IN THEM
     IF YOU GO THERE, YOU FALL INTO THE PIT (& LOSE!)
 SUPER BATS - TWO OTHER ROOMS HAVE SUPER BATS. IF YOU
     GO THERE, A BAT GRABS YOU AND TAKES YOU TO SOME OTHER
     ROOM AT RANDOM. (WHICH MIGHT BE TROUBLESOME)

     WUMPUS:
 THE WUMPUS IS NOT BOTHERED BY THE HAZARDS (HE HAS SUCKER
 FEET AND IS TOO BIG FOR A BAT TO LIFT).  USUALLY
 HE IS ASLEEP. TWO THINGS WAKE HIM UP: YOUR ENTERING
 HIS ROOM OR YOUR SHOOTING AN ARROW.
     IF THE WUMPUS WAKES, HE MOVES (P=.75) ONE ROOM
 OR STAYS STILL (P=.25). AFTER THAT, IF HE IS WHERE YOU
 ARE, HE EATS YOU UP (& YOU LOSE!)

     YOU:
 EACH TURN YOU MAY MOVE OR SHOOT A CROOKED ARROW
   MOVING: YOU CAN GO ONE ROOM (THRU ONE TUNNEL)
   ARROWS: YOU HAVE 5 ARROWS. YOU LOSE WHEN YOU RUN OUT.
   EACH ARROW CAN GO FROM 1 TO 5 ROOMS. YOU AIM BY TELLING
   THE COMPUTER THE ROOM#S YOU WANT THE ARROW TO GO TO.
   IF THE ARROW CAN'T GO THAT WAY (IE NO TUNNEL) IT MOVES
   AT RAMDOM TO THE NEXT ROOM.
     IF THE ARROW HITS THE WUMPUS, YOU WIN.
     IF THE ARROW HITS YOU, YOU LOSE.

    WARNINGS:
     WHEN YOU ARE ONE ROOM AWAY FROM WUMPUS OR HAZARD,
    THE COMPUTER SAYS:
 WUMPUS-  'I SMELL A WUMPUS'
 BAT   -  'BATS NEARBY'
 PIT   -  'I FEEL A DRAFT'
"""
		output += "\n\n" + self.ReadAdjacentRooms(self.playerLocation)
		output += "YOU ARE IN CAVE {}\n".format(self.TranslateSelfToOut(self.playerLocation))
		output += "TUNNELS LEAD TO CAVES "
		output += str(self.TranslateSelfToOut(self.graph[self.playerLocation][0])) + " "
		output += str(self.TranslateSelfToOut(self.graph[self.playerLocation][1])) + " "
		output += str(self.TranslateSelfToOut(self.graph[self.playerLocation][2]))
		return output


if __name__ == "__main__":
	cont = WumpController()
	
	while True:
		s = input().rstrip()
		print("\n")
		y = s.split()
		if y[0] == "n":
			print(cont.Reset())
		elif y[0] == 'm':
			print(cont.MovePlayer(int(y[1])))
		elif y[0] == 's':
			print(cont.ShootArrow([int(i) for i in y[1:]]))
		elif y[0] == 'a':
			print(cont.GetArrowCount())