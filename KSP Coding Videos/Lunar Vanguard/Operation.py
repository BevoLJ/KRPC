import krpc
import math
import time
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

        self.target_orbit = 225000

        self.body = self.vessel.orbit.body
        self.radius_eq = self.vessel.orbit.body.equatorial_radius
        self.mu = self.vessel.orbit.body.gravitational_parameter

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

    def pitch(self):
        _R_ap = self.apoapsis_radius()
        _R_pe = self.periapsis_radius()
        _R_eq = self.radius_eq
        _speed = self.vessel_speed()
        _mu = self.mu
        _to = float(self.target_orbit)

        @jit(nopython=True)
        def pitch_calcs():
            _t_radius = _to + _R_eq
            _v_ap = math.sqrt((2 * _mu * _R_pe) / (_R_ap * (_R_ap + _R_pe)))
            _t_ap_v = math.sqrt((2 * _mu * _R_pe) / (_t_radius * (_t_radius + _R_pe)))
            _t_ap_dv = _t_ap_v - _v_ap
            _p_ap_dv = _t_ap_dv / 4
            _pitch = (90 - (1.22 * math.sqrt(_speed))) + (_p_ap_dv / 5)
            return _pitch

        return pitch_calcs()

    def twr(self):
        _thrust = self.thrust()
        _mass = self.mass()
        _alt = self.altitude()
        _mu = self.mu

        _twr = (_thrust / ((_mu / ((_alt + self.radius_eq) ** 2)) * _mass))
        return _twr

    def stage_deltav(self):
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
            _delta_v = _ve * math.log(_mass / (_mass - _total_fuel_mass))
            return _delta_v

        return dv_calcs()

    def apoapsis_speed(self):
        _R_ap = self.apoapsis_radius()
        _R_pe = self.periapsis_radius()
        _mu = self.mu

        @jit(nopython=True)
        def ap_dv_calc():
            _v_ap = math.sqrt((2 * _mu * _R_pe) / (_R_ap * (_R_ap + _R_pe)))
            return _v_ap

        return ap_dv_calc()

    def target_apoapsis_speed_dv(self):
        _R_pe = self.periapsis_radius()
        _R_eq = self.radius_eq
        _mu = self.mu
        _to = float(self.target_orbit)
        _v_ap = self.apoapsis_speed()

        @jit(nopython=True)
        def ap_dv_calc():
            _t_radius = _to + _R_eq
            _t_ap_v = math.sqrt((2 * _mu * _R_pe) / (_t_radius * (_t_radius + _R_pe)))
            _t_ap_dv = _t_ap_v - _v_ap
            return _t_ap_dv

        return ap_dv_calc()

    def circular_speed(self):
        _R_ap = self.apoapsis_radius()
        _mu = self.mu

        @jit(nopython=True)
        def circular_speed_calc():
            _circ_v = math.sqrt(_mu / _R_ap)
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

    def maneuver_burn_time(self, _maneuver_deltav):
        _isp = max(self.specific_impulse(), 1)
        _thrust = max(1, self.max_thrust() * 1000)
        # if _isp == 1:
        #     _isp = self.next_stage_isp()
        #     _thrust = self.next_stage_thrust()
        _mass = self.mass() * 1000
        _dv = _maneuver_deltav

        @jit(nopython=True)
        def burn_time_calc():
            _burn_time = 9.82 * _mass * _isp * (1 - math.e ** (-_dv / (9.82 * _isp))) / _thrust
            return _burn_time

        return burn_time_calc()

    @staticmethod
    @jit(nopython=True)
    def time_to_burn(_node_eta, _burn_time):
        return _node_eta - (_burn_time / 2)

    def launch_ui(self):
        _mode = "Pre-Flight Checks"
        _screen_size = self.conn.ui.rect_transform.size
        _panel = self.conn.ui.add_panel()
        _rect = _panel.rect_transform
        _rect.size = (200, 100)
        _rect.position = (400 - (_screen_size[0] / 2), 100)
        # Testing ui.messages
        self.conn.ui.message("Launch Mode: " + _mode, 5.0, self.conn.ui.MessagePosition.top_center)

        _text_1 = _panel.add_text("Enter Target Orbit in Km")
        _text_1.rect_transform.position = (5, 30)
        _text_1.size = 14

        _target_orbit = _panel.add_input_field()
        _target_orbit.rect_transform.position = (0, 10)
        _launch_button = _panel.add_button("Launch")
        _launch_button.rect_transform.position = (0, -20)

        _button_clicked = self.conn.add_stream(getattr, _launch_button, 'clicked')

        while _mode == "Pre-Flight Checks":
            if _button_clicked():
                self.target_orbit = (float(_target_orbit.value) * 1000)
                # \todo\ replace "Cruise" with "Launch" when done testing.
                _mode = "Launch"
                _button_clicked.clicked = False
            time.sleep(0.4)

        self.control.activate_next_stage()
        _panel.remove()
        return _mode

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
