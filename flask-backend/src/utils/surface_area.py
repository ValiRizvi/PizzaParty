import math 

def getTotalSurfaceArea(size: str, number: str):

    match size:
        case 'small':
            diameter = 10
        case 'medium':
            diameter = 12
        case 'large':
            diameter = 14
        case _: # x-large is written differently between chains so its just the default to simplify
            diameter = 16

    radius = diameter / 2
    area = math.pi * (radius ** 2)

    return area * int(number)





