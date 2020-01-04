"""
Advent of Code 2019 - Day 3

This program will read in data from a .dat file, and save the instructions
as vertices of a wire rather than the instructions

Author: Tom Kite
"""

import numpy as np
import sys

guide = {
        "R": np.array( [1,0] ),
        "L": np.array( [-1,0] ),
        "U": np.array( [0,1] ),
        "D": np.array( [0,-1] )
        }

def input_to_coords(instructions):
    output = np.ndarray( (0,2) )
    output = np.vstack( (output, [0,0]) )
    for step in instructions:
        output = np.vstack( (output, output[-1] + int(step[1:]) * guide[step[0]]) )
    
    return output

def read_data(filename):
    try:
        inputA, inputB = np.genfromtxt(filename, dtype = str, delimiter = ',')
    except:
        print("Data file could not be opened/interpreted")
        sys.exit()
    outputA, outputB = input_to_coords(inputA), input_to_coords(inputB)
    return outputA, outputB

def read_data2(filename):
    try:
        inputA, inputB = np.genfromtxt(filename, dtype = str, delimiter = ',')
    except:
        print("Data file could not be opened/interpreted")
        sys.exit()
    return inputA, inputB

def do_wires_cross(coordA,coordB,coordX,coordY):
    if (coordA[0] == coordB[0]):
        # AB rund up/down
        if (  (coordA[1] < coordX[1] < coordB[1] or coordB[1] < coordX[1] < coordA[1]) and ( coordX[0] < coordA[0] < coordY[0] or coordY[0] < coordA[0] < coordX[0] ) ):
            return True, coordA[0], coordX[1]
        else:
            return False, 0, 0
    elif(coordX[0] == coordY[0]):
        return do_wires_cross(coordX,coordY,coordA,coordB)
    else:
        return False, 0, 0
        
def distance1(coordList):
    newList = []
    for coords in coordList:
        newList.append(abs(coords[0]) + abs(coords[1]))
    return newList

def trace_along_wire(target_coord,instructions):
    distance = 0
    current_coord = np.array( [0,0] )
    for inst in instructions:
        for i in range( int(inst[1:]) ):
            current_coord += guide[inst[0]]
            distance += 1
            if (current_coord[0] == target_coord[0] and current_coord[1] == target_coord[1]):
                return distance


instructionsA, instructionsB = read_data2("301.dat")

wireA, wireB = input_to_coords(instructionsA), input_to_coords(instructionsB)

cross_list = np.ndarray( (0,2) )
for i in range( len(wireA)-1 ):
    for j in range( len(wireB)-1 ):
        tempBool, tempCoord1, tempCoord2 = do_wires_cross( wireA[i], wireA[i+1], wireB[j], wireB[j+1] )
        if (tempBool):
            cross_list = np.vstack( (cross_list, [tempCoord1,tempCoord2]) )

cross_list = cross_list[np.argsort(distance1(cross_list))]

print( cross_list )

distance_list = []

for coord in cross_list:
    dist1 = trace_along_wire( coord, instructionsA )
    dist2 = trace_along_wire( coord, instructionsB )
    distance_list.append( dist1+dist2 )
    
print( min(distance_list) )

