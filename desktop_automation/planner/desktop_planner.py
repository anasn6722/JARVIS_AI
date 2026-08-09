class DesktopPlanner:
    """Convert desktop commands into structured actions."""
    
    ACTIONS = {
        # Window listing / information
        "show windows": "list_windows",
        "list windows": "list_windows",
        "show all windows": "list_windows",
        "list all windows": "list_windows",
    
        "active window": "active_window",
        "current window": "active_window",
        "what is active": "active_window",
    
        # Focus / switch
        "focus": "focus_window",
        "focus window": "focus_window",
        "switch to": "focus_window",
        "switch window to": "focus_window",
        "bring": "focus_window",
        "bring window": "focus_window",
        "bring forward": "focus_window",
    
        # Minimize
        "minimize": "minimize_window",
        "minimize window": "minimize_window",
        "hide": "minimize_window",
        "hide window": "minimize_window",
    
        # Maximize
        "maximize": "maximize_window",
        "maximize window": "maximize_window",
        "make full screen": "maximize_window",
        "expand": "maximize_window",
    
        # Restore
        "restore": "restore_window",
        "restore window": "restore_window",
        "show": "restore_window",
        "show window": "restore_window",
        "bring back": "restore_window",
    
        # Close
        "close": "close_window",
        "close window": "close_window",
        "exit": "close_window",
        "exit window": "close_window",
    }
    
    def plan(self, command):
        """Convert a text command into an action and target."""
    
        if not command:
            return None
    
        command = " ".join(command.lower().strip().split())
    
        # Commands without a target.
        if command in self.ACTIONS:
            action = self.ACTIONS[command]
    
            if action in {
                "list_windows",
                "active_window",
            }:
                return {
                    "action": action,
                    "target": None,
                }
    
            return None
    
        # Commands that require a target.
        #
        # Sort phrases by length so that:
        #
        # "focus window VS Code"
        #
        # is matched before:
        #
        # "focus VS Code"
        #
        # This prevents shorter phrases from stealing commands
        # from more specific phrases.
        phrases = sorted(
            self.ACTIONS.items(),
            key=lambda item: len(item[0]),
            reverse=True,
        )
    
        for phrase, action in phrases:
            prefix = phrase + " "
    
            if not command.startswith(prefix):
                continue
            
            target = command[len(prefix):].strip()
    
            if not target:
                return None
    
            if action in {
                "list_windows",
                "active_window",
            }:
                return None
    
            return {
                "action": action,
                "target": target,
            }
    
        return None
    