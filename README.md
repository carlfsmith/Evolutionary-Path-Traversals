# Evolutionary-Path-Traversals
Code contains logic which creates various competing paths with the sole objective of traversing a user defined graymap -with black terrain being the most cost effective. 

This program uses a library called xlsxwriter to generate a graph. To install follow the instructions here:
https://xlsxwriter.readthedocs.org/getting_started.html

The library is commented out by default, but to use it comment back in line 11 (import..) and 280 (draw_graph..).

The main loop is set to 5 minutes, which processes about 6000 generations. This can be changed on line 264 (5*60)

To make the code compatible with python 2.7, the time module used was changed to clock() instead of process_time()
