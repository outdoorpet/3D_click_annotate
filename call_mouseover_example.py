import numpy as np
from _3D_mouseclick import visualize3DData

array = np.array([[1,2,3,4,5], [6,7,8,9,10], [100,200,300,400,500]]).transpose()
annotes = ['a','b','c','d','e']
visualize3DData(array, annotes)

