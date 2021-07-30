import dearpygui.dearpygui as dpg
import tkinter as tk
import threading
import time

dpg.setup_registries()  # Registries for mouse and keyboard press events

root = tk.Tk()
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
screen_height = screen_height - int(0.05*screen_height)

slither_data = [] # List of points and their respective direction. [[x_coordinate, y_coordinate], direction]
snake_length = 0
snake_direction = 2  # Keeps a track of direction of the snake. 1=West, 2=North, 3=East, 4=South
direction_change_data = []  # List of change of directions. [[x_coordinate, y_coordinate], direction]


def initial_slither_points():
    # Function sets all the points required to draw the snake
    global snake_length, snake_direction, slither_data

    head_point = [25, 25]
    tail_point = [25, 10]
    snake_length = head_point[1] - tail_point[1]
    for point in range(snake_length):
        slither_data.append([[head_point[0], (head_point[1] - point)], snake_direction])

    slither_data.append([tail_point, snake_direction])


def move_snakeDispatcher():
    # Function creates a new thread that controls the continuous movement of the snake while the main code is listening
    # for any keyboard or mouse events to occur
    move_snake_thread = threading.Thread(name="line_tool", target=move_snake, args=(), daemon=True)
    move_snake_thread.start()


def move_snake():
    global slither_data, snake_length, snake_direction, direction_change_data

    while True:
        if slither_data[0][0][1] == 50 or slither_data[0][0][0] == 50:  # Check if the snake touches the walls
            print('Game over!')
            break  # End Game

        else:
            for index in range(len(slither_data)):
                # This loop controls the continuous motion of the snake
                if slither_data[index][1] == 1:
                    # Move West. Subtract X
                    slither_data[index][0][0] -= 1

                elif slither_data[index][1] == 2:
                    # Move North. Add Y
                    slither_data[index][0][1] += 1

                elif slither_data[index][1] == 1:
                    # Move East. Add X
                    slither_data[index][0][0] += 1

                elif slither_data[index][1] == 1:
                    # Move South. Subtract Y
                    slither_data[index][0][1] -= 1

            for index in range(len(slither_data)-1):
                # This loops checks if any of the points have reached the change of direction point and changes the
                # snake direction accordingly
                if slither_data[index+1][0] in get_points_from_data(direction_change_data):
                    # If the point of the snake is found in the list of direction of changes, then get the direction
                    # and update the snake direction
                    slither_data[index+1][1] = get_direction_from_data(slither_data[index+1][0], direction_change_data)


        dpg.configure_item(item=snake, points=get_points_from_data(slither_data))
        time.sleep(0.1)


def get_points_from_data(data):
    # Functions takes entire data of slither and returns only the points
    slither_points = []
    for index in range(len(data)):
        slither_points.append(data[index][0])

    return slither_points


def get_direction_from_data(point, data):
    # Functions takes the entire data and extracts a particular direction for a given point
    for index in range(len(data)):
        if point == data[index][0]:
            return index


def key_release_handler(sender, app_data):
    # Function listening to key release events. Arrow keys change snake direction and keeps a track of the point when
    # the key even occurs
    global snake_direction, direction_change_data, slither_data

    head_point = slither_data[0][0][:]

    if app_data == 37:
        snake_direction = 1
        slither_data[0][0][1] = snake_direction  # Change direction of head point
        direction_change_data.append([head_point, snake_direction])

    elif app_data == 38:
        snake_direction = 2
        slither_data[0][0][1] = snake_direction
        direction_change_data.append([head_point, snake_direction])

    elif app_data == 39:
        snake_direction = 3
        slither_data[0][0][1] = snake_direction
        direction_change_data.append([head_point, snake_direction])

    elif app_data == 40:
        snake_direction = 4
        slither_data[0][0][1] = snake_direction
        direction_change_data.append([head_point, snake_direction])


initial_slither_points()
time.sleep(1)

dpg.setup_viewport()
dpg.set_viewport_title("Snakey")
dpg.configure_viewport(0, x_pos=0, y_pos=0, width=screen_width, height=(screen_height))

with dpg.window(pos=[0, 0], autosize=True, no_collapse=True, no_resize=True, no_close=True, no_move=True,
                no_title_bar=True):
    with dpg.plot(no_menus=False, no_title=True, no_box_select=True, no_mouse_pos=True, width=500,
                  height=500, equal_aspects=True):
        ...
        default_x = dpg.add_plot_axis(axis=0, no_gridlines=False, no_tick_marks=True, no_tick_labels=False, label="",
                                      lock_min=True)
        dpg.set_axis_limits(axis=default_x, ymin=0, ymax=50)
        default_y = dpg.add_plot_axis(axis=1, no_gridlines=False, no_tick_marks=True, no_tick_labels=False, label="",
                                      lock_min=True)
        dpg.set_axis_limits(axis=default_y, ymin=0, ymax=50)

        snake = dpg.draw_polyline(points=get_points_from_data(slither_data), thickness=1, color=[0, 255, 0])

        dpg.draw_rectangle(pmin=[10, 10], pmax=[12, 12], thickness=0, color=[255, 0, 0], fill=[255, 0, 0])

    dpg.add_button(label="Move", callback=move_snakeDispatcher)

    dpg.add_key_release_handler(callback=key_release_handler)

dpg.start_dearpygui()