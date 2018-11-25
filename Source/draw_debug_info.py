import numpy as np
import cv2

def draw_debug_info( frame, metadata ):
    
    bordered_frame   = draw_border_line(frame, metadata['xrate'])
    frame_with_rects = draw_rects(bordered_frame, metadata['rects'])

    draw_fps(frame, metadata['fps'])
    draw_counter(frame, metadata['carcounter'])
    
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


def draw_rects(frame, rects):
   
    height, width, channels = frame.shape
    for i in range(0, len(rects)):
        cv2.rectangle(frame,rects[i][0],rects[i][1],(0,255,0),2)

    #TODO check is it needed
    return frame

def draw_fps(frame, fps):
    
    height, width, channels = frame.shape
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame,'fps: ' + str(fps),(width - 150,25), font, 0.6,(0,255,0),1,cv2.LINE_AA)

    #TODO check is it needed
    return frame

def draw_counter(frame, counter):
    
    height, width, channels = frame.shape
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame,'counter: ' + str(counter),(width - 150,50), font, 0.6,(0,255,0),1,cv2.LINE_AA)

    #TODO check is it needed
    return frame
