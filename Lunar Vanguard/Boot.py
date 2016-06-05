import krpc


class BootUp:
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
        self.target_orbit_inc = 0

        self.body = self.vessel.orbit.body
        self.radius_eq = self.vessel.orbit.body.equatorial_radius
        self.gravitational_parameter = self.vessel.orbit.body.gravitational_parameter
        self.rotational_period = self.vessel.orbit.body.rotational_period

        self.ut = self.conn.add_stream(getattr, self.conn.space_center, "ut")
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
        self.longitude = self.conn.add_stream(getattr, self.vessel.flight(), 'longitude')
        self.LAN = self.conn.add_stream(getattr, self.vessel.orbit, 'longitude_of_ascending_node')
        self.eccentricity = self.conn.add_stream(getattr, self.vessel.orbit, 'eccentricity')
        # self.altitude = self.conn.add_stream(getattr, self.vessel.flight(), 'mean_altitude')
        # vessel_pitch = conn.add_stream(getattr, vessel.flight(), 'gravity_pitch')
        # heading = conn.add_stream(getattr, vessel.flight(), 'heading')
        # self.vessel_velocity_vector = self.conn.add_stream(getattr, self.vessel_flight_bdy(), 'velocity')
        # self.vessel_pitch = self.conn.add_stream(getattr, self.vessel.flight(), 'gravity_pitch')
        # self.heading = self.conn.add_stream(getattr, self.vessel.flight(), 'heading')

        # self.ves_reference_frame = self.conn.add_stream(getattr, self.vessel, 'reference_frame')
        # self.ves_direction = self.conn.add_stream(self.vessel.direction, self.ves_reference_frame())
        self.orb_reference_frame = self.conn.add_stream(getattr, self.vessel, 'orbital_reference_frame')
        self.vessel_orbit_direction = self.conn.add_stream(self.vessel.direction, self.orb_reference_frame())

        self.bdy_reference_frame = self.conn.add_stream(getattr, self.body, 'reference_frame')
        self.bdy__non_rot_reference_frame = self.conn.add_stream(getattr, self.body, 'non_rotating_reference_frame')
        self.vessel_flight_bdy = self.conn.add_stream(self.vessel.flight, self.bdy_reference_frame())
        self.vessel_flight_bdy_non_rot = self.conn.add_stream(self.vessel.flight, self.bdy__non_rot_reference_frame())
        self.vessel_sur_speed = self.conn.add_stream(getattr, self.vessel_flight_bdy(), 'speed')
        self.vessel_orb_speed = self.conn.add_stream(getattr, self.vessel_flight_bdy_non_rot(), 'speed')
