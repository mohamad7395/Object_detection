#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 17:48:48 2022

@author: mohamad
"""

import cv2
import matplotlib.pyplot as plt
import os.path
import numpy as np
from scipy.interpolate import interp1d


#%%

def extract_frame(vid_name):
    


    cam = cv2.VideoCapture("tr_vid/{}.mp4".format(vid_name))

    fps = cam.get(cv2.CAP_PROP_FPS)
    print(fps)

    i = 0
    while True:
        
        
        
        ret,frame = cam.read()
        
        if ret==False:
            break
        
        if (i%12)==0:
            print("pic printed")

            cv2.imwrite("tr_pic/{vid}/{pic}.jpg".format(vid = vid_name,pic = int(i/12)),frame)
            i+=1
        
        else:    i += 1 
        
    

        
    
    pass
    cam.release()
    cv2.destroyAllWindows()   

#%%

def find_center():
    
    greenLower = (29, 36, 6)
    greenUpper = (95, 255, 255)
    
    path = "tr_pic/find center/"
    
    result = []
    
    
    for i in range(60):
        
        print(i)
        
        folder = path + str(i) +"/"
        file_result=[]
        pic_num = 0
        lst = os.listdir(folder)
        lst2 =[s.replace(".jpg", '') for s in lst]
        lst3=[int(x) for x in lst2 if x != ".DS_Store"]
        lst3.sort()
        
        

        for pic_num in lst3:
            
            pic_path = folder + str(pic_num) + '.jpg'
            frame = cv2.imread(pic_path)
            # print(pic_path)
            blurred = cv2.GaussianBlur(frame, (3, 3), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
            
            mask = cv2.inRange(hsv, greenLower, greenUpper)

            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
            
            
            cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if cnts[0]:
        
                c = max(cnts[0], key=cv2.contourArea)
                    
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                
                height = 640 - center[1]
                print(height)
                file_result.append(height)
            else: 
                os.remove(pic_path)
                print(str(pic_num)+ "deleted" + '_'*20)
        result.append(file_result)      
                    
                    
                    
              
    print(result)         
    return result

    
def find_center2():
    
    greenLower = (20, 36, 6)
    greenUpper = (95, 255, 255)
    
    path = 'tr_pic/5/2.jpg'
    
    frame = cv2.imread(path)
    blurred = cv2.GaussianBlur(frame, (3, 3), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(hsv, greenLower, greenUpper)

    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    
    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    

    if cnts[0]:
        
        c = max(cnts[0], key=cv2.contourArea)
    

    
        
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        
        cv2.circle(frame, center, 3, (0, 0, 255), -1)
        
        plt.imshow(frame)
        
        return frame
        
        
    else: print("hi")






   

    
#%%   


if __name__ == "__main__":
    
    # for i in range(31,36):
        
    #     extract_frame(str(i))
    
    DSet = find_center()
    import pickle
    with open('labels.plk', 'wb') as f:
        pickle.dump(DSet, f)

    
    # print(a[5])
    
    # y = np.array(a[5])
    # x = np.array(list(range(len(y))))
    
    # f = interp1d(x, y, kind='quadratic')
    
    # x_new = np.linspace(x.min(), x.max(),500)
    
    # y_new = f(x_new)
    
    # plt.plot(x_new,y_new)
    
    # plt.scatter(x,y)
    
    
 