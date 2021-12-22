from abc import ABCMeta, abstractmethod
from random import randint, sample, choice
from math import pi
from typing import List

MAX = 12
def rand() -> int: return randint(1, MAX)

# Incorrect areas are generated the same regardless of the shape chosen
class baseShape(metaclass=ABCMeta):
    @abstractmethod
    def getArea(self) -> None:
        raise NotImplementedError("getArea() must be implemented on shapes inheriting baseShape")
    
    def wrongAreas(self) -> List[int]:
        area = self.getArea()
        return [area + offset if (choice([True, False]) or area - offset <= 0) else area - offset for offset in sample(range(1, MAX), 3)]

# Shapes implement the following:
# generate() : Generates new dimensions
# getArea()  : Returns shape's area
# __str__()  : Generates prompt
# wrong()    : Returns formula for shape area (displayed on one wrong answer)

class Circle(baseShape):
    def generate(self) -> None:
        self.radius = rand()
    
    def getArea(self) -> float:
        return pi * (self.radius ** 2)
        
    def __str__(self) -> str:
        return f"Circle with radius {self.radius}"
    
    def wrong(self) -> str:
        return "The formula for a circle's area is π * Radius²"
    
class Rectangle(baseShape):
    def generate(self) -> None:
        self.width, self.height = rand(), rand()
        
    def getArea(self) -> int:
        return self.width * self.height
    
    def __str__(self) -> str:
        return f"Rectangle with width {self.width} and height {self.height}"

    def wrong(self) -> str:
        return "The formula for a rectangles's area is Base * Height"

class Triangle(baseShape):
    def generate(self) -> None:
        self.base, self.height = rand(), rand()
    
    def getArea(self) -> float:
        return (self.base * self.height) / 2
    
    def __str__(self) -> str:
        return f"Triangle with base {self.base} and height {self.height}"
    
    def wrong(self) -> str:
        return "The formula for a triangles's area is (Base * Height)/2"
    
shapesArr = [Circle, Rectangle, Triangle] # Allows for easy access to all shapes