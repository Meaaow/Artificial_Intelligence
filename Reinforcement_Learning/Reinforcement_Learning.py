import numpy as np
import copy
import math
import time

gamma = 0.9
epsilon = 0.1

# nsew .. ewsn

# priority : enws

with open("input0.txt", "r") as infile:
    data = infile.readlines()
    grid_size = int(data[0])
    no_cars = int(data[1])
    no_obstacles = int(data[2])
    obstacles_string = data[3:no_obstacles+3]
    start_locations_string = data[no_obstacles+3:no_obstacles+no_cars+3]
    end_locations_string = data[no_obstacles+no_cars+3:no_obstacles+no_cars+no_cars+3]

    obstacles = []
    for ii in obstacles_string:
        cood = ii.strip().split(',')
        obstacles.append((int(cood[1]), int(cood[0])))

    start_locations = []
    for ii in start_locations_string:
        cood = ii.strip().split(',')
        start_locations.append((int(cood[1]), int(cood[0])))

    end_locations = []
    for el in end_locations_string:
        cood = el.strip().split(',')
        end_locations.append((int(cood[1]), int(cood[0])))

    print("grid_size: ", grid_size, "no_cars: ", no_cars, "no_obstacles", no_obstacles)
    print(obstacles, start_locations, end_locations)




#0-up 1-right 2-down 3-left
#0-up 2-right 1-down 3-left

U = 0
R = 2
D = 1
L = 3

turn_left_dict = {}
turn_left_dict[U] = L
turn_left_dict[R] = U
turn_left_dict[D] = R
turn_left_dict[L] = D

turn_right_dict = {}
turn_right_dict[U] = R
turn_right_dict[R] = D
turn_right_dict[D] = L
turn_right_dict[L] = U


def policy_utility(init_car_pos,term_car_pos, utility_matrix, reward_matrix, policy_matrix):
    global cc
    while True:
        delta=0
        copied_utility_marix = copy.deepcopy(utility_matrix)
        for i in range(grid_size):
            for j in range(grid_size):
                cc += 1
                # print("cc", cc, i, j)
                max_value = list()
                if i==term_car_pos[0] and j==term_car_pos[1]:
                    utility_matrix[i,j] = reward_matrix[i,j]
                    policy_matrix[i,j] = None
                else:

                    u = copied_utility_marix[i,j]
                    l = copied_utility_marix[i,j]
                    d = copied_utility_marix[i,j]
                    r = copied_utility_marix[i,j]

                    if i-1 >= 0:
                        u = copied_utility_marix[i-1,j]

                    if j-1 >= 0:
                        l = copied_utility_marix[i,j-1]

                    if i+1 < grid_size:
                        d = copied_utility_marix[i+1,j]

                    if j+1 < grid_size:
                        r = copied_utility_marix[i,j+1]

                    max_value.append(0.7*u + 0.1* (r + l + d))
                    max_value.append(0.7*d + 0.1* (r + l + u))
                    max_value.append(0.7*r + 0.1* (u + l + d))
                    max_value.append(0.7*l + 0.1* (r + u + d))

                    utility_matrix[i,j]=reward_matrix[i,j] + gamma*max(max_value)
                    policy_matrix[i,j]=max_value.index(max(max_value))


                delta = max(delta, abs(utility_matrix[i,j] - copied_utility_marix[i,j]))

        if delta < epsilon * (1 - gamma) / gamma:
            break

    money=[]
   
    for j in range(10):
        pos = init_car_pos
        current_money=0
        np.random.seed(j)
        swerve = np.random.random_sample(1000000)
        k=0
        count=0
        while pos != term_car_pos:
            count+=1
            move = policy_matrix[pos]
            if count>1:
                current_money+=reward_matrix[pos]
                print("curr", current_money)
            print("swerve",swerve[k])
            print(np.finfo(type(swerve[k])))
            if swerve[k] > 0.7:
                if swerve[k] > 0.8:
                    if swerve[k] > 0.9:
                        # move=turn_left(turn_left(move))
                        move=turn_left_dict[turn_left_dict[move]]

                    else:
                        # move=turn_right(move)
                        move=turn_right_dict[move]
                else:
                    # move=turn_left(move)
                    move=turn_left_dict[move]

            else:
                move=policy_matrix[pos]
            print "Move is:",move
            if math.isnan(move):
                pos=term_car_pos
            if move==U:
                if pos[0]-1>=0:
                    pos = pos[0]-1, pos[1]
            elif move==R:
                if pos[1]+1<grid_size:
                    pos = pos[0], pos[1]+1
            elif move==D:
                if pos[0]+1 < grid_size:
                    pos = pos[0]+1, pos[1]
            elif move==L:
                if pos[1]-1>=0:
                    pos = pos[0], pos[1]-1
            k+=1

            if math.isnan(policy_matrix[pos]):
                pos = term_car_pos
                current_money += reward_matrix[pos]
                print("curr", current_money)

        money.append(current_money)
        print "total", money
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    avg=sum(money) / len(money)
    ravg = int(np.floor(avg))
    print ravg
    return ravg


cc = 0
answers = []
outfile = open("output.txt", "w")
st = time.time()
for i in range(len(start_locations)):
# for i in range(1):
#     i = 4
    utility_matrix = np.zeros([grid_size, grid_size])
    reward_matrix = np.zeros([grid_size, grid_size])
    policy_matrix = np.zeros([grid_size, grid_size])
    reward_matrix.fill(-1)
    if start_locations[i] == end_locations[i]:
        ans = 100
    else:
        reward_matrix[end_locations[i][0],end_locations[i][1]]=99 #kyu 99?
        for j in obstacles:
            reward_matrix[j[0],j[1]]=-101
        ans = policy_utility(start_locations[i],end_locations[i],utility_matrix,reward_matrix,policy_matrix)
    # print(utility_matrix)
    # print(policy_matrix)
    # print(reward_matrix)
    outfile.write(str(ans)+"\n")

    answers.append(ans)


outfile.close()
print time.time() - st




# 3.02198791504 3.27248692513 9
# 31.8110239506
