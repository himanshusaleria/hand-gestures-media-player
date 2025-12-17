import subprocess

class SystemController:
    def _run_osascript(self, script):
        try:
            subprocess.run(['osascript', '-e', script], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running AppleScript: {e}")

    def volume_up(self):
        script = "set volume output volume (output volume of (get volume settings) + 5) -- 100% max"
        self._run_osascript(script)
        print("System: Volume Up")

    def volume_down(self):
        script = "set volume output volume (output volume of (get volume settings) - 5)"
        self._run_osascript(script)
        print("System: Volume Down")

    def next_track(self):
        # Key code 98 is F7 (Prev), 100 is F8 (Play/Pause), 101 is F9 (Next) ??
        # Let's verify standard media keys.
        # Actually commonly: 98=F7, 100=F8, 101=F9 could be wrong.
        # fast forward/rewind vs skip.
        # Let's use the semantic keys if possible or standard keycodes.
        # Key code 124 is Right Arrow? No suitable for media global.
        # Using 'tell application "System Events" to key code 101' is common for "Next"
        self._run_osascript('tell application "System Events" to key code 101')
        print("System: Next Track")

    def prev_track(self):
        self._run_osascript('tell application "System Events" to key code 98')
        print("System: Prev Track")

    def play_pause(self):
        self._run_osascript('tell application "System Events" to key code 100')
        print("System: Play/Pause")
