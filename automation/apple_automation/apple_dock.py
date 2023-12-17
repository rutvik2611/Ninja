import subprocess

def remove_chrome_from_dock():
    applescript = """
    tell application "System Events"
        if exists process "Google Chrome" then
            tell application "Google Chrome" to quit
        end if
        delay 2
        tell application "Dock"
            delete every dock item where its name is "Google Chrome"
        end tell
    end tell
    """
    subprocess.run(['osascript', '-e', applescript])

if __name__ == "__main__":
    remove_chrome_from_dock()