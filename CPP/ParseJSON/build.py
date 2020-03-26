#!/usr/bin/python3.6
import os

# Make sure you build the boost libraries first. 
# 
os.system("g++ ParseJSON.cpp -I ../Boost/boost_1_70_0 -DDEBUG_LEVEL=0; ./a.out") 
