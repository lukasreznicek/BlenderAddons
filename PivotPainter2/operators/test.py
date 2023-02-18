import math,random, numpy, bitstring
import numpy as np


from ast import literal_eval

float_str = "-0b101010101"
result = float(literal_eval(float_str))




def packTextureBits(f16):
    f16= int(f16)
    f16+=1024
    sign = (f16 & 0x8000)<<16
    

    if (f16 & 0x7fff) == 0:
        expVar = 0
    else:
        expVar = ((((f16 >> 10)& 0x1f)-15+127)<< 23)
     
    mant =(f16 & 0x3ff)<< 13
    f16= (sign | expVar) | mant

    #16-bit int to 32-bit float

    
    tmp=numpy.array(f16, dtype=numpy.int32)
    tmp.dtype = numpy.float32

    return tmp




print(packTextureBits(32))
