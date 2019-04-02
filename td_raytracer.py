# In progress plz no roast
import tkinter
from math import sin, cos, radians

root = tkinter.Tk()

canvas = tkinter.Canvas(root, width = 400, height = 400)
canvas.pack()

# Draw the sides of the pillars.
# Not rectangles so that we know with which side the light ray intersects.
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

light_source = canvas.create_oval(lsx0, lsy0, lsx1, lsy1, fill = "yellow")

# Create 360 rays of light.
# Use sin and cos to calculate x and y displacement from light source center to x1 and y1.
rays = []
for i in range(361):
    x_displacement = 200 * cos(radians(i)) # adj = hyp*cos(x)
    y_displacement = 200 * sin(radians(i)) # opp = hyp*sin(x)
    rays.append(canvas.create_line(lsc_x, lsc_y, lsc_x + x_displacement, lsc_y + y_displacement, fill = "yellow"))

# Detect light rays that overlap with pillar sides and create a new line from the light source to the point of intersection (of the pillar side and light ray).
for i in pillars:
    obstructed_rays = tkinter.find_overlapping(canvas.coords(i))
    for i in obstructed_rays:
        

tkinter.mainloop()
