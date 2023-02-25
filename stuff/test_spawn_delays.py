import math

# Example spawnpoints (replace with your own data)
spawnpoints = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]

# Calculate center of the area
center_x = sum(x for x, y in spawnpoints) / len(spawnpoints)
center_y = sum(y for x, y in spawnpoints) / len(spawnpoints)

# Calculate distances from center and maximum distance
distances = [math.sqrt((x - center_x)**2 + (y - center_y)**2) for x, y in spawnpoints]
max_distance = max(distances)

# Calculate weights based on distances
weights = [(max_distance - distance) / max_distance for distance in distances]

# Normalize weights
weight_sum = sum(weights)
probabilities = [weight / weight_sum for weight in weights]

# Print results
for spawnpoint, probability in zip(spawnpoints, probabilities):
    print(f"Spawnpoint {spawnpoint}: probability = {probability:.2f}")