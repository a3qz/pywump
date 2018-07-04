#Ryan Michalec
import random

class WumpController: 
	def __init__(self):
		self.num_arrows = 5

		num_rooms = 20
		self.graph = {}
		self.contains = {}
		hazards = ["B", "B", "H", "H"]
		for room in range(num_rooms):
			self.graph[room] = []
			self.contains[room] = ""

		# make list to draw from
		tempList = list(range(num_rooms))
		random.shuffle(tempList)

		# for each room, get it a valid neighbor if it has < 3 neighbors
		for room in tempList:
			while len(self.graph[room]) < 3: 
				# choose another room at random; skip if self or already has three neighbors
				test = random.choice(range(num_rooms))
				if(test != room and len(self.graph[test]) != 3):
					self.graph[room].append(test)
					self.graph[test].append(room)

		# choose unique starting locations for the fixed hazards 
		random.shuffle(tempList)
		locationlist = tempList[:4]
		for num in list(range(4)):
			self.contains[locationlist[num]] = hazards[num]
		
		# put the wumpus anywhere
		self.wumpLocation = random.choice(range(num_rooms))

		# put the player in an unoccupied space
		self.playerLocation = random.choice(range(num_rooms))
		while(self.contains[self.playerLocation] != "" or self.playerLocation == self.wumpLocation):
			self.playerLocation = random.choice(range(num_rooms))

		# debug code, remove
		for x in self.contains:
			print(x, ": ", self.contains[x])
		print(self.playerLocation)
		print(self.wumpLocation)
	
	def Reset(self):
		self.__init__()
		pass

if __name__ == "__main__":
	WumpController2 = WumpController()