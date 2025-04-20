import matplotlib.pyplot as plt
import matplotlib.patches as patches

IMAGE_WIDTH = 640
IMAGE_HEIGHT = 640

# Load polygon from the first file (skip class label)
with open('sample_polygon.txt', 'r') as f:
    first_line = f.readline().strip()
    values = list(map(float, first_line.split()))
    polygon = values[1:]  # Skip the first value (class label)

# Load YOLO box coordinates from the second file (skip class label)
with open('sample_polygon_converted.txt', 'r') as f:
    first_line = f.readline().strip()
    values = list(map(float, first_line.split()))
    # Extract the YOLO box result (x_center, y_center, width, height)
    x_center, y_center, width, height = values[1:]  # Skip the first value (class label)

# Convert normalized YOLO coordinates to image coordinates
x_center *= IMAGE_WIDTH
y_center *= IMAGE_HEIGHT
width *= IMAGE_WIDTH
height *= IMAGE_HEIGHT

# Calculate the bounding box corner coordinates
x_min = x_center - width / 2
y_min = y_center - height / 2

# Debug prints to check the YOLO box coordinates
print(f"YOLO Box Coordinates:")
print(f"Center: ({x_center}, {y_center})")
print(f"Width: {width}, Height: {height}")
print(f"Bounding Box: x_min={x_min}, y_min={y_min}")

# Convert polygon to pixel coordinates
poly_x = [polygon[i] * IMAGE_WIDTH for i in range(0, len(polygon), 2)]
poly_y = [polygon[i] * IMAGE_HEIGHT for i in range(1, len(polygon), 2)]

# Plot
fig, ax = plt.subplots()
# Plot the polygon
ax.plot(poly_x + [poly_x[0]], poly_y + [poly_y[0]], 'b-', label='Polygon')  # Close the loop
# Plot the YOLO box (ensure the rectangle appears)
rect = patches.Rectangle((x_min, y_min), width, height, linewidth=2, edgecolor='r', facecolor='none', label='YOLO Box')
ax.add_patch(rect)

# Set plot limits
ax.set_xlim(0, IMAGE_WIDTH)
ax.set_ylim(IMAGE_HEIGHT, 0)
ax.set_aspect('equal')
ax.legend()
plt.title("Polygon vs YOLO Bounding Box")
plt.show()
