import time
import sys
import math
import random


def SA():
    #read data
    def getDistanceMatrix(graph,numCities):
        distanceMatrix = [[0 for x in range(numCities)]for y in range(numCities)]
        for i in range(numCities):
            for j in range(numCities):
                ix = graph[i][1]
                iy = graph[i][2]
                jx = graph[j][1]
                jy = graph[j][2]
                distanceMatrix[i][j] = math.sqrt(pow(ix-jx,2)+pow(iy-jy,2))
        return distanceMatrix

    def getEnergy(cityOrder,distanceMatrix,numCities):
        energy = 0
        for i in range(numCities-1):
            city1 = cityOrder[i]
            city2 = cityOrder[i+1]
            energy = energy + distanceMatrix[city1][city2]
        city1 = cityOrder[0]
        city2 = cityOrder[numCities-1]
        energy = energy+distanceMatrix[city1][city2]
        return energy

    def swap(order,a,b,numCitis):
        if(order.index(a)>order.index(b)):
            temp = a
            a = b
            b = temp
        aPos = order.index(a)
        bPos = order.index(b)
        cPos = aPos+1
        dPos = bPos+1
        temp = order
        temp[aPos] = b
        temp[bPos] = a

        newOrder = []
        newOrder.extend(temp[0:aPos+1])
        temp1 = temp[cPos:bPos+1]
        temp1 = temp1[::-1]
        newOrder.extend(temp1)
        newOrder.extend(temp[dPos:numCitis])
        return newOrder

    def acceptance(difference,temperature):
        if -difference/temperature > 0.0000001:
            prob = math.exp((difference)/temperature)
        else:
            prob = 0
        return prob

    if len(sys.argv) < 4:
        print "Error: not enough input arguments"

    filename = sys.argv[1]
    cutoff_time = sys.argv[3]
    random_seed = sys.argv[4]
    random.seed(random_seed)

    a=open('DATA/'+filename,'r')
    graphData=a.read().split('\n')
    a.close()
    numCities = int(graphData[2].split(' ')[1])
    graph = []
    for i in graphData[5:numCities+5]:
        temp = i.split(' ')
        graph.append((float(temp[0]),float(temp[1]),float(temp[2])))
    #create the distance matrix
    distanceMatrix = getDistanceMatrix(graph,numCities)
    #Annealing parameters
    temperature = 900
    coolingRate = 0.995
    endTemperature = 100
    bestEnergy = sys.float_info.max

    #initalize solution by random
    cityOrder = [i for i in range(numCities)]
    random.shuffle(cityOrder)
    bestEnergy = getEnergy(cityOrder,distanceMatrix,numCities)
    currentEnergy = bestEnergy
    #annealing loop
    trace = open('../output/'+filename.split('.')[0] + '_simulatedAnnealing_' + str(cutoff_time) + '_' + str(random_seed) + '.trace','w')
    iter = 0
    start_time = time.time()
    current_time = start_time
    threshold = 0
    while temperature > endTemperature and (current_time-start_time)<cutoff_time:
        for numIteration in range(min(600,int(numCities*(numCities-1)/2))):
            tempOrder = cityOrder
            city1 = 0
            city2 = 0
            while city1 == city2:
                city1 = random.randint(0,numCities-1)
                city2 = random.randint(0,numCities-1)
            currentEnergy = getEnergy(cityOrder,distanceMatrix,numCities)
            newOrder = swap(cityOrder,city1,city2,numCities)
            newEnergy = getEnergy(newOrder,distanceMatrix,numCities)
            index1,index2 = cityOrder.index(city1), cityOrder.index(city2)
            cityOrder[index1],cityOrder[index2] = cityOrder[index2],cityOrder[index1]
            difference = currentEnergy - newEnergy

            #check energy
            a = acceptance(difference,temperature)
            b = random.random()
            #print difference,a,b
            if difference > 0:
                currentEnergy = newEnergy
                if currentEnergy < bestEnergy:
                    bestSoln = newOrder
                    bestEnergy = currentEnergy
                cityOrder = newOrder
                current_time = time.time()
                trace.write('%f,%d\n' %(current_time-start_time,bestEnergy))
            elif a > b:
                cityOrder = newOrder
            iter = iter+1
        temperature = temperature*coolingRate

    solution = open('../output/'+filename.split('.')[0] + '_simulatedAnnealing_' + str(cutoff_time) + '_' + str(random_seed) + '.sol','w')
    solution.write('%d' %bestEnergy + '\n')
    count = 0
    while count < len(bestSoln)-1:
        solution.write('%d,%d,%d'%(bestSoln[count],bestSoln[count+1],distanceMatrix[bestSoln[count]][bestSoln[count+1]])+'\n')
        count = count + 1
    solution.write('%d,%d,%d'%(bestSoln[count],bestSoln[0],distanceMatrix[bestSoln[count]][bestSoln[0]])+'\n')
    solution.close()
    # trace
    trace.close()
    pass


def main():
    SA()

if __name__ == '__main__':
    # run the experiments
    main()