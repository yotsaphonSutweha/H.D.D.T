from math import *
import numpy as np
from collections import Counter
class KNN:
    def __init__(self):
        super().__init__()

    def k_nearest_neighbours(self, data, predict, k=3):
        distances = []
        for instance in data:
            diagnosis = instance[-1]
            features = instance[:-1]
            ed = np.linalg.norm(np.array(features) - np.array(predict))
            distances.append([ed, diagnosis])
                
        votes = [i[1] for i in sorted(distances)[:k]]
        votes_result = Counter(votes).most_common(1)[0][0]

        return votes_result    
