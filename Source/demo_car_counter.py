import numpy as np
import cv2
import time

import draw_debug_info as dbg
import fps_counter as fps

def demo_car_counter( fileName ):
    cap = cv2.VideoCapture(fileName)
    ret, frame = cap.read()
    if ret == False:
        return

    height, width, channels = frame.shape
    widthCenter = round(width / 2);

    counter = fps.fps_counter(5)
    while(cap.isOpened()):
        counter.new_frame()

        ret, frame = cap.read()
        if ret == True:

            #TODO_issue_1
            #TODO_issue_2
            #TODO_issue_3 

            #TODO delete
            time.sleep(0.02)

            #TODO use real data for metadata's filling
            metadata = dict(xrate=0.5, carcounter=42, fps=counter.show_fps(),
                            rects=[((20,100), (120, 200)), ((320,200), (420, 300))])
            debug_frame = dbg.draw_debug_info(frame, metadata)
            cv2.imshow('frame',debug_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # Release everything if job is finished
    cap.release()
    cv2.destroyAllWindows()
