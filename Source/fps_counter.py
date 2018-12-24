import datetime

#class for fps (frame per seconds) counting
class fps_counter:
    # constructor
    # /param num_of_frames - number of frames that is used for fps counting
    def __init__(self, num_of_frames):
        self.frames_ramaining = num_of_frames
        self.times = [0 for i in range(0, self.frames_ramaining)]
        self.pointer = -1

    # /brief signals that new frame isprocessedgir
    def new_frame(self):
        self.pointer = (self.pointer + 1) % len(self.times)
        self.times[self.pointer] = datetime.datetime.now()


        if (self.frames_ramaining != 0):
            self.frames_ramaining = self.frames_ramaining - 1

    # /brief get current value of fps
    def show_fps(self):
        if self.pointer == -1:
            return 0

        prev_pointer = (self.pointer + 1 + self.frames_ramaining) % len(self.times)

        time_diff = self.times[self.pointer] - self.times[prev_pointer]
        time_for_one_frame = (time_diff.seconds + time_diff.microseconds/1E6) / (len(self.times) - self.frames_ramaining)

        return round(1 / time_for_one_frame) if time_for_one_frame != 0 else 0
