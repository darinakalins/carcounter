import cv2
import sys

import draw_debug_info as dbg
import fps_counter as fps
import car_counter_utilites as car_counter

def demo_car_counter( fileName ):

    cap = cv2.VideoCapture(fileName)
    background_subtractor = cv2.createBackgroundSubtractorMOG2(history=256)
    ret, frame = cap.read()
    if ret == False:
        return

    height, width, channels = frame.shape
    width_center = int(width / 2);

    stopline_coords = [width_center, 0, width_center, height]
    size_constraints = [0.05 * width, 0.05 * height]

    cars_num = 0
    counter = fps.fps_counter(5)
    while(cap.isOpened()):
        counter.new_frame()

        ret, frame = cap.read()
        if ret == True:

            # get objects
            crossed_cars_rects = car_counter.process_frame(frame, size_constraints, 
                                                           stopline_coords, background_subtractor)
            cars_num = cars_num + len(crossed_cars_rects)
            metadata = dict(xrate=0.5, carcounter=cars_num, fps=counter.show_fps(),
                            rects=crossed_cars_rects)
            debug_frame = dbg.draw_debug_info(frame, metadata)
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
