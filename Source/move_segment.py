import cv2
import numpy as np

class default_segmentation:

    def __init__(self):
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2(history=256)

    def extract_background(self, frame):
        foreground_mask = self.background_subtractor.apply(frame)
        cv2.imshow('mask', foreground_mask)
        return foreground_mask


class diff_of_accumulateWeighted:

    def __init__(self):
        self.bkg_img_1 = []
        self.bkg_img_1 = []

    def extract_background(self, frame):
        height, width, channels = frame.shape

        gray_frame = None
        if channels > 1:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray_frame = frame.copy()
        flt_gray_frame = np.float32(gray_frame)/255.0

        # process initial frame
        if not np.any(self.bkg_img_1) or not np.any(self.bkg_img_2):
            self.bkg_img_1 = flt_gray_frame.copy()
            self.bkg_img_2 = flt_gray_frame.copy()
            return None

        cv2.accumulateWeighted(flt_gray_frame, self.bkg_img_1, 0.5001)
        cv2.accumulateWeighted(flt_gray_frame, self.bkg_img_2, 0.5)

        background1 = cv2.normalize(src=self.bkg_img_1, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        #cv2.imshow('bkg_img_1', background1)
        background2 = cv2.normalize(src=self.bkg_img_2, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        #cv2.imshow('bkg_img_2', background2)

        background = cv2.absdiff(background1, background2)
        cv2.imshow('absdiff', background)

        ret, threshed = cv2.threshold(background,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        cv2.imshow('threshed', threshed)

        return threshed
