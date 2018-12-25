import cv2
import random
import scipy as sp

import car_counter_utilites as utils
import move_segment as ms
import numpy as np

#class for tracking cars through frames
class car_tracker:
    # constructor
    def __init__(self):
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2(history=256)
        self.cars = {}
        self.uid_generator = -1

        self.move_segmentor = ms.default_segmentation()

    # generates new unique id
    def gen_uid(self):
        self.uid_generator += 1
        return self.uid_generator

    # get deteckted cars rectangles
    def get_car_rects(self):
        results = []
        for uid, place in self.cars.items():
                results.append(place['cur_rect'])
        return results

    def get_colors(self):
        results = []
        for uid, place in self.cars.items():
            results.append(place['color'])
        return results

    # get deteckted cars rectangles
    def get_car_tracks(self):
        results = []
        for uid, place in self.cars.items():
                results.append(place['track'])
        return results

    # get cars rectangles from background
    def get_car_rects_from_bkg(self, frame):
        foreground_mask = self.move_segmentor.extract_background(frame)

        if not (foreground_mask is None):
            height, width, channels = frame.shape

            width_center = int(width / 2)
            size_constraints = [0.05 * width, 0.05 * height]
            return utils.extract_objects_rects(foreground_mask, size_constraints)
        else:
            return []

    def add_new_car(self, car_rect, color):
        rect_center = (round(car_rect[0] + car_rect[2]/2), round(car_rect[1] + car_rect[3]/2))
        self.cars[self.gen_uid()] = {'rects':[car_rect], 'cur_rect': car_rect, 'color' : color,
                                     'track' : [rect_center], 'expired' : False}


    def change_existed_car(self, uid, car_rect):
        cur_track = self.cars[uid]['track'].copy()
        cur_color = self.cars[uid]['color']
        rect_center = (round(car_rect[0] + car_rect[2]/2), round(car_rect[1] + car_rect[3]/2))
        cur_track.append(rect_center)
        cur_rects = self.cars[uid]['rects'].copy()
        cur_rects.append(car_rect)
        self.cars[uid] = {'rects':cur_rects, 'cur_rect': car_rect, 'color' : cur_color,
                          'track' : cur_track, 'expired' : False}

    def interpolate_track(self, uid):
        track_for_interpolate = self.cars[uid]['track'].copy()
        x, y = zip(*track_for_interpolate)
        fp, residuals, rank, sv, rcond = sp.polyfit(x, y, 3, full=True)
        f = sp.poly1d(fp)
        fx = sp.linspace(x[0], x[-1]+30, 20).astype(int)
        y_interp = f(fx).astype(int)
        self.cars[uid]['track'] = list(zip(fx, y_interp))

    def interpolate_rects(self, uid):
        rects_for_interpolate = self.cars[uid]['rects'].copy()
        cur_rect = self.cars[uid]['cur_rect'].copy()
        x, y, w, h = zip(*rects_for_interpolate)
        fp, residuals, rank, sv, rcond = sp.polyfit(x, y, 3, full=True)
        f = sp.poly1d(fp)
        fx = sp.linspace(x[0], x[-1]+30, 100).astype(int)
        y_interp = f(fx).astype(int)
        fp, residuals, rank, sv, rcond = sp.polyfit(w, h, 3, full=True)
        f = sp.poly1d(fp)
        fw = sp.linspace(w[0], w[-1]+30, 100).astype(int)
        h_interp = f(fw).astype(int)
        rects = list(zip(fx, y_interp, fw, h_interp))
        self.cars[uid]['rects'] = rects
        cur_rect = rects[-1]
        self.cars[uid]['cur_rect'] = cur_rect


    def process_frame(self, frame, pred):
        #indexes of cars which are suit for predicat
        results = []

        # set old cars expired
        for uid, info in self.cars.items():
            info['expired'] = True

        objs = self.get_car_rects_from_bkg(frame)

        #for every detected car choose suit previous rect
        for obj in objs:

            # maximal intersection square and its car(rect) uid
            max_S = 0
            max_uid = -1

            for uid, info in self.cars.items():
                if info['expired']:
                    intersection_rect = utils.intersection(obj, info['cur_rect'])
                    if intersection_rect:
                        # intersection is not empty. Check value for maximum
                        intersection_square = intersection_rect[2] * intersection_rect[3]
                        if max_S < intersection_square:
                            max_S = intersection_square
                            max_uid = uid
 
            if (max_uid != -1):
                #check for predicat
                if pred and pred(self.cars[max_uid]['cur_rect'], obj):
                    results.append(max_uid)
                self.change_existed_car(max_uid, obj)
                if len(self.get_car_rects()) > 30:
                    self.interpolate_track(max_uid)
                    self.interpolate_rects(max_uid)

            else:
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), -1)
                self.add_new_car(obj, color)

        # collect ids of expired cars
        ids2remove = []
        # set old cars expired
        for uid, info in self.cars.items():
            if info['expired']:
                ids2remove.append(uid)

        for uid in ids2remove:
            self.cars.pop(uid)

        return self.get_car_rects(), self.get_colors(), results