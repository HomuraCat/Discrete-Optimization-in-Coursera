import matplotlib.pyplot as plt

# Read the TSP data from the file
with open("out.txt", "r") as file:
    lines = file.readlines()

lines = lines[1:]
# Extract the coordinates from the file
coordinates = []
for line in lines:
    x, y = map(float, line.strip().split())
    coordinates.append((x, y))

# Plot the TSP result
x_coords = [coord[0] for coord in coordinates]
y_coords = [coord[1] for coord in coordinates]

plt.figure(figsize=(8, 8))
plt.plot(x_coords, y_coords, 'bo-')
plt.scatter(x_coords[0], y_coords[0], color='red', label='Start')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('TSP Result')
plt.legend()
plt.grid(True)
plt.show()

