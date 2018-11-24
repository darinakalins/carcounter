import numpy as np
import cv2

def draw_debug_info( frame, xrate, metadata ):
    
    bordered_frame = draw_border_line(frame, xrate)

    #TODO_issue_4 show fps, bounding rects and counter from metadata  

    return bordered_frame

def draw_border_line(frame, xrate):
    if (xrate < 0 or xrate > 1):
        return frame
    
    height, width, channels = frame.shape
    widthCenter = round(width * xrate)
    cv2.line(frame,(widthCenter, 0),(widthCenter, height),(0,0,255),3)

    #TODO check is it needed
    return frame
