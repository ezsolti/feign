#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 11:05:39 2019

@author: zsolt
"""

import time

start = time.time()
for _ in range(1000000):
    Point(3,4).inBetween(Point(4,5),Point(2,9))
end = time.time()
print(end - start)


start = time.time()
for _ in range(1000000):
    Point(3,4).inBetweenOld(Point(4,5),Point(2,9))
end = time.time()
print(end - start)

x=3
start = time.time()
for _ in range(10000000):
    x*x
end = time.time()
print(end - start)


start = time.time()
for _ in range(10000000):
    x**2
end = time.time()
print(end - start)

start = time.time()
for _ in range(10000000):
    math.pow(x,2)
end = time.time()
print(end - start)