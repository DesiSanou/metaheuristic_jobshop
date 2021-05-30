# metaheuristic_jobshop

To run code, use main.py file 
<pre>

several options can be used:
--instances : list the instances name to test, separated by -; 
              used all to test all the instances (aaa1, ft06, ft20, ft10, la01, la02)
--save_result: to save the results in a json file. 
                This file can be processed in the file named process_results.py
--create_figs : to save figures after running the code
--show: whether you want to plot the result figures or not (default: False)

python main.py --instances aaa1-ft20 

These  are results obtained by using the basic solver. It can be a reference to check that  
if other heuristics improve the makespan.

Basic Result : 

instance    size      best    runtime    makespan    ecart
----------  ------  ------  ---------  ----------  -------

aaa1        2x3         11          0          12      9.1
ft06        6x6         55          0          75     36.4
ft10        10x10      930          0        1588     70.8
ft20        20x5      1165          0        2454    110.6
la01        10x5       666          0         776     16.5
la02        10x5       655          0         736     12.4


</pre>
