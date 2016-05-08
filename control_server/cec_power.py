import cec

ps4_dict = {"info": "35",
            "back": "0d",
            "select": "00",
            "delete": "10",
            "dvd_menu": "11",
            "up": "01",
            "down": "02",
            "left": "03",
            "right": "04",
            "root_menu": "09",
            "fast_forward": "49",
            "rewind": "48"
            }

cecconfig = cec.libcec_configuration()

cecconfig.strDeviceName   = "pyLibCec"
cecconfig.bActivateSource = 0
cecconfig.deviceTypes.Add(cec.CEC_DEVICE_TYPE_RECORDING_DEVICE)
cecconfig.clientVersion = cec.LIBCEC_VERSION_CURRENT

lib = cec.ICECAdapter.Create(cecconfig)
lib.Open("RPI")


def standby_device(index):
    lib.StandbyDevices(index)

def power_on_device(index):
    lib.PowerOnDevices(index)

def power_status(index):
    return 1 - lib.GetDevicePowerStatus(index)

def ps4_command(cmd):
    lib.Transmit(lib.CommandFromString("14:44:" + ps4_dict[cmd]))
