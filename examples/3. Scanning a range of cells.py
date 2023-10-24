# Run scan of single frequency on a square-shaped area of probes.

import csv
import pyvisa
from ems import Device

# Connecting to Spectrum Analyzer.
# For list of all available devices, use
# print(rm.list_resources())
rm = pyvisa.ResourceManager()
spectrum_analyzer = rm.open_resource('USB0::0x1AB1::0x0960::DSA8E163700013::INSTR')

# Define EM Scanner
device = Device()

def ScanProbe(Col, Row):

    print("Scanning Probe", Col, Row)
    device.SwitchProbe(Col, Row)
    # Start Scan. Wait for synchronization using *OPC?
    spectrum_analyzer.write(':INIT:IMM;*OPC?')
    spectrum_analyzer.read()
    print("Cell Scanned")
    # Collect results.
    output = spectrum_analyzer.query(':TRAC? trace1')

    # the output is a single string
    output = output.split(",")
    # A block header is present at the start of all trace returns. This needs to be removed.
    # The first element has the header, followed by the first coordinate.
    x = output[0].split(" ")
    output[0] = x[1]
    # Convert the list of strings to list of floats
    output = [float(x) for x in output]

    # Find the maximum Value
    sweep_points = len(output)
    largest_value = -999
    for i in range(0, sweep_points):
        if(output[i] > largest_value):
            largest_value = output[i]

    return largest_value

# Reset Spectrum Analyzer
spectrum_analyzer.write('*RST')
# Initilise Spectrum Analyzer
spectrum_analyzer.write(':INIT:CONT 0')
spectrum_analyzer.write('POW:GAIN 1')
spectrum_analyzer.write('POW:ATT 0')
spectrum_analyzer.write('SWE:POIN 101') # This is the minimum for DSA 875
spectrum_analyzer.write(':SENS:BAND:RES 100000')

spectrum_analyzer.timeout = 250000

# Define target frequency. 48MHz
spectrum_analyzer.write('FREQ:STAR  48000000')
spectrum_analyzer.write('FREQ:STOP  48000000')

# Top left probe has coordinates (0,0)

# Define Selection Area
probe_area_cornerAC = int(input("Enter the column number of the top left corner of scan "))
probe_area_cornerAR = int(input("Enter the row number of the top left corner of scan "))

probe_area_cornerBC = int(input("Enter the column number  of the bottom right corner of scan "))
probe_area_cornerBR = int(input("Enter the row number of the bottom right corner of scan "))

# Open CSV File
with open('SingFreq.csv', 'w', newline='') as file:

    # Loop over all rows and column between corners
    for col in range(probe_area_cornerAC, probe_area_cornerBC):
        for row in range(probe_area_cornerAR, probe_area_cornerBR):
                
                result = ScanProbe(col, row)
                
                writer = csv.writer(file)
                # Write [column, row, result] into CSV File.
                writer.writerow([col, row, result])
print("Scan Complete")