#!/usr/bin/python

# Copyright (C) 1015 

# Author: Vinod NK

"""
Script to copy images from origin to target path.

When an image is created in target path, the creation date of this image is
the creation date of the origin directory. This is because if exists a new folder
in the origin path, all photos has highest priority to copy in the target path.

For check if one image on target path has a new image to replace it,
get the last modified date of the target image and compare with the creation
date of origin directory. If the directory creation date is greater than the
last modified date of image, replace the image.
"""

import os
import imghdr
from stat import *
from PIL import Image

base_width = 300
path = "/apps/images/Fotos/"
target = "/apps/images/"
dirs = os.listdir(path)

def create_image(original_image, local_image, date_dir):
    try:
        print("Creating...")
        im = Image.open(original_image)
        # Resize the image
        wpercent = (base_width / float(im.size[0]))
        hsize = int((float(im.size[1]) * float(wpercent)))
        im = im.resize((base_width, hsize))
        file_image = open(local_image, 'w+')
        im.save(local_image)
        st = os.stat(local_image)
        os.utime(local_image, (st[ST_ATIME], date_dir))
        print("OK date new image: ", date_dir)
    except OSError:
        print("Oops! cannot create image OSError: " + original_image)
    except IOError:
        print("Oops! cannot create image IOError: " + original_image)

for file in dirs:
    dir_path = path + file + "/"

    if os.path.isdir(dir_path) and not os.listdir(dir_path) == []:
        # Get the creation date of directory
        date_dir = os.path.getctime(dir_path)
        print("\nDir: " + dir_path + ", Date str: ", date_dir)

        for image in os.listdir(dir_path):
            dir_image = dir_path + image
            extension = imghdr.what(dir_image);

            # If the file is a imge jpeg (if if added new extensio, check authLoginLogicV2 mashup)
            if os.path.isfile(dir_image) and extension == "jpeg":
                print("Image: " + dir_image)
                # Create name of directory fot the local image.
                local_image = target + image

                if os.path.exists(local_image):
                    print("Image exists")
                    date_file = os.path.getmtime(local_image)
                    print("Date image", date_file)

                    if int(date_dir) > int(date_file):
			print("Create image")
                        create_image(dir_image, local_image, date_dir)
                else:
                    print("Image no exists")
                    create_image(dir_image, local_image, date_dir)
