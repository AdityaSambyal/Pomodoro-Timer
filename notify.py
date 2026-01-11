try:
    from plyer import notification
    def notify(title, message):
        notification.notify(title=title, message=message)
except Exception:
    def notify(title, message):
        print(f"NOTIFY: {title} - {message}")
