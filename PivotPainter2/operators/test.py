import math,random
import numpy as np

def findTextureDimensions(ObjectToProcessCount):
 
    DecrementerTotal = 1600 #small enough to avoid uv precision issues without using high precision values
    evenNumber = (ObjectToProcessCount%2.0)==0
    HalfEvenNumber = ((ObjectToProcessCount/2.0)%2.0)==0
    HalfNumber = math.ceil(ObjectToProcessCount/2.0)
    modResult = 1
    RowCounter = 1
    newDecrementerTotal = HalfNumber if HalfNumber < DecrementerTotal else DecrementerTotal
    decrementAmount =  2 if HalfEvenNumber == True else 1
    complete = False

    while complete == False:
        modResult = ObjectToProcessCount%newDecrementerTotal
        complete = modResult == 0 or newDecrementerTotal < 1 
        
        if complete== False:
            newDecrementerTotal-=decrementAmount 
        if newDecrementerTotal < 1:
            newDecrementerTotal=1
    
    if newDecrementerTotal==1 or ((ObjectToProcessCount/newDecrementerTotal)>DecrementerTotal):
            y=math.floor(math.sqrt(ObjectToProcessCount))
            x=math.ceil((ObjectToProcessCount/math.floor(y)))
            return [int(x),int(y)]
    else:
        return [int(newDecrementerTotal),int((ObjectToProcessCount/newDecrementerTotal))]




print(findTextureDimensions(855))

# NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin


