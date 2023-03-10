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
    allInputs = "w a s d u i o p j k l ; m".split(" ")
    # up:w down:s left:a right:d
    # P:u K:i S:o HS:p
    # D:j Dash:k RC:l Taunt:';' DF:m
    indexes = [allInputs.index(x) for x in inputs if x in allInputs]
    labels = np.zeros(len(allInputs), dtype=np.int32)
    labels[indexes] = 1
    return labels


def copy_image_to_labeled(img_unlabeled, imID, test=True):
    DIR = "./dataset/labeled"
    im_labeled = os.path.join(DIR, f"{imID}.{img_unlabeled.split('.')[-1]}")
    if test:
        print(f"{img_unlabeled} to {im_labeled}")
    else:
        shutil.copy(img_unlabeled, im_labeled)


def label_new_dataset(start,loops, lastID=0):
    imID = lastID + 1
    new_data = {"imageID": [], "label": []}
    DIR = "./dataset/unlabeled"
    plt.ion()
    fullnames = []
    filenames = []
    for filename in os.listdir(DIR):
        filenames.append(filename)
    filenames.sort()
    print(len(filenames[start:-1]))
    for filename in filenames[start:-1]:
        fullname = os.path.join(DIR, filename)
        im = cv2.imread(fullname)
        plt.imshow(im)
        inputs = input("Enter game inputs:")
        if inputs == "b":
            os.remove(fullname)
            print("removed"+fullname)
            continue
        elif inputs == "q":
            print("ended")
            break
        label = create_label(inputs)
        add_data_pair(new_data, [imID, label])
        copy_image_to_labeled(fullname, imID, test=False)
        fullnames.append(fullname)
        imID += 1
        if imID - lastID > loops:
            break
    # for name in fullnames:
    #     os.remove(name)
    return new_data


def main(start=0,loops=10000):
    labels_path = "labels.csv"
    df = pd.DataFrame({"imageID": [], "label": []})
    if os.path.exists(labels_path):
        df = pd.read_csv(labels_path)
    start = df.shape[0]
    print(start)
    new_data = label_new_dataset(start, loops, df.shape[0])
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
        tc,bc,lc,rc = [int(shape[0]*0.78),int(shape[0]*(1-0.02)),int(shape[1]*0.72),int(shape[1]*(1-0.05))]
        while success:
            image = image[tc:bc, lc:rc]
            image = cv2.resize(image,(100,100))
            cv2.imwrite(f"{unlabeled_dir}/frame{count:06}.png", image)  # save frame as JPEG file
            success, image = vidcap.read()
            count += 1
            if count > num_frames:
                break


main(start=0,loops=30)
# extract_frames(start=1,num_frames=1000000)
