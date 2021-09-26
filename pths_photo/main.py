import cv2
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import skimage.measure
import scipy
from skimage import feature

from skimage import io


#_______________________________________
# For finding edges

def find_edges(img):
    ans = cv2.Canny(img, 255/3, 255)
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
    return th2 # try th1, th2

#_______________________________________
# For finding gradients

def gradient(img):
    laplacian = cv2.Laplacian(img,cv2.CV_8U)
    sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
    sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)
    return laplacian # try sobelx/sobely

#_______________________________________
# for applying different kernels
# I used averaging kernel    

def apply_kernel(img):
    kernel_size = 5
    kernel = np.ones((kernel_size,kernel_size),np.float32)/(kernel_size**2)
    ans = cv2.filter2D(img,-1,kernel)
    return ans


def main():
    photo_dir = './photos'
    result_name = './results/project_test102c.avi'
    n = -1

    photo_files = []
    for p in Path(photo_dir).iterdir():
        if p.is_file() and "DS" not in str(p):
            # print(p)
            photo_files.append(str(p))
    photo_files.sort()
    # print(photo_files)
    print("found " + str(len(photo_files)) + " photos")
    
    imgs = []
    orig_imgs = []
    img_ffts = []
    shift = []
    img = cv2.imread(photo_files[0])
    height, width, layers = img.shape
    pooln = 2
    # height = int(height/(pooln**2))
    # width = int(width/(pooln**2))
    size = (width, height)

    # par_img = cv2.imread(photo_files[0])/len(photo_files)
    # for i, photo_file in enumerate(photo_files[1:]):
    #     par_img += cv2.imread(photo_file)/len(photo_files)
    # par_img = par_img.astype(np.uint8) 
    # cv2.imwrite("filename.jpg", par_img) 
    # raise(Exception("SAS"))
        # print(img.shape)

    for i, photo_file in enumerate(photo_files[0:n]):
        print(i)
        img_orig = cv2.imread(photo_file)
        img = cv2.imread(photo_file, 0)
        imgsc = io.imread(photo_file, as_gray=True)


        # img = apply_kernel(img)
        # img = threshold(img)
        # img = apply_kernel(img)
        # img = find_edges(img)
        # img = getBordered(img, 10)
        img = feature.canny(imgsc, sigma=5).astype(np.float)*255
        # img = np.multiply(resc, 255*np.ones((height, width)))
        # img /= np.max(img)
        # img = resc
        # img_res = feature.canny(imgsc, sigma=0.0001)
        # for a in img_res:
        #     for b in a:
        #         if b:
        #             print(b)
        img = apply_kernel(img)
        img = img*(255/np.max(img))
        img = apply_kernel(img)
        img = img*(255/np.max(img))


        # img = skimage.measure.block_reduce(img, (pooln,pooln), np.max)
        # for j in range(0):
        #     img, img2 = np.gradient(img)
        #     img = np.absolute(img)
        #     img += np.absolute(img2)
        # # img /= np.max(img)
        # # img *= 255
        # img = img.astype(np.uint8) 
        # img = skimage.measure.block_reduce(img, (pooln,pooln), np.max)



        # print(np.max(img))
        # print(img.shape)
        # img = np.multiply((np.ma.masked_where(img>200, img)).mask, img)
        # img = cv2.bitwise_not(img)

        # fimg = img-127
        # print(img)
        # print(img.shape)
        # img = img[:,:,2:3]
        # print(img.shape)

        # raise(Exception("SAS"))
        # img = cv2.normalize(img,  img, 0, 255, cv2.NORM_MINMAX)
        # print(img.shape)
        img_fft = (np.fft.fft2(img))#np.fft.fftshift
        # print(img_fft.shape)
        img_ffts.append(img_fft)
        # if i > 0:
            # if i == 1:
            # print(type(img_fft))
        parent_fft = img_ffts[0]
        corr = np.absolute(np.fft.fftshift(np.fft.ifft2(np.multiply(parent_fft, np.conjugate(img_ffts[-1])))))#
        # corr = scipy.signal.medfilt2d(corr)
        max_x, max_y = np.unravel_index(np.argmax(corr, axis=None), corr.shape)
        # print(max_x, max_y)
        shift.append((int(max_x-height/2), int(max_y-width/2)))
            # shift.append((0,0))

        # if i == 3:  
        #     # X, Y = np.meshgrid(range(size[0]), range(size[1]))
        #     # fig = plt.figure(figsize=(6,6))
        #     # ax = fig.add_subplot(111, projection='3d')
        #     # ax.plot_surface(X, Y, corr)
        #     plt.imshow(corr)
        #     plt.show()

        # for j in range(img.shape[0]):
        #     for k in range(img.shape[1]):
        #         if img[j][k] == 256:
        #             img[j][k] = 254
        #             print(".", end="")
        # print(shift[-1][0])
        # print(shift[-1][1])
        M = np.float32([[1,0,shift[-1][0]],[0,1,shift[-1][1]]])
        img = cv2.warpAffine(img,M,size)
        img_orig = cv2.warpAffine(img_orig,M,size)

        
        img = np.stack((img,img, img), axis=2)
        # print(img.shape)
        # imgs.append(img)
        orig_imgs.append(img_orig)
        imgs.append(img)

    # print(shift)

    out = cv2.VideoWriter(result_name,cv2.VideoWriter_fourcc(*'DIVX'), 2, size)

    # for i, img in enumerate(imgs):
    #     print(i)
    #     cv2.imwrite("./results/2img" + str(i)+".jpg", img)


    for i, img in enumerate(imgs):#orig_imgs
        print(i)
        out.write(img)
    out.release()

    # print(imgs[0])


