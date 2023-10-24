# Run scan of range of frequencies on single probe. Save result to CSV file.

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

# Read and set target probe
probe_location_C = int(input("Enter Column "))
probe_location_R = int(input("Enter Row "))

device.SwitchProbe(probe_location_C, probe_location_R)

# Reset Spectrum Analyzer
spectrum_analyzer.write('*RST')
# Initilise Spectrum Analyzer
spectrum_analyzer.write(':INIT:CONT 0')
spectrum_analyzer.write('POW:GAIN 1')
spectrum_analyzer.write('POW:ATT 0')
spectrum_analyzer.write(':SENS:BAND:RES 100000')

# Define target frequencies. 1MHz - 200MHz
spectrum_analyzer.write('FREQ:STAR  1000000')
spectrum_analyzer.write('FREQ:STOP  200000000')

# Start Scan. Wait for synchronization using *OPC?
spectrum_analyzer.write(':INIT:IMM;*OPC?')
spectrum_analyzer.read()

# Collect results. Output is a single string with containing all amplitudes.
output = spectrum_analyzer.query(':TRAC? trace1')

# the output is a single string 
output = output.split(",")
# A block header is present at the start of all trace returns. This needs to be removed.
# The first element has the header, followed by the first coordinate.
x = output[0].split(" ")
output[0] = x[1]
# Convert the list of strings to list of floats
output = [float(x) for x in output]

# Open CSV File
with open('FreqRange.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for i in range(0, len(output)):
        # Calculate the frequency of the point
        frequency = 1000000 + (i/len(output)) * (199000000)
        # Write [Frequency, Amplitude] to CSV file.
        writer.writerow([frequency, output[i]])