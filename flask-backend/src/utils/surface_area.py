import math 

# calculates surface area of pizza(s) in square inches
def getTotalSurfaceArea(size: str, number: str):

    match size:
        case 'Small':
            diameter = 10
        case 'Medium':
            diameter = 12
        case 'Large':
            diameter = 14
        case _: # x-large is written differently between chains so its just the default to simplify
            diameter = 16

    radius = diameter / 2
    
    surfaceArea = math.pi * (radius ** 2)

    surfaceArea *= float(number)

    return surfaceArea


