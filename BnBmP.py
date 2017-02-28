import numpy as np
import pandas as pd
import copy
import time
from heapq import *
import ClimbHill as CH
import sys

class BranchandBound:
	def __init__(self,address):
		ATL = open("./DATA/"+address,"r")
		self.filename = address
		print ATL.readline()#NAME: ATLANTA
		print ATL.readline()#COMMENT: 20 locations in Atlanta
		num = filter(str.isdigit, (ATL.readline())) #DIMENSION: 20
		num = int(num)
		print ATL.readline()#EDGE_WEIGHT_TYPE: EUC_2D
		print ATL.readline()#NODE_COORD_SECTION
		data = np.array([0]*3*num,dtype="float").reshape(num,3)

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
		self.dim = num
		nocp = copy.copy(nodedismatrix)
		self.C = nocp
		self.distanceM = nodedismatrix
		test = CH.ClimbHill(address)
		self.UB,self.solution = test.hillClimbingforBnB(100,1000)
		print self.UB,self.solution
		self.n = num
		self.LB = 0
		self.BOUND = np.inf
		self.cutoff = 600
		
	#THIS FUNCTION IS USED FOR CALCULATE INDEX MIN VALUE OF A ROW
	def rowMin(self,costmatrix,i):
		
		n = costmatrix.shape[0]
		minvalue = costmatrix[i,0]
		for j in range(0,n):
			if costmatrix[i,j]<minvalue:
				minvalue = costmatrix[i,j]
		if minvalue == np.inf:
			minvalue = 0
		
		return minvalue

	#THIS FUNCTION IS USED FOR CALCULATE INDEX MIN VALUE OF A COLUMN
	def colMin(self,costmatrix,j):
		
		n = costmatrix.shape[0]
		minvalue = costmatrix[0,j]
		for i in range(0,n):
			if costmatrix[i,j]<minvalue:
				minvalue = costmatrix[i,j]
		if minvalue == np.inf:
			minvalue = 0
		return minvalue

	#THIS FUNCTION IS USED FOR COMPUTING ROW REDUCTION
	def rowReduction(self,costmatrix):
		n = costmatrix.shape[0]
		row = 0
		for i in range(0,n):
			rmin = self.rowMin(costmatrix,i)
			if np.isinf(rmin) == False:
				row += rmin

			for j in range (0,n):
				if np.isinf(costmatrix[i,j]) == False:
					costmatrix[i,j] = costmatrix[i,j]-rmin		
		return row,costmatrix

	#THIS FUNCTION IS USED FOR COMPUTING COLUMN REDUCTION
	def colReduction(self,costmatrix):
		n = costmatrix.shape[0]
		col = 0
		for j in range (0,n):
			cmin = self.colMin(costmatrix,j)
			if np.isinf(cmin) == False:
				col += cmin
			for i in range (0,n):
				if np.isinf(costmatrix[i,j]) ==False:
					costmatrix[i,j] = costmatrix[i,j] - cmin
					
		
		return col,costmatrix

	#THIS FUNCTION IS USED FOR SETTING A ROW TO ALL INFINITY VALUE
	def deleteRow(self,matrix,i):
		for x in range(0,matrix.shape[1]):
			matrix[i,x] = np.inf
		return matrix

	#THIS FUNCTION IS USED FOR SETTING A COLUMN TO ALL INFINITY VALUE
	def deleteCol(self,matrix,j):
		for x in range(0,matrix.shape[0]):
			matrix[x,j] = np.inf
		return matrix

	#THIS FUNCTION IS USED FOR GETTING THE INCREASED LOWER BOUND  VALUE FOR A CERTAIN PATH AND UPDATED COST MATRIX FOR THAT PATH. INPUT ARE COST MATRIX AND PATH.
	def getCost(self,cost,inputlist):
		frmatrix = copy.copy(cost)
		extra = 0
		if len(inputlist)<=1:
			return extra,frmatrix
		for i in range(0,len(inputlist)-1):
			#print "FRMT",frmatrix
			#print [inputlist[i],inputlist[i+1]]
			extra += frmatrix[inputlist[i],inputlist[i+1]]
			frmatrix[inputlist[i+1],inputlist[i]] = np.inf
			frmatrix = self.deleteRow(frmatrix,inputlist[i])
			frmatrix = self.deleteCol(frmatrix,inputlist[i+1])
			#print frmatrix
			r,frmatrix = self.rowReduction(frmatrix)
			c,frmatrix = self.colReduction(frmatrix)
			extra = extra+r+c
			#print frmatrix
		#print "THIS IS EXTRA",extra
		#print "THIS IS MAtrixafterreduce",frmatrix
		return extra,frmatrix


	#THIS FUNCTION IS CORE ALGORITHM FUNCTION.
	def coreAlgo(self):
		n = self.n
		t0 = time.clock()
		cost = self.distanceM
		traceFileName = '../output/%s_BnB_%d.trace' % (self.filename.split('.')[0], self.cutoff)
		traceFile = open(traceFileName, 'w')
		solFileName = '../output/%s_BnB_%d.sol' % (self.filename.split('.')[0], self.cutoff)
		solFile = open(solFileName, 'w')
		#print "Initial cost\n",cost
		t = time.clock()-t0
		traceFile.write('%f, %d \n' % (t, int(self.UB)))
		lb,cost = self.rowReduction(cost)
		self.LB+=lb
		#print "rowreduction cost\n",cost
		lb,cost = self.colReduction(cost)
		self.LB+=lb
		print "colreduction cost\n",cost
		FirstRuducedM = cost
		print self.LB
		##CORE START
		mPriorityQueue = []
		#heappush(PriorityQueue,(self.LB,[0]))
		heappush(mPriorityQueue,(self.n,self.LB,[0]))

		#print "t is ",t0
		while len(mPriorityQueue) != 0 :
			
			#print "ttttt is ",t
			t = time.clock()-t0
			if t >= self.cutoff:
				print "LINE 186"
				print "CUTOFF TIME"
				print "ANS WITHIN CUTOFF TIME:", self.UB,self.solution
				solFile.write('%d' % (int(self.UB)))
				solFile.write('\n')
				print self.solution
				for i in range(0,len(self.solution)-1):
					solFile.write('%d %d %d \n' %(self.solution[i],self.solution[i+1],self.C[self.solution[i],self.solution[i+1]]))
				solFile.close()

				return self.UB,self.solution
			
			#node = heappop(PriorityQueue)
			node = heappop(mPriorityQueue)
			templen = node[0]
			tempLB = node[1]
			templist = node[2]
			if self.UB>tempLB :
				
				bulb,bumx= self.getCost(FirstRuducedM,templist)
				#print "BUMX\n",self.getCost(FirstRuducedM,templist)
				for i in range (0,self.n):     #THIS NEED TO BE RESET
					if i not in templist:
						st = templist[-1]
						des = i
						newtemplist = copy.copy(templist)
						newtemplist.append(i)
						llbb,tempmtx = self.getCost(bumx,[templist[-1],i])
						#print "FINISH ONE getCost"
						newlb = self.LB+llbb+bulb
						if newlb<=self.UB and len(templist)<=self.n-1:
							#heappush(PriorityQueue,(newlb,newtemplist))
							minlb = np.inf
							idx = 0
							ntplst = []
							##BOOST##
							for x in range(0,self.n):
								if x not in newtemplist:
									ntplst = copy.copy(newtemplist)
									ntplst = ntplst.append(x)
									tmplb = self.getCost(tempmtx,[newtemplist[-1],x])
									if minlb>tmplb:

										minlb = tmplb
										idx = x
							#print "FINISH LIST getCost"
							if newlb+minlb<self.UB:
								if len(ntplst)!=self.n:
									ntplst = copy.copy(newtemplist)
									ntplst.append(idx)
									heappush(mPriorityQueue,((self.n-len(ntplst)),newlb+minlb,ntplst))
								else:
									print "I GOT A POSSIBLE SOLUTION#################################"
									print newlb+minlb
									print "NTPLIST",ntplst
									self.UB = newlb+minlb
									t1 = time.clock()-t0
									traceFile.write('%f, %d \n' % (t1, int(self.UB)))
									cp = copy.copy(ntplst)
									cp.append(0)
									self.solution = cp
									print "self.solution",self.solution
							else:
								heappush(mPriorityQueue,(self.n-len(newtemplist),newlb,newtemplist))
								#print len(templist)
								currenttime = time.clock()-t0
								#print currenttime
								if currenttime>=self.cutoff:
									print "BREAKWITHIN WHILE"
									break

							
							#print "NEWLB,LIST",newlb,newtemplist

						if self.UB>newlb and len(newtemplist)==self.n:
							print "I GOT A POSSIBLE SOLUTION#################################"
							print newlb
							print newtemplist
							self.UB = newlb
							t2 = time.clock()
							traceFile.write('%f, %d \n' % (t2, int(self.UB)))
							cp = copy.copy(newtemplist)
							cp.append(0)
							print cp
							self.solution = cp
							print "self.solution",self.solution
		traceFile.close()
		solFile.write('%d' % (int(self.UB)))
		solFile.write('\n')
		for i in range(0,len(self.solution)-1):
			
			print self.distanceM[self.solution[i],self.solution[i+1]]
			solFile.write('%d %d %d \n' %(self.solution[i],self.solution[i+1],self.C[self.solution[i],self.solution[i+1]]))
		solFile.close()
			
		print "LINE 192"
		print self.UB
		print self.solution
		print self.distanceM




