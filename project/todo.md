# Todo: 
2. Make the worker.py stable, by increasing the maximum runtime. Make a quick analysis of the number of points, and dimensions in the dataset. If the workload takes too much time, notify the user about the problem. 
3. Put the worker.py into kubernetes, and make the application scalable by launching multiple workers. 
4. Make the worker output the classification results - this means a change in the actual docker container, by modifying the runner.py
5. Make the dataset uploader, for custom datasets. 
6. Make it possible to test the algorithms on the datasets. 
7. Insert a terms and conditions, in a scrollable modal upon user sign in. 
8. Ensure we can evaluate recall and precision aswell. 
9. Make checks on the inputs for the parameters, cause right now we can run a lot of invalid input. 
10. Add functionality to remove test results


