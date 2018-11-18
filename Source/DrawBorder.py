import numpy as np
import cv2

def DrawBorderLine( fileName ):
    cap = cv2.VideoCapture(fileName)
    ret, frame = cap.read()
    if ret == False:
        return

    height, width, channels = frame.shape
    widthCenter = round(width / 2);
    
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            cv2.line(frame,(widthCenter, 0),(widthCenter, height),(0,0,255),3)
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # Release everything if job is finished
    cap.release()
    cv2.destroyAllWindows()
