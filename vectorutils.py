import math
import numpy as np


def euclidian_distance(v1, v2):
  """
  The euclidian function to count the distance between 2 vector
  For Magnitude distance
  """
  # if both doesn't have the same length
  if (len(v1) != len(v2)):
    return -1
  # Match both vector into 1 zip :
  zip_vector = zip(v1, v2)

  # sum of all the sqrt(x**2)
  sum = 0
  for a, b in zip_vector:
    sum += (a - b) ** 2

  return math.sqrt(sum)


def cosine_similarity(v1, v2):
  """
  Solving the cosine similarity between 2 vectors
  For orientation similarity
  """

  v1v2 = sum([a * b for a, b in zip(v1, v2)])

  norm_v1_2 = math.sqrt(sum([x ** 2 for x in v1]))
  norm_v2_2 = math.sqrt(sum([x ** 2 for x in v2]))

  return (v1v2 / (norm_v1_2 * norm_v2_2))



