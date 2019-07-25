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
            #test
            print(' ' + str(sheet.cell_value(i,j)))
            
            array.append(sheet.cell_value(i, j)) 

        #test
        print("\n")
read_from_excel(file_name_one, first_average)
read_from_excel(file_name_two, second_average)

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
print(minkowski_distance(first_average, second_average, 1))
print(minkowski_distance(first_average, second_average, 2))
