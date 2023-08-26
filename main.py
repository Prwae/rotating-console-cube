import math
import os
import time
import shutil


def draw_line(x1, y1, x2, y2, symbol):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        print("\033[%d;%dH%s" % (y1 + 1, x1 + 1, symbol), end='', flush=True)

        if x1 == x2 and y1 == y2:
            break

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def main(width, height, line_symbol, fps):
    while True:
        clear_screen()
        time_now = time.time()
        angle_x = time_now % (2 * math.pi)
        angle_y = (time_now * 0.5) % (2 * math.pi)
        angle_z = (time_now * 0.2) % (2 * math.pi)

        console_columns, console_lines = shutil.get_terminal_size()

        indent_top = (console_lines // 2) - height // 16
        indent_left = (console_columns // 2) - width // 16

        cos_angle_x = math.cos(angle_x)
        sin_angle_x = math.sin(angle_x)
        cos_angle_y = math.cos(angle_y)
        sin_angle_y = math.sin(angle_y)
        cos_angle_z = math.cos(angle_z)
        sin_angle_z = math.sin(angle_z)

        vertices = [
            (-1, -1, -1),
            (1, -1, -1),
            (1, 1, -1),
            (-1, 1, -1),
            (-1, -1, 1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, 1, 1),
        ]

        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7),
        ]

        rotated_vertices = []
        for vertex in vertices:
            x, y, z = vertex
            new_x = cos_angle_x * x - sin_angle_x * z
            new_z = sin_angle_x * x + cos_angle_x * z
            new_y = cos_angle_y * y - sin_angle_y * new_z
            final_x = cos_angle_z * new_x - sin_angle_z * new_y
            final_y = sin_angle_z * new_x + cos_angle_z * new_y
            rotated_z = final_y * sin_angle_z + new_z * cos_angle_z
            rotated_vertices.append((final_x, final_y, rotated_z))

        for edge in edges:
            start_vertex = rotated_vertices[edge[0]]
            end_vertex = rotated_vertices[edge[1]]

            x1 = int(start_vertex[0] * width) + indent_left
            y1 = int(start_vertex[1] * height) + indent_top
            x2 = int(end_vertex[0] * width) + indent_left
            y2 = int(end_vertex[1] * height) + indent_top

            draw_line(x1, y1, x2, y2, line_symbol)

        time.sleep(1/fps)


if __name__ == "__main__":
    width = int(input("Input width: "))
    height = int(input("Input height: "))
    line_symbol = input("Input symbol (or string), with which the cube will be drawn: ")
    fps = int(input("Input speed of rotating in FPS (faster speed may affect on stability): "))
    main(width, height, line_symbol, fps)
