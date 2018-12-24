import cv2

class default_segmentation:

    def __init__(self):
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2(history=126)

    def extract_background(self, frame):
        foreground_mask = self.background_subtractor.apply(frame)
        _, foreground_mask = cv2.threshold(foreground_mask, 127, 255, cv2.THRESH_BINARY)
        foreground_mask = cv2.medianBlur(foreground_mask, 5)
        foreground_mask = cv2.morphologyEx(foreground_mask, cv2.MORPH_CLOSE,
                                           cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5)))
        cv2.imshow('mask', foreground_mask)
        return foreground_mask
