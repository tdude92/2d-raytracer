import tkinter
from math import sin, cos, radians

root = tkinter.Tk()

canvas = tkinter.Canvas(root, width = 400, height = 400)
canvas.pack()

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

# Light Source Coordinates
lsx0 = 195
lsy0 = 195
lsx1 = 205
lsy1 = 205

# Light Source Center Coordinates
lsc_x = (lsx0 + lsx1) / 2
lsc_y = (lsy0 + lsy1) / 2

# Create 360 rays of light.
# Use sin and cos to calculate x and y displacement from light source center to x1 and y1.
rays = []
for i in range(1, 361):
    x_displacement = 400 * cos(radians(i)) # adj = hyp*cos(x)
    y_displacement = 400 * sin(radians(i)) # opp = hyp*sin(x)
    rays.append(canvas.create_line(lsc_x, lsc_y, lsc_x + x_displacement, lsc_y + y_displacement, fill = "yellow"))

# Detect light rays that overlap with pillar sides and create a new line from the light source to the point of intersection (of the pillar side and light ray).
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
                raise ValueError
        else:
            # Calculate point of intersection x-value if slopes are not undefined.
            poi_x = (s_b - r_b) / (r_m - s_m)
            # Calculate point of intersection y-value if slopes are not undefined.
            poi_y = r_m*poi_x + r_b

        # Delete and replace line with new line.
        canvas.delete(j)
        rays.append(canvas.create_line(lsc_x, lsc_y, poi_x, poi_y, fill = "yellow"))

light_source = canvas.create_oval(lsx0, lsy0, lsx1, lsy1, fill = "white", outline = "yellow")

tkinter.mainloop()
