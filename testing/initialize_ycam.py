import pylablib as pll
from pylablib.devices import Andor

TEMPERATURE_SETPOINT = -50
VS_SPEED = 1.92
HS_SPEED = 2
PREAMP_MODE = 1  # set preamp gain = 2.
pll.par["devices/dlls/andor_sdk2"] = "C:/Program Files/Andor SOLIS"
print(str(Andor.get_cameras_number_SDK2()) + ' camera(s) found.')

try:
    cam = Andor.AndorSDK2Camera(idx=0, temperature=TEMPERATURE_SETPOINT)
    cam.set_cooler(on=True)
    cam.set_vsspeed(VS_SPEED)
    cam.set_amp_mode(preamp=PREAMP_MODE, hsspeed=HS_SPEED)
    # cam.setup_kinetic_mode(3, num_acc=3, num_prescan=1)
    cam.set_exposure(1e-3)
    cam.set_trigger_mode('int')
    cam.setup_shutter("open")
except Exception as e:
    cam.close()
    print(e)