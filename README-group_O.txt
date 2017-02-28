All the algorithm can be implemented by using the following command with 'DATA' folder in the same directory:

python Run.py datafile method cutoff_time random_seed

e.g.
python Run.py UMissouri.tsp appro_nearest 200 1


"method" parameter has the following options:
BnB,hillclimbing,appro_mst,appro_nearest,sa


IMPORTANT NOTE: 
The hill climbing method can either find 1 solution or find the current best solution within the cutoff time. There is no random restart part in this code. When generating plots or do the performance analysis, we use a list of seeds, which has the length of the list 50 or 10 respectively, to generate trace file or average best solution. The performance shown in the report is 10-seed-average performance. 
