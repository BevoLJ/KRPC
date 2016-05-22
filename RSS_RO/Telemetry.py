import krpc
import math

conn = krpc.connect(name='Launch Program', address='127.0.0.1', rpc_port=50000, stream_port=50001)

Tar_orb = 175000
inc = 29


class Readings:
    def __init__(self):
        # \todo\ Clean unused streams
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
        # self.ksc_name = self.conn.add_stream(getattr, self.body(), 'name')

        self.alt = self.conn.add_stream(getattr, self.vessel.flight(), 'mean_altitude')
        self.apoapsis = self.conn.add_stream(getattr, self.vessel.orbit, 'apoapsis_altitude')
        self.periapsis = self.conn.add_stream(getattr, self.vessel.orbit, 'periapsis_altitude')
        self.R_ap = self.conn.add_stream(getattr, self.vessel.orbit, 'apoapsis')
        self.R_pe = self.conn.add_stream(getattr, self.vessel.orbit, 'periapsis')
        self.a = self.conn.add_stream(getattr, self.vessel.orbit, 'semi_major_axis')
        self.Radius = self.conn.add_stream(getattr, self.vessel.orbit, 'radius')
        self.orb_speed = self.conn.add_stream(getattr, self.vessel.orbit, 'speed')
        self.ETAap = self.conn.add_stream(getattr, self.vessel.orbit, 'time_to_apoapsis')
        self.ETApe = self.conn.add_stream(getattr, self.vessel.orbit, 'time_to_periapsis')
        # self.ecc = self.conn.add_stream(getattr, self.vessel.orbit, 'eccentricity')
        self.inc = self.conn.add_stream(getattr, self.vessel.orbit, 'inclination')
        # self.Node = self.conn.add_stream(getattr, self.vessel.orbit, 'longitude_of_ascending_node')
        # self.w = self.conn.add_stream(getattr, self.vessel.orbit, 'argument_of_periapsis')
        # self.period = self.conn.add_stream(getattr, self.vessel.orbit, 'period')

        self.mu = self.conn.add_stream(getattr, self.body(), 'gravitational_parameter')
        self.R_eq = self.conn.add_stream(getattr, self.body(), 'equatorial_radius')
        self.Rot_p = self.conn.add_stream(getattr, self.body(), 'rotational_period')
        self.Lat = self.conn.add_stream(getattr, self.vessel.flight(), 'latitude')
        # self.Lon = self.conn.add_stream(getattr, self.vessel.flight(), 'longitude')

        # self.srf_reference_frame = self.conn.add_stream(getattr, self.vessel, 'surface_reference_frame')
        # self.vessel_flight_srf = self.conn.add_stream(self.vessel.flight, self.srf_reference_frame())
        self.bdy_reference_frame = self.conn.add_stream(getattr, self.body(), 'reference_frame')
        self.vessel_flight_bdy = self.conn.add_stream(self.vessel.flight, self.bdy_reference_frame())

        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        #              V E S S E L               #
        #           T E L E M E T R Y            #
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

        self.name = self.conn.add_stream(getattr, self.vessel, 'name')
        self.thrust = self.conn.add_stream(getattr, self.vessel, 'thrust')
        self.specific_impulse = self.conn.add_stream(getattr, self.vessel, 'specific_impulse')
        self.mass = self.conn.add_stream(getattr, self.vessel, 'mass')
        self.vessel_speed = self.conn.add_stream(getattr, self.vessel_flight_bdy(), 'speed')
        self.vessel_velocity_vector = self.conn.add_stream(getattr, self.vessel_flight_bdy(), 'velocity')
        self.vessel_pitch = self.conn.add_stream(getattr, self.vessel.flight(), 'pitch')
        self.heading = self.conn.add_stream(getattr, self.vessel.flight(), 'heading')
        self.Q = self.conn.add_stream(getattr, self.vessel.flight(), 'dynamic_pressure')
        # self.heading_error = self.conn.add_stream(getattr, self.auto_pilot(), 'error')
        # self.roll = self.conn.add_stream(getattr, self.vessel.flight(), 'roll')
        # self.prograde = self.conn.add_stream(getattr, self.vessel.flight(), 'prograde')
        # self.atmospheric_D = self.conn.add_stream(getattr, self.vessel.flight(), 'atmosphere_density')
        # self.dyn_press = self.conn.add_stream(getattr, self.vessel.flight(), 'dynamic_pressure')
        # self.ang_att = self.conn.add_stream(getattr, self.vessel.flight(), 'angle_of_attack')
        # self.side_ang = self.conn.add_stream(getattr, self.vessel.flight(), 'sideslip_angle')
        # self.velocity = self.conn.add_stream(getattr, self.vessel.flight(), 'velocity')
        # self.direction = self.conn.add_stream(getattr, self.vessel.flight(), 'direction')
        # self.vessel_prograde = self.conn.add_stream(getattr, self.vessel_flight_bdy(), 'prograde')
        # self.surface_altitude = self.conn.add_stream(getattr, self.vessel.flight(), 'surface_altitude')
        # self.situation = self.conn.add_stream(getattr, self.vessel, 'situation')
        # self.met = self.conn.add_stream(getattr, self.vessel, 'met')

        self.t_radius = Tar_orb + self.Radius()


def v_ap():
    _v_ap = math.sqrt((2 * Readings().mu() * Readings().R_pe()) /
                      (Readings().R_ap() * (Readings().R_ap() + Readings().R_pe())))
    return _v_ap


def ap_v_dv():
    t_ap_v = math.sqrt((2 * Readings().mu() * Readings().R_pe()) /
                       (Readings().t_radius * (Readings().t_radius + Readings().R_pe())))
    t_ap_dv = t_ap_v - v_ap()
    return t_ap_dv


def twr():
    _twr = Readings().thrust() / ((Readings().mu() / ((Readings().alt() + Readings().R_eq()) ** 2)) * Readings().mass())
    return _twr


def circ_dv():
    _circ_v = math.sqrt(Readings().mu() / Readings().R_ap())
    _circ_dv = _circ_v - v_ap()
    return _circ_dv


# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#                 F O R                  #
#           D E B U G G I N G            #
# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

def list_modules(part):
    for p in part:
        mod = p.modules
        for m in mod:
            print(m.name)


def list_actions(part):
    for p in part:
        mod = p.modules
        print(" ")
        print("- A C T I O N S -")
        for m in mod:
            print("- " + m.name)
            # print(m.fields)
            act = m.actions
            for a in act:
                print("   " + a)
        print(" ")
        print("- F I E L D S -")
        for m in mod:
            print("- " + m.name)
            flds = m.fields
            for k, v in flds.items():
                print("   " + k, v)
