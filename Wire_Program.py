import cv2
import numpy as np

wireColor=(128,128,128)
notWireColor=(0,0,0)
electronColor=(0,255,255)
tailColor=(0,128,255)

wire=1
notWire=0
electron=3
tail=2


def show(img, title="image", wait=30):
    d=np.max(img.shape)
    h,w=img.shape[:2]
    unitSize=120//d
    resized = cv2.resize(np.uint8(img), (unitSize*w,unitSize*h), interpolation = cv2.INTER_AREA)
    cv2.imshow(title, resized)
    cv2.waitKey(wait) # 0 means wait for key input. postive value waits for that many milliseconds
    
def showCA(ca, wait=0):
    h,w = ca.shape[:2]
    out = np.zeros((h,w,3))

    out[ca==wire]=wireColor
    out[ca==notWire]=notWireColor
    out[ca==electron]=electronColor
    out[ca==tail]=tailColor
    show(out, wait=wait)
    
def load(filename):
    img=cv2.imread(filename)
    h,w = img.shape[:2]
    out = np.zeros((h,w))
    out[img[:,:,1]<100]=notWire
    out[img[:,:,1]>150]=electron
    out[np.logical_and(img[:,:,1]<150,img[:,:,2]>150)]=tail
    out[np.logical_and(img[:,:,1]<150,img[:,:,0]>100)]=wire
    return out
    
    

def iterate(world):
    newWorld=world*1
    kernel=np.int16([[1,1,1],
                     [1,0,1],
                     [1,1,1]])
    whereTheElectronsAre=np.int16(world==electron)
    neighborCount=cv2.filter2D(whereTheElectronsAre,-1,kernel,borderType=cv2.BORDER_CONSTANT)
    newWorld[world==notWire]=notWire
    newWorld[world==electron]=tail
    newWorld[world==tail]=wire
    newWorld[world==wire]=wire
    newWorld[np.logical_and(np.logical_and(world==wire,1<=neighborCount),neighborCount<=2)]=electron
    return newWorld



world=np.array([[0,0,0,0,0],
                [0,0,0,0,0],
                [1,1,1,3,0],
                [0,0,0,0,1],
                [0,0,0,0,1]])

import cv2
import numpy as np

wireColor=(128,128,128)
notWireColor=(0,0,0)
electronColor=(0,255,255)
tailColor=(0,128,255)

wire=1
notWire=0
electron=3
tail=2


def show(img, title="image", wait=30):
    d=np.max(img.shape)
    h,w=img.shape[:2]
    unitSize=1200//d
    resized = cv2.resize(np.uint8(img), (unitSize*w,unitSize*h), interpolation = cv2.INTER_AREA)
    cv2.imshow(title, resized)
    cv2.waitKey(wait) # 0 means wait for key input. postive value waits for that many milliseconds
    
def showCA(ca, wait=0,title = "image"):
    h,w = ca.shape[:2]
    out = np.zeros((h,w,3))

    out[ca==wire]=wireColor
    out[ca==notWire]=notWireColor
    out[ca==electron]=electronColor
    out[ca==tail]=tailColor
    show(out, wait = wait,title=title)
    
def load(filename):
    img=cv2.imread(filename)
    h,w = img.shape[:2]
    out = np.zeros((h,w))
    out[img[:,:,1]<100]=notWire
    out[img[:,:,1]>150]=electron
    out[np.logical_and(img[:,:,1]<150,img[:,:,2]>150)]=tail
    out[np.logical_and(img[:,:,1]<150,img[:,:,0]>100)]=wire
    return out
    
    

def iterate(layerOne,layerTwo,layerThree):
    newWorld=layerOne*1
    
    kernel_1 = np.int16([[1,1,1],[1,0,1],[1,1,1]])
    kernel_2 = np.int16([[0,0,0],[0,1,0],[0,0,0]])
    kernel_3 = np.int16([[0,0,0],[0,1,0],[0,0,0]])
    
    lifeCheckOne = np.int16(layerOne == electron)
    lifeCheckTwo = np.int16(layerTwo == electron)
    lifeCheckThree = np.int16(layerThree == electron)
	
    neighborCount = cv2.filter2D(lifeCheckOne,-1,kernel_1,borderType=cv2.BORDER_CONSTANT,)
    neighborCount = neighborCount + cv2.filter2D(lifeCheckTwo,-1,kernel_2,borderType = cv2.BORDER_CONSTANT,)
    neighborCount = neighborCount + cv2.filter2D(lifeCheckThree,-1,kernel_3,borderType = cv2.BORDER_CONSTANT,)
    
    newWorld[layerOne==notWire]=notWire
    newWorld[layerOne==electron]=tail
    newWorld[layerOne==tail]=wire
    newWorld[layerOne==wire]=wire
    newWorld[np.logical_and(np.logical_and(layerOne==wire,1<=neighborCount),neighborCount<=2)]=electron
    return newWorld

world=load("image4.png")
world2=load("image5.png")
world3=load("image6.png")

fps = 1000

while True:
    showCA(world,1000//fps,title="1")
    world=iterate(world,world2,world3)
    
    showCA(world2,1000//fps,title="2")
    world2=iterate(world2,world3,world)
    
    showCA(world3,1000//fps,title="3")
    world3=iterate(world3,world,world2)
