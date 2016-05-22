import math
import time

from Telemetry import Readings, twr, ap_v_dv, circ_dv

Tar_orb = 175000
inc = 29

tel = Readings()
KSC = tel.KSC
vessel = KSC.active_vessel
control = vessel.control
ap = vessel.auto_pilot


class GravityTurn:

    @staticmethod
    def lift_off():
        control.sas = True
        control.rcs = False
        control.throttle = 1
        engine_actions(cur_stage_engs(), 'Activate Engine')
        while twr() < 1:
            time.sleep(0.2)
        control.activate_next_stage()
        while tel.vessel_speed() < 80.0:
            time.sleep(0.2)

    @staticmethod
    def gravity_start():
        control.sas = False
        ap.engage()
        ap.target_pitch_and_heading(gravity_pitch(), (azimuth_init() + 90))
        time.sleep(0.3)
        while tel.Q() < 30:
            ap.target_pitch_and_heading(gravity_pitch(), (azimuth_init() + 90))
            time.sleep(0.2)

    @staticmethod
    def max_q():
        # \todo\ Setup P.I.D. to not use stock SAS
        ap.disengage()
        control.sas = True
        time.sleep(0.2)
        control.sas_mode = KSC.SASMode.prograde
        while tel.Q() > 30:
            time.sleep(0.5)

    @staticmethod
    def gravity_finish():
        control.sas = False
        ap.engage()
        ap.target_pitch_and_heading(gravity_pitch(), (azimuth_init() + 90))
        while (engine_status(cur_stage_engs(), "ModuleEnginesRF", "Status")) != "Flame-Out!":
            ap.target_pitch_and_heading(gravity_pitch(), (azimuth_init() + 90))
            time.sleep(0.3)
        ap.disengage()
        control.sas = True


class OrbitalInsertion:

    @staticmethod
    def start_insertion():
        ap.engage()
        print("Starting insertion")
        ap.target_pitch_and_heading(-1*ap_v_dv()/5, (azimuth_init() + 90))
        time.sleep(1)
        while tel.ETAap() > 120:
            ap.target_pitch_and_heading(-1*ap_v_dv()/5, (azimuth_init() + 90))
            time.sleep(1)
        ap.disengage()
        ullage()

    @staticmethod
    def orb_insertion():
        ap.engage()
        print("Orbital insertion")
        while tel.orb_speed() < 7000 and circ_dv() > 200:
            ap.target_pitch_and_heading(-1*ap_v_dv()/5, (azimuth_init() + 90))
            time.sleep(1)
        while tel.orb_speed() < 7700 and circ_dv() > 10:
            ap.target_pitch_and_heading(-1*ap_v_dv()/5, (azimuth_init() + 90))
            time.sleep(.1)


def azimuth_init():
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
    t_orb_v = math.sqrt(Readings().mu() / (Tar_orb + Readings().Radius()))

    inert_az = math.asin(max(min(math.cos(_inc / math.cos(tel.Lat())), 1), -1))
    _VXRot = t_orb_v * math.sin(inert_az) - velocity_eq * math.cos(tel.Lat())
    _VYRot = t_orb_v * math.cos(inert_az)

    _Az = math.fmod(math.atan2(_VXRot, _VYRot) + 360, 360)

    az = _Az

    if node == "Descending":
        if _Az <= 90:
            az = 180 - _Az
        elif _Az >= 270:
            az = 540 - _Az

    return az


def gravity_pitch():
    # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
    #      G R A V I T Y   P I T C H         #
    # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

    if tel.R_ap() < tel.t_radius:
        pitch = (84 - (1.25 * math.sqrt(tel.vessel.orbit.speed))) - (ap_v_dv() / 4.5)
    else:
        pitch = ap_v_dv() / 5

    return pitch

    # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
    #   E N G   M o d R F   A C T I O N S    #
    # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#


def eng_list_tuples():
    list_eng_tuples = []
    engines = Readings().parts.with_module("ModuleEnginesRF")
    for part in engines:
        eng_tup = (part.stage, part.name)
        list_eng_tuples.append(eng_tup)
    list_eng_tuples.sort()

    return list_eng_tuples


def cur_stage_engs():
    stage_num_set = set()
    englist = []
    list_eng_tuples = eng_list_tuples()
    engines = Readings().parts.with_module("ModuleEnginesRF")
    for part in engines:
        stage_num_set.update(str(part.stage))
    num_stages = len(stage_num_set)

    next_stage_engs_list = [item for item in list_eng_tuples if item[0] == num_stages]

    while len(next_stage_engs_list) > 0:
        _eng = next_stage_engs_list.pop()
        englist.append(_eng[1])

    return englist


def cur_stage():
    engines = tel.parts.with_module("ModuleEnginesRF")
    _cur_stage_engs = cur_stage_engs()
    for _eng in engines:
        if _eng.name == _cur_stage_engs[0]:
            return _eng.stage


def engine_actions(eng_to_activate, action):
    engines = Readings().parts.with_module("ModuleEnginesRF")
    for _eng in engines:
        if _eng.name == eng_to_activate[0]:
            mods = _eng.modules
            for mod in mods:
                if mod.name == "ModuleEnginesRF":
                    m = mod
                    m.set_action(action, True)


def engine_status(eng_to_monitor, mod_monitored, state):
    engines = Readings().parts.with_module("ModuleEnginesRF")
    for _eng in engines:
        if _eng.name == eng_to_monitor[0]:
            mods = _eng.modules
            for mod in mods:
                if mod.name == mod_monitored:
                    m = mod
                    return m.get_field(state)


def solid_engs(stage):
    engines = Readings().parts.with_module("ModuleEnginesRF")
    stage = stage
    solid = []
    for _eng in engines:
        if not _eng.engine.can_restart:
            if _eng.stage == stage:
                solid.append(_eng)
    return solid


def liquid_engs(stage):
    engines = Readings().parts.with_module("ModuleEnginesRF")
    stage = stage
    liquid = []
    for _eng in engines:
        if _eng.engine.can_restart:
            if _eng.stage == stage:
                liquid.append(_eng)
    return liquid


def prop_status():
    _liq_engs = liquid_engs(cur_stage())
    for eng in _liq_engs:
        mod = eng.modules
        for m in mod:
            if m.name == "ModuleEnginesRF":
                prop = m.get_field("Propellant")
                return prop


def ullage():
    control.throttle = 0
    engine_actions(liquid_engs(cur_stage()), 'Shutdown Engine')
    time.sleep(1.5)
    control.activate_next_stage()
    time.sleep(1)
    control.throttle = 1
    while prop_status() == "Very Unstable":
        time.sleep(0.2)
    time.sleep(1)
    engine_actions(liquid_engs(cur_stage()), 'Activate Engine')