def main2():

    test_num = 13
    photo_dir = './photos'
    result_name = './results2/project_test'+str(test_num)+'.avi'

    photo_files = []
    for p in Path(photo_dir).iterdir():
        if p.is_file() and "DS" not in str(p):
            # print(p)
            photo_files.append(str(p))
    photo_files.sort()
    # print(photo_files)
    print("found " + str(len(photo_files)) + " photos")

    final_imgs = []

    surf = cv2.xfeatures2d.SURF_create()
    bf = ф(cv2.NORM_L1, crossCheck=False)

    img_1_orig = cv2.imread(photo_files[0])
    img_1 = img_1_orig
    # img_1 = cv2.Canny(img_1_orig, 255/3, 255)
    # img_1 = cv2.Laplacian(img_1_orig, cv2.CV_8U)
    # img_1 = cv2.cvtColor(img_1, cv2.COLOR_RGB2HSV)
    # cv2.imwrite("./results2/t"+str(test_num)+"img0.jpg", img_1)
    height, width, layers = img_1.shape
    size = (width, height)
    keypoints_surf_1, descriptors_1 = surf.detectAndCompute(img_1, None)
    # cv2.imwrite("./results2/t4img0.jpg", img_1)
    final_imgs.append(img_1_orig)

    for i, photo_file in enumerate(photo_files[1:6]):
        print(i+1)

        img_2_orig = cv2.imread(photo_files[i+1])
        img_2 = img_2_orig
        # img_2 = cv2.Canny(img_2_orig, 255/3, 255)
        # img_2 = cv2.Laplacian(img_2_orig,cv2.CV_8U)
        # img_2 = cv2.cvtColor(img_2, cv2.COLOR_RGB2HSV)

        keypoints_surf_2, descriptors_2 = surf.detectAndCompute(img_2, None)

        # Match descriptors.
        matches = bf.match(descriptors_2,descriptors_1)
        matches = sorted(matches, key = lambda x:x.distance)
        # print(matches)
        src_pts = np.float32([keypoints_surf_2[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints_surf_1[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        print(mask)
        t = [(M[0][2]),(M[1][2])]
        s = [(M[0][0]**2+M[1][0]**2)**(0.5), (M[0][1]**2+M[1][1]**2)**(0.5)]
        rot = [[M[0][0]/s[0], M[1][0]/s[0]],[M[0][1]/s[1], M[1][1]/s[1]]]

        print(t)
        print(s)
        print(rot)

        img_2_pred = cv2.warpPerspective(img_2, M, (img_1_orig.shape[1], img_1_orig.shape[0]))
        

        if abs(rot[0][1]) < 0.2 and abs(rot[1][0]) < 0.2:   # if s[0] < 1.1 and s[1] < 1.1:
            print("good")
            cv2.imwrite("./results2/good"+str(test_num)+"img" + str(i+1)+".jpg", img_2_pred)
            final_imgs.append(img_2_pred)
            if (i+1)%10 == 0:# and ((abs(rot[0][1]) < 0.02 and abs(rot[1][0]) < 0.02) or (abs(s[0]-1) < 0.1 and abs(s[1]-1) < 0.1)):
                print("change")   
                img_1 = img_2_pred
                keypoints_surf_1, descriptors_1 = surf.detectAndCompute(img_1, None)
        # break
        else:
            cv2.imwrite("./results2/bad"+str(test_num)+"img" + str(i+1)+".jpg", img_2_pred)


    out = cv2.VideoWriter(result_name,cv2.VideoWriter_fourcc(*'DIVX'), 2, size)

    for i, img in enumerate(final_imgs):#orig_imgs
        print(i)
        out.write(img)
    out.release()



if __name__ == '__main__':
    # main()
    main2()



# [[ 1.02586693e+00, -1.21268235e-03, -4.90408860e+01], [ 2.03292307e-02,  1.01964158e+00, -5.37155670e+01], [ 5.44274877e-06,  5.71212769e-06,  1.00000000e+00]]
# s = [(M[0][0]**2+M[1][0]**2)**(0.5), (M[0][1]**2+M[1][1]**2)**(0.5)]
# rot = [[M[0][0]/s[0], M[1][0]/s[0]],[M[0][1]/s[1], M[1][1]/s[1]]]

# [[-1.01443658e+00, -1.12995516e+00,  2.23929304e+03], [-4.43456088e-01, -5.27282104e-01,  9.94918307e+02], [-4.58062899e-04, -4.87383665e-04,  1.00000000e+00]]
