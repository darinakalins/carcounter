import cv2

def draw_debug_info( frame, metadata ):

    draw_border_line(frame, metadata['xrate'])
    draw_rects(frame, metadata['rects'])

    draw_fps(frame, metadata['fps'])
    draw_counter(frame, metadata['carcounter']) 

    return frame

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
    for rect in rects:
        x, y, w, h = rect
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

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
