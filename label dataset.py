import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import cv2
import shutil

def add_data_pair(data,data_pair):
    data["imageID"].append(data_pair[0])
    data["label"].append(data_pair[1])
    
def create_label(inputs):
    allInputs = ["w","a","s","d"]
    indexes = [allInputs.index(x) for x in inputs if x in allInputs]
    labels = np.zeros(len(allInputs),dtype=np.int32)
    labels[indexes] = 1
    return labels


def copy_image_to_labeled(img_unlabeled,imID,test=False):
    DIR = "./dataset/labeled"
    im_labeled = os.path.join(DIR,f"{imID}.{img_unlabeled.split('.')[-1]}")
    if test:
        print(im_labeled)
    else:
        shutil.copy(img_unlabeled,im_labeled)


def label_new_dataset(loops,lastID=0):
    imID = lastID+1
    new_data = {"imageID":[],"label":[]}
    DIR = "./dataset/unlabeled"
    plt.ion()
    fullnames = []
    for filename in os.listdir(DIR):
        fullname = os.path.join(DIR,filename)
        im = cv2.imread(fullname)
        plt.imshow(im)
        inputs = input("Enter game inputs:")
        label = create_label(inputs)
        add_data_pair(new_data,[imID,label])
        copy_image_to_labeled(fullname,imID)
        fullnames.append(fullname)
        imID += 1
        if imID-lastID>loops:
            break
    for name in fullnames:
        os.remove(name)
    return new_data

def main(loops=10000):
    labels_path = "labels.csv"
    df = pd.DataFrame({"imageID":[],"label":[]})
    if os.path.exists(labels_path):
        df = pd.read_csv(labels_path)
    new_data = label_new_dataset(loops,df.shape[0])
    new_df = pd.DataFrame(new_data)
    new_df = pd.concat([df,new_df])
    new_df.to_csv(labels_path, encoding='utf-8', index=False)
    print(new_df)

main(10)
