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
    
def showCA(ca, wait=0, title = "image"):
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

town = load("image4.png")
town2 = load("image5.png")
town3 = load("image6.png")
fps=2

#Plays the picture
while True:
	showCA(town,1000//fps,title="1")
	town  = iterate (town,town2,town3)
	showCA(town2,1000//fps,title="2")
	town2  = iterate (town2,town,town3)
	showCA(town3,1000//fps,title="3")
	town3  = iterate (town3,town,town2)
