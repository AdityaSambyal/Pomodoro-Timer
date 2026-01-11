import os
from PySide6.QtWidgets import QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt
from timer import PomodoroTimer
from settings import load_settings, save_settings
from notify import notify
from settings_dialog import SettingsDialog
from sounds import SoundManager
from haptics import HapticsManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pomodoro")
        self.timer = PomodoroTimer()

        settings = load_settings()
        if settings:
            self.timer.update_settings(settings)
        # runtime settings
        self.settings = settings or {}
        self.enable_sound = self.settings.get('sound', True)
        self.enable_haptics = self.settings.get('haptics', False)
        self.sound = SoundManager()
        self.haptics = HapticsManager()

        central = QWidget()
        self.setCentralWidget(central)
        v = QVBoxLayout(central)

        self.mode_label = QLabel(self.timer.mode.capitalize())
        self.mode_label.setAlignment(Qt.AlignCenter)
        self.time_label = QLabel(self._format_time(self.timer.remaining))
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size: 48px;")

        h = QHBoxLayout()
        self.start_btn = QPushButton("Start")
        self.pause_btn = QPushButton("Pause")
        self.reset_btn = QPushButton("Reset")
        self.set_btn = QPushButton("Settings")
        h.addWidget(self.start_btn); h.addWidget(self.pause_btn); h.addWidget(self.reset_btn); h.addWidget(self.set_btn)

        v.addWidget(self.mode_label)
        v.addWidget(self.time_label)
        v.addLayout(h)

        self.start_btn.clicked.connect(self.timer.start)
        self.pause_btn.clicked.connect(self.timer.pause)
        self.reset_btn.clicked.connect(self.timer.reset)
        self.set_btn.clicked.connect(self.open_settings)

        self.timer.time_changed.connect(self.on_time_changed)
        self.timer.mode_changed.connect(self.on_mode_changed)
        self.timer.finished.connect(self.on_finished)
        self.timer.running_changed.connect(self.on_running_changed)

        self.on_running_changed(self.timer.is_running)

    def on_time_changed(self, seconds):
        self.time_label.setText(self._format_time(seconds))

    def on_mode_changed(self, mode):
        self.mode_label.setText(mode.capitalize())

    def on_finished(self):
        notify("Pomodoro", f"{self.timer.mode.capitalize()} finished!")
        # play sound/haptic if enabled
        if getattr(self, 'enable_sound', True):
            try:
                self.sound.play_finish()
            except Exception:
                pass
        if getattr(self, 'enable_haptics', False):
            try:
                self.haptics.perform()
            except Exception:
                pass

    def on_running_changed(self, running):
        self.start_btn.setEnabled(not running)
        self.pause_btn.setEnabled(running)

    def open_settings(self):
        dlg = SettingsDialog(self)
        if dlg.exec():
            s = dlg.values()
            save_settings(s)
            self.timer.update_settings(s)
            # update runtime flags
            self.enable_sound = s.get('sound', self.enable_sound)
            self.enable_haptics = s.get('haptics', self.enable_haptics)

    def _format_time(self, seconds):
        m = seconds // 60
        s = seconds % 60
        return f"{int(m):02d}:{int(s):02d}"
