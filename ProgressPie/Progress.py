#!/usr/bin/env python3

import os
import sys
import math
import argparse

from typing import Tuple

class ProgressPie:
    def __init__(self, center_x: int, center_y: int, radius: int):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.test_x = 0
        self.test_y = 0

    @staticmethod
    def ArcCot(x: float ,y: float) -> float:
        return (math.pi / 2) - math.atan(y / x)

    def TestPointToPolar(self) -> Tuple[float, float]:
        dx = self.test_x - self.center_x
        dy = self.test_y - self.center_y

        r = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
        angle_from_y_rads = ProgressPie.ArcCot(dx, dy)

        return (r, angle_from_y_rads)

    def QueryPoint(self, test_x: float, test_y: float, percentage: float) -> str:
        self.test_x = test_x
        self.test_y = test_y

        # get the polar representation of the test point
        r, angle_rel_y = self.TestPointToPolar()

        # if r is greater than the radius, it lies outside, and is white
        if r > self.radius:
            return "white"

        # if we got this far, check how many radians the pie spans
        percentage_span_rads = (percentage / 100.0) * (math.pi * 2)
        start_angle = math.pi / 2
        end_angle = start_angle - percentage_span_rads

        if angle_rel_y < start_angle and angle_rel_y > end_angle:
            return "black"
        else:
            return "white"


def main(args):
    if args.filename and not os.path.exists(args.filename):
        print(f"file {args.filename} does not exist", file=sys.stderr)
        sys.exit(-1)

    try:
        with open(args.filename) as infile:
            lines = infile.readlines()
            nb_lines = int(lines[0].strip().split(' ')[0])
            print(f"total number of lines: {len(lines) - 1}...")
            print(f"going to read {nb_lines} lines...")

            lines_read = 0
            while lines_read < nb_lines:
                line_to_process = lines[lines_read + 1]

                pp = ProgressPie(50, 50, 50)

                try:
                    line_to_process_split = line_to_process.replace('\n', '').split(' ')
                    percentage = float(line_to_process_split[0])
                    point_x = float(line_to_process_split[1])
                    point_y = float(line_to_process_split[2])

                    color = pp.QueryPoint(point_x, point_y, percentage)
                    print(f"Case #{lines_read + 1}: {color}")

                except Exception as eln:
                    print(f"error understanding line {line_to_process}, skipping...")

                lines_read += 1

    except Exception as e:
        print(f"an exception occurred for {args.filename} : {e}", file=sys.stderr)
        sys.exit(-1)



if __name__ == '__main__':
    options = argparse.ArgumentParser(description="Progress Pie: Given a file with percentages and coordinates,"
                                                  "compute where the coordinates lie")
    options.add_argument("--file", dest="filename", required=True, help="Path to the input file")
    args = options.parse_args()
    main(args)
