import math
import numpy as np

num = 61



import math
def sqrt_int(X: int):
    N = math.floor(math.sqrt(X))
    while bool(X % N):
        N -= 1
    M = X // N
    return M, N

print(sqrt_int(23))


print('__')


# a = np.zeros(shape=(2,5,4))
# print(a)

# arr=np.arange(2*7*1)
# arr_2d=arr.reshape(2,7,1)    #Reshapes 1d array in to 2d, containing 10 rows and 5 columns.

# arr_2d


# print(arr_2d)



def remap_values(old_value, old_min, old_max, new_min, new_max):
    old_value = abs(old_value)

    OldRange = (old_max - old_min)  
    NewRange = (new_max - new_min)  
    NewValue = (((old_value - old_min) * NewRange) / OldRange) + new_min

    return NewValue



#Input Z for X axis
aa = remap_values(90, 180, 360, 0, 255)
print(math.ceil(abs(aa)))



# NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin


import bpy, math
from mathutils import Vector,Matrix

def applyTransform(sMatrix, passedOb):
    if passedOb != None:
        tmp = eval(sMatrix)
        mtx = Matrix(tmp)
        passedOb.location = [mtx,-mtx,mtx] # Flip Z and Y axis.
        mtx.transpose() # From BL Stack user.
        rot_x_neg90 = Matrix.Rotation(math.pi/2.0, 4, ‘X’) # From Kastoria.
        passedOb.matrix_world = rot_x_neg90 * mtx # From Kastoria.

# Matrix string from Houdini object.
s = "[, , , ]“
ob = bpy.data.objects.get(”Camera")
applyTransform(s,ob)