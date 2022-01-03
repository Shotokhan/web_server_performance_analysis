# web_server_performance_analysis

This repository contains different experiments concerning the performance analysis of a web server. <br>

- ```flask_docker``` folder contains the actual web server used, the ```docker-compose.yml``` file contains specs about cpu and memory to allocate;
- ```capacity_test``` folder contains output files and scripts used to perform a capacity test: the goal is to find the peak of the ratio ```throughput / response_time``` w.r.t the offered load;
- ```workload_characterization``` folder contains a bunch of files related to the activity of extracting a synthetic workload from a realistic workload, such that the two workloads have the same impact on low-level parameters (the "same impact" test is done using hypothesis tests);
- ```design_of_experiment``` folder contains some files about the design of a set of tests, in which there is a certain number of factors, each one able to assume certain levels, and the goal is to determine the impact of each factor and of the interaction between factors on some performance metrics, such as response time and throughput.

Tests are executed via Apache JMeter; in the folders there are .jmx files, which are JMeter test plans.

