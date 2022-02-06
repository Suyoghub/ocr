import cv2 
import pickle 

with open("embeddings.pickle","rb") as f:
    d = pickle.load(f)

print(d)