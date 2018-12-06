import cv2
import numpy as np

import car_counter_utilites as utils
import move_segment as ms

#class for tracking cars through frames
class car_tracker:
    # constructor
    def __init__(self):
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2(history=256)
        self.cars = {}
        self.uid_generator = -1

        self.move_segmentor = ms.diff_of_accumulateWeighted()

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

    # get cars rectangles from background
    def get_car_rects_from_bkg(self, frame):
        foreground_mask = self.move_segmentor.extract_background(frame)

        if not (foreground_mask is None):
            height, width, channels = frame.shape

            width_center = int(width / 2);
            size_constraints = [0.05 * width, 0.05 * height]
            return utils.extract_objects_rects(foreground_mask, size_constraints)
        else:
            return []

    def add_new_car(self, car_rect):
        rect_center = (round(car_rect[0] + car_rect[2]/2), round(car_rect[1] + car_rect[3]/2))
        self.cars[self.gen_uid()] = {'cur_rect': car_rect,'track' : [rect_center], 'expired' : False}

        print('new car!\n')


    def change_existed_car(self, uid, car_rect):
        cur_track = self.cars[uid]['track'].copy()
        rect_center = (round(car_rect[0] + car_rect[2]/2), round(car_rect[1] + car_rect[3]/2))
        cur_track.append(rect_center)

        self.cars[uid] = {'cur_rect': car_rect,'track' : cur_track, 'expired' : False}

    # TODO optimize
    def process_frame(self, frame, pred):
        #indexes of cars which are suit for predicat
        results = []

        # set old cars expired
        for uid, info in self.cars.items():
            info['expired'] = True

        objs = self.get_car_rects_from_bkg(frame)
        for obj in objs:

            # maximal intersection square and its car(rect) index
            max_S = 0
            max_uid = -1

            for uid, place in self.cars.items():
                intersection_rect = utils.intersection(obj, place['cur_rect'])
                if intersection_rect:
                    # intersection is not empty. Check value for maximum
                    intersection_square = intersection_rect[2] * intersection_rect[3]
                    if max_S < intersection_square:
                        max_S = intersection_square
                        max_uid = uid
 
            if (max_uid != -1):
                #check for predicat
                if ( pred and pred(self.cars[max_uid]['cur_rect'], obj)):
                    results.append(max_uid)
                self.change_existed_car(max_uid, obj)

            else:
                self.add_new_car(obj)

        # collect ids of expired cars
        ids2remove = []
        # set old cars expired
        for uid, info in self.cars.items():
            if info['expired']:
                ids2remove.append(uid)

        for uid in ids2remove:
            self.cars.pop(uid)

        return (self.get_car_rects(), results)