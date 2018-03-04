import sys
import os
from machinekit import hal
from machinekit import rtapi as rt
from machinekit import config as c
if sys.version_info >= (3, 0):
    import configparser
else:
    import ConfigParser as configparser

_MAX_AXES = 9


def get_pin(name):
    if name in hal.pins:
        return hal.pins[name]
    else:
        return None


c.load_ini('hardware.ini')

rt.loadrt('hal_bb_gpio', output_pins='826,827,923,926,930', input_pins='807,810,814,817,818,819,912,914,915,916,917,918,924,941')
rt.loadrt(c.find('PRUCONF', 'DRIVER'), 'prucode=%s/%s' % (c.Config().EMC2_RTLIB_DIR, c.find('PRUCONF', 'PRUBIN')),
          pru=1, num_stepgens=6, num_pwmgens=1, halname='hpg')

# axis_enable_signal = hal.Signal('emcmot.00.enable', hal.HAL_BIT)
# hal.Pin('hpg.stepgen.00.enable').link(axis_enable_signal)
# axis_enable_signal.set(True)
# pos_cmd_signal = hal.Signal('emcmot.00.pos-cmd', hal.HAL_FLOAT)
# hal.Pin('hpg.stepgen.00.position-cmd').link(pos_cmd_signal)
# pos_fb_signal = hal.Signal('emcmot.00.pos-fb', hal.HAL_FLOAT)
# hal.Pin('hpg.stepgen.00.position-fb').link(pos_fb_signal)

hal.Pin('hpg.stepgen.00.dirsetup').set(c.find('AXIS_0', 'DIRSETUP'))
hal.Pin('hpg.stepgen.00.dirhold').set(c.find('AXIS_0', 'DIRHOLD'))

hal.Pin('hpg.stepgen.00.steplen').set(c.find('AXIS_0', 'STEPLEN'))
hal.Pin('hpg.stepgen.00.stepspace').set(c.find('AXIS_0', 'STEPSPACE'))

hal.Pin('hpg.stepgen.00.position-scale').set(c.find('AXIS_0', 'SCALE'))

hal.Pin('hpg.stepgen.00.maxvel').set(c.find('AXIS_0', 'STEPGEN_MAX_VEL'))
hal.Pin('hpg.stepgen.00.maxaccel').set(c.find('AXIS_0', 'STEPGEN_MAX_ACC'))
hal.Pin('hpg.stepgen.00.minvel').set(c.find('AXIS_0', 'STEPGEN_MIN_VEL'))

#sets XStep      P8.12
hal.Pin('hpg.stepgen.00.steppin').set(812)
#sets XDir       P8.11
hal.Pin('hpg.stepgen.00.dirpin').set(811)

servo_thread = 'servo_thread'
rt.newthread(servo_thread, c.find('TASK', 'CYCLE_TIME') * 1e9, fp=True)

hal.addf('hpg.capture-position', servo_thread)
hal.addf('bb_gpio.read', servo_thread)
# TODO: HAL comps

rcomp = hal.RemoteComponent('command-interface', timer=100)
for i in range(_MAX_AXES):
    rcomp.newpin('joint%i.position-cmd' % i, hal.HAL_FLOAT, hal.HAL_OUT)
    rcomp.newpin('joint%i.position-fb' % i, hal.HAL_FLOAT, hal.HAL_IN)
    rcomp.newpin('joint%i.enable' % i, hal.HAL_BIT, hal.HAL_IO)
    rcomp.newpin('joint%i.position-min' % i, hal.HAL_FLOAT, hal.HAL_IO)
    rcomp.newpin('joint%i.position-max' % i, hal.HAL_FLOAT, hal.HAL_IO)
rcomp.ready()

for i in range(_MAX_AXES):
    pin = get_pin('hpg.stepgen.%02i.position-cmd' % i)
    if pin:
        rcomp.pin('joint%i.position-cmd' % i).link(pin)
    pin = get_pin('hpg.stepgen.%02i.position-fb' % i)
    if pin:
        pin.link(rcomp.pin('joint%i.position-fb' % i))
    pin = get_pin('hpg.stepgen.%02i.enable' % i)
    if pin:
        rcomp.pin('joint%i.enable' % i).link(pin)
    rcomp.pin('joint%i.position-max' % i).set(80)

hal.addf('hpg.update', servo_thread)
hal.addf('bb_gpio.write', servo_thread)

hal.start_threads()

# start haltalk server after everything is initialized
# else binding the remote components on the UI might fail
hal.loadusr('haltalk')
