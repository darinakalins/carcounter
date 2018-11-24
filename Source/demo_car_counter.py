import numpy as np
import draw_debug_info as dbg
import cv2

def demo_car_counter( fileName ):
    cap = cv2.VideoCapture(fileName)
    ret, frame = cap.read()
    if ret == False:
        return

    height, width, channels = frame.shape
    widthCenter = round(width / 2);
    
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:

            #TODO_issue_1
            #TODO_issue_2
            #TODO_issue_3 
            
            debug_frame = dbg.draw_debug_info(frame, 0.5, none)
            cv2.imshow('frame',debug_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # Release everything if job is finished
    cap.release()
    cv2.destroyAllWindows()
