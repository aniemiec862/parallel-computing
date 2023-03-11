import random

def get_random_point():
    return random.random(), random.random()

def is_inside(x, y):
    return (x ** 2 + y ** 2) < 1

points_to_generate = 1000
points_inside = 0

for _ in range(points_to_generate):
    x, y = get_random_point()
    if is_inside(x, y):
        points_inside += 1

pi = 4 * (points_inside/ float(points_to_generate))
print(pi)