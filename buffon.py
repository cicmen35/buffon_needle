import random
import math
import numpy as np

def buffon_needle_pi(num_trials, needle_length, line_spacing):
    '''
    Returns calculation only. (Copied from GeeksForGeeks)
    '''
    crossings = 0
    for _ in range(num_trials):
        angle_degrees = random.uniform(0, 90)  # random angle in degrees [0, 90]
        angle_radians = math.radians(angle_degrees) 
        distance = random.uniform(0, line_spacing / 2)  # random distance from the center of the needle to the nearest line
        if distance <= (needle_length / 2) * math.sin(angle_radians):  # check if the needle crosses a line
            crossings += 1
    if crossings == 0:  # avoid division by zero
        return None
    return (2 * needle_length * num_trials) / (crossings * line_spacing)  # estimate


def buffon_needle_pi_with_data(num_trials, needle_length, line_spacing, num_lines=5):
    '''
    Returns (pi_estimate, list of needle dicts) for visualization.
    '''
    rng = np.random.default_rng()
    
    board_size = num_lines * line_spacing
    xc    = rng.uniform(0, board_size, num_trials)  # random x, y center coordinates for each needle
    yc    = rng.uniform(0, board_size, num_trials)  
    theta = rng.uniform(0, np.pi, num_trials)   # random orientation angle [0, pi]
    dx = (needle_length / 2) * np.cos(theta)    # half-length offsets from the needle center to its endpoints
    dy = (needle_length / 2) * np.sin(theta)

    y1 = yc - dy    # vertical start of needle
    y2 = yc + dy    # vertical end of needle
    crosses = (np.floor(y1 / line_spacing) != np.floor(y2 / line_spacing))  # separates crossed needles

    needles = []
    # append crossed needles and return them
    for i in range(num_trials):
        needle = {
            'x1': xc[i] - dx[i],
            'y1': y1[i],
            'x2': xc[i] + dx[i],
            'y2': y2[i],
            'crosses': bool(crosses[i])
        }
        needles.append(needle)

    c = int(crosses.sum())
    pi_est = (2 * needle_length * num_trials) / (c * line_spacing) if c > 0 else None   # buffons formula
    return pi_est, needles
