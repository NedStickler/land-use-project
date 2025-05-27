
import numpy as np
from shapely.geometry import box


def recursive_min_partition(w: float, h: float, min: float = 0.1) -> tuple[float, float] | function:
    """Returns the width and height of the smallest possible
    equal partition of a rectangle with an area larger than min using recursion.

    Args:
        w (float): The width of the rectangle, or x2 - x1.
        h (float): The height of the rectangle, or y2 - y1.
        min (float): The smallest acceptable area of the resulting partitioned rectangles. Default = 0.1.
    
    Returns:
        tuple[float, float] | function: Either the smallest width and height (base case) or the next recursive call.
    
    Raises:
        ValueError: If the smallest minimum area is less than 0.001.
    """
    if min < 0.001: raise ValueError("Minimum bbox area must be at least 0.001 metres")
    new_w = w / 2
    new_h = h / 2
    if new_w * new_h < min:
        return w, h
    return recursive_min_partition(new_w, new_h, min)


def log_min_partition(w: float, h: float, min: float = 0.1):
    """Returns the width and height of the smallest possible
    equal partition of a rectangle with an area larger than min using maths.

    Args:
        w (float): The width of the rectangle, or x2 - x1.
        h (float): The height of the rectangle, or y2 - y1.
        min (float): The smallest acceptable area of the resulting partitioned rectangles. Default = 0.1.
    
    Returns:
        tuple[float, float]: The smallest width and height of the minumum partition.
    
    Raises:
        ValueError: If the smallest minimum area is less than 0.001.
    """
    if min < 0.001: raise ValueError("Minimum bbox area must be at least 0.001 metres")
    splits = np.floor(0.5 * np.log2(w * h / min))
    return w / 2**splits, h / 2**splits


def split_bbox(bbox: box, min_area: float, partition_func: function = log_min_partition) -> list[box]:
    """Splits a bbox into n smaller, proportional bboxes greater than min_size using a partition function.
    
    Args:
        bbox (box): Bounding box to be partitioned.
        min_area (float): The minimum area of the resulting partitions.
        partition_func (function): The function to calculate the minimum width and height of the smallest partitions.
    
    Returns:
        list[box]: A list of the resulting partitioned bounding boxes.

    """
    bounds = bbox.bounds
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    w, h = partition_func(width, height, min_area)

    bboxes = []
    for i in range(int(width / w)):
        for j in range(int(height / h)):
            b = box(bounds[0] + i * w, bounds[1] + j * h, bounds[0] + (i+1) * w, bounds[1] + (j+1) * h)
            bboxes.append(b)
    return bboxes