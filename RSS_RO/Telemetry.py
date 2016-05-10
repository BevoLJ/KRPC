import krpc, math

class Orb_info:
    def __init__(self, setup):

        self.conn = setup.conn
        self.vessel = setup.vessel
        self.KSC = setup.KSC

        self.ut = self.conn.add_stream(getattr, self.conn.space_center, "ut")
        self.body = self.conn.add_stream(getattr, self.vessel.orbit, 'body')
        self.ksc_name = self.conn.add_stream(getattr, self.body(), 'name')

        self.alt = self.conn.add_stream(getattr, self.vessel.flight(), 'mean_altitude')
        self.apoaps = self.conn.add_stream(getattr, self.vessel.orbit, 'apoapsis_altitude')
        self.periaps = self.conn.add_stream(getattr, self.vessel.orbit, 'periapsis_altitude')
        self.R_ap = self.conn.add_stream(getattr, self.vessel.orbit, 'apoapsis')
        self.R_pe = self.conn.add_stream(getattr, self.vessel.orbit, 'periapsis')
        self.a = self.conn.add_stream(getattr, self.vessel.orbit, 'semi_major_axis')
        self.R = self.conn.add_stream(getattr, self.vessel.orbit, 'radius')
        self.speed = self.conn.add_stream(getattr, self.vessel.orbit, 'speed')
        self.period = self.conn.add_stream(getattr, self.vessel.orbit, 'period')
        self.ETAap = self.conn.add_stream(getattr, self.vessel.orbit, 'time_to_apoapsis')
        self.ETApe = self.conn.add_stream(getattr, self.vessel.orbit, 'time_to_periapsis')
        self.ecc = self.conn.add_stream(getattr, self.vessel.orbit, 'eccentricity')
        self.inc = self.conn.add_stream(getattr, self.vessel.orbit, 'inclination')
        self.Node = self.conn.add_stream(getattr, self.vessel.orbit, 'longitude_of_ascending_node')
        self.w = self.conn.add_stream(getattr, self.vessel.orbit, 'argument_of_periapsis')

        self.mu = self.conn.add_stream(getattr, self.body(), 'gravitational_parameter')
        self.R_eq = self.conn.add_stream(getattr, self.body(), 'equatorial_radius')
        self.Rot_p = self.conn.add_stream(getattr, self.body(), 'rotational_period')
        self.Lat = self.conn.add_stream(getattr, self.vessel.flight(), 'latitude')
        self.Lon = self.conn.add_stream(getattr, self.vessel.flight(), 'longitude')

        self.V_ap = math.sqrt((2 * self.mu() * self.R_pe() ) / ( self.R_ap() * ( self.R_ap() + self.R_pe() )))
        self.V_pe = math.sqrt((2 * self.mu() * self.R_ap() ) / ( self.R_pe() * ( self.R_ap() + self.R_pe() )))
        self.circ_V = math.sqrt( self.mu() / self.R_ap() )
        self.circ_dV = self.circ_V - self.V_ap

class Vessel_info:
    def __init__(self, setup):
        
        self.conn = setup.conn
        self.vessel = setup.vessel
        self.name = self.conn.add_stream(getattr, self.vessel, 'name')
        self.situation = self.conn.add_stream(getattr, self.vessel, 'situation')
        self.thrust = self.conn.add_stream(getattr, self.vessel, 'thrust')
        self.specific_impulse = self.conn.add_stream(getattr, self.vessel, 'specific_impulse')
        self.mass = self.conn.add_stream(getattr, self.vessel, 'mass')
        self.surface_altitude = self.conn.add_stream(getattr, self.vessel.flight(), 'surface_altitude')
        self.speed = self.conn.add_stream(getattr, self.vessel.flight(), 'speed')
        self.velocity = self.conn.add_stream(getattr, self.vessel.flight(), 'velocity')
        self.direction = self.conn.add_stream(getattr, self.vessel.flight(), 'direction')
        self.pitch = self.conn.add_stream(getattr, self.vessel.flight(), 'pitch')
        self.heading = self.conn.add_stream(getattr, self.vessel.flight(), 'heading')
        self.roll = self.conn.add_stream(getattr, self.vessel.flight(), 'roll')
        self.prograde = self.conn.add_stream(getattr, self.vessel.flight(), 'prograde')
        self.atmo_D = self.conn.add_stream(getattr, self.vessel.flight(), 'atmosphere_density')
        self.dyn_press = self.conn.add_stream(getattr, self.vessel.flight(), 'dynamic_pressure')
        self.ang_att = self.conn.add_stream(getattr, self.vessel.flight(), 'angle_of_attack')
        self.side_ang = self.conn.add_stream(getattr, self.vessel.flight(), 'sideslip_angle')
        self.Q = self.conn.add_stream(getattr, self.vessel.flight(), 'dynamic_pressure')



