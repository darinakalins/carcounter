import cv2
import time
import sys

import draw_debug_info as dbg
import fps_counter as fps
import car_tracker as car

def demo_car_counter( fileName ):

    cap = cv2.VideoCapture(fileName)
    background_subtractor = cv2.createBackgroundSubtractorMOG2(history=256)
    ret, frame = cap.read()
    if ret == False:
        return

    height, width, channels = frame.shape
    width_center = int(width / 2);
    def bound_predicat(old_rect, new_rect):
        if (old_rect[0] < width_center and new_rect[0] >= width_center):
            return True
        else:
            return False

    stopline_coords = [width_center, 0, width_center, height]


    cars_num = 0
    counter = fps.fps_counter(5)
    car_tracker = car.car_tracker()

    time_to_sleep = 0.2
    while(cap.isOpened()):
        counter.new_frame()

        ret, frame = cap.read()
        if ret == True:

            time.sleep(time_to_sleep)
            # get objects
            (crossed_cars_rects, res_ind) = car_tracker.process_frame(frame, bound_predicat)
            cars_num = cars_num + len(res_ind)

            metadata = dict(xrate=0.5, carcounter=cars_num, fps=counter.show_fps(),
                            rects=crossed_cars_rects)
            debug_frame = dbg.draw_debug_info(frame, metadata)

            cv2.imshow('frame',debug_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if cv2.waitKey(1) & 0xFF == ord('s'):
                time_to_sleep = time_to_sleep + 0.1
            if cv2.waitKey(1) & 0xFF == ord('f') and time_to_sleep != 0.0:
                print('!!!!!\n')
                time_to_sleep = time_to_sleep - 0.1
        else:
            break

    # Release everything if job is finished
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    demo_car_counter(sys.argv[1])
