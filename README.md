# CORK1024C

These scripts were first developed for CORK and BPR (paroscientific sensors) by Martin Heesemann ([@mheesema](https://github.com/MHee))
The following process can be applied to any paroscientific sensor that has the standard paroscientific calibration coefficients applied:

* U0
* Y1
* Y2
* C1
* C2
* C3
* D1
* T1
* T2
* T3
* T4

ONC/NRCAN owned paroscientific sensors have sensor identification numbers. These IDs don't change and whenever an instrument get recalibrated the coefficients will change but will be attached to the same ID.

There are **two** python scripts in this repo:

 1. calibrateBPRData.py
 2. Calibrate_1024C_TestData.py

The first one is a general script that has a bunch of functions defined that will be used in the second script. This script can be used to calibrate any number of paroscientific sensors, so its suitable for any BPR/CORK.

The second script is the executable script for the CORK1024C data:
 1. it reads the hexadecimal values as strings from the file (will ignore DMAS timestamps or other non-hexstring values in the line) and converts it to integer decimal values based on 8 characters -> saves them into a large list
  -  at the same time it converts the hexdecimal time into a datetime format
  -  saves everything in a list
2. goes through each item in the list and applies the calibration formula and coefficients identified in calibrateBPRData.py
3. saves it into a dictionary and then dataframe to plot and save

**-Requirements-**:
 - python 3
 - input data as file of hexstrings
