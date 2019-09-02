#!/usr/bin/env python
# coding: utf-8

# # Meaningful Play Score Assigner V1
# Accepts a topology of choices in the form of several weighted adjacency matrices, each with a 1 for any viable connection, and a 999 for the desired ending. Then, it performs q-learning based calculations and outputs a score of meaningfulness based on the average of the pairwise weighted minkowski distances.

# In[1]:


from math import *
from decimal import Decimal
import numpy as np
import xlsxwriter


# ### Define Q-Learning Class
# 
# Define the functions for q-learning and for outputting the optimal path and q-tables.

# In[2]:


class QAgent():
    
    def __init__(self, alpha, gamma, location_to_state, rewards, state_to_location, Q):
        """ Initialize alpha, gamma, states, actions, rewards, and Q-values
        """
        self.gamma = gamma  
        self.alpha = alpha 
        
        self.location_to_state = location_to_state
        self.rewards = rewards
        self.state_to_location = state_to_location
        
        self.Q = Q
        
    def training(self, start_location, end_location, iterations):
        """Training the system in the given environment to move from a start state to an end state
        """
        rewards_new = np.copy(self.rewards)
        
        #set reward for end state to 999 to incentivize reaching desired end
        ending_state = self.location_to_state[end_location]
        rewards_new[ending_state, ending_state] = 999

        #Loop for iterations
        for i in range(iterations):
            #Randomly pick a state to observe
            current_state = np.random.randint(0,len(self.rewards)) 
            playable_actions = []

            #Construct list of possible actions
            for j in range(len(self.rewards)):
                if rewards_new[current_state,j] > 0:
                    playable_actions.append(j)

            #Only run updates if observed state has performable actions
            if len(playable_actions) > 0:
                next_state = np.random.choice(playable_actions)

                #Calculate temporal difference
                TD = rewards_new[current_state,next_state] +                         self.gamma * self.Q[next_state, np.argmax(self.Q[next_state,])] - self.Q[current_state,next_state]
                #compare overlapping Q values
                #even w/o same value could encode same policy (where max/mins are)

                #updates Q-value using Bellman equation
                self.Q[current_state,next_state] += self.alpha * TD

        route = [start_location]
        next_location = start_location
        
        # Get the route 
        return self.get_optimal_route(start_location, end_location, next_location, route, self.Q)
        
    # Get the optimal route
    def get_optimal_route(self, start_location, end_location, next_location, route, Q):
        
        while(next_location != end_location):
            starting_state = self.location_to_state[start_location]
            next_state = np.argmax(Q[starting_state,])
            #episilon?
            next_location = self.state_to_location[next_state]
            route.append(next_location)
            start_location = next_location
        
        return route


# ### Accept file names
# 
# Get user input file names for comparison

# In[3]:


#topology txt file to score
filename = input("Please input the name of the topology .txt file you want to score: ")

#get topology from file
with open(filename) as textFile:
    rewards = np.array([[int(digit) for digit in line.strip().split(",")] for line in textFile])
    
#list of averaged q-tables to take minkowski differences of
averaged_tables = []

# Define the states
location_to_state = {
    'Start' : 0,
    '1D' : 1,
    '1N1' : 2,
    '1N2' : 3,
    '1C' : 4,
    '2D' : 5,
    '2N1' : 6,
    '2N2' : 7,
    '2C' : 8,
    '3D' : 9,
    '3N1' : 10,
    '3N2' : 11,
    '3C' : 12,
    '4D' : 13,
    '4N1' : 14,
    '4N2' : 15,
    '4C' : 16,
    'E1' : 17,
    'E2' : 18,
    'E3' : 19,
    'E4' : 20
}

# Map indices to locations
state_to_location = dict((state,location) for location,state in location_to_state.items())

# Initialize parameters
gamma = 0.75 # Discount factor (discounts previous rewards)
alpha = 0.9 # Learning rate

#generates excel spreadsheet containing all q-tables in a given path
def to_excel(paths_taken, qtables, final_state):
    """store data in excel
    """
    workbook = xlsxwriter.Workbook(filename + final_state + '.xlsx')
    worksheet = workbook.add_worksheet()

    #write all paths taken into first worksheet
    col = 0
    for row, data in enumerate(paths_taken):
        worksheet.write_row(row, col, data)

    #write each q-table to another worksheet
    for table, data in enumerate(qtables):
        worksheet = workbook.add_worksheet()
        for row, data2 in enumerate(qtables[table]):
            worksheet.write_row(row, col, data2)

    workbook.close()
    
#Take set of q-tables and average them into one q-table
def qaverage(table_set):
    num = 0
    output_table = table_set[0].copy()
    for i in range(len(table_set[0][0])):
        for j in range(len(table_set[0])):
            for k in range(len(table_set)):
                num += table_set[k][j][i]
            output_table[j][i] = num / len(table_set)
            num = 0
            
    return output_table

#Handle all q-learning for a given topology
def qmaster(final_state):
    #array to store the final optimal path of each 1000 iterations
    paths_taken = []
    #array to store the final Q-Table of each 1000 iterations
    qtables = []
    for i in range(100):
      qagent = QAgent(alpha, gamma, location_to_state, rewards,  state_to_location, np.array(np.zeros([21,21])))
      paths_taken.append(qagent.training('Start', final_state, 1000))
      qtables.append(qagent.Q)

    #output the current run to an excel file
    to_excel(paths_taken, qtables, final_state)
    averaged_tables.append(qaverage(qtables))

#run qmaster for each file name input
for i in range(4):
    qmaster('E' + str(i + 1))
    
print(averaged_tables[i])


# ### Pairwise Minkowski Difference
# 
# Now that the averaged q-tables are stored, we can calculate the minkowski differences in a pairwise fashion, average them up, and then spit them out.

# In[6]:


#altered from
#https://www.geeksforgeeks.org/minkowski-distance-python/

#convert array into 1D vector for ease of manipulation
def vectorize(input_array):
    output_array = []
    for i in range(21):
        for j in range(21):
            output_array.append(input_array[i][j])
            
    return output_array

#Apply weighting function to give high score to early states
def apply_weights(array):
    #These values can be adjusted to change weights
    #----------------------------------------------
    level_one = 0.3
    level_two = 0.25
    level_three = 0.2
    level_four = 0.15
    level_five = 0.1
    #----------------------------------------------
    
    for i in range(441):
        #check what the i index would be in a 21x21 2D array
        index = i // 21

        if index == 0:
            array[i] = array[i] * level_one
        elif index in range(1, 5):
            array[i] = array[i] * level_two
        elif index in range(5, 9):
            array[i] = array[i] * level_three
        elif index in range(9, 13):
            array[i] = array[i] * level_four
        elif index in range(13, 17):
            array[i] = array[i] * level_five
        elif index in range(17, 21):
            array[i] = 0
            
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
    # all the values of vector in parallel 
    return (p_root(sum(pow(abs(a-b), p_value) 
            for a, b in zip(x, y)), p_value))

#vectorize averaged tables and apply weights
vectors = []
for i in range(len(averaged_tables)):
    vectors.append(vectorize(averaged_tables[i]))
    vectorize(averaged_tables[i])
    
#calculate minkowski distances in a pairwise fashion
distances = []
acc = 0
for i in range(len(averaged_tables) - 1):
    for j in range(i + 1, len(vectors)):
        distance = minkowski_distance(vectors[i], vectors[j], 1)
        distances.append(distance)
        acc += distance
        
print(acc / len(distances))


# In[ ]:




