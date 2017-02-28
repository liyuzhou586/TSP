import math
import random
import sys
import time

def appro_nearest(filename,cutoff,seed):
    # to ensure enough inputs' arguements
  
    # to utilize inputs' arguements
    filename = filename
    cutoff_time = cutoff
    random_seed = seed
    random.seed(random_seed)

    # to define necessary variables
    point_data = {}
    point_dis = {}
    path_dis = []
    tour_num = []
    tour_dis = 0
    total_time = 0

    # to read file and store data
    file = open('DATA/'+filename, 'r')
    line = file.readline()
    while line.find("NODE_COORD_SECTION") == -1:
        line = file.readline()
    while 1:
        line = file.readline()
        if line.find("EOF") != -1:
            break
        (i, x, y) = line.split()
        i = int(i)
        x = float(x)
        y = float(y)
        point_data[i] = (x, y)
    point_data_raw = point_data.copy()

    # to generate random original seed
    root = random.randint(1,len(point_data))
    root_num = root
    tour_num.append(root_num)

    # to generate following TSP points
    start_time = time.clock()
    while len(point_data) > 1 and total_time < cutoff_time:
        for i in point_data:
            if i != root_num:
                x = point_data[i][0] - point_data[root_num][0]
                y = point_data[i][1] - point_data[root_num][1]
                point_dis[i] = math.sqrt(x*x+y*y)
        add_point = min(point_dis.items(), key=lambda x: x[1])[0]
        tour_num.append(add_point)
        path_dis.append(point_dis[add_point])
        tour_dis = tour_dis + point_dis[add_point]

        # to change root
        del point_data[root_num]
        point_dis = {}
        root_num = add_point

        total_time = time.clock() - start_time

    # to include the original point to the tour
    x = point_data_raw[root][0] - point_data_raw[root_num][0]
    y = point_data_raw[root][1] - point_data_raw[root_num][1]
    final_path_dis = math.sqrt(x*x+y*y)
    tour_dis = tour_dis+ final_path_dis
    tour_num.append(root)
    path_dis.append(final_path_dis)
    # print tour_dis
    # print tour_num
    # print path_dis
    # print total_time

    # output file
    # solution
    solution = open('../output/'+filename.split('.')[0] + '_appro_nearest_' + str(cutoff_time) + '_' + str(random_seed) + '.sol','w')
    solution.write('%d' %tour_dis + '\n')
    count = 0
    while count < len(tour_num)-1:
        solution.write('%d %d %d'%(tour_num[count],tour_num[count+1],path_dis[count])+'\n')
        count = count + 1
    solution.close()
    # trace
    trace = open('../output/'+filename.split('.')[0] + '_appro_nearest_' + str(cutoff_time) + '_' + str(random_seed) + '.trace','w')
    trace.write('%f %d' %(total_time,tour_dis))
    trace.close()


def main():
    print "Main"
    filename = sys.argv[1]
    cutoff = sys.argv[2]
    seed = sys.argv[3]
    appro_nearest(filename,cutoff,seed)
    print "Finish"


if __name__ == '__main__':
    main()


