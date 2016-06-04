import krpc
import numpy
from numba import jit


class Operations:
    conn = krpc.connect(name='name')

    KSC = conn.space_center
    vessel = KSC.active_vessel
    ap = vessel.auto_pilot
    control = vessel.control
    parts = vessel.parts
    engines = parts.with_module("ModuleEnginesRF")

    def __init__(self):
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        #       C O M M U N I C A T I O N        #
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

        self.target_orbit_alt = 225000
        self.target_orbit_inc = 28

        self.body = self.vessel.orbit.body
        self.radius_eq = self.vessel.orbit.body.equatorial_radius
        self.gravitational_parameter = self.vessel.orbit.body.gravitational_parameter

        self.ut = self.conn.add_stream(getattr, self.conn.space_center, "ut")
        self.ETA_ap = self.conn.add_stream(getattr, self.vessel.orbit, 'time_to_apoapsis')
        self.apoapsis_radius = self.conn.add_stream(getattr, self.vessel.orbit, 'apoapsis')
        self.periapsis_radius = self.conn.add_stream(getattr, self.vessel.orbit, 'periapsis')
        self.apoapsis_altitude = self.conn.add_stream(getattr, self.vessel.orbit, 'apoapsis_altitude')
        self.periapsis_altitude = self.conn.add_stream(getattr, self.vessel.orbit, 'periapsis_altitude')
        self.Q = self.conn.add_stream(getattr, self.vessel.flight(), 'dynamic_pressure')
        self.thrust = self.conn.add_stream(getattr, self.vessel, 'thrust')
        self.max_thrust = self.conn.add_stream(getattr, self.vessel, 'max_thrust')
        self.specific_impulse = self.conn.add_stream(getattr, self.vessel, 'vacuum_specific_impulse')
        self.mass = self.conn.add_stream(getattr, self.vessel, 'mass')
        self.altitude = self.conn.add_stream(getattr, self.vessel.flight(), 'mean_altitude')
        self.latitude = self.conn.add_stream(getattr, self.vessel.flight(), 'latitude')
        self.rotational_period = self.conn.add_stream(getattr, self.body, 'rotational_period')
        # vessel_pitch = conn.add_stream(getattr, vessel.flight(), 'pitch')
        # heading = conn.add_stream(getattr, vessel.flight(), 'heading')
        # self.vessel_velocity_vector = self.conn.add_stream(getattr, self.vessel_flight_bdy(), 'velocity')
        # self.vessel_pitch = self.conn.add_stream(getattr, self.vessel.flight(), 'pitch')
        # self.heading = self.conn.add_stream(getattr, self.vessel.flight(), 'heading')

        self.bdy_reference_frame = self.conn.add_stream(getattr, self.body, 'reference_frame')
        self.vessel_flight_bdy = self.conn.add_stream(self.vessel.flight, self.bdy_reference_frame())
        self.vessel_speed = self.conn.add_stream(getattr, self.vessel_flight_bdy(), 'speed')
        # altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')

        self.spin_solids = "SnubOtron"

        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        #         S E T   H E A D I N G          #
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

    def pitch(self):
        _R_ap = self.apoapsis_radius()
        _R_pe = self.periapsis_radius()
        _R_eq = self.radius_eq
        _speed = self.vessel_speed()
        _µ = self.gravitational_parameter
        _to = float(self.target_orbit_alt)

        @jit(nopython=True)
        def pitch_calcs():
            _t_radius = _to + _R_eq
            _v_ap = numpy.sqrt((2 * _µ * _R_pe) / (_R_ap * (_R_ap + _R_pe)))
            _t_ap_v = numpy.sqrt((2 * _µ * _R_pe) / (_t_radius * (_t_radius + _R_pe)))
            _t_ap_dv = _t_ap_v - _v_ap
            _p_ap_dv = _t_ap_dv / 4
            _pitch = (90 - (1.22 * numpy.sqrt(_speed))) - (_p_ap_dv / 5)
            return _pitch

        return pitch_calcs()

    # /todo/ BROKEN! Need to fix
    def azimuth_init(self):

        _R_eq = self.radius_eq
        _inc = float(self.target_orbit_inc)
        _lat = self.latitude()
        _to = float(self.target_orbit_alt)
        _µ = self.gravitational_parameter
        _Rot_p = self.rotational_period()
        node = "Ascending"

        if _inc < 0:
            node = "Descending"
            _inc = numpy.fabs(_inc)

        if (numpy.fabs(_lat)) > _inc:
            _inc = numpy.fabs(_lat)
        if (180 - numpy.fabs(_lat)) < _inc:
            _inc = (180 - numpy.fabs(_lat))

        print("_inc: " + str(_inc))

        @jit(nopython=True)
        def Az_calcs():
            velocity_eq = (2 * numpy.pi * _R_eq) / _Rot_p
            t_orb_v = numpy.sqrt(_µ / (_to + _R_eq))

            inert_az = numpy.arcsin(max(min(numpy.cos(_inc / numpy.cos(_lat)), 1), -1))
            _VXRot = t_orb_v * numpy.sin(inert_az) - velocity_eq * numpy.cos(_lat)
            _VYRot = t_orb_v * numpy.cos(inert_az)

            return numpy.fmod(numpy.arctan2(_VXRot, _VYRot) + 360, 360)

        _az = Az_calcs()
        print("_az: " + str(_az))

        # This is wrong.  Should return just _az
        # need to figure out why it always returns 0
        if node == "Ascending":
            return _az + 90  # I should not need the +90 here

        if node == "Descending":
            if _az <= 90:
                return 180 - _az
            elif _az >= 270:
                return 540 - _az

        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        #           V E L O C I T Y              #
        #         A n d   D e l t a  V           #
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

    def twr(self):
        _thrust = self.thrust()
        _mass = self.mass()
        _alt = self.altitude()
        _µ = self.gravitational_parameter

        _twr = (_thrust / ((_µ / ((_alt + self.radius_eq) ** 2)) * _mass))
        return _twr

    def stage_dv(self):
        _engine = self.get_active_engine()
        _isp = max(_engine.engine.specific_impulse, 1)
        # if _isp == 1:
        #     _isp = self.next_stage_isp()
        #     _engine = self._example_(self.next_stage_engs())
        _prop_used = _engine.engine.propellants
        _stage = _engine.decouple_stage
        _parts = self.vessel.parts.in_decouple_stage(_stage)
        _total_fuel_mass = 0
        _mass = self.mass()
        for _p in _parts:
            if _p.resources.names == _prop_used:
                _dry_mass = _p.dry_mass
                _wet_mass = _p.mass
                _total_fuel_mass = _total_fuel_mass + (_wet_mass - _dry_mass)

        @jit(nopython=True)
        def dv_calcs():
            _ve = _isp * 9.8
            _dv = _ve * numpy.log(_mass / (_mass - _total_fuel_mass))
            return _dv

        return dv_calcs()

    def apoapsis_speed(self):
        _R_ap = self.apoapsis_radius()
        _R_pe = self.periapsis_radius()
        _µ = self.gravitational_parameter

        @jit(nopython=True)
        def ap_dv_calc():
            _v_ap = numpy.sqrt((2 * _µ * _R_pe) / (_R_ap * (_R_ap + _R_pe)))
            return _v_ap

        return ap_dv_calc()

    def target_apoapsis_speed_dv(self):
        _R_pe = self.periapsis_radius()
        _R_eq = self.radius_eq
        _µ = self.gravitational_parameter
        _to = float(self.target_orbit_alt)
        _v_ap = self.apoapsis_speed()

        @jit(nopython=True)
        def ap_dv_calc():
            _t_radius = _to + _R_eq
            _t_ap_v = numpy.sqrt((2 * _µ * _R_pe) / (_t_radius * (_t_radius + _R_pe)))
            _t_ap_dv = _v_ap - _t_ap_v
            return _t_ap_dv

        return ap_dv_calc()

    def circular_speed(self):
        _R_ap = self.apoapsis_radius()
        _µ = self.gravitational_parameter

        @jit(nopython=True)
        def circular_speed_calc():
            _circ_v = numpy.sqrt(_µ / _R_ap)
            return _circ_v

        return circular_speed_calc()

    def circ_dv(self):
        _circ_v = self.circular_speed()
        _v_ap = self.apoapsis_speed()

        @jit(nopython=True)
        def circ_dv_calc():
            _circ_dv_calc = _circ_v - _v_ap
            return _circ_dv_calc

        return circ_dv_calc()

    def maneuver_burn_time(self, _maneuver_dv):
        _isp = max(self.specific_impulse(), 1)
        _thrust = max(1, self.max_thrust() * 1000)
        # if _isp == 1:
        #     _isp = self.next_stage_isp()
        #     _thrust = self.next_stage_thrust()
        _mass = self.mass() * 1000
        _dv = _maneuver_dv

        @jit(nopython=True)
        def burn_time_calc():
            _mdot = _thrust / 9.82 / _isp
            _burn_time = _mass * (1 - numpy.e ** (-_dv / _isp / 9.82)) / _mdot
            return _burn_time

        return burn_time_calc()

    @staticmethod
    @jit(nopython=True)
    def time_to_burn(_node_eta, _burn_time):
        return _node_eta - (_burn_time / 2)

    # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
    #   E N G   M o d R F   A C T I O N S    #
    # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

    def active_next_stage_engines(self):
        _stage = self.get_active_engine().decouple_stage
        for _eng in self.engines:
            if _eng.decouple_stage == (_stage - 1): _eng.engine.active = True

    def eng_status(self):
        _mod = self.get_active_engine().modules
        for _m in _mod:
            if _m.name == "ModuleEnginesRF":
                return _m.get_field("Status")

    def get_active_engine(self):
        for _eng in self.engines:
            if _eng.engine.active: return _eng

    def eng_list_tuples(self):
        _list_eng_tuples = []
        for _part in self.engines:
            _eng_tup = (_part.stage, _part)
            _list_eng_tuples.append(_eng_tup)
        _list_eng_tuples.sort()

        return _list_eng_tuples

    def next_stage_engs(self):
        _stage_num_set = set()
        _englist = []
        _list_eng_tuples = self.eng_list_tuples
        for _part in self.engines:
            _stage_num_set.update(str(_part.stage))
        _num_stages = len(_stage_num_set)

        _next_stage_engs_list = [item for item in _list_eng_tuples if item[0] == _num_stages - 1]

        while len(_next_stage_engs_list) > 0:
            _eng = _next_stage_engs_list.pop()
            _englist.append(_eng[1])

        return _englist

    def next_stage_isp(self):
        for _en in self.next_stage_engs():
            return _en.engine.vacuum_specific_impulse

    def next_stage_thrust(self):
        for _en in self.next_stage_engs():
            return _en.engine.max_thrust * 1000

    @staticmethod
    def _example_(_list):
        for item in _list:
            return item
