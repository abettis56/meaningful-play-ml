#altered from
#https://www.geeksforgeeks.org/reading-excel-file-using-python/
#https://www.geeksforgeeks.org/minkowski-distance-python/
import xlrd
from math import *
from decimal import Decimal

#Set up arrays of average q-values
first_average = []
second_average = []
    
#Prompt user for input of file names
file_name_one = input("Please input name of first averaged q-table: ")
file_name_two = input("Please input name of second averaged q-table: ")

#Read files into arrays
def read_from_excel(file_name, array):
    loc = (file_name + ".xlsx") 
      
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0) 
      
    # For row 0 and column 0 
    sheet.cell_value(0, 0) 
      
    for i in range(21):
        for j in range(21):
            array.append(sheet.cell_value(i, j)) 
            
read_from_excel(file_name_one, first_average)
read_from_excel(file_name_two, second_average)

#Apply weighting function to give high score to early states
def apply_weights(array):
    level_one = 0
    level_two = 0
    level_three = 0
    level_four = 0
    level_five = 0
    
    for i in range(441):
        #check what the i index would be in a 21x21 2D array
        index = i // 21

        if index == 0:
            array[i] = array[i] * 0.3
        elif index in range(1, 5):
            array[i] = array[i] * 0.25
        elif index in range(5, 9):
            array[i] = array[i] * 0.2
        elif index in range(9, 13):
            array[i] = array[i] * 0.15
        elif index in range(13, 17):
            array[i] = array[i] * 0.1
        elif index in range(17, 21):
            array[i] = array[i] * 0.05

apply_weights(first_average)
apply_weights(second_average)

#Calculate Minkowski distance between arrays
  
# Function distance between two points  
# and calculate distance value to given 
# root value(p is root value) 
def p_root(value, root): 
      
    root_value = 1 / float(root) 
    return round (Decimal(value) **
             Decimal(root_value), 3) 
  
def minkowski_distance(x, y, p_value): 
      
    # pass the p_root function to calculate 
    # all the value of vector parallely  
    return (p_root(sum(pow(abs(a-b), p_value) 
            for a, b in zip(x, y)), p_value))

#Output distances with p-values 1 and 2
print("Minkowski distance with p-value 1 (Manhattan Distance): " + str(minkowski_distance(first_average, second_average, 1)))
print("Minkowski distance with p-value 2 (Euclidean Distance): " + str(minkowski_distance(first_average, second_average, 2)))
