import sys
from mst_approx import Run_MSTapprox
from appro_nearest import appro_nearest
import BnBmP as BnB
import ClimbHill as HC
from Annealing import SA

def main():
	length = len(sys.argv)
	if length>5 or length < 3:
		print "You should input at most 4 parameters and at least 3:\nFilename\nMethod (BnB,hillclimbing,appro_mst,appro_nearest,sa)\nCutoff Time\nSeed"
		exit(1)

	filename = sys.argv[1]
	method = sys.argv[2]
	cutoff = sys.argv[3]
	
	if method == "appro_mst":
		randomseed = sys.argv[4]
		print "YOUR METHOD IS APPPROXIMATION_MST"
		Run_MSTapprox(filename,int(cutoff),int(randomseed))
		print "APPPROXIMATION_MST HAS FINISHED"
	if method =="appro_nearest":
		randomseed = sys.argv[4]
		print "YOUR METHOD IS APPPROXIMATION_NEAREST NEIGHBOUR"
		appro_nearest(filename,int(cutoff),int(randomseed))
		print "APPPROXIMATION_NEAREST NEIGHBOUR HAS FINISHED"
	if method =="BnB":
		print "YOUR METHOD IS BnB"
		BnB.test_BnB(filename,int(cutoff))
		print "BnB HAS FINISHED"
	if method =="hillclimbing":
		randomseed = sys.argv[4]
		print "YOUR METHOD IS HillClimbing"
		HC.test_ClimbHill(filename,int(cutoff),int(randomseed))
		print "HillClimbing HAS FINISHED"
	if method =="sa":
		randomseed = sys.argv[4]
		print "YOUR METHOD IS Simulated Annealing"
		SA()
		print "Simulated Annealing HAS FINISHED"



if __name__ == '__main__':
	main()