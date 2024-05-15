import sys, os

# csfp - current_script_folder_path
csfp = os.path.abspath(os.path.dirname('RK_Stuff/CORK1024C'))
if csfp not in sys.path:
    sys.path.insert(0, csfp)

# import the calibrateBPRData.py class CalibrationCoefficients that contains
# methods of how to get the coefficients for each sensor from the submitted files
# and then parses the ASCII converted string values in actual physical entities

from calibrateBPRData import CalibrationCoefficients 

# read in the parameter for your sensors (ID for logger and files with coefficients for paro and platinum)
CC  = CalibrationCoefficients( 
           ID=0x06,
         # ID for BPR in hexformat
           parofile = 'parosci.txt',
           thermsfile = 'therms.txt',
           platinumfile = 'platinum.txt')

# data file containing hexstrings
data = ('TestData/20240510_1024C_firstTestData_fixed.log')

# get the calibration coefficients (PC*) for each sensor
PC1 = CC.getParoCoeffs(43397) # BH paro
PC2 = CC.getParoCoeffs(107553) # SF paro
PLC = CC.getPlatinumCoeffs(0x9C) # Platinum Coeffs
print(PLC)

# read in all lines from hexstring file and convert to ASCII 


import pandas as pd
import re
df = pd.read_csv(data,sep=' ',names=['Timestamp','hexLine'])
print(df)
Raw=[]
for line in df['hexLine']:
    try:
                        # Minimum sample with time, id, Tint, 1 Paros, and 00 has 26 characters
                        hexBlock=re.search(r'[\dA-Fa-f]{26,}',line)
                        #print(hexBlock.group(0))
                        x=re.findall(r'[\dA-Fa-f]{8}',hexBlock.group(0))
                        x[1]=x[1][2:]
                        t=CC.calibratePPCTime(int(x[0],16)).strftime('%Y-%m-%d %H:%M:%S')
                        if not x[2] == 'FFFFFFFF':
                            xData=[int(xi,16) for xi in x[1:]]
                        else:
                            xData=[int(xi,16) for xi in x[1:]]
                            xData[1]=0
                        Raw.append([t,xData])
                        #                    Data=CCD.calibrateData(xData)
    except:
                        pass
    
    print(Raw[0:5])

# create a set of lists that will be used to collect the individual sensor readings
paroSFPressure = []
paroBHPressure = []
paroBHTemperature=[]
marineTemperature=[]
time=[]

# read each line and calibrate each value
for line in Raw:
        time.append(line[0])
        
        paroBHTemperature.append(CC.calibrateParoT(line[1][1],Coeffs=PC1))
        
        
        mTemp=CC.calibratePlatinum(line[1][0],Coeffs=PLC)
        print(mTemp)
        marineTemperature.append(mTemp)
        paroBHPressure.append(CC.calibrateParoP(line[1][2],Coeffs=PC1,xFT=line[1][1], Temp=mTemp))
        paroSFPressure.append(CC.calibrateParoP(line[1][3],Coeffs=PC2,xFT=None, Temp=mTemp))

# create a dictionary that represents the calibrated values in order of the hexstring input
# then for easy use convert to a dataframe
dict_1 = {'Time':time,'MarineTemp':marineTemperature,'Borehole Temp':paroBHTemperature,
          'Borehole Pressure':
          paroBHPressure, 'Seafloor Pressure':paroSFPressure}
df2 = pd.DataFrame.from_dict(dict_1)
df2.set_index(pd.to_datetime(df2['Time']),inplace=True) # set the time as index

# plot the individual sensor readings versus time and save output as image and csv data file
import matplotlib.pyplot as plt
fig=plt.figure(figsize=[11,8])
df2.plot(subplots=True,figsize=[11,8])
plt.savefig('1024C_testData_May9-2024.png')
df2.to_csv('1024C_testData_May9-2024.csv')
