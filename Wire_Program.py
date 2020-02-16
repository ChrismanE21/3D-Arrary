#Three Dimensional Cellular Automata Motifs

import cv2
import numpy as np

#Wire World
wireColor=(128,128,128)
notWireColor=(0,0,0)
electronColor=(0,255,255)
tailColor=(0,128,255)
wire=1
notWire=0
electron=3
tail=2

#Game of Life
aliveColor = (200,200,200)
deadColor = (255,255,255)
alive = 1
dead = 0


def show(img, wait = 30, title = "image"):#Shows the picture
    d = np.max(img.shape)
    h, w = img.shape[:2]
    unitSize = 500//d
    resized = cv2.resize(np.uint8(img), (unitSize*w,unitSize*h), interpolation = cv2.INTER_AREA)
    cv2.imshow(title, resized)
    cv2.waitKey(wait)  # 0 means wait for key input. postive value waits for that many milliseconds
    
def showWireWorld(allLayers, wait = 0 , title = "image"):#Paints the picture for Wire World
	number_of_layers = len(allLayers)

	for x in range(number_of_layers):
		
		name = str(x)
		
		h,w = allLayers[x].shape[:2]
		out = np.zeros((h,w,3))

		out[allLayers[x]==wire]=wireColor
		out[allLayers[x]==notWire]=notWireColor
		out[allLayers[x]==electron]=electronColor
		out[allLayers[x]==tail]=tailColor
		
		show(out, wait = wait ,title = name)
		
def showGameOfLife(allLayers, wait = 0, title = "image"):#Paints the picture for Conway's Game of Life
	number_of_layers = len(allLayers)
	
	for x in range(number_of_layers):
		
		name = str(x)
		
		h,w = allLayers[x].shape[:2]
		out = np.zeros((h,w,3))
		
		out[allLayers[x] == dead] = deadColor
		out[allLayers[x] == alive] = aliveColor
		
		show(out, wait = wait, title = name)
		
def loadWireWorld(filename):#Extracts a picture from a file
    img=cv2.imread(filename)
    h,w = img.shape[:2]
    out = np.zeros((h,w))
    out[img[:,:,1]<100]=notWire
    out[img[:,:,1]>150]=electron
    out[np.logical_and(img[:,:,1]<150,img[:,:,2]>150)]=tail
    out[np.logical_and(img[:,:,1]<150,img[:,:,0]>100)]=wire
    return out
    
def loadGameofLife(filename):
	img=cv2.imread(filename)
	h,w = img.shape[:2]
	out = np.zeros((h,w))
	out[img[:, :, 1]<100] = alive
	out[img[:, :, 1]>=150] = dead
	return out

def iterateWireWorld(allLayers):#Appiyes the rules for Wrie World
	newLayers = allLayers.copy()
    
	kernel_current = np.int16([[1,1,1],[1,0,1],[1,1,1]])
	kernel_near = np.int16([[0,0,0],[0,1,0],[0,0,0]])
    
	for x in range(number_of_layers):
		
		#This set up avoids an index error with lifeCheckThree
		if(x != number_of_layers - 1):
			lifeCheckOne = np.int16(allLayers[x] == electron)
			lifeCheckTwo = np.int16(allLayers[x-1] == electron)
			lifeCheckThree = np.int16(allLayers[x+1] == electron)
		else:
			lifeCheckOne = np.int16(allLayers[x] == electron)
			lifeCheckTwo = np.int16(allLayers[x-1] == electron)
			lifeCheckThree = np.int16(allLayers[x-number_of_layers+1] == electron)
	
		neighborCount = cv2.filter2D(lifeCheckOne,-1,kernel_current,borderType=cv2.BORDER_CONSTANT,)
		neighborCount = neighborCount + cv2.filter2D(lifeCheckTwo,-1,kernel_near,borderType = cv2.BORDER_CONSTANT,)
		neighborCount = neighborCount + cv2.filter2D(lifeCheckThree,-1,kernel_near,borderType = cv2.BORDER_CONSTANT,)
		
		newLayers[x][allLayers[x] == notWire]= notWire
		newLayers[x][allLayers[x] == electron]= tail
		newLayers[x][allLayers[x] == tail]= wire
		newLayers[x][allLayers[x] == wire]= wire
		newLayers[x][np.logical_and(np.logical_and(allLayers[x] == wire,1<=neighborCount),neighborCount<=2)]=electron
    
	return newLayers

def iterateGameOfLife(allLayers):
	newLayers = allLayers.copy() * 1 #creats a copy
	
	kernel_current = np.int16([[1 ,1 ,1], [1, 0, 1], [1, 1, 1]])
	kernel_near = np.int16([[1 ,1 ,1], [1, 1, 1], [1, 1, 1]])#How gets counted as a person
	
	for x in range(number_of_layers):
	
		if(x != number_of_layers - 1):
			lifeCheckOne = np.int16(allLayers[x] == alive)
			lifeCheckTwo = np.int16(allLayers[x-1] == alive)
			lifeCheckThree = np.int16(allLayers[x+1] == alive)
		else:
			lifeCheckOne = np.int16(allLayers[x] == alive)
			lifeCheckTwo = np.int16(allLayers[x-1] == alive)
			lifeCheckThree = np.int16(allLayers[x-number_of_layers+1] == alive)

		neighborCount = cv2.filter2D(lifeCheckOne,-1,kernel_current,borderType=cv2.BORDER_CONSTANT,)
		neighborCount = neighborCount + cv2.filter2D(lifeCheckTwo,-1,kernel_near,borderType = cv2.BORDER_CONSTANT,)
		neighborCount = neighborCount + cv2.filter2D(lifeCheckThree,-1,kernel_near,borderType = cv2.BORDER_CONSTANT,)

		newLayers[x][np.logical_and(allLayers[x] == alive, 7 > neighborCount)] = dead #under population
		newLayers[x][np.logical_and(allLayers[x] == alive, 12 < neighborCount)] = dead #over population
		newLayers[x][np.logical_and(allLayers[x] == dead, np.logical_and(neighborCount >= 7, neighborCount <= 12))] = alive #revive
		
	return newLayers
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

allLayers = [] #list of pictures
listNames = []
doneTypeing = 0
number_of_layers = 0

fps = 40 #speed

correct = 0
print("Type rule set to contuine.\nGame of Life\nWire World\n")

while (correct == 0):
	rules = input(" ")
	if (rules != "Game of Life" and rules != "Wire World"):
		print("Sorry! Your choice may have a typo.")
	else:
		correct = 1

print("Good, next enter the files names with their extenstions")		

while rules == "Game of Life":#Game of Life Game
	while doneTypeing == 0:#user types file names and the picture is turn into a arrary; which is put into a arrary of arraries allLayers
		world = input(" ")
	
		if world != "END": 
			listNames.append(world)
			world = loadGameofLife("" +world+ "")
			allLayers.append(world)
		else:
			doneTypeing = 1
	
	number_of_layers = len(allLayers)
	
	showGameOfLife(allLayers,1000//fps, number_of_layers)
	allLayers = iterateGameOfLife (allLayers)

while rules == "Wire World":#Wire World Game
	while doneTypeing == 0:#user types file names and the picture is turn into a arrary; which is put into a arrary of arraries allLayers
		world = input(" ")
	
		if world != "END":
			listNames.append(world)
			world = loadWireWorld("" +world+ "")
			allLayers.append(world)
		else:
			doneTypeing = 1
	
	number_of_layers = len(allLayers)
	
	showWireWorld(allLayers,1000//fps, number_of_layers)
	allLayers = iterateWireWorld (allLayers)
#third dem. celluar automata
