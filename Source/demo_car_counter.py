import cv2
import time
import sys

import draw_debug_info as dbg
import fps_counter as fps
import car_tracker as car

def demo_car_counter(file_name):

    cap = cv2.VideoCapture(file_name)
    background_subtractor = cv2.createBackgroundSubtractorMOG2(history=256)
    ret, frame = cap.read()
    if ret == False:
        return

    height, width, channels = frame.shape
    width_center = int(width / 2)

    def bound_predicat(old_rect, new_rect):
        if (old_rect[0] < width_center and new_rect[0] >= width_center):
            return True
        else:
            return False

    stopline_coords = [width_center, 0, width_center, height]


    cars_num = 0
    counter = fps.fps_counter(5)
    car_tracker = car.car_tracker()
    debug_info = dbg.debug_info()

    time_to_sleep = 0.01
    while(cap.isOpened()):
        counter.new_frame()

        ret, frame = cap.read()
        if ret == True:

            time.sleep(time_to_sleep)
            # get objects
            cars_rects, colors, res_ind = car_tracker.process_frame(frame, bound_predicat)
            cars_num = cars_num + len(res_ind)
            debug_info.set_xrate(0.5)
            debug_info.set_counter(cars_num)
            debug_info.set_rects(cars_rects)
            debug_info.set_colors(colors)
            debug_info.set_fps(counter.show_fps())
            debug_info.set_tracks(car_tracker.get_car_tracks())

            debug_frame = debug_info.draw(frame)

            cv2.imshow('frame',debug_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # Release everything if job is finished
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    demo_car_counter(sys.argv[1])

