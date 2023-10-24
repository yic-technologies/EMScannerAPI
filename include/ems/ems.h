#ifdef __cplusplus
#define EMS_EXTERN extern "C"
#else
#define EMS_EXTERN
#endif

#ifdef EMS_EXPORT
#define EMS_DECLARE_EXPORT __declspec(dllexport)
#else
#define EMS_DECLARE_EXPORT __declspec(dllimport)
#endif

#define EMS_API EMS_EXTERN EMS_DECLARE_EXPORT

typedef struct EMS_Device	EMS_Device;
typedef unsigned int		EMS_Size;
typedef unsigned long long	EMS_SerialNumber;

enum EMS_Error {
	EMS_Success = 0,
	EMS_Error_NoDeviceFound,
	EMS_Error_NullPtrArgument,
	EMS_Error_CommunicationFailed,
	EMS_Error_NotImplemented,
	EMS_Error_CellOutOfRange
};

enum EMS_DeviceType {
	EMS_DeviceType_None = -1,
	EMS_DeviceType_EMS08 = 0,
	EMS_DeviceType_EMSR08 = 1,
};

//Connects a device if one exists. If no device is connected, there is no need to call EMS_Disconnect.
EMS_API EMS_Error		EMS_ConnectDevice(EMS_Device** device_ptr);
//You must call EMS_Disconnect for any connected device to reclaim any resources used.
EMS_API EMS_Error		EMS_DisconnectDevice(EMS_Device* device);
EMS_API EMS_Error		EMS_GetDeviceType(EMS_Device* device, EMS_DeviceType* device_type);
EMS_API EMS_Error		EMS_IsScannerAttached(EMS_Device* device, bool* value);
EMS_API EMS_Error		EMS_GetScannerSize(EMS_Device* device, int* columns, int* rows);
//Returns the distance between each probe column * 0.01mm
EMS_API EMS_Error		EMS_GetScannerProbeGap(EMS_Device* device, int* gap);
//Returns the angle of a scanner's internal probe.
//NOTE: The returned value is NOT the angle itself.
//0: Vertical, loop pointing 45 degrees
//1: Vertical, perpendicular to type 0
EMS_API EMS_Error		EMS_GetScannerProbeAngle(EMS_Device* device, int column, int row, int* angle);
EMS_API EMS_Error		EMS_SwitchProbe(EMS_Device* device, int column, int row);



