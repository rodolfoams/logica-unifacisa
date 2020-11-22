from graphics import Text, Point, Line, GraphWin, color_rgb
from random import randint, shuffle
from argparse import ArgumentParser
from PIL import Image
import io
import os

os.environ["PATH"] += ":/usr/local/bin:/usr/local/bin/gs"


def get_input_args():
    parser = ArgumentParser()
    parser.add_argument('--window_width', type=int, default=500,
                        help="The width of the display window.")
    parser.add_argument('--window_height', type=int, default=500,
                        help="The height of the display window.")
    parser.add_argument('--square_size', type=int, default=50,
                        help="The legth of the side of each square in the Karnaugh map.")
    parser.add_argument('--filename', type=str, default="karnaugh.jpg",
                        help="The output file containing the Karnaugh map.")
    return parser.parse_args()


def get_k_map_lines(window_width, window_height, square_dim):
    k_map_lines = []
    for i in range(5):

        # Default horizontal line
        h_line_x_begin = window_width/2 - 2*square_dim
        h_line_x_end = window_width/2 + 2*square_dim
        h_line_y = window_height/2 + square_dim*(i-2)

        # Default vertical line
        v_line_x = window_width/2 + square_dim*(i-2)
        v_line_y_begin = window_height/2 - 2*square_dim
        v_line_y_end = window_height/2 + 2*square_dim

        if i % 2 == 1:
            h_line_x_end += square_dim
            v_line_y_end += square_dim

        elif i == 2:
            h_line_x_begin -= square_dim
            v_line_y_begin -= square_dim

        k_map_lines.extend([
            Line(
                Point(h_line_x_begin, h_line_y),
                Point(h_line_x_end, h_line_y)
            ),
            Line(
                Point(v_line_x, v_line_y_begin),
                Point(v_line_x, v_line_y_end)
            )]
        )

    return k_map_lines


def get_k_map_variable_labels(window_width, window_height, square_dim, variables):
    labels = []
    labels.append(Text(Point(int(window_width/2 - 2.5*square_dim),
                             window_height/2 - square_dim), variables[0][1]))
    labels.append(Text(Point(int(window_width/2 - 2.5*square_dim),
                             window_height/2 + square_dim), variables[0][0]))

    labels.append(
        Text(Point(int(window_width/2 + 2.5*square_dim), window_height/2), variables[1][0]))
    labels.append(Text(Point(int(window_width/2 + 2.5*square_dim),
                             int(window_height/2 - 1.5*square_dim)), variables[1][1]))
    labels.append(Text(Point(int(window_width/2 + 2.5*square_dim),
                             int(window_height/2 + 1.5*square_dim)), variables[1][1]))

    labels.append(Text(Point(int(window_width/2 - square_dim),
                             window_height/2 - 2.5*square_dim), variables[2][1]))
    labels.append(Text(Point(int(window_width/2 + square_dim),
                             window_height/2 - 2.5*square_dim), variables[2][0]))

    labels.append(
        Text(Point(int(window_width/2), window_height/2 + 2.5*square_dim), variables[3][0]))
    labels.append(
        Text(Point(int(window_width/2 - 1.5*square_dim), window_height/2 + 2.5*square_dim), variables[3][1]))
    labels.append(
        Text(Point(int(window_width/2 + 1.5*square_dim), window_height/2 + 2.5*square_dim), variables[3][1]))

    return labels


def get_k_map_values():
    return [[randint(0, 1) for i in range(4)] for j in range(4)]


def get_k_map_text_values(window_width, window_height, square_dim, k_map_values):
    return [Text(Point(window_width/2 + (x-2)*square_dim + square_dim/2, window_height/2 + (y-2)*square_dim + square_dim/2), str(k_map_values[x][y])) for x in range(4) for y in range(4)]


def main(window_width, window_height, square_dim, filename):

    window = GraphWin("Karnaugh Map", window_width, window_height)

    window.setBackground(color_rgb(255, 255, 255))

    for line in get_k_map_lines(window_width, window_height, square_dim):
        line.setWidth(1)
        line.setFill(color_rgb(0, 0, 0))
        line.draw(window)

    variables = [(chr(i), chr(i) + "'") for i in range(65, 91)]
    shuffle(variables)
    for label in get_k_map_variable_labels(window_width, window_height, square_dim, variables):
        label.setTextColor('black')
        label.setSize(30)
        label.draw(window)

    k_map_values = get_k_map_values()
    for text in get_k_map_text_values(window_width, window_height, square_dim, k_map_values):
        text.setTextColor('black')
        text.setSize(30)
        text.draw(window)
    # print(k_map_values)
    ps = window.postscript(colormode='color')
    img = Image.open(io.BytesIO(ps.encode('utf-8')))
    img.save(filename)

    window.close()


if __name__ == "__main__":
    args = get_input_args()
    main(window_width=args.window_width,
         window_height=args.window_height,
         square_dim=args.square_size,
         filename=args.filename)
