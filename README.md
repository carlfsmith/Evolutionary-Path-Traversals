# Evolutionary-Path-Traversals
Code contains logic which creates various competing paths with the sole objective of traversing a user defined graymap -with black terrain being the most cost effective. 

Populations contain chromosomes made up of genes which determine an angle and associated number of steps. When the population is propagated, a chromosome which is likely 'weak' (high cost value), will 'die' and another will be born from two fit chromosomes -inheriting half the genes from both parents. Randomness is added in the form of chance mutations in genes or for random genes to be dropped or added. A graph production api is included which shows costs for chromosomes over generations.
 master

This program uses a library called xlsxwriter to generate a graph which shows minimum chromosome costs for a population over time. To install follow the instructions here:
https://xlsxwriter.readthedocs.org/getting_started.html

The library is commented out by default, but to use it comment back in line 11 (import..) and 280 (draw_graph..).

The main loop is set to 5 minutes, which processes about 6000 generations. This can be changed on line 264 (5*60)

To make the code compatible with python 2.7, the time module used was changed to clock() instead of process_time()
