import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Create a figure and axis
fig, ax = plt.subplots()

# Draw the car body (reversed coordinates)
car_body = patches.Polygon(
    [(300, 370), (260, 370), (240, 330), (110, 330), (90, 370), (50, 370),
     (50, 340), (80, 330), (110, 300), (200, 300), (240, 330), (300, 350)],
    closed=True,
    facecolor='black'  # Change car body color to black
)
ax.add_patch(car_body)

# Draw the windows (reversed coordinates)
window1 = patches.Polygon([(195, 305), (230, 330), (165, 330), (165, 305)], closed=True, facecolor='black')  # Change window color to black
window2 = patches.Polygon([(120, 305), (95, 330), (160, 330), (160, 305)], closed=True, facecolor='black')  # Change window color to black
ax.add_patch(window1)
ax.add_patch(window2)

# Draw the wheels (reversed coordinates)
wheel1 = patches.Circle((240, 370), 17, facecolor='black')
wheel2 = patches.Circle((110, 370), 17, facecolor='black')
ax.add_patch(wheel1)
ax.add_patch(wheel2)

# Draw the road (reversed coordinates)
road = patches.Rectangle((0, 0), 640, 10, facecolor='gray')
ax.add_patch(road)

# Set aspect ratio and limits
ax.set_aspect('equal')
ax.set_xlim(0, 320)
ax.set_ylim(0, 400)

# Remove axes for a cleaner look
ax.axis('off')

# Reverse the plot by 180 degrees
ax.invert_xaxis()
ax.invert_yaxis()

# Show the plot
plt.show()