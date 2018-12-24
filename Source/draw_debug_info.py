import cv2


class debug_info:

    def __init(self):
        self.xrate = 0.5
        self.rects = []
        self.colors = []
        self.fps = 0
        self.counter = 0
        self.tracks = []

    def set_xrate(self, xrate):
        self.xrate = xrate

    def set_rects(self, rects):
        self.rects = rects.copy()

    def set_colors(self, colors):
        self.colors = colors.copy()
        
    def set_fps(self, fps):
        self.fps = fps

    def set_counter(self, counter):
        self.counter = counter 

    def set_tracks(self, tracks):
        self.tracks = tracks.copy()   

    def draw(self, frame):

        self.draw_border_line(frame, self.xrate)
        self.draw_rects(frame, self.rects, self.colors)

        self.draw_fps(frame, self.fps)
        self.draw_counter(frame, self.counter)

        self.draw_tracks(frame, self.tracks, self.colors)

        return frame

    def draw_border_line(self, frame, xrate):
        if (xrate < 0 or xrate > 1):
            return frame

        height, width, channels = frame.shape
        widthCenter = round(width * xrate)
        cv2.line(frame,(widthCenter, 0),(widthCenter, height),(0,0,255),2)

        #TODO check is it needed
        return frame


    def draw_rects(self, frame, rects, colors):

        height, width, channels = frame.shape
        for i, rect in enumerate(rects):
            x, y, w, h = rect
            overlay = frame.copy()

            cv2.rectangle(overlay, (x, y), (x+w, y+h), colors[i],  cv2.FILLED)
            opacity = 0.3
            cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0, frame)

        return frame

    def draw_fps(self, frame, fps):

        height, width, channels = frame.shape
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,'fps: ' + str(fps),(width - 150,25), font, 0.6,(0,255,0),1,cv2.LINE_AA)

        return frame

    def draw_counter(self, frame, counter):

        height, width, channels = frame.shape
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,'counter: ' + str(counter),(width - 150,50), font, 0.6,(0,255,0),1,cv2.LINE_AA)

        return frame

    def draw_tracks(self, frame, tracks, colors):
        for j, track in enumerate(tracks):
            for i in range(0, len(track)-1):
                cv2.line(frame,track[i],track[i+1],colors[j],2)
