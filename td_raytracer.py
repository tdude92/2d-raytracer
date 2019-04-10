import tkinter
from math import sin, cos, radians
from random import randint
from time import sleep

def create_rays(pillars, lsc_x, lsc_y):
    """
    Arguments: List of pillar IDs; Light source center coords: x and y.

    Function: Create rays that are obstructed by pillar walls.

    Returns: A list of ray IDs.
    """

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
                # Calculate point of intersection x-value if slopes are not undefined.
                poi_x = (s_b - r_b) / (r_m - s_m)
                # Calculate point of intersection y-value if slopes are not undefined.
                poi_y = r_m*poi_x + r_b

            # Delete and replace line with new line.
            canvas.delete(j)
            rays.append(canvas.create_line(lsc_x, lsc_y, poi_x, poi_y, fill = "yellow"))

    return rays


if __name__ == "__main__":
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

    # Light Source Center Coordinates.
    lsc_x = 200
    lsc_y = 200

    # Pick a random number to be the angle that the light source will go.
    ls_angle = randint(0, 360) # Change this to change where the light source goes.

    # Detect if an are around lsc is colliding with a pillar. If true, change the angle accordingly (using the Law of Reflection). If false, do nothing. 
    # Then move the lsc a bit before repeating.
    def animation(lsc_x, lsc_y):
        # Create Rays.
        rays = create_rays(pillars, lsc_x, lsc_y)

        collisions = canvas.find_overlapping(lsc_x - 5, lsc_y - 5, lsc_x + 5, lsc_y + 5)

        # Check if the lamp is overlapping with a pillar side.
        if collisions:
            pass
        
        # Find the x and y displacements of the lamp.
        ls_xd = 5 * cos(radians(ls_angle)) # Light Source x-displacement.
        ls_yd = 5 * sin(radians(ls_angle)) # Light Source y-displacement.

        # Delete Rays.
        for i in rays:
            canvas.delete(i)

        # Move light source centers and the lamp.
        lsc_x += ls_xd
        lsc_y -= ls_yd

        root.after_idle(animation, lsc_x, lsc_y)

    animation(lsc_x, lsc_y)

    root.mainloop()