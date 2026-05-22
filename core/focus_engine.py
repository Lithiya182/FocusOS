import threading
import time

class FocusTimer:

    def __init__(self, update_callback, finish_callback):

        self.default_time = 10
        self.time_left = self.default_time
        self.running = False
        self.paused = False

        self.update_callback = update_callback
        self.finish_callback = finish_callback

    def start(self, minutes=None):

        if minutes is not None:
            self.default_time = 10
            self.time_left = self.default_time

        if not self.running:
            self.running = True
            self.paused = False

            thread = threading.Thread(target=self.run_timer)
            thread.daemon = True
            thread.start()

    def run_timer(self):

        while self.running and self.time_left > 0:

            if not self.paused:

                mins = self.time_left // 60
                secs = self.time_left % 60

                timer_text = f"{mins:02}:{secs:02}"

                self.update_callback(timer_text)

                time.sleep(1)

                self.time_left -= 1

            else:
                time.sleep(0.2)

        if self.time_left <= 0:

            self.running = False
            self.finish_callback()

    def pause(self):

        self.paused = True

    def resume(self):

        self.paused = False

    def stop(self):

        self.running = False
        self.time_left = self.default_time

        self.update_callback("50:00")