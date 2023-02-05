import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import cv2
import shutil


def add_data_pair(data, data_pair):
    data["imageID"].append(data_pair[0])
    data["label"].append(data_pair[1])


def create_label(inputs):
    allInputs = "w a s d q y h u i o j k l".split(" ")  # q: dash, y: FD, h: burst, p:RC, u:P, j:K, i:S, k:HS, o:D
    indexes = [allInputs.index(x) for x in inputs if x in allInputs]
    labels = np.zeros(len(allInputs), dtype=np.int32)
    labels[indexes] = 1
    return labels


def copy_image_to_labeled(img_unlabeled, imID, test=False):
    DIR = "./dataset/labeled"
    im_labeled = os.path.join(DIR, f"{imID}.{img_unlabeled.split('.')[-1]}")
    if test:
        print(im_labeled)
    else:
        shutil.copy(img_unlabeled, im_labeled)


def label_new_dataset(loops, lastID=0):
    imID = lastID + 1
    new_data = {"imageID": [], "label": []}
    DIR = "./dataset/unlabeled"
    plt.ion()
    fullnames = []
    for filename in os.listdir(DIR):
        fullname = os.path.join(DIR, filename)
        im = cv2.imread(fullname)
        plt.imshow(im)
        # plt.show()
        inputs = input("Enter game inputs:")
        if inputs == "b":
            os.remove(fullname)
            continue
        elif inputs == "q":
            break
        plt.close()
        label = create_label(inputs)
        add_data_pair(new_data, [imID, label])
        copy_image_to_labeled(fullname, imID)
        fullnames.append(fullname)
        imID += 1
        if imID - lastID > loops:
            break
    for name in fullnames:
        os.remove(name)
    return new_data


def main(loops=10000):
    labels_path = "labels.csv"
    df = pd.DataFrame({"imageID": [], "label": []})
    if os.path.exists(labels_path):
        df = pd.read_csv(labels_path)
    new_data = label_new_dataset(loops, df.shape[0])
    new_df = pd.DataFrame(new_data)
    new_df = pd.concat([df, new_df])
    new_df.to_csv(labels_path, encoding='utf-8', index=False)
    print(new_df)

def extract_frames(start=1,num_frames=1000000):
    vid_dir = "./dataset/video"
    unlabeled_dir = "./dataset/unlabeled"
    i = 1
    for filename in os.listdir(vid_dir):
        fullname = os.path.join(vid_dir, filename)
        vidcap = cv2.VideoCapture(fullname)
        vidcap.set(1, start)
        success, image = vidcap.read()
        count = 0
        shape = image.shape
        print([x//2 for x in shape])
        tc,bc,lc,rc = [int(shape[0]*0.78),int(shape[0]*(1-0.02)),int(shape[1]*0.72),int(shape[1]*(1-0.05))]
        while success:
            image = image[tc:bc, lc:rc]
            image = cv2.resize(image,(100,100))
            cv2.imwrite(f"{unlabeled_dir}/frame{count}.png", image)  # save frame as JPEG file
            success, image = vidcap.read()
            count += 1
            if count > num_frames:
                break


# main(20)
extract_frames(start=1)
