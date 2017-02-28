import numpy as np
import math
import time
import sys
import random

class ClimbHill:
	def __init__(self,address):
		self.filename = address
		ATL = open("DATA/"+address,"r")
		self.cityname = ATL.readline()
		#NAME: ATLANTA
		#print ATL.readline()#COMMENT: 20 locations in Atlanta
		num = filter(str.isdigit, (ATL.readline())) #DIMENSION: 20
		num = int(num)
		print ATL.readline()#EDGE_WEIGHT_TYPE: EUC_2D
		print ATL.readline()#NODE_COORD_SECTION
		data = np.array([0]*3*num,dtype="float").reshape(num,3)
		print ATL.readline()
		for i in range (0,num):
			data[i,:] = ATL.readline().split(" ")
		#print data

		nodedismatrix = np.array([np.inf]*num*num,dtype="float").reshape(num,num)
		for i in range(0,num):
			for j in range(i+1,num):
				xd = data[i,1]-data[j,1]
				yd = data[i,2]-data[j,2]
				nodedismatrix[i,j] = np.round(np.sqrt(xd*xd+yd*yd))
				nodedismatrix[j,i] = nodedismatrix[i,j]
		#print nodedismatrix
		self.cities = np.arange(nodedismatrix.shape[0]).tolist()
		#print self.cities
		self.costmatrix = nodedismatrix

		

	#THIS FUNCTION IS USED TO INITIALIZE THE PATH WITH PERMUTATION.
	def firstPermutation(self,cities,seed):
	    np.random.seed(seed)
	    citiesPerm = np.random.permutation(cities)
	    citiesPerm = np.append(citiesPerm, citiesPerm[0])
	    return citiesPerm
	#THIS FUNTION IS USED FOR CALCULATING THE CURRENT TOTAL COST
	def cal_totalCost(self,citiesPerm,distMatrix):
	    cost = 0
	    for i in range(len(citiesPerm)-1):
	        cost += distMatrix[citiesPerm[i]][citiesPerm[i+1]]
	    return cost

	#THIS FUNTION IS A SWAP FUNCTION FOR SWAP I AND J ELEMENT OF A PATH
	def swap(self,citiesPerm,i,j):
	    newCitiesPerm = citiesPerm[:]
	    newCitiesPerm[i+1:j+1] = citiesPerm[j:i:-1]
	    return newCitiesPerm


	#THIS FUNCTION IS CORE ALGORITHM AND IS BUILD FOR INITIALIZING BRANCH AND BOUND UPPER BOUND.
	def hillClimbingforBnB(self,cutoff,randseed):	    
	    cities = self.cities
	    distMatrix = self.costmatrix
	    citiesPerm = self.firstPermutation(cities,randseed)    
	    bestCost = self.cal_totalCost(citiesPerm,distMatrix)
	    start = time.time()
	    elapsed = 0
	    while(elapsed < cutoff):
	        while True:
	            minchange = 0
	            for i in range(0,len(cities)-2):
	                for j in range(i+2,len(cities)):
	                    change = (distMatrix[citiesPerm[i]][citiesPerm[j]] 
	                              + distMatrix[citiesPerm[i+1]][citiesPerm[j+1]]
	                              - distMatrix[citiesPerm[i]][citiesPerm[i+1]]
	                              - distMatrix[citiesPerm[j]][citiesPerm[j+1]]
	                              )
	                  
	                    if(minchange > change ):
	                        minchange = change
	                        
	                        min_i = i
	                        min_j = j
	                  
	            citiesPerm = self.swap(citiesPerm,min_i,min_j)
	       
	           
	            bestCost += minchange
	            endTime = time.time()
	            elapsed = endTime - start
	            

	            citiesPermX = citiesPerm[0:-1]
	            for w in range(len(citiesPermX)):
	                if citiesPermX[w] == 0:
	                    zeroIndex = w
	                    break
	                
	            firstHalf = citiesPermX[zeroIndex:]
	            secondHalf = citiesPermX[0:zeroIndex]
	            permStartWithZero = np.append(firstHalf, secondHalf)
	            permStartWithZero = np.append(permStartWithZero,0)
	            if minchange >= -0.1:
	                citiesPerm = citiesPerm[0:-1]
	                zeroposition = 0
	                for i in range(0,len(citiesPerm)):
	                	if citiesPerm[i]==0:
	                		zeroposition = i
	                left = citiesPerm[0:zeroposition]
	                right = citiesPerm[zeroposition:]
	                citiesPerm = np.concatenate((right,left))
	                citiesPerm = citiesPerm.tolist()
	                citiesPerm.append(0)
	                return int(bestCost), citiesPerm

	#THIS FUNCTION IS CORE ALGORITHM FUNCTION. 
	def hillClimbing(self,cutoff,randseed):	   
	    cities = self.cities
	    distMatrix = self.costmatrix
	    citiesPerm = self.firstPermutation(cities,randseed)    
	    bestCost = self.cal_totalCost(citiesPerm,distMatrix)
	    traceFileName = '../output/%s_hillClimbing_%d_%d.trace' % (self.filename.split('.')[0], cutoff, randseed)
	    traceFile = open(traceFileName, 'w')
	    solFileName = '../output/%s_hillClimbing_%d_%d.sol' % (self.filename.split('.')[0], cutoff, randseed)
	    solFile = open(solFileName,'w')
	    start = time.time()
	    elapsed = 0
	    while(elapsed < cutoff):
	        while True:
	            minchange = 0
	            for i in range(0,len(cities)-2):
	                for j in range(i+2,len(cities)):
	                    change = (distMatrix[citiesPerm[i]][citiesPerm[j]] 
	                              + distMatrix[citiesPerm[i+1]][citiesPerm[j+1]]
	                              - distMatrix[citiesPerm[i]][citiesPerm[i+1]]
	                              - distMatrix[citiesPerm[j]][citiesPerm[j+1]]
	                              )
	                  
	                    if(minchange > change ):
	                        minchange = change
	                        
	                        min_i = i
	                        min_j = j
	                  
	            citiesPerm = self.swap(citiesPerm,min_i,min_j)
	       
	           
	            bestCost += minchange
	            endTime = time.time()
	            elapsed = endTime - start
	            if elapsed>cutoff:
	            	solFile.write('%d' %int(bestCost))
	            	solFile.write('\n')
	            	for index in range(0,len(citiesPerm)-1):
	            		solFile.write('%d %d %d \n' % (citiesPerm[index],citiesPerm[index+1],distMatrix[citiesPerm[index],citiesPerm[index+1]]))
	            	solFile.close()
	            	traceFile.close()
	            	return int(bestCost),citiesPerm

	            

	            citiesPermX = citiesPerm[0:-1]
	            for w in range(len(citiesPermX)):
	                if citiesPermX[w] == 0:
	                    zeroIndex = w
	                    break
	                
	            firstHalf = citiesPermX[zeroIndex:]
	            secondHalf = citiesPermX[0:zeroIndex]
	            permStartWithZero = np.append(firstHalf, secondHalf)
	            permStartWithZero = np.append(permStartWithZero,0)
	            traceFile.write('%f %d \n' %(elapsed,int(bestCost)))


	            if minchange >= -0.1:
	                citiesPerm = citiesPerm[0:-1]
	                zeroposition = 0
	                for i in range(0,len(citiesPerm)):
	                	if citiesPerm[i]==0:
	                		zeroposition = i
	                left = citiesPerm[0:zeroposition]
	                right = citiesPerm[zeroposition:]
	                citiesPerm = np.concatenate((right,left))
	                citiesPerm = citiesPerm.tolist()
	                citiesPerm.append(0)
	                solFile.write('%d' %int(bestCost))
	                solFile.write('\n')
	                for index in range(0,len(citiesPerm)-1):
	                	solFile.write('%d %d %d \n' % (citiesPerm[index],citiesPerm[index+1],distMatrix[citiesPerm[index],citiesPerm[index+1]]))

	                #print int(bestCost),citiesPerm
	                solFile.close()
	                traceFile.close()
	                return int(bestCost), citiesPerm
	
def test_ClimbHill(filename,cutoff,seed):
	CH = ClimbHill(filename)
	rs = CH.hillClimbing(cutoff,seed)
	return rs


def main():
	filename = sys.argv[1]
	cutoff = int(sys.argv[2])
	seed = int(sys.argv[3])
	test_ClimbHill(filename,cutoff,seed)

#THIS FUNCTION WAS BUILT FOR GENERATING ALL RESULTS FOR COMPARING.
def gen_all():
	fn = ['Roanoke.tsp','Toronto.tsp','UMissouri.tsp', \
                 'SanFrancisco.tsp','Denver.tsp','NYC.tsp','Champaign.tsp', \
                 'Boston.tsp','Philadelphia.tsp','Atlanta.tsp',\
                 'UKansasState.tsp','Cincinnati.tsp']
	seeds = np.arange(0,10000,200)
	rs = []

	for i in range(0,len(fn)):
		tmp = 0
		for seed in seeds:
			tmp += test_ClimbHill(fn[i],15,seed)[0]
		tmpavg = tmp/10
		rs.append(tmpavg)
	print "THIS IS FINAL RESULT",rs

		











if __name__ == '__main__':
	main()
