from ctypes import *
from sys import platform, argv
import os
from enum import Enum
from typing import Tuple

dirname = os.path.dirname(argv[0])
lib = windll.LoadLibrary(dirname + "\\EMSAPI.dll")

class DeviceType(Enum):
    NONE = -1
    EMS08 = 0
    EMSR08 = 1

class EMSException(Exception):
    pass

class UnknownException(EMSException):
    def __init__(self, code):
        self.code = code
        super().__init__(f"Error code: {code}")

class NoDeviceFoundException(EMSException): pass
class InvalidArgumentException(EMSException): pass
class CommunicationFailedException(EMSException): pass
class NotImplementedException(EMSException): pass
class CellOutOfRangeException(EMSException): pass

def CheckForError(error):
    if error == 0: return
    elif error == 1:
        raise NoDeviceFoundException
    elif error == 2:
        raise InvalidArgumentException
    elif error == 3:
        raise CommunicationFailedException
    elif error == 4:
        raise NotImplementedException
    elif error == 5:
        raise CellOutOfRangeException
    else:
        raise UnknownException(error)

class Device:
    def __init__(self):
        self._device = c_void_p(None)
        error = lib.EMS_ConnectDevice(byref(self._device))
        CheckForError(error)

    def __del__(self):
        if not self._device: return
        error = lib.EMS_DisconnectDevice(self._device)
        CheckForError(error)

    def GetDeviceType(self) -> DeviceType:
        result = c_int(-1)
        error = lib.EMS_GetDeviceType(self._device, byref(result))
        CheckForError(error)
        return DeviceType(result.value)
    
    def IsScannerAttached(self) -> bool:
        result = c_bool()
        error = lib.EMS_IsScannerAttached(self._device, byref(result))
        CheckForError(error)
        return result.value
    
    def GetScannerSize(self) -> Tuple[int, int]:
        columns = c_int32()
        rows = c_int32()
        error = lib.EMS_GetScannerSize(self._device, byref(columns), byref(rows))
        CheckForError(error)
        return (columns.value, rows.value)
    
    def GetScannerProbeGap(self):
        result = c_int()
        error = lib.EMS_GetScannerProbeGap(self._device, byref(result))
        CheckForError(error)
        return result.value
    
    def GetScannerProbeAngle(self, column : int, row : int):
        result = c_int()
        error = lib.EMS_GetScannerProbeAngle(self._device, c_int(column), c_int(row), byref(result))
        CheckForError(error)
        return result.value
    
    def SwitchProbe(self, column : int, row : int):
        error = lib.EMS_SwitchProbe(self._device, c_int(column), c_int(row))
        CheckForError(error)

if __name__ == "__main__":
    print(lib)
    device = Device()
    print(device.GetDeviceType())
    print(device.GetScannerSize())
    print(device.GetScannerProbeGap())
    print(device.GetScannerProbeAngle(0, 0))
    print(device.SwitchProbe(4, 5))
    print(device.SwitchProbe(1, 1))