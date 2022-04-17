import os
from PIL import Image
import shutil

folder_a ='./image/game/'

list1=[]

for i in os.listdir(folder_a):
    if os.path.isfile(folder_a + i):
        list1.append(i)

for i in range(len(list1)):
    imagefile = os.path.join(folder_a, list1[i])
    imagedata = Image.open(imagefile)
    newimage = folder_a + list1[i][:-4] + ".webp"
    print(newimage)
    imagedata.save(newimage, quality=95, optimize=True)