######################################################################################
            # import the necessary packages    #
              
import cv2
import numpy as np
import imutils
import time
import Seed

            # import the necessary packages    #             

######################################################################################
            # reading the video file and parameter    #

#open the video file
cap = cv2.VideoCapture("test1.m4v")

               # reading the video file and parameter    #
######################################################################################
            # variables and input from users    #
# should give the user of input of areaL, areaH(this is can be adjust in different objects, but usually test different value then get the optimal one)
# should give the user of input of speed of the object

# give different lines and try to count by different part 
num_seed1   = 0
num_seed2   = 0
num_seed3   = 0

#cap.set(3,400) #set width
#cap.set(4,300) #set height

areaL = 800   # by testing many time, then know the area of one seed

areaH = 8000  # when seeds are together will has influence

#give the user to input
#areaL = input("Please input the areaL(min area of your object,default：800):")
#if the areaH is too small ， then has influence on when the object become together or very close
#areaH = input("Please input the areaLH(max area of your object，default：8000):")
# should give the user of input of speed of the object,has influence on tracking
#speed = input("Please input the speed of your object(the faster, the number should be larger,default：4):")
speed = 3
#should input of noise decreasing, bigger the number, less noise  
#denoise = input("Please input threshold to decrease noise (the bigger, noise will decrease,default：40):")
denoise = 40
deley_time = input("Input delay_time: ")
# initialize the first frame in the video stream
firstFrame = None

w_v = int(cap.get(3)) #get width of the video
h_v = int(cap.get(4)) #get height of the video
print("the width of video:",w_v)
print("the height of video:",h_v)

line_down1 = int(h_v/4)   # line1 to detect seeds
line_down2 = int(2*h_v/4)   # line2 to detect seeds
line_down3 = int(4*h_v/5)   # line3 to detect seeds

mx = int(w_v/2)
my = int(h_v/2)
font = cv2.FONT_HERSHEY_SIMPLEX
seeds = []
max_seeds_num = 500
sid = 1
                # variables and input from users   #
###################################################################################### 
            # Background substraction    #
num_frame = 0               
while(cap.isOpened()):
    num_frame +=1
#    print("This is the ", num_frame, " th frame")
    ret, frame = cap.read()   #read a frame
    frame_ori = frame

    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)   #change to gray, decease some noise
        gray2 = cv2.GaussianBlur(gray, (21, 21), 0)    #blur , decease more noise

        #if the first frame is None, initialize it
        if firstFrame is None:
                firstFrame = gray
                continue

        # compute the absolute difference between the current frame and first frame
        frame2 = cv2.absdiff(firstFrame,gray)        
        ret,thresh1 = cv2.threshold(frame2,int(denoise),255,cv2.THRESH_BINARY)  #decrese the noise
        kernel = np.ones((9,9),np.uint8)
        opening_ori = cv2.morphologyEx(frame2, cv2.MORPH_OPEN, kernel)
        closing_ori = cv2.morphologyEx(opening_ori, cv2.MORPH_CLOSE, kernel)
        opening = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

                    # Background substraction    #
######################################################################################
            # if there are no more frames to show   #
               
    except:
        #print("EOF")
        print('The seeds crossing line_1 are ',num_seed1)
        print('The seeds crossing line_2 are ',num_seed2)
        print('The seeds crossing line_3 are ',num_seed3)
        break
    
            # if there are no more frames to show   #
