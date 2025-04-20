import os

def polygon_to_yolo(polygon_values):
    # Convert to floats
    coords = [float(v) for v in polygon_values]

    # Separate into x and y
    x_coords = coords[0::2]  # even indices
    y_coords = coords[1::2]  # odd indices

    min_x = min(x_coords)
    max_x = max(x_coords)
    min_y = min(y_coords)
    max_y = max(y_coords)

    x_center = (min_x + max_x) / 2
    y_center = (min_y + max_y) / 2
    width = max_x - min_x
    height = max_y - min_y

    return x_center, y_center, width, height

def convert_sample_polygon(input_path, output_path):
    with open(input_path, 'r') as infile:
        lines = infile.readlines()

    with open(output_path, 'w') as outfile:
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 5:
                class_id = parts[0]
                polygon_points = parts[1:]
                try:
                    x_center, y_center, width, height = polygon_to_yolo(polygon_points)
                    outfile.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
                except Exception as e:
                    print(f"Error processing line: {line.strip()} — {e}")
            else:
                print(f"Skipping non-polygon line: {line.strip()}")

# File paths
script_dir = os.path.dirname(os.path.abspath(__file__))
input_txt = os.path.join(script_dir, "sample_polygon.txt")
output_txt = os.path.join(script_dir, "sample_polygon_converted.txt")

convert_sample_polygon(input_txt, output_txt)
print("✅ Conversion complete!")
# The output file will be saved in the same directory as the script with the name "sample_polygon_converted.txt".
