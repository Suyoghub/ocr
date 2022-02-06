import cv2 
import pickle 

with open("final.pickle","rb") as f:
    d = pickle.load(f)

for i in d:
    image,label = i 
    print(i)
    print(d)
