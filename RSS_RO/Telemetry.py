import krpc, math

class _Telemetry:
	def __init__(self):

		#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
		#       C O M M U N I C A T I O N       #
		#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

		self.conn = krpc.connect( name='A4 Launch Program', address='127.0.0.1', rpc_port=50000, stream_port=50001)
		self.KSC = self.conn.space_center
		self.vessel = self.KSC.active_vessel
		self.parts = self.vessel.parts
		self.control = self.vessel.control
		self.auto_pilot = self.vessel.auto_pilot
		self.engines = self.parts.with_module("ModuleEnginesRF")

		#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
		#             O R B I T A L             #
		#           T E L E M E T R Y           #
		#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

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
		self.orb_speed = self.conn.add_stream(getattr, self.vessel.orbit, 'speed')
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

		#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
		#              V E S S E L              #
		#           T E L E M E T R Y           #
		#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

		self.name = self.conn.add_stream(getattr, self.vessel, 'name')
		self.situation = self.conn.add_stream(getattr, self.vessel, 'situation')
		self.thrust = self.conn.add_stream(getattr, self.vessel, 'thrust')
		self.specific_impulse = self.conn.add_stream(getattr, self.vessel, 'specific_impulse')
		self.mass = self.conn.add_stream(getattr, self.vessel, 'mass')
		self.surface_altitude = self.conn.add_stream(getattr, self.vessel.flight(), 'surface_altitude')
		self.vessel_speed = self.conn.add_stream(getattr, self.vessel.flight(), 'speed')
		self.velocity = self.conn.add_stream(getattr, self.vessel.flight(), 'velocity')
		self.direction = self.conn.add_stream(getattr, self.vessel.flight(), 'direction')
		self.vessel_pitch = self.conn.add_stream(getattr, self.vessel.flight(), 'pitch')
		self.heading = self.conn.add_stream(getattr, self.vessel.flight(), 'heading')
		self.roll = self.conn.add_stream(getattr, self.vessel.flight(), 'roll')
		self.prograde = self.conn.add_stream(getattr, self.vessel.flight(), 'prograde')
		self.atmo_D = self.conn.add_stream(getattr, self.vessel.flight(), 'atmosphere_density')
		self.dyn_press = self.conn.add_stream(getattr, self.vessel.flight(), 'dynamic_pressure')
		self.ang_att = self.conn.add_stream(getattr, self.vessel.flight(), 'angle_of_attack')
		self.side_ang = self.conn.add_stream(getattr, self.vessel.flight(), 'sideslip_angle')
		self.Q = self.conn.add_stream(getattr, self.vessel.flight(), 'dynamic_pressure')

		self.twr = self.thrust() / (( self.mu() / (( self.alt() + self.R_eq() )**2 )) * self.mass() )

		#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
		#               P A R T S               #
		#           T E L E M E T R Y           #
		#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

		self.list_eng_tuples = eng_list_tuples(self.engines)
		self.cur_stage_engs = cur_stage_engs(self.engines)

class Target_orb:
	def __init__(self, Tar_orb, tel):

		self.Tar_orb = Tar_orb
		self.tel = tel

		self.Tar_R = self.Tar_orb + self.tel.R()
		self.T_V_ap = math.sqrt((2 * self.tel.mu() * self.tel.R_pe() ) / ( self.Tar_R * ( self.tel.R_ap() + self.tel.R_pe() )))
		
		self.T_ap_dV = self.T_V_ap - self.tel.V_ap
		self.T_orb_V = math.sqrt( tel.mu() / self.Tar_R )

def eng_list_tuples(engines):
	list_eng_tuples = []

	for part in engines:
		eng_tup = (part.stage,part.name)
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



