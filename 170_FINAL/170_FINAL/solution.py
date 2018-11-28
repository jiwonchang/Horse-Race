import os
import heapq
from heapq import heappush, heappop
import operator


path = 'cs170_final_inputs/'
solutions_path = "verified_outputs/"


#####################################
# A L G O R I T H M S
#####################################
"""
The algorithm for calculating the highest performance rating.
Input: A 2D matrix where the index is each horse (zero indexed, so 0th index is 1st horse) and the ajacency list of each horse in that index
Output: A 2D list: A list consisting of lists that indicate the groupings. 
	For example, the return value [ [1, 4, 6], [2, 3], [5] ] means that we use Horse 1, 4, 6. then Horse 2, 3. then Horse 5. 
"""
def trivial_algorithm(matrix_array):
	#algorithm here
	solution_list = []

	index = 0
	for horse_list in matrix_array:
		solution_list.append([index])
		index += 1

	return solution_list

def greedy_algorithm(matrix_array):
	#algorithm here
	
	solution_list = []
	vertex_count = len(matrix_array[0])

	friendCount = dict()
	for i in range(vertex_count):
		netRelationships = 0
		for x in range(vertex_count):
			if i != x:
				netRelationships+= matrix_array[i][x]
		friendCount[i] = netRelationships

	#import pdb; pdb.set_trace()
	sortedFriendCount = sorted(friendCount.items(), key=operator.itemgetter(1))

	
	currHorse = sortedFriendCount.pop()
	currTeam = [currHorse[0]]
	while sortedFriendCount:
		nextFriend = sortedFriendCount.pop()
		if matrix_array[currHorse[0]][nextFriend[0]]:
			currTeam.append(nextFriend[0])
		else:
			solution_list.append(currTeam)
			currTeam = [nextFriend[0]]
		currHorse = nextFriend
	solution_list.append(currTeam)
	#import pdb; pdb.set_trace()

	return solution_list

# Starts with ma performance horse, picks next horse greedily based on performance rating
def greedy_2(matrix_array):
	#algorithm here
	solution_list = []
	numHorses = len(matrix_array)
	maxheap = []
	groupedHorses = set()
	neighbours = {}
	neighboursRev = {}

	for horse_index in range(numHorses):
		weight = matrix_array[horse_index][horse_index] 
		heappush(maxheap, (-1*weight, horse_index))
		# Pop returns the smallest item from the heap, which will be the highest weight horse

		neighbourHeap = []
		neighbourHeapRev = []
		for neighbour_index in range(numHorses):
			if horse_index != neighbour_index:
				edge = matrix_array[horse_index][neighbour_index]
				edgeRev = matrix_array[neighbour_index][horse_index]
				weight = matrix_array[neighbour_index][neighbour_index] 
				if (edge == 1): 
					heappush(neighbourHeap, (-1*weight, neighbour_index))
				if (edgeRev == 1):
					heappush(neighbourHeapRev, (-1*weight, neighbour_index))

		neighbours[horse_index] = neighbourHeap
		neighboursRev[horse_index] = neighbourHeapRev 

	while maxheap:
		(weight, maxHorse) = heappop(maxheap) 
		if maxHorse not in groupedHorses:
			groupedHorses.add(maxHorse)

			currTeam = [maxHorse]
			currHorse = maxHorse
			while neighbours[currHorse]:

				(weight, neighbour) = heappop(neighbours[currHorse])
				if neighbour not in groupedHorses:
					currTeam.append(neighbour)
					groupedHorses.add(neighbour)
					currHorse = neighbour

			currHorse = maxHorse
			while neighboursRev[currHorse]:
				(weight, neighbour) = heappop(neighboursRev[currHorse])
				if neighbour not in groupedHorses:
					currTeam = [neighbour] + currTeam #append to front of team
					groupedHorses.add(neighbour)
					currHorse = neighbour

			solution_list.append(currTeam)

	return solution_list

def bfsHelper(matrix_array, node, farDepth, neighbors, numHorses, groupedHorses, visitedSet):
        maxDepth = 0
        neighborHeap = []
        visitedSet.add(node)
        for neighbor_index in range(numHorses):
                edge = matrix_array[node][neighbor_index]
                if edge == 1:
                        if neighbor_index not in groupedHorses and neighbor_index not in visitedSet:
                                neighborDepth = bfsHelper(matrix_array, neighbor_index, farDepth, neighbors, numHorses, groupedHorses, visitedSet)
                                farDepth[neighbor_index] = neighborDepth
                                maxDepth = max(maxDepth, 1 + neighborDepth)
                                heappush(neighborHeap, (neighborDepth, neighbor_index))
        neighbors[node] = neighborHeap
        return maxDepth
        

def bfsRevHelper(matrix_array, node, farDepth, neighborsRev, numHorses, groupedHorses, visitedRevSet):
        maxDepth = 0
        neighborRevHeap = []
        visitedRevSet.add(node)
        for neighbor_index in range(numHorses):
                edgeRev = matrix_array[neighbour_index][node]
                if edgeRev == 1:
                        if neighbor_index not in groupedHorses and neighbor_index not in visitedSet:
                                neighborDepth = bfsRevHelper(matrix_array, neighbor_index, farDepth, neighborsRev, numHorses, groupedHorses, visitedSet)
                                farDepth[neighbor_index] = neighborDepth
                                maxDepth = max(maxDepth, 1 + neighborDepth)
                                heappush(neighborRevHeap, (neighborDepth, neighbor_index))
        neighborsRev[node] = neighborRevHeap
        return maxDepth

def bfsLongestGreedyPath(matrix_array):
        #algorithm here
        solution_list = []
        numHorses = len(matrix_array)
	maxheap = []
	groupedHorses = set()
	neighbors = {}
	neighborsRev = {}
	#parent = {} # used to track the predecessor in a specific path
	#tempParent = {} # temporary place to store potential parent, in case this temporary parent does not end up as the actual parent (in the team)
	farDepth = {} # the depth, or distance, of the farthest child from that node
	farRevDepth = {} # the depth, or distance, of the farthest child in the reverse graph from that node

	for horse_index in range(numHorses):
                farDepth[horse_index] = 0
                #parent[horse_index] = None
                #tempParent[horse_index] = None

	for horse_index in range(numHorses):
                weight = matrix_array[horse_index][horse_index] 
		heappush(maxheap, (-1*weight, horse_index))
		# Pop returns the smallest item from the heap, which will be the highest weight horse

		#neighbourHeap = []
		#neighbourHeapRev = []
		#for neighbour_index in range(numHorses):
		#	if horse_index != neighbour_index:
		#		edge = matrix_array[horse_index - 1][neighbour_index - 1]
		#		edgeRev = matrix_array[neighbour_index - 1][horse_index - 1]
		#		if (edge == 1):
		#			weight = matrix_array[neighbour_index - 1][neighbour_index - 1] 
		#			heappush(neighbourHeap, (-1*weight, neighbour_index - 1))
		#		if (edgeRev == 1):
		#			weight = matrix_array[neighbour_index - 1][neighbour_index - 1] 
		#			heappush(neighbourHeapRev, (-1*weight, neighbour_index - 1))
                #
		#neighbours[horse_index-1] = neighbourHeap
		#neighboursRev[horse_index-1] = neighbourHeapRev 

	while maxheap:
		(pathLength, maxHorse) = heappop(maxheap)
		if maxHorse not in groupedHorses:

                        visitedSet = set([])
                        visitedRevSet = set([])
                        farDepth[horse_index] = bfsHelper(matrix_array, horse_index, farDepth, neighbors, numHorses, groupedHorses, visitedSet)
                        farRevDepth[horse_index] = bfsHelper(matrix_array, horse_index, farDepth, neighborsRev, numHorses, groupedHorses, visitedRevSet)

			currTeam = [maxHorse]
			currHorse = maxHorse
			while neighbors[currHorse]:
				(pathLength, neighbor) = heappop(neighbors[currHorse])
				if neighbor not in groupedHorses:
					currTeam.append(neighbor)
					groupedHorses.add(neighbor)
					currHorse = neighbor

			currHorse = maxHorse
			while neighborsRev[currHorse]:
				(pathLength, neighbour) = heappop(neighborsRev[currHorse])
				if neighbor not in groupedHorses:
					currTeam = [neighbor] + currTeam
					groupedHorses.add(neighbor)
					currHorse = neighbor

			solution_list.append(currTeam)

	return solution_list


#####################################
# S C O R E 	C A L C U L A T O R
#####################################
"""
Calculates the score of the grouping
Input:
	groupings_list:			[[list]]		a list of the groupings returned by algorithm
	matrix_array			[[list]]		the matrix that was parsed from the input
Output:
	score:					int 			score of the algorithm
"""
def calculate_score(groupings_list, matrix_array):
	cummulative_score = 0
	for grouping in groupings_list:
		counter = 0
		local_sum = 0

		for horse_index in grouping:
			counter += 1
			local_sum += matrix_array[horse_index][horse_index]

		cummulative_score += (local_sum * counter)
	return cummulative_score



#####################################
# P A R S I N G 	C O D E
#####################################
for filename in range(1,1):
	# for each file in the folder
	filename = str(filename) + ".in"
	with open(path + filename) as f:
		#print filename
		lines = f.readlines()
		number_of_lines = int(lines[0])		# first line in the input file is number of rows

		# create a list of length equal to the matrix size (i.e. number of lines)
		matrix_array = [0 for x in range(number_of_lines)]
		# print number_of_lines
		for i in range(1, number_of_lines + 1):
			# each line in the input file, after the first line
			lines[i] = lines[i].strip()
			list_of_elements_in_line = [int(s) for s in lines[i].split(' ')]
			matrix_array[i-1] =  list_of_elements_in_line

		# When you have a full algorithm, feel free to merge the algorithm in a NEW method above from your branch
		# and change this next line to run the method with your algorithm, and see how it outputs.
		# MAKE SURE TO NAME THE OUTPUT FILE SOMETHING UNIQUE THAT YOU CAN REFERENCE TO
		# For example, when running the trivial algorithm, I named the file "trivial_algorithm_run_1" and then "trivial_algorithm_run_2", etc...
		solution_list = bfsLongestGreedyPath(matrix_array)
		name_of_my_output_file = "bfsLongestGreedy_run_1"


		score = calculate_score(solution_list, matrix_array)
		with open(name_of_my_output_file + "_Scores.txt", "a+") as output_file:
			output_file.write(str(score) + '\n')

		with open(name_of_my_output_file + "_Teams.out", "a+") as output_file:		
			for solution in solution_list:
				for element in solution:
					output_file.write(str(element) + ' ')
				output_file.write('; ')
			output_file.write('\n')

                with open(name_of_my_output_file + "_Scores.txt") as f:
                        lines = f.readlines()
                        total = 0
                        for i in range(600):
                                score = int(lines[i].strip())
                                total += score

                        print(total/600)
