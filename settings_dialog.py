from PySide6.QtWidgets import QDialog, QFormLayout, QSpinBox, QDialogButtonBox, QCheckBox
from PySide6.QtCore import Qt
from settings import load_settings

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.work = QSpinBox()
        self.work.setRange(5, 180)
        self.work.setValue(int(parent.timer.work/60))
        self.short = QSpinBox(); self.short.setRange(1,60); self.short.setValue(int(parent.timer.short_break/60))
        self.long = QSpinBox(); self.long.setRange(5,120); self.long.setValue(int(parent.timer.long_break/60))
        self.cycles = QSpinBox(); self.cycles.setRange(1,10); self.cycles.setValue(parent.timer.cycles_before_long)
        form = QFormLayout(self)
        form.addRow("Work (min)", self.work)
        form.addRow("Short break (min)", self.short)
        form.addRow("Long break (min)", self.long)
        form.addRow("Cycles before long", self.cycles)
        # sound/haptics
        settings = load_settings()
        self.sound_chk = QCheckBox()
        self.sound_chk.setChecked(settings.get('sound', True))
        self.haptics_chk = QCheckBox()
        self.haptics_chk.setChecked(settings.get('haptics', False))
        form.addRow("Enable sound", self.sound_chk)
        form.addRow("Enable haptics (macOS)", self.haptics_chk)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel, Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        form.addWidget(buttons)

    def values(self):
        return {
            "work": int(self.work.value())*60,
            "short_break": int(self.short.value())*60,
            "long_break": int(self.long.value())*60,
            "cycles_before_long": int(self.cycles.value()),
            "sound": bool(self.sound_chk.isChecked()),
            "haptics": bool(self.haptics_chk.isChecked())
        }