######################################################################################
            # draw countour for every seed    #
               
    _, contours0, hierarchy = cv2.findContours(closing,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # detect contours
    # for every contour in every frame
    num_cnt = 0
    for cnt in contours0:
        num_cnt+=1
 #       print("This is the ",num_cnt, "cnt of frame")
        area = cv2.contourArea(cnt)    # get the area of every contour, that is the area of the seed
 #       print("The area of this contour is", area)
        M = cv2.moments(cnt)   #From this moments, you can extract useful data like area, centroid etc
        # if the area is too small or too large, skip this
        if area< int(areaL) or area> int(areaH) :   
            continue

 # if the object fit our requirement then draw center of contour       
#get the centroid of the contours
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
 #       cv2.circle(frame,(cx,cy), 5, (0,0,255), -1)# get and draw the center of the contours
 #       print("The coords of the seeds is cx:",cx,"cy:",cy)
       #get the rectangle of contours
        x,y,w,h = cv2.boundingRect(cnt)   #get the x,y,weight, height of the bounding
#        print("The w ",w, "and h of the seed is",h)
#        frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2) # get and draw the rectangle of contours,Let (x,y) be the top-left coordinate of the rectangle and (w,h) be its width and height.
        areaRec = w*h 
        new = True   # means that this is a new seed

                # draw countour for every seed    #
######################################################################################
            #   TRACKING    #
        num_seed = 0

        for i in seeds:
            num_seed += 1
 #           print("This is the ",num_seed, "th seed of frame")
 #           print("The tracks is ", i.getTracks())
            if len(i.getTracks()) >= 2:
 #               print("The length of i.getTrackes is", len(i.getTracks()) )
                pts = np.array(i.getTracks(), np.int32) # make tracks become ndarray 
 #               print("The pts is ", pts)
                pts = pts.reshape((-1,1,2))
 #               print("The updated pts is ", pts)
            if (abs(cx - i.getX()) <= 18  and (cy-i.getY()) <=int(speed)*h*0.83 ):   #The object is near one already detected before
                new = False
                i.updateCoords(cx,cy)
                if (i.going_DOWN(line_down1,line_down1) == True):
                    num_seed1 += 1
                """
                    if area > 5000:
                        num_seed1 += 2
                    else:
                        num_seed1 += 1
                """
                if (i.going_DOWN(line_down2,line_down2) == True):
                    num_seed2 += 1
                '''
                    if area > 5000:
                        num_seed2 += 2
                    else:
                        num_seed2 += 1
                '''
                if (i.going_DOWN(line_down3,line_down3) == True):
#                    print("The area is ",area)
                    #print("The areaRec is ",areaRec)
                    num_seed3 += 1
                '''
                    if area > 5000:
                        num_seed3 += 2
                    else:
                        num_seed3 += 1
                '''
                break
            if i.getState() == '1':
                    if i.getDir() == 'down' and i.getY() > down_limit:
                        i.setDone()
            if i.timeOut():
                index = seeds.index(i)
                seeds.pop(index)
                del i
        if new == True:
            p = Seed.MySeed(sid,cx,cy,max_seeds_num)
            seeds.append(p)
            sid +=1
            
               #   TRACKING    #
######################################################################################        
            # put text and line on video    #
            
#    for i in seeds:
 #       cv2.putText(frame, str(i.getId()),(i.getX(),i.getY()),font,0.3,i.getRGB(),1,cv2.LINE_AA)

    str_down1 = 'DOWN1: '+ str(num_seed1)
    str_down2 = 'DOWN2: '+ str(num_seed2)
    str_down3 = 'DOWN3: '+ str(num_seed3)
 #   cv2.putText(frame, str_down1 ,(10,line_down1-20),font,0.5,(255,255,255),2,cv2.LINE_AA)
 #   cv2.putText(frame, str_down1 ,(10,line_down1-20),font,0.5,(255,0,0),1,cv2.LINE_AA)
 #   cv2.putText(frame, str_down2 ,(10,line_down2-20),font,0.5,(255,255,255),2,cv2.LINE_AA)
 #   cv2.putText(frame, str_down2 ,(10,line_down2-20),font,0.5,(255,0,0),1,cv2.LINE_AA)
#    cv2.putText(frame, str_down3 ,(10,line_down3-20),font,0.5,(255,255,255),2,cv2.LINE_AA)
 #   cv2.putText(frame, str_down3 ,(10,line_down3-20),font,0.5,(255,0,0),1,cv2.LINE_AA)
    
#    frame = cv2.line(frame, (0,line_down1), (w_v,line_down1), (0,255,0), thickness=2) #draw a green line at 1/4 place to detect seeds
#    frame = cv2.line(frame, (0,line_down2), (w_v,line_down2), (0,255,0), thickness=2) #draw a green line at 2/4 place to detect seeds
#    frame = cv2.line(frame, (0,line_down3), (w_v,line_down3), (0,255,0), thickness=2) #draw a green line at 3/4 place to detect seeds

              # put text and line on video    #
######################################################################################
    cv2.imshow('Seed Count Application',frame)
    time.sleep(float(deley_time))

    #Abort and exit with 'Q' or ESC
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    cv2.imshow('Seed Count Application_grau_blur',gray2)
    cv2.imshow('Seed Count Application_gray',gray)
    cv2.imshow('Seed Count Application_after line',frame_ori)
    cv2.imshow('Seed Count Application_after open_noise',opening_ori)
    cv2.imshow('Seed Count Application_after open_close_noise',closing_ori)
    cv2.imshow('Seed Count Application_after open',opening)
    cv2.imshow('Seed Count Application_after open_close',closing)
    
    
cap.release() #release video file
cv2.destroyAllWindows() #close all openCV windows