def test_BnB(filename,cutofftiem):
	path = filename
	Bb = BranchandBound(path)
	Bb.cutoff = cutofftiem
	Bb.coreAlgo()


def main():
	path = sys.argv[1]
	cutofftiem = int(sys.argv[2])
	test_BnB(path,cutofftiem)



def gen_all():
	fn = ['Roanoke.tsp','Toronto.tsp','UMissouri.tsp', \
                 'SanFrancisco.tsp','Denver.tsp','NYC.tsp','Champaign.tsp', \
                 'Boston.tsp','Philadelphia.tsp','Atlanta.tsp',\
                 'UKansasState.tsp','Cincinnati.tsp']
	for i in range(0,len(fn)):
		test_BnB(fn[i],600)


if __name__ == '__main__':
	gen_all()







'''
distanceM = np.array([[np.inf,10,8,9,7],[10,np.inf,10,5,6],
			[8,10,np.inf,8,9],[9,5,8,np.inf,6],[7,6,9,6,np.inf]],dtype="float")

Bb = BranchandBound("./DATA/Cincinnati.tsp")
Bb.coreAlgo()

'''

'''
SanFrancisco 810196
NYC 1555060
Roanoke 655454
Atlanta 2003763
Champaign 52643
Cincinnati 277952
Philadelphia 1395981
UKansasState 62962
Toronto 1176151
UMissouri 132709
Boston 893536
Denver 100431
'''
