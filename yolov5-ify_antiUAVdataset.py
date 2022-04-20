import os
from vid_to_frames import vid_to_frames
import json
import tqdm
import cv2


# switch for RGB or IR
img_type = 'RGB'


# create a 'IR' and 'RGB' folder and create the two folders 'images' and 'labels' in each
os.makedirs(img_type + '/images', exist_ok=True)
os.makedirs(img_type + '/labels', exist_ok=True)

# loop through al the folders in the 'test-dev' directory
for folder in tqdm.tqdm(os.listdir('test-dev')):
    # get the folder name as a string
    folder_name = str(folder)
    # in the folder, use the vid_to_frames() function from the vid_to_frames.py script to convert the "RGB.mp4" video to frames and save the frames to the 'images' folder
    img_files = vid_to_frames('test-dev/' + folder_name + '/' + img_type + '.mp4', img_type + '/images/', folder_name)
    
    # read the 'RGB_label.json' json and parse it into a dictionary
    labels_dict = json.loads(open('test-dev/' + folder_name + '/' + img_type + '_label.json').read())

    # ensure that length of img_files and labels_dict["gt_rect"] are the same
    assert len(img_files) == len(labels_dict["gt_rect"])

    # get width and height of the first image in img_files
    first_img = cv2.imread(img_files[0])
    img_width, img_height = ((first_img).shape[1], (first_img).shape[0])

    # loop through the img_files, while also getting the index of the current file
    for i, img_file in enumerate(img_files):
        # unpack the current label from the labels_dict
        label = labels_dict["gt_rect"][i]
        if label == []:
            # no label for this image, write a blank label
            with open(img_type + '/labels/' + img_file.split('.')[0].split('/')[-1] + '.txt', 'w') as f:
                pass
            continue
        x_center = label[0]
        y_center = label[1]
        width = label[2]
        height = label[3]


        # create a new label file in the 'labels' folder with the same name as the image file but with a '.txt' extension
        with open(img_type + '/labels/' + img_file.split('.')[0].split('/')[-1] + '.txt', 'w') as f:
            # normalize the x and y center coordinates and the width and height
            x_center = (x_center + width/2) / img_width
            y_center = (y_center + height/2) / img_height
            width = width / img_width
            height = height / img_height
            # write the x_center, y_center, width, height to the label file
            f.write("0" + ' ' + str(x_center) + ' ' + str(y_center) + ' ' + str(width) + ' ' + str(height))

