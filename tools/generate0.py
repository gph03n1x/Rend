#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import uuid
import sys



def generate_data(lower_bound, upper_bound, number_count):
    return list(set([
        (
            random.randint(lower_bound, upper_bound),
            random.randint(lower_bound, upper_bound)
        )
        for num in range(int(number_count))
    ]))

def generate_weights(sum_bound, count):
    weights = []
    for rep in range(count):
        w1 = random.random()
        w2 = sum_bound - w1
        weights.append([w1, w2])
    return weights

if __name__ == "__main__":
    if len(sys.argv) < 5:
        sys.exit("python generate.py [file] [number of points] [lower bound] [higher bound]")

    lower_bound = int(sys.argv[3])
    upper_bound = int(sys.argv[4])

    points = generate_data(lower_bound, upper_bound, sys.argv[2])

    points_with_uuid = [[*point, str(uuid.uuid4())] for point in points]
    data = {"points": points_with_uuid, "weights": generate_weights(1, 20)}
    with open(sys.argv[1], "w") as points_dat:
        import json
        print(type(data))
        json.dump(data, points_dat)
