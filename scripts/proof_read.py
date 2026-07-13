"""
My cheap ass can't afford tokens,
so this script will take a message from nvim,
then open the browser and ask Claude to proofread that message in a way
that it only outputs the text,
and copy that message to the clipboard.
"""
# First part: Copy from nvim to clipboard
# It will rely on the fact that my "y" sends to a register per my nvim config
import pyautogui
# You are expected to use those 3 seconds to click on the windows that has nvim/vim open
pyautogui.sleep(3)
pyautogui.press(['g','g',])
pyautogui.hotkey('shift','v')
pyautogui.hotkey('shift','g')
pyautogui.write('y')
pyautogui.hotkey('win','b')
import i3ipc
i3 = i3ipc.Connection()
tree = i3.get_tree()
windows = tree.find_classed("^Brave-browser$")
if windows:
    win = windows[0]
    win.command("focus")
    pyautogui.sleep(1)
pyautogui.hotkey('ctrl', 't')          # new tab, auto-focuses the omnibox
pyautogui.write('claude.ai', interval=0.03)
pyautogui.press('enter')
pyautogui.sleep(2)
pyautogui.press('tab')
pyautogui.write(
    'Proofread this message and reply with ONLY the corrected text, '
    'no comments: ',
    interval=0.02,
)
pyautogui.sleep(0.01)
pyautogui.hotkey('ctrl','v')
pyautogui.sleep(0.05)
pyautogui.press('enter')
# Regex search on window title/name
#windows = tree.find_named("Brave")[0]
