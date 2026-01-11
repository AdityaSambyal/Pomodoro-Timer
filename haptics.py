import platform

class HapticsManager:
    def __init__(self):
        self.platform = platform.system().lower()
        self._mgr = None
        self._winsound = None
        if self.platform == 'darwin':
            try:
                # optional: requires pyobjc (pyobjc-framework-AppKit)
                from AppKit import NSHapticFeedbackManager
                self._mgr = NSHapticFeedbackManager.defaultPerformer()
            except Exception:
                self._mgr = None
        elif self.platform == 'windows':
            try:
                import winsound
                self._winsound = winsound
            except Exception:
                self._winsound = None

    def perform(self, style='light'):
        """Try to perform haptic feedback; falls back to a short sound if unavailable."""
        if self.platform == 'darwin' and self._mgr is not None:
            try:
                # 0 == generic pattern; performanceTime 0 is default
                self._mgr.performFeedback_performanceTime_(0, 0)
                return
            except Exception:
                pass
        if self.platform == 'windows' and self._winsound is not None:
            try:
                # Use MessageBeep as a short feedback
                self._winsound.MessageBeep(self._winsound.MB_OK)
                return
            except Exception:
                pass
        # fallback: try a short sound
        try:
            from sounds import SoundManager
            SoundManager().play_haptic_beep()
        except Exception:
            pass
