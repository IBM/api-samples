'''
This is a utility class to be used by the task manager.
'''
import time


class Timer():

    second_count_format = '{0:.2f}'
    start_time = 0

    def start(self):
        self.reset()
        self.start_time = time.time()

    def reset(self):
        self.start_time = 0

    def is_running(self):
        return self.start_time > 0

    def get_time_elapsed(self):
        return time.time() - self.start_time

    def has_timeout(self, timeout=30):
        return self.get_time_elapsed() > timeout

    def print_time_elapsed(self):
        print("Time elapsed: " +
              self.second_count_format.format(self.get_time_elapsed()) +
              " seconds.")

    def sleep(self, number_of_seconds):
        time.sleep(number_of_seconds)
