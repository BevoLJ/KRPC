import krpc
import math

conn = krpc.connect(name='Launch Program', address='127.0.0.1', rpc_port=50000, stream_port=50001)


class Telemetry:
    def __init__(self):
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        #       C O M M U N I C A T I O N        #
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

        self.conn = conn
        self.KSC = self.conn.space_center
        self.vessel = self.KSC.active_vessel
        self.parts = self.vessel.parts
        self.control = self.vessel.control
        self.auto_pilot = self.vessel.auto_pilot

        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        #             O R B I T A L              #
        #           T E L E M E T R Y            #
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

        self.ut = self.conn.add_stream(getattr, self.conn.space_center, "ut")
        self.body = self.conn.add_stream(getattr, self.vessel.orbit, 'body')
        self.ksc_name = self.conn.add_stream(getattr, self.body(), 'name')

        self.alt = self.conn.add_stream(getattr, self.vessel.flight(), 'mean_altitude')
        self.apoapsis = self.conn.add_stream(getattr, self.vessel.orbit, 'apoapsis_altitude')
        self.periapsis = self.conn.add_stream(getattr, self.vessel.orbit, 'periapsis_altitude')
        self.R_ap = self.conn.add_stream(getattr, self.vessel.orbit, 'apoapsis')
        self.R_pe = self.conn.add_stream(getattr, self.vessel.orbit, 'periapsis')
        self.a = self.conn.add_stream(getattr, self.vessel.orbit, 'semi_major_axis')
        self.Radius = self.conn.add_stream(getattr, self.vessel.orbit, 'radius')
        self.orb_speed = self.conn.add_stream(getattr, self.vessel.orbit, 'speed')
        # self.period = self.conn.add_stream(getattr, self.vessel.orbit, 'period')
        self.ETAap = self.conn.add_stream(getattr, self.vessel.orbit, 'time_to_apoapsis')
        self.ETApe = self.conn.add_stream(getattr, self.vessel.orbit, 'time_to_periapsis')
        self.ecc = self.conn.add_stream(getattr, self.vessel.orbit, 'eccentricity')
        self.inc = self.conn.add_stream(getattr, self.vessel.orbit, 'inclination')
        # self.Node = self.conn.add_stream(getattr, self.vessel.orbit, 'longitude_of_ascending_node')
        # self.w = self.conn.add_stream(getattr, self.vessel.orbit, 'argument_of_periapsis')

        self.mu = self.conn.add_stream(getattr, self.body(), 'gravitational_parameter')
        self.R_eq = self.conn.add_stream(getattr, self.body(), 'equatorial_radius')
        self.Rot_p = self.conn.add_stream(getattr, self.body(), 'rotational_period')
        self.Lat = self.conn.add_stream(getattr, self.vessel.flight(), 'latitude')
        # self.Lon = self.conn.add_stream(getattr, self.vessel.flight(), 'longitude')

        self.srf_reference_frame = self.conn.add_stream(getattr, self.vessel, 'surface_reference_frame')
        self.vessel_flight_srf = self.conn.add_stream(self.vessel.flight, self.srf_reference_frame())
        self.bdy_reference_frame = self.conn.add_stream(getattr, self.body(), 'reference_frame')
        self.vessel_flight_bdy = self.conn.add_stream(self.vessel.flight, self.bdy_reference_frame())

        self.V_ap = math.sqrt((2 * self.mu() * self.R_pe()) / (self.R_ap() * (self.R_ap() + self.R_pe())))
        self.V_pe = math.sqrt((2 * self.mu() * self.R_ap()) / (self.R_pe() * (self.R_ap() + self.R_pe())))
        self.circ_V = math.sqrt(self.mu() / self.R_ap())
        self.circ_dV = self.circ_V - self.V_ap

        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        #              V E S S E L               #
        #           T E L E M E T R Y            #
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

        self.name = self.conn.add_stream(getattr, self.vessel, 'name')
        # self.situation = self.conn.add_stream(getattr, self.vessel, 'situation')
        self.thrust = self.conn.add_stream(getattr, self.vessel, 'thrust')
        self.specific_impulse = self.conn.add_stream(getattr, self.vessel, 'specific_impulse')
        self.mass = self.conn.add_stream(getattr, self.vessel, 'mass')
        # self.surface_altitude = self.conn.add_stream(getattr, self.vessel.flight(), 'surface_altitude')
        self.vessel_speed = self.conn.add_stream(getattr, self.vessel_flight_bdy(), 'speed')
        # self.vessel_prograde = self.conn.add_stream(getattr, self.vessel_flight_bdy(), 'prograde')
        self.vessel_velocity_vector = self.conn.add_stream(getattr, self.vessel_flight_bdy(), 'velocity')
        # self.velocity = self.conn.add_stream(getattr, self.vessel.flight(), 'velocity')
        # self.direction = self.conn.add_stream(getattr, self.vessel.flight(), 'direction')
        self.vessel_pitch = self.conn.add_stream(getattr, self.vessel.flight(), 'pitch')
        self.heading = self.conn.add_stream(getattr, self.vessel.flight(), 'heading')
        # self.roll = self.conn.add_stream(getattr, self.vessel.flight(), 'roll')
        # self.prograde = self.conn.add_stream(getattr, self.vessel.flight(), 'prograde')
        # self.atmospheric_D = self.conn.add_stream(getattr, self.vessel.flight(), 'atmosphere_density')
        # self.dyn_press = self.conn.add_stream(getattr, self.vessel.flight(), 'dynamic_pressure')
        # self.ang_att = self.conn.add_stream(getattr, self.vessel.flight(), 'angle_of_attack')
        # self.side_ang = self.conn.add_stream(getattr, self.vessel.flight(), 'sideslip_angle')
        self.Q = self.conn.add_stream(getattr, self.vessel.flight(), 'dynamic_pressure')
        # self.heading_error = self.conn.add_stream(getattr, self.auto_pilot(), 'error')

        self.twr = self.thrust() / ((self.mu() / ((self.alt() + self.R_eq()) ** 2)) * self.mass())

        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        #               P A R T S                #
        #           T E L E M E T R Y            #
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

        self.engines = self.parts.with_module("ModuleEnginesRF")
        self.list_eng_tuples = eng_list_tuples(self.engines)
        self.cur_stage_engs = cur_stage_engs(self.engines)


class TargetOrb:
    def __init__(self, tar_orb):
        self.Tar_orb = tar_orb
        self.tel = Telemetry()

        self.Tar_R = self.Tar_orb + self.tel.Radius()
        self.T_V_ap = math.sqrt((2 * self.tel.mu() * self.tel.R_pe()) /
                                (self.Tar_R * (self.tel.R_ap() + self.tel.R_pe())))

        self.T_ap_dV = self.T_V_ap - self.tel.V_ap
        self.T_orb_V = math.sqrt(self.tel.mu() / self.Tar_R)


def eng_list_tuples(engines):
    list_eng_tuples = []

    for part in engines:
        eng_tup = (part.stage, part.name)
        list_eng_tuples.append(eng_tup)
    list_eng_tuples.sort()

    return list_eng_tuples


def cur_stage_engs(engines):
    stage_num_set = set()
    englist = []
    list_eng_tuples = eng_list_tuples(engines)

    for part in engines:
        stage_num_set.update(str(part.stage))
    num_stages = len(stage_num_set)

    next_stage_engs_list = [item for item in list_eng_tuples if item[0] == num_stages]

    while len(next_stage_engs_list) > 0:
        eng = next_stage_engs_list.pop()
        englist.append(eng[1])

    return englist
