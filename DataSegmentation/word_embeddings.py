from base64 import encode
import os
import pickletools
from typing import final
import cv2
import pickle


final_array = list()
labels = list()

embedding = set()


def encode_label(s):
    encoded_word = list()
    d = dict()
    #TODO: creating new embeddings
    # base = os.path.join(os.getcwd(),"dataset")
    # for _,_,i in os.walk(base):
    #     for each_file in i:
    #         if each_file.endswith(".jpg"):
    #             path = os.path.join(base,each_file) 
    #             label = each_file[:-4].split(" ")
    #             for each_word in label:
    #                 embedding.add(each_word)

    # for index,each_word in enumerate(embedding):
    #     d[each_word] = index
    
    # with open("embeddings.pickle","wb") as f: 
    #     pickle.dump(d,f)

    #end TODO
    with open("embeddings.pickle","rb") as f:
        d = pickle.load(f)
    
    print(d)
    for i in s.split(" "):
        if d[i]:
            print(f"{i} -> {d[i]}")
            encoded_word.append(d[i])

    return encoded_word

def get_images():
    base = os.path.join(os.getcwd(),"dataset")
    for _,_,i in os.walk(base):
        for each_file in i:
            if each_file.endswith(".jpg"):
                path = os.path.join(base,each_file)
                label = each_file[:-4]
                
                image = cv2.imread(path)
                embedded_label = encode_label(label)
                final_array.append([image,embedded_label])
                cv2.imshow(label,image)
                cv2.waitKey(100)
                # os.remove(each_file)

    
    with open("final.pickle","wb") as f:
        pickle.dump(final_array,f)
        
    return final_array

if __name__ == "__main__":
    print(get_images())