import numpy as np
import xlsxwriter

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
    'Defensive' : 17,
    'Neutral1' : 18,
    'Neutral2' : 19,
    'Compliant' : 20
}

# Define the actions
actions = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]


# Define the rewards for each state (1's represent possible paths to other states)
rewards = np.array([[0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])

# Maps indices to locations
state_to_location = dict((state,location) for location,state in location_to_state.items())

# Initialize parameters
gamma = 0.75 # Discount factor (discounts previous rewards)
alpha = 0.9 # Learning rate

# Get file name and final state from user
file_name = input("Please enter a name for the spreadsheet file: ")
final_state = input("Please enter the code of the final state: ")

class QAgent():
    
    # Initialize alpha, gamma, states, actions, rewards, and Q-values
    def __init__(self, alpha, gamma, location_to_state, actions, rewards, state_to_location, Q):
        
        self.gamma = gamma  
        self.alpha = alpha 
        
        self.location_to_state = location_to_state
        self.actions = actions
        self.rewards = rewards
        self.state_to_location = state_to_location
        
        self.Q = Q
        
    # Training the system in the given environment to move from a start state to an end state
    def training(self, start_location, end_location, iterations):
        
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
                TD = rewards_new[current_state,next_state] + \
                        self.gamma * self.Q[next_state, np.argmax(self.Q[next_state,])] - self.Q[current_state,next_state]
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
        
        #print(route)
        return route

#outputs 2D array
def to_excel(paths_taken, qtables):
    """store data in excel
    """
    workbook = xlsxwriter.Workbook(file_name + '.xlsx')
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
        
#array to store the final optimal path of each 1000 iterations
paths_taken = []
#array to store the final Q-Table of each 1000 iterations
qtables = []
for i in range(100):
  qagent = QAgent(alpha, gamma, location_to_state, actions, rewards,  state_to_location, np.array(np.zeros([21,21])))
  paths_taken.append(qagent.training('Start', final_state, 1000))
  qtables.append(qagent.Q)

to_excel(paths_taken, qtables)

#qagent.training('1C', '5N1', 1000)
#print (qagent.training('1C', '5N1', 1000))
#to_excel(qagent.training('1C', '5N1', 1000))