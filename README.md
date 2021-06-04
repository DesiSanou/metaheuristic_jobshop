# meta-jobshop

This branch provide Taboo and Descend method of jobshop problem.

To execute this project you need to create conda environment with python 3.7 and install the requirement packages

`conda create -n 'your env' python=3.7`

`pip install -r requirements.txt`

And then, you can use several options to execute :
--instances : list the instances name to test, separated by -; 
              used all to test all the instances (aaa1, ft06, ft20, ft10, la01, la02)
--save_result: to save the results in a json file. 
                This file can be processed in the file named process_results.py
--create_figs : to save figures after running the code
--show: whether you want to plot the result figures or not (default: False)

`python main.py --instances aaa1-ft20 --save_result --create_figs --show`

![image](https://user-images.githubusercontent.com/16137402/120869939-e7863d00-c597-11eb-82ab-ef8c121dea65.png)








