import tkinter
from math import sin, cos, radians
from time import sleep

# Light Source Coordinates
lsx0 = 195
lsy0 = 195
lsx1 = 205
lsy1 = 205

def create_rays(lsc_x, lsc_y):
    # Create 360 rays of light.
    # Input: Light source center x and y coords.
    # Returns: A list of line IDs.
    # Use sin and cos to calculate x and y displacement from light source center to x1 and y1.
    rays = []
    for i in range(721):
        x_displacement = 400 * cos(radians(i/2)) # adj = hyp*cos(x)
        y_displacement = 400 * sin(radians(i/2)) # opp = hyp*sin(x)
        rays.append(canvas.create_line(lsc_x, lsc_y, lsc_x + x_displacement, lsc_y + y_displacement, fill = "yellow"))
    return rays


def calculate_obstructions(pillars, lsc_x, lsc_y):
    # Detect light rays that overlap with pillar sides and create a new line from the light source to the point of intersection (of the pillar side and light ray).
    # Input: List of pillar sides, Light source center x and y coords.
    # Returns: None.
    global rays

    for i in pillars:
        obstructed_rays_with_imposters = list(canvas.find_overlapping(*canvas.coords(i)))

        # Weed out imposter pillars.
        obstructed_rays = [i for i in obstructed_rays_with_imposters if not i in pillars]

        for j in obstructed_rays:
            s_ep = canvas.coords(i) # Side endpoints.
            r_ep = canvas.coords(j) # Ray endpoints.

            try:
                # Calculate slope of the lines.
                s_m = (s_ep[1] - s_ep[3]) / (s_ep[0] - s_ep[2])
                r_m = (r_ep[1] - r_ep[3]) / (r_ep[0] - r_ep[2])
                # Calculate y-intercept of the lines.
                s_b = s_ep[1] - s_m*s_ep[0]
                r_b = r_ep[1] - r_m*r_ep[0]
            except ZeroDivisionError:
                # Account for vertical lines with undefined slopes.
                if s_ep[0] - s_ep[2] == 0 and r_ep[0] - r_ep[2] == 0:
                    # The closer endpoint is the point of intersection.
                    if abs(s_ep[1] - lsc_y) < abs(s_ep[3] - lsc_y):
                        poi_x = s_ep[0]
                        poi_y = s_ep[1]
                    else:
                        poi_x = s_ep[2]
                        poi_y = s_ep[3]
                elif s_ep[0] - s_ep[2] == 0:
                    # Calculate defined slope and y-intercept.
                    r_m = (r_ep[1] - r_ep[3]) / (r_ep[0] - r_ep[2])
                    r_b = r_ep[1] - r_m*r_ep[0]
                    # Calculate point of intersection if the side has an undefined slope.
                    poi_x = s_ep[0]
                    poi_y = r_m*poi_x + r_b
                elif r_ep[0] - r_ep[2] == 0:
                    # Calculate defined slope and y-intercept.
                    s_m = (s_ep[1] - s_ep[3]) / (s_ep[0] - s_ep[2])
                    s_b = s_ep[1] - s_m*s_ep[0]
                    # Calculate point of intersection if the ray has an undefined slope.
                    poi_x = r_ep[0]
                    poi_y = s_m*poi_x + s_b
                else:
                    poi_x = lsc_x
                    poi_y = lsc_y
            else:
                # Calculate point of intersection x-value if slopes are not undefined.
                poi_x = (s_b - r_b) / (r_m - s_m)
                # Calculate point of intersection y-value if slopes are not undefined.
                poi_y = r_m*poi_x + r_b

            # Delete and replace line with new line.
            canvas.delete(j)
            rays.append(canvas.create_line(lsc_x, lsc_y, poi_x, poi_y, fill = "yellow"))


def del_rays(rays):
    out = rays
    for i in out:
        canvas.delete(i)
        out.remove(i)
    return out

