import cv2
from pathlib import Path
import numpy as np


from pathlib import Path
from svgtrace import trace

from random import randint


#_______________________________________
        # For finding edges

def find_edges(img, try_x):
    ans = cv2.Canny(img,try_x,200)
    return ans

#_______________________________________
# For finding white (any color) text 

def find_colr_mask(img):
    # define range of color (for not grayscale / colorful images)
    # lower_color = np.array([110,50,50])
    # upper_color = np.array([130,255,255])
    lower_color = np.array([240])
    upper_color = np.array([255])
    ans = cv2.inRange(img, lower_color, upper_color)
    return ans

#_______________________________________
# For thresholding image

def threshold(img):
    ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                cv2.THRESH_BINARY,11,2)
    th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv2.THRESH_BINARY,11,2)
    return th3 # try th1, th2

#_______________________________________
# For finding gradients

def gradient(img):
    laplacian = cv2.Laplacian(img,cv2.CV_64F)
    sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
    sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)
    return laplacian # try sobelx/sobely

#_______________________________________
# for applying different kernels
# I used averaging kernel    

def apply_kernel(img, kernel_size=3):
    kernel_size = kernel_size
    kernel = np.ones((kernel_size,kernel_size),np.float32)/(kernel_size**2)
    ans = cv2.filter2D(img,-1,kernel)
    return ans

#_______________________________________



def read_files(images_dir):
    images = []
    for p in Path(images_dir).iterdir():
        if p.is_file() and (".jpg" in str(p) or ".png" in str(p) or ".jpeg" in str(p)):
            print(p)
            images.append(cv2.imread(str(p)))
    return images



def main():
    images_dir = '/Users/ukhatov/Documents/Projects/rome/start'
    result_dir = '/Users/ukhatov/Documents/Projects/rome/finish'

    svg_flag = True
    phi=1
    theta=1
    alpha=10
    maxIntensity = 255.0


    images = read_files(images_dir)
    print(str(len(images)) + " images have been read")

    # preprocessed_images = preprocess(images)
    preprocessed_images = []

    try_x_cur = [5]
    for try_x in [25]:#[25, 50, 100, 150, 200]:
        for i, img in enumerate(images):
            # img = apply_kernel(img)
            # img = find_edges(img, try_x_cur[i])
            # # img = cv2.bitwise_not(img)
            # # img = apply_kernel(img, 5)
            # # img = (maxIntensity/phi)*(img/(maxIntensity/theta))**alpha
            # # img = np.uint8(img)
            # # img = find_edges(img,1300)
            # img = cv2.bitwise_not(img)
            # img2 = find_colr_mask(img1)
            # ans = img2
            preprocessed_images.append(img)




    file_names = []

    Path(result_dir).mkdir(exist_ok=True)
    for i, preprocessed_image in enumerate(preprocessed_images):
        # rnd_int = randint(10000, 100000)
        rnd_int=0
        file_name=f"{result_dir}/result_{i}_{rnd_int}.png"
        file_names.append(file_name)
        cv2.imwrite(file_name, preprocessed_image)


    if svg_flag:
        for file_name in file_names:
            bw = open(file_name[:-4]+".svg", "w")
            bw.write(trace(file_name, True))
            bw.close()

if __name__ == '__main__':
	main()
