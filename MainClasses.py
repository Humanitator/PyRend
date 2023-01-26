# This file contains some primary classes for rendering shapes and other objects

from typing_extensions import Self
from VectorMath import Vector2
from Transforms import Transform3D, Transform2D
import math

# Parent class for geometric 3D primaries
class Primary3D:
    transform = None
    fill = None

    #Initialization
    def __init__(self, transform: Transform3D, fill: str) -> None:
        self.fill = fill
        self.transform = transform


#Parent class for geometric 2D primaries
class Primary2D:
    transform = None
    fill = None

    #Initialization
    def __init__(self, transform: Transform2D, fill: str) -> None:
        self.fill = fill
        self.transform = transform
        

#Basically a 2D array used for screen
class Grid:
    #Basic
    xSize = None
    ySize = None
    grid = None

    #Drawing
    fill = None
    empty = None

    #Plot a point
    def Plot(self, position: Vector2, fill = "[fill]"):
        if fill == "[fill]":
            fill = self.fill

        if (position.x >= 0 and position.x < self.xSize) and (position.y >= 0 and position.y < self.ySize): #Check if position is in grid range
            self.grid[position.y][position.x] = fill

    # Empties the grid
    def Clear(self):
        for y in range(self.ySize):
            for x in range(self.xSize):
                self.grid[y][x] = self.empty

    #Flip grid vertically
    def FlipV (self) -> Self:
        fArr = []
        for y in range(self.ySize):
            fArr.append(self.grid[self.ySize - y - 1])
        self.grid = fArr
        return fArr

    #Flip grid horizontally
    def FlipH (self) -> Self:
        fArr = []
        for y in range(self.ySize):
            fArr.append([])
            for x in range(self.xSize):
                fArr[y].append(self.grid[y][self.xSize - x - 1])
        self.grid = fArr
        return fArr

    #Convert grid to string
    def __str__(self) -> str:
        text = ""
        for y in range(self.ySize):
            for x in range(self.xSize):
                text += str(self.grid[y][x])
                text += " "
            text += "\n"
        return text
    
    #Initialization
    def __init__(self, xSize: int, ySize: int, fill = "#", empty = " ") -> None:
        self.xSize = max(xSize, 1)
        self.ySize = max(ySize, 1)

        self.fill = fill
        self.empty = empty

        self.grid = [[empty for j in range(xSize)] for i in range(ySize)]