def del_ls(light_source):
    canvas.remove(light_source)


def move_ls(direction, rays, light_source):
    global lsx0
    global lsy0
    global lsx1
    global lsy1

    if direction == 1:
        # Up
        lsy0 -= 10
        lsy1 -= 10
    elif direction == 2:
        # Down
        lsy0 += 10
        lsy1 += 10
    elif direction == 3:
        # Left
        lsx0 -= 10
        lsx1 -= 10
    elif direction == 4:
        # Right
        lsx0 += 10
        lsx1 += 10


# Event Handlers (For Moving)
def up(event):
    move_ls(1, rays, light_source)

    del_rays(rays)
    del_ls(light_source)

    lsc_x = (lsx0 + lsx1) / 2
    lsc_y = (lsy0 + lsy1) / 2

    create_rays(lsc_x, lsc_y)
    calculate_obstructions(pillars, lsc_x, lsc_y)

    light_source = canvas.create_oval(lsx0, lsy0, lsx1, lsy1, fill = "white", outline = "yellow")


def down(event):
    move_ls(2, rays, light_source)

    del_rays(rays)
    del_ls(light_source)

    lsc_x = (lsx0 + lsx1) / 2
    lsc_y = (lsy0 + lsy1) / 2

    create_rays(lsc_x, lsc_y)
    calculate_obstructions(pillars, lsc_x, lsc_y)

    light_source = canvas.create_oval(lsx0, lsy0, lsx1, lsy1, fill = "white", outline = "yellow")


def left(event):
    move_ls(3, rays, light_source)

    del_rays(rays)
    del_ls(light_source)

    lsc_x = (lsx0 + lsx1) / 2
    lsc_y = (lsy0 + lsy1) / 2

    create_rays(lsc_x, lsc_y)
    calculate_obstructions(pillars, lsc_x, lsc_y)

    light_source = canvas.create_oval(lsx0, lsy0, lsx1, lsy1, fill = "white", outline = "yellow")


def right(event):
    move_ls(4, rays, light_source)

    del_rays(rays)
    del_ls(light_source)

    lsc_x = (lsx0 + lsx1) / 2
    lsc_y = (lsy0 + lsy1) / 2

    create_rays(lsc_x, lsc_y)
    calculate_obstructions(pillars, lsc_x, lsc_y)

    light_source = canvas.create_oval(lsx0, lsy0, lsx1, lsy1, fill = "white", outline = "yellow")


if __name__ == "__main__":
    root = tkinter.Tk()

    canvas = tkinter.Canvas(root, width = 400, height = 400, bg = "black")
    canvas.pack()

    # Bind Key Events to Handlers (For Moving)
    canvas.bind("w", up)
    canvas.bind("s", down)
    canvas.bind("a", left)
    canvas.bind("d", right)

    # Draw the sides of the pillars.
    # Not rectangles because we want to know which side the rays intersects with.
    pillars = []
    y0 = 25
    for i in range(4):
        x0 = 25
        for i in range(4):
            pillars.append(canvas.create_line(x0, y0, x0, y0 + 50, fill = "black"))
            pillars.append(canvas.create_line(x0, y0, x0 + 50, y0, fill = "black"))
            pillars.append(canvas.create_line(x0 + 50, y0, x0 + 50, y0 + 50, fill = "black"))
            pillars.append(canvas.create_line(x0, y0 + 50, x0 + 50, y0 + 50, fill = "black"))
            x0 += 100
        y0 += 100

    # Light Source Center Coordinates
    lsc_x = (lsx0 + lsx1) / 2
    lsc_y = (lsy0 + lsy1) / 2

    # Draw the rays
    rays = create_rays(lsc_x, lsc_y)

    # Calculate obstructions
    calculate_obstructions(pillars, lsc_x, lsc_y)

    light_source = canvas.create_oval(lsx0, lsy0, lsx1, lsy1, fill = "white", outline = "yellow")

    tkinter.mainloop()
