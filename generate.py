import random
import uuid
import sys

if len(sys.argv) < 2:
    sys.exit("python generate.py [number of points]")

lower_bound = -100
upper_bound = 100

points = list(set([
    (
        random.randint(lower_bound, upper_bound),
        random.randint(lower_bound, upper_bound)
    )
    for num in range(int(sys.argv[1]))
]))

points_with_uuid = [(*point, str(uuid.uuid4())) for point in points]

with open("points.dat", "w") as points_dat:
    points_dat.write(str(points_with_uuid))