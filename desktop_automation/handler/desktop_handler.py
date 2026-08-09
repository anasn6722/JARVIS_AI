class DesktopHandler:
    """High-level desktop automation commands."""
    
    
    def __init__(self, controller):
        self.controller = controller
    
    # =====================================================
    # FOCUS
    # =====================================================
    
    def focus_window(self, target):
        """Focus a window by name."""
    
        if not target:
            return "Please tell me which window to focus."
    
        success, message = self.controller.focus_window(target)
    
        return message
    
    # =====================================================
    # CLOSE
    # =====================================================
    
    
    # =====================================================
    # ACTIVE WINDOW
    # =====================================================
    
    def active_window(self):
        """Return information about the active window."""
    
        window = self.controller.active_window()
    
        if not window:
            return "I couldn't determine the active window."
    
        return f"The active window is {window['title']}."
    
    # =====================================================
    # LIST WINDOWS
    # =====================================================
    
    def list_windows(self):
        """Return visible desktop windows."""
    
        windows = self.controller.list_windows()
    
        if not windows:
            return "I couldn't find any visible windows."
    
        titles = [
            window["title"]
            for window in windows
        ]
    
        return "\n".join(titles)
    