import dearpygui.dearpygui as dpg

from windows.screen_resolution import get_screen_resolution
from theme_settings import *

# Record screen resolution
screen_width, screen_height = get_screen_resolution()

# Subtract Taskbar and title bar height
screen_height = screen_height - int(0.05*screen_height)

# Set up the base layout for all child windows
with dpg.window(label="Base window", no_title_bar=True, width=screen_width,
                height=screen_height, pos=[0, 0], no_resize=True, no_close=True, no_move=True) as base_window:

    with dpg.child(label="Score Board", width=int(0.4*screen_width), height=50, horizontal_scrollbar=True,
                   no_scrollbar=True) as score_board:
        dpg.set_item_theme(item=score_board, theme=score_board_theme)

        with dpg.group(horizontal=True, parent=score_board) as tool_group:
            dpg.add_dummy()
            dpg.add_text(default_value="Points: ")
