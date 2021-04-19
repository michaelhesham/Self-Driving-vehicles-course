import numpy as np 

b = np.array([-1,-4,0,2,3,4,5,-6])
b = b.clip(0)

print(b)