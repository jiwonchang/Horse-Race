import os
import heapq
from heapq import heappush, heappop
import random
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


def greedy_random(matrix_array):
	#algorithm here
	solution_list = []
	numHorses = len(matrix_array)
	maxheap = []
	groupedHorses = set()
	neighbours = {}
	neighboursRev = {}

	for horse_index in range(numHorses):
		#import pdb; pdb.set_trace()
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

	#need array of horses here
	#use rand_gen to deplete horse 
	while maxheap:
		#import pdb; pdb.set_trace()
		randInt = random.randint(0, len(maxheap)-1)
		(weight, maxHorse) = maxheap.pop(randInt)
		#(weight, maxHorse) = heappop(maxheap) 
		if maxHorse not in groupedHorses:
			groupedHorses.add(maxHorse)

			currTeam = [maxHorse]
			currHorse = maxHorse
			while neighbours[currHorse]:

				if len(currTeam) % 2 == 0:
					(weight, neighbour) = heappop(neighbours[currHorse])
				else:
					randInt = random.randint(0, len(neighbours[currHorse])-1)
					(weight, neighbour) = (neighbours[currHorse]).pop(randInt)

				if neighbour not in groupedHorses:
					currTeam.append(neighbour)
					groupedHorses.add(neighbour)
					currHorse = neighbour

			currHorse = maxHorse
			while neighboursRev[currHorse]:

				if len(currTeam) % 2 == 0:
					(weight, neighbour) = heappop(neighboursRev[currHorse])
				else:
					randInt = random.randint(0, len(neighboursRev[currHorse])-1)
					(weight, neighbour) = (neighboursRev[currHorse]).pop(randInt)

				if neighbour not in groupedHorses:
					currTeam = [neighbour] + currTeam #append to front of team
					groupedHorses.add(neighbour)
					currHorse = neighbour

			solution_list.append(currTeam)

	return solution_list




# help methods to calculate priority based on longest path
def dfsHelper(matrix_array, node, farDepth, neighbors, numHorses, groupedHorses, visitedSet):
        maxDepth = 0
        neighborHeap = []
        visitedSet.add(node)
        for neighbor_index in range(numHorses):
                edge = matrix_array[node][neighbor_index]
                if edge == 1:
                        if neighbor_index not in groupedHorses and neighbor_index not in visitedSet:
                                neighborDepth = dfsHelper(matrix_array, neighbor_index, farDepth, neighbors, numHorses, groupedHorses, visitedSet)
                                farDepth[neighbor_index] = neighborDepth
                                maxDepth = max(maxDepth, 1 + neighborDepth)
                                heappush(neighborHeap, (neighborDepth, neighbor_index))
        neighbors[node] = neighborHeap
        return maxDepth
        

def dfsRevHelper(matrix_array, node, farDepth, neighborsRev, numHorses, groupedHorses, visitedRevSet):
        maxDepth = 0
        neighborRevHeap = []
        visitedRevSet.add(node)
        for neighbor_index in range(numHorses):
                edgeRev = matrix_array[neighbor_index][node]
                if edgeRev == 1:
                        if neighbor_index not in groupedHorses and neighbor_index not in visitedRevSet:
                                neighborDepth = dfsRevHelper(matrix_array, neighbor_index, farDepth, neighborsRev, numHorses, groupedHorses, visitedRevSet)
                                farDepth[neighbor_index] = neighborDepth
                                maxDepth = max(maxDepth, 1 + neighborDepth)
                                heappush(neighborRevHeap, (neighborDepth, neighbor_index))
        neighborsRev[node] = neighborRevHeap
        return maxDepth





def dfsLongestGreedy(matrix_array):
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

	while maxheap:
		(pathLength, maxHorse) = heappop(maxheap)
		
		if maxHorse not in groupedHorses:
                        groupedHorses.add(maxHorse)
                        
                        visitedSet = set([])
                        visitedRevSet = set([])
                        farDepth[horse_index] = dfsHelper(matrix_array, maxHorse, farDepth, neighbors, numHorses, groupedHorses, visitedSet)
                        farRevDepth[horse_index] = dfsRevHelper(matrix_array, maxHorse, farDepth, neighborsRev, numHorses, groupedHorses, visitedRevSet)

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
				(pathLength, neighbor) = heappop(neighborsRev[currHorse])
				if neighbor not in groupedHorses:
					currTeam = [neighbor] + currTeam
					groupedHorses.add(neighbor)
					currHorse = neighbor

			solution_list.append(currTeam)

	return solution_list




# helper methods to calculate priority based on highest score and longest path
def dfsPointHelper(matrix_array, node, farDepth, neighbors, numHorses, groupedHorses, visitedSet):
        maxDepth = 1
        maxPoints = matrix_array[node][node] * 1
        defaultPoint = matrix_array[node][node]
        sumPoints = matrix_array[node][node]
        neighborHeap = []
        visitedSet.add(node)
        #THIS IS WHERE I CLONED THE VISITEDSET UP TILL THAT POINT
        #oldVisitedSet = set(visitedSet)
        for neighbor_index in range(numHorses):
                edge = matrix_array[node][neighbor_index]
                if edge == 1:
                        #HERE WE CLONE THE CLONE
                        #visitedSet = set(oldVisitedSet)
                        if neighbor_index not in groupedHorses and neighbor_index not in visitedSet and neighbor_index != node:
                                neighborDepth, neighborSum = dfsPointHelper(matrix_array, neighbor_index, farDepth, neighbors, numHorses, groupedHorses, visitedSet)
                                sumPoints = defaultPoint + neighborSum
                                farDepth[neighbor_index] = neighborDepth
                                maxDepths = max(maxDepth, 1 + neighborDepth)
                                maxPoints = max(maxPoints, sumPoints * maxDepth)
                                heappush(neighborHeap, (maxPoints, neighbor_index))
        neighbors[node] = neighborHeap
        return (maxDepth, sumPoints)

def dfsRevPointHelper(matrix_array, node, farDepth, neighborsRev, numHorses, groupedHorses, visitedRevSet):
        maxDepth = 1
        maxPoints = matrix_array[node][node]
        defaultPoint = matrix_array[node][node]
        sumPoints = matrix_array[node][node]
        neighborRevHeap = []
        visitedRevSet.add(node)
        #oldVisitedRevSet = set(visitedRevSet)
        for neighbor_index in range(numHorses):
                edgeRev = matrix_array[neighbor_index][node]
                if edgeRev == 1:
                        #visitedRevSet = set(oldVisitedRevSet)
                        if neighbor_index not in groupedHorses and neighbor_index not in visitedRevSet and neighbor_index != node:
                                neighborDepth, neighborSum = dfsRevPointHelper(matrix_array, neighbor_index, farDepth, neighborsRev, numHorses, groupedHorses, visitedRevSet)
                                sumPoints = defaultPoint + neighborSum
                                farDepth[neighbor_index] = neighborDepth
                                maxDepth = max(maxDepth, 1 + neighborDepth)
                                maxPoints = max(maxPoints, sumPoints * maxDepth)
                                heappush(neighborRevHeap, (maxPoints, neighbor_index))
        neighborsRev[node] = neighborRevHeap
        return (maxDepth, sumPoints)


def dfsLongestPointGreedy(matrix_array):
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
	descendDepthHash = {}

	for horse_index in range(numHorses):
                farDepth[horse_index] = 0
                #parent[horse_index] = None
                #tempParent[horse_index] = None

	for horse_index in range(numHorses):
                weight = matrix_array[horse_index][horse_index] 
		heappush(maxheap, (-1*weight, horse_index))
		# Pop returns the smallest item from the heap, which will be the highest weight horse

	while maxheap:
		(pathLength, maxHorse) = heappop(maxheap)
		
		if maxHorse not in groupedHorses:
                        groupedHorses.add(maxHorse)
                        
                        visitedSet = set([])
                        visitedRevSet = set([])
                        farDepth[horse_index] = dfsPointHelper(matrix_array, maxHorse, farDepth, neighbors, numHorses, groupedHorses, visitedSet)[0]
                        farRevDepth[horse_index] = dfsRevPointHelper(matrix_array, maxHorse, farDepth, neighborsRev, numHorses, groupedHorses, visitedRevSet)[0]

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
				(pathLength, neighbor) = heappop(neighborsRev[currHorse])
				if neighbor not in groupedHorses:
					currTeam = [neighbor] + currTeam
					groupedHorses.add(neighbor)
					currHorse = neighbor

			solution_list.append(currTeam)

	return solution_list



def dfsPointRandomGreedy(matrix_array):
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

	while maxheap:
                randInt = random.randint(0, len(maxheap)-1)
		(pathLength, maxHorse) = maxheap.pop(randInt)
		
		if maxHorse not in groupedHorses:
                        groupedHorses.add(maxHorse)
                        
                        visitedSet = set([])
                        visitedRevSet = set([])
                        farDepth[horse_index] = dfsPointHelper(matrix_array, maxHorse, farDepth, neighbors, numHorses, groupedHorses, visitedSet)[0]
                        farRevDepth[horse_index] = dfsRevPointHelper(matrix_array, maxHorse, farDepth, neighborsRev, numHorses, groupedHorses, visitedRevSet)[0]

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
				(pathLength, neighbor) = heappop(neighborsRev[currHorse])
				if neighbor not in groupedHorses:
					currTeam = [neighbor] + currTeam
					groupedHorses.add(neighbor)
					currHorse = neighbor

			solution_list.append(currTeam)

	return solution_list

def randomAlgo(matrix_array):
        solution_list = []
	numHorses = len(matrix_array)
	maxheap = []
	groupedHorses = set()
	neighbors = {}
	neighborsRev = {}

	for horse_index in range(numHorses):
		#weight = matrix_array[horse_index][horse_index] 
		#heappush(maxheap, (-1*weight, horse_index))
                maxheap.append(horse_index)
                
		# Pop returns the smallest item from the heap, which will be the highest weight horse

		neighborHeap = []
		neighborHeapRev = []
		for neighbor_index in range(numHorses):
			if horse_index != neighbor_index:
				edge = matrix_array[horse_index][neighbor_index]
				edgeRev = matrix_array[neighbor_index][horse_index]
				#weight = matrix_array[neighbor_index][neighbor_index] 
				if (edge == 1): 
					#heappush(neighborHeap, (-1*weight, neighbor_index))
                                        neighborHeap.append(neighbor_index)
				if (edgeRev == 1):
					#heappush(neighborHeapRev, (-1*weight, neighbor_index))
                                        neighborHeapRev.append(neighbor_index)

		neighbors[horse_index] = neighborHeap
		neighborsRev[horse_index] = neighborHeapRev 

	#need array of horses here
	#use rand_gen to deplete horse 
	while maxheap:
		#import pdb; pdb.set_trace()
		randInt = random.randint(0, len(maxheap)-1)
		#(weight, maxHorse) = maxheap.pop(randInt)
		maxHorse = maxheap.pop(randInt)
		#(weight, maxHorse) = heappop(maxheap) 
		if maxHorse not in groupedHorses:
			groupedHorses.add(maxHorse)

			currTeam = [maxHorse]
			currHorse = maxHorse
			while neighbors[currHorse]:
				randInt = random.randint(0, len(neighbors[currHorse])-1)
				neighbor = (neighbors[currHorse]).pop(randInt)

				if neighbor not in groupedHorses:
					currTeam.append(neighbor)
					groupedHorses.add(neighbor)
					currHorse = neighbor

			currHorse = maxHorse
			while neighborsRev[currHorse]:
				randInt = random.randint(0, len(neighborsRev[currHorse])-1)
				neighbor = (neighborsRev[currHorse]).pop(randInt)

				if neighbor not in groupedHorses:
					currTeam = [neighbor] + currTeam #append to front of team
					groupedHorses.add(neighbor)
					currHorse = neighbor

			solution_list.append(currTeam)

	

	return solution_list

def randMergeAlgo(matrix_array):
        solution_list = []
	numHorses = len(matrix_array)
	maxheap = []
	groupedHorses = set()
	neighbors = {}
	neighborsRev = {}

	for horse_index in range(numHorses):
		#weight = matrix_array[horse_index][horse_index] 
		#heappush(maxheap, (-1*weight, horse_index))
                maxheap.append(horse_index)
                
		# Pop returns the smallest item from the heap, which will be the highest weight horse

		neighborHeap = []
		neighborHeapRev = []
		for neighbor_index in range(numHorses):
			if horse_index != neighbor_index:
				edge = matrix_array[horse_index][neighbor_index]
				edgeRev = matrix_array[neighbor_index][horse_index]
				#weight = matrix_array[neighbor_index][neighbor_index] 
				if (edge == 1): 
					#heappush(neighborHeap, (-1*weight, neighbor_index))
                                        neighborHeap.append(neighbor_index)
				if (edgeRev == 1):
					#heappush(neighborHeapRev, (-1*weight, neighbor_index))
                                        neighborHeapRev.append(neighbor_index)

		neighbors[horse_index] = neighborHeap
		neighborsRev[horse_index] = neighborHeapRev

        defaultNeighbors = dict(neighbors)
        defaultNeighborsRev = dict(neighborsRev)
        #print("defaultNeighbors: ")
        #print("")
        #print("")
        #print(defaultNeighbors)
        #print("defaultNeighborsRev: ")
        #print(defaultNeighborsRev)

	#need array of horses here
	#use rand_gen to deplete horse 
	while maxheap:
		#import pdb; pdb.set_trace()
		randInt = random.randint(0, len(maxheap)-1)
		#(weight, maxHorse) = maxheap.pop(randInt)
		maxHorse = maxheap.pop(randInt)
		#(weight, maxHorse) = heappop(maxheap) 
		if maxHorse not in groupedHorses:
			groupedHorses.add(maxHorse)

			currTeam = [maxHorse]
			currHorse = maxHorse
			while neighbors[currHorse]:
				randInt = random.randint(0, len(neighbors[currHorse])-1)
				neighbor = (neighbors[currHorse]).pop(randInt)

				if neighbor not in groupedHorses:
					currTeam.append(neighbor)
					groupedHorses.add(neighbor)
					currHorse = neighbor

			currHorse = maxHorse
			while neighborsRev[currHorse]:
				randInt = random.randint(0, len(neighborsRev[currHorse])-1)
				neighbor = (neighborsRev[currHorse]).pop(randInt)

				if neighbor not in groupedHorses:
					currTeam = [neighbor] + currTeam #append to front of team
					groupedHorses.add(neighbor)
					currHorse = neighbor

			solution_list.append(currTeam)

	### THIS IS WHERE WE BEGIN MERGING!!!!

        mergedTeams = []
        teamScores = {}
        teamScoreHeap = []
        usedTeam = []
        #stores all team scores by the index of the first horse
	for team in solution_list:
                #teamSum = 0
                #for horse in team:
                #        horsePerformance = matrix_array[horse][horse]
                #        teamSum += horsePerformance
                #teamScore = teamSum * len(team)
                teamScore = calcTeamScore(team)
                heappush(teamScoreHeap, (-teamScore, team))

        while teamScoreHeap:
                (team1Score, team1) = heappop(teamScoreHeap)
                mergeCount = 0
                #print(team1)
                for (team2Score, team2) in teamScoreHeap:
                        print("team2[0]: " + str(team2[0]))
                        print("team1[len(team1)-1]: " + str(team1[len(team1)-1]))
                        print(defaultNeighborsRev[team1[0]])
                        if team2[0] in defaultNeighbors[team1[len(team1)-1]]:
                                print("Merging team1 + team2: " + str(team1) + " + " + str(team2))
                                newTeam = team1 + team2
                                teamScoreHeap.remove(team2)
                                newTeamScore = calcTeamScore(newTeam)
                                heappush(teamScoreHeap, (newTeamScore, newTeam))
                                mergeCount += 1
                                break
                        elif team2[len(team2)-1] in defaultNeighborsRev[team1[0]]:
                                print("RevMerging team2 + team1: " + str(team2) + " + " + str(team1))
                                newTeam = team2 + team1
                                teamScoreHeap.remove(team2)
                                newTeamScore = calcTeamScore(newTeam)
                                heappush(teamScoreHeap, (newTeamScore, newTeam))
                                mergeCount += 1
                                break
                        else:
                                print("no cigar")
                if mergeCount == 0:
                        mergedTeams.append(team1)
                        
        solution_list = mergedTeams
	

	return solution_list

# helper methods to calculate priority based on highest score and longest path
def dfsHashPointHelper(matrix_array, node, farDepth, neighbors, numHorses, groupedHorses, visitedSet):
        maxDepth = 1
        maxPoints = matrix_array[node][node] * 1
        defaultPoint = matrix_array[node][node]
        sumPoints = matrix_array[node][node]
        neighborHeap = []
        visitedSet.add(node)
        #THIS IS WHERE I CLONED THE VISITEDSET UP TILL THAT POINT
        oldVisitedSet = set(visitedSet)
        for neighbor_index in range(numHorses):
                edge = matrix_array[node][neighbor_index]
                if edge == 1:
                        #HERE WE CLONE THE CLONE
                        visitedSet = set(oldVisitedSet)
                        if neighbor_index not in groupedHorses and neighbor_index not in visitedSet and neighbor_index != node:
                                neighborDepth, neighborSum = dfsPointHelper(matrix_array, neighbor_index, farDepth, neighbors, numHorses, groupedHorses, visitedSet)
                                sumPoints = defaultPoint + neighborSum
                                farDepth[neighbor_index] = neighborDepth
                                maxDepths = max(maxDepth, 1 + neighborDepth)
                                maxPoints = max(maxPoints, sumPoints * maxDepth)
                                heappush(neighborHeap, (maxPoints, neighbor_index))
        neighbors[node] = neighborHeap
        return (maxDepth, sumPoints)

def dfsRevHashPointHelper(matrix_array, node, farDepth, neighborsRev, numHorses, groupedHorses, visitedRevSet):
        maxDepth = 1
        maxPoints = matrix_array[node][node]
        defaultPoint = matrix_array[node][node]
        sumPoints = matrix_array[node][node]
        neighborRevHeap = []
        visitedRevSet.add(node)
        oldVisitedRevSet = set(visitedRevSet)
        for neighbor_index in range(numHorses):
                edgeRev = matrix_array[neighbor_index][node]
                if edgeRev == 1:
                        visitedRevSet = set(oldVisitedRevSet)
                        if neighbor_index not in groupedHorses and neighbor_index not in visitedRevSet and neighbor_index != node:
                                neighborDepth, neighborSum = dfsRevPointHelper(matrix_array, neighbor_index, farDepth, neighborsRev, numHorses, groupedHorses, visitedRevSet)
                                sumPoints = defaultPoint + neighborSum
                                farDepth[neighbor_index] = neighborDepth
                                maxDepth = max(maxDepth, 1 + neighborDepth)
                                maxPoints = max(maxPoints, sumPoints * maxDepth)
                                heappush(neighborRevHeap, (maxPoints, neighbor_index))
        neighborsRev[node] = neighborRevHeap
        return (maxDepth, sumPoints)


def dfsLongestHashPointGreedy(matrix_array):
        #algorithm here
    """
    THE POINT BEHIND THIS FUNCTION IS TO GIVE EVERY VERTEX ITS OWN VISITED SET, BUT THEN TO ALSO KEEP A FARTHEST DESCENDANT COUNT HASHSET
    SO THAT WE CAN EASILY RECALL THE DEEPEST DEPTH OF A NODE AND PREVENT THE PROGRAM FROM TRAVERSING PATHS THAT WE ALREADY HAVE GONE BEFORE.
    NEED TO STILL FIGURE OUT HOW TO "REMOVE" A DESCENDANT FROM THE DESCENDANT COUNT IF ONE OF A VERTEX'S DESCENDANT GETS GROUPED.
    """
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
	descendDepthHash = {}

	for horse_index in range(numHorses):
                farDepth[horse_index] = 0
                #parent[horse_index] = None
                #tempParent[horse_index] = None

	for horse_index in range(numHorses):
                weight = matrix_array[horse_index][horse_index] 
		heappush(maxheap, (-1*weight, horse_index))
		# Pop returns the smallest item from the heap, which will be the highest weight horse

	while maxheap:
		(pathLength, maxHorse) = heappop(maxheap)
		
		if maxHorse not in groupedHorses:
                        groupedHorses.add(maxHorse)
                        
                        visitedSet = set([])
                        visitedRevSet = set([])
                        farDepth[horse_index] = dfsPointHelper(matrix_array, maxHorse, farDepth, neighbors, numHorses, groupedHorses, visitedSet)[0]
                        farRevDepth[horse_index] = dfsRevPointHelper(matrix_array, maxHorse, farDepth, neighborsRev, numHorses, groupedHorses, visitedRevSet)[0]

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
				(pathLength, neighbor) = heappop(neighborsRev[currHorse])
				if neighbor not in groupedHorses:
					currTeam = [neighbor] + currTeam
					groupedHorses.add(neighbor)
					currHorse = neighbor

			solution_list.append(currTeam)

	return solution_list






def calcTeamScore(team):
        teamSum = 0
        for horse in team:
                horsePerformance = matrix_array[horse][horse]
                teamSum += horsePerformance
        teamScore = teamSum * len(team)
        return teamScore




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
for filename in range(1, 600+1):
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

		#solution_list = dfsLongestPointGreedy(matrix_array)

		score = -1
		for i in range(0 + 1):
                        if i == 0:
                                curr_solution = dfsLongestHashPointGreedy(matrix_array)
                        elif i > 0:
                                curr_solution = randMergeAlgo(matrix_array)
                        curr_score = calculate_score(curr_solution, matrix_array)
                        if curr_score > score:
                                score = curr_score
                                solution_list = curr_solution

                        #print('Current Best: ' + str(score))
			#print('\n')

		name_of_my_output_file = "dfsLongHashPointGreedy_run_1"


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
                
        print("average:" + str(total/600))
