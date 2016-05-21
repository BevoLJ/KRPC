import math
import time
from Telemetry import Telemetry, TargetOrb

Tar_orb = 175000
inc = 29

Tar = TargetOrb(Tar_orb)
tel = Telemetry()
vessel = tel.vessel
control = tel.control
ap = tel.auto_pilot


def lift_off():
    control.sas = True
    control.rcs = False
    control.throttle = 1
    engine_actions(tel.cur_stage_engs, 'Activate Engine')
    while Telemetry().twr < 1:
        time.sleep(0.2)
    control.activate_next_stage()
    while tel.vessel_speed() < 80.0:
        time.sleep(0.2)


def gravity_turn():
    ap.engage()
    ap.set_pid_parameters(kp=1.0, ki=0.0, kd=0.0)
    while tel.vessel_speed() < 6000:
        if tel.Q() < 30:
            ap.target_pitch_and_heading(gravity_pitch(Tar), (azimuth_init(Tar) + 90))
        else:
            ap.reference_frame = vessel.surface_velocity_reference_frame
            ap.target_direction = (0, 1, 0)
        time.sleep(0.1)


def azimuth_init(tar):
    # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
    #         S E T   H E A D I N G          #
    # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

    _inc = inc

    if _inc > 0:
        node = "Ascending"
    else:
        node = "Descending"
        _inc = math.fabs(_inc)

    if (math.fabs(tel.Lat())) > _inc:
        _inc = math.fabs(tel.Lat())
    if (180 - math.fabs(tel.Lat())) < _inc:
        _inc = (180 - math.fabs(tel.Lat()))

    velocity_eq = ((2 * math.pi * tel.Radius()) / tel.Rot_p())

    inert_az = math.asin(max(min(math.cos(_inc / math.cos(tel.Lat())), 1), -1))
    _VXRot = tar.T_orb_V * math.sin(inert_az) - velocity_eq * math.cos(tel.Lat())
    _VYRot = tar.T_orb_V * math.cos(inert_az)

    _Az = math.fmod(math.atan2(_VXRot, _VYRot) + 360, 360)

    if node == "Ascending":
        az = _Az
    elif node == "Descending":
        if _Az <= 90:
            az = 180 - _Az
        elif _Az >= 270:
            az = 540 - _Az

    return az


def gravity_pitch(tar):
    # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
    #      G R A V I T Y   P I T C H         #
    # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

    tar = tar

    if tel.R_ap() < tar.Tar_R:
        # pitch = (85 - (1.2 * math.sqrt(tel.orb_speed() - 70))) - (tar.T_ap_dV / 4.5)
        pitch = (87 - (1.2 * math.sqrt(tel.vessel_speed()))) - (tar.T_ap_dV / 4.5)
    else:
        pitch = tar.T_ap_dV / 4.5

    return pitch


def engine_actions(eng_to_activate, action):
    # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
    #   E N G   M o d R F   A C T I O N S    #
    # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

    for eng in tel.engines:
        if eng.name == eng_to_activate[0]:
            mods = eng.modules
            for mod in mods:
                if mod.name == "ModuleEnginesRF":
                    m = mod
                    m.set_action(action, True)
