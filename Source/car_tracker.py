import cv2

import car_counter_utilites as utils

#class for tracking cars through frames
class car_tracker:
    # constructor
    def __init__(self):
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2(history=256)
        self.cars = []


    # TODO optimize
    def process_frame(self, frame, pred = None):
        results = []
        prev_cars = self.cars.copy()

        height, width, channels = frame.shape
        width_center = int(width / 2);

        stopline_coords = [width_center, 0, width_center, height]
        size_constraints = [0.05 * width, 0.05 * height]

        used_indexes = []
        new_cars_counter = 0
        objs = utils.extract_objects_rects(frame, size_constraints, self.background_subtractor)
        for obj in objs:
            max_S = 0
            max_ind = -1

            for i in range(0, len(prev_cars)):
                intersection_rect = utils.intersection(obj, prev_cars[i])
                if intersection_rect != None and max_S < intersection_rect[2] * intersection_rect[3]:
                    max_S = intersection_rect[2] * intersection_rect[3]
                    max_ind = i

            if max_ind != -1:
                self.cars[max_ind] = obj
                used_indexes.append(max_ind)

            else:
                self.cars.append(obj)
                new_cars_counter = new_cars_counter + 1
                print('new car!\n')

            for i in range(len(prev_cars) - 1, 0 - 1, -1):
                if i not in used_indexes:
                    print('remove ',i,' from list ', range(0, len(prev_cars)))
                    self.cars.remove(self.cars[i])

        return (self.cars, new_cars_counter)