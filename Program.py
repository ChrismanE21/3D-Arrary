import cv2
import numpy as np

#Sets up veribles
aliveColor = (0,255,255)
deadColor = (0)

alive = 1
dead = 0

def show(img, title="image", wait=30):
    d = np.max(img.shape)
    h, w = img.shape[:2]
    unitSize = 500//d
    resized = cv2.resize(np.uint8(img), (unitSize*w,unitSize*h), interpolation = cv2.INTER_AREA)
    cv2.imshow(title, resized)
    cv2.waitKey(wait) 
	
def showCA(ca, wait=0,title="image"):
    h,w = ca.shape[:2]
    out = np.zeros((h,w,3))

    out[ca == alive] = aliveColor
    out[ca == dead] = deadColor
    show(out, wait = wait,title=title)

#This loads in the picture and idenfies what it shows
def load(filename):
    img = cv2.imread(filename)
    h,w = img.shape[:2]
    out = np.zeros((h,w))
    out[img[:, :, 1]<100] = alive
    out[img[:, :, 1]>=150] = dead
    return out
    
#This updates the pictures while keeping the old picture
def iterate(layerOne,layerTwo,layerThree):
	print(layerOne)
	
	newGenTown = layerOne * 1 #creats a copy
	
	
	kernel_1 = np.int16([[0 ,1 ,0], [1, 0, 1], [0, 1, 0]])#adds connections
	kernel_2 = np.int16([[0 ,0 ,0], [0, 1, 0], [0, 0, 0]])#town2 connection
	kernel_3 = np.int16([[0 ,0 ,0], [0, 1, 0], [0, 0, 0]])#town3 connection
	
	lifeCheckOne = np.int16(layerOne == alive)
	lifeCheckTwo = np.int16(layerTwo == alive)
	lifeCheckThree = np.int16(layerThree == alive)
	
	neighborCount = cv2.filter2D(lifeCheckOne,-1,kernel_1,borderType=cv2.BORDER_CONSTANT,)
	neighborCount = neighborCount + cv2.filter2D(lifeCheckTwo,-1,kernel_2,borderType = cv2.BORDER_CONSTANT,)
	neighborCount = neighborCount + cv2.filter2D(lifeCheckThree,-1,kernel_3,borderType = cv2.BORDER_CONSTANT,)
	
	newGenTown[np.logical_and(layerOne == alive, 2 > neighborCount)] = dead #under population
	newGenTown[np.logical_and(layerOne == alive, 4 < neighborCount)] = dead #over population
	newGenTown[np.logical_and(layerOne == dead, 3 == neighborCount)] = alive #revive
	return newGenTown

#Loads the picture to be used as data.
town = load("image1.png")
town2 = load("image2.png")
town3 = load("image3.png")
fps=2

#Plays the picture
while True:
	showCA(town,1000//fps,title="1")
	town  = iterate (town,town2,town3)
	showCA(town2,1000//fps,title="2")
	town2  = iterate (town2,town,town3)
	showCA(town3,1000//fps,title="3")
	town3  = iterate (town3,town,town2)
	
    

#//////////////////////////////////////////////////////////////////////////////////////////////////////




	





