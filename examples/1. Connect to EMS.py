# Display information about connected Scanner

from ems import Device
device = Device()
print(device.GetDeviceType())
print(device.GetScannerSize())
print(device.GetScannerProbeGap())