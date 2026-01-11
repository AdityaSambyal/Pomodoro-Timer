from PySide6.QtCore import QObject, Signal, QTimer
from datetime import datetime, timedelta

class PomodoroTimer(QObject):
    time_changed = Signal(int)
    mode_changed = Signal(str)
    running_changed = Signal(bool)
    finished = Signal()

    def __init__(self, work=25*60, short_break=5*60, long_break=15*60, cycles_before_long=4):
        super().__init__()
        self.work = work
        self.short_break = short_break
        self.long_break = long_break
        self.cycles_before_long = cycles_before_long
        self.mode = "work"
        self.remaining = work
        self.is_running = False
        self.completed_cycles = 0
        self._end_time = None
        self._timer = QTimer()
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._tick)

    def start(self):
        if self.is_running:
            return
        if self._end_time is None:
            self._end_time = datetime.now() + timedelta(seconds=self.remaining)
        self._timer.start()
        self.is_running = True
        self.running_changed.emit(True)

    def pause(self):
        if not self.is_running:
            return
        self._timer.stop()
        if self._end_time:
            self.remaining = max(0, int((self._end_time - datetime.now()).total_seconds()))
        self._end_time = None
        self.is_running = False
        self.running_changed.emit(False)

    def reset(self):
        self._timer.stop()
        self._end_time = None
        self.is_running = False
        self.remaining = self._current_mode_duration()
        self.running_changed.emit(False)
        self.time_changed.emit(self.remaining)

    def _tick(self):
        if self._end_time is None:
            return
        rem = int((self._end_time - datetime.now()).total_seconds())
        if rem <= 0:
            self.remaining = 0
            self.time_changed.emit(0)
            self._timer.stop()
            self.is_running = False
            self._end_time = None
            self.finished.emit()
            self._handle_session_end()
            self.running_changed.emit(False)
        else:
            self.remaining = rem
            self.time_changed.emit(rem)

    def _handle_session_end(self):
        if self.mode == "work":
            self.completed_cycles += 1
            if self.completed_cycles % self.cycles_before_long == 0:
                self.mode = "long break"
            else:
                self.mode = "short break"
        else:
            self.mode = "work"
        self.remaining = self._current_mode_duration()
        self.mode_changed.emit(self.mode)
        self.time_changed.emit(self.remaining)

    def _current_mode_duration(self):
        if self.mode == "work":
            return self.work
        elif self.mode == "short break":
            return self.short_break
        else:
            return self.long_break

    def update_settings(self, d):
        self.work = d.get("work", self.work)
        self.short_break = d.get("short_break", self.short_break)
        self.long_break = d.get("long_break", self.long_break)
        self.cycles_before_long = d.get("cycles_before_long", self.cycles_before_long)
        if not self.is_running:
            self.remaining = self._current_mode_duration()
            self.time_changed.emit(self.remaining)
