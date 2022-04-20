import os
from PIL import Image

folder_a ='./image/game/'

list1=[]

for i in os.listdir(folder_a):
    if os.path.isfile(folder_a + i):
        list1.append(i)

for i in range(len(list1)):
    imagefile = os.path.join(folder_a, list1[i])
    imagedata = Image.open(imagefile)
    if ".webp" not in list1[i] :
     newimage = folder_a + list1[i].replace('.png', '') + ".webp"
     print(newimage)
     imagedata.save(newimage, quality=95, optimize=True)
     os.remove(folder_a + list1[i])