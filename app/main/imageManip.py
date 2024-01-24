import os, sys
from pathlib import Path
import calendar, time;
from PIL import Image
from config import Config

UPLOADED_IMAGES_DEST = Config.UPLOADED_IMAGES_DEST

def cropNsave(image, email, x1, y1, x2, y2):
    # Small icon 200 x 250
    # Profile icon 400 x 500
    try:
        print (image)
        print (type(image))
        print (image.content_length)
        print (image.filename)
        original = Image.open(image)
        filename = email.split("@")[0]
        cropped = original.crop((float(x1), float(y1), float(x2), float(y2)))
        resized = cropped.resize((400, 500), Image.ANTIALIAS)
        newImgName = filename + "_" + str(calendar.timegm(time.gmtime())) + ".png"
        empPhotoDir = UPLOADED_IMAGES_DEST / "employeePhotos"
        if not os.path.exists(empPhotoDir):
            print ("Making: " + str(empPhotoDir))
            os.makedirs(empPhotoDir)            
        else:
            os.chdir(empPhotoDir)
            existing_files = os.listdir(empPhotoDir)
            for f in existing_files:                
                if filename in f:
                    os.remove(f)
        resized.save(empPhotoDir / newImgName,'png')
    except OSError as err:
        print("OS error: {0}".format(err))
        exit()
    return newImgName