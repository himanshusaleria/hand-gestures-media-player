from pynput.keyboard import Key, Controller

class SystemController:
    def __init__(self):
        self.keyboard = Controller()

    def volume_up(self):
        self.keyboard.tap(Key.media_volume_up)
        print("System: Volume Up")

    def volume_down(self):
        self.keyboard.tap(Key.media_volume_down)
        print("System: Volume Down")

    def next_track(self):
        self.keyboard.tap(Key.media_next)
        print("System: Next Track")

    def prev_track(self):
        self.keyboard.tap(Key.media_previous)
        print("System: Prev Track")

    def play_pause(self):
        self.keyboard.tap(Key.media_play_pause)
        print("System: Play/Pause")

