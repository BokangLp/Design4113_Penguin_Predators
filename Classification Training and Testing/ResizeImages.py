import cv2 as cv
import os
import matplotlib.pyplot as plt

# Resize images to 128x128 and save to new path
def imageResize():
    folder_path = r'C:\Users\Bokang Lepolesa\OneDrive - University of Cape Town\SCHOOL WORK\UCT\Year 4\Design\PenguinsPredatorsTesting\Penguin'
    folder_path2 = r'C:\Users\Bokang Lepolesa\OneDrive - University of Cape Town\SCHOOL WORK\UCT\Year 4\Design\PHBTesting\Penguin'
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        image = cv.imread(file_path)
        image = cv.cvtColor(image,cv.COLOR_BGR2RGB)
        height,width,channels = image.shape
    


        newImage = cv.resize(image, [128,128], cv.INTER_LANCZOS4)

        newFile_path = os.path.join(folder_path2, filename)
        cv.imwrite(newFile_path,newImage)


if __name__ == "__main__":
    imageResize()