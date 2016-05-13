import krpc, math, Telemetry

class Azumuth_init:
	def __init__(self, Tar, inc, tel):

		self.Tar = Tar
		self.tel = tel
		self.inc = inc

		if self.inc > 0:
			self.node = "Ascending"
		else:
			self.node = "Descending"
			self.inc = math.fabs(self.inc)

		if (math.fabs(tel.Lat())) > self.inc:
			self.inc = math.fabs(tel.Lat())
		if ( 180 - math.fabs(tel.Lat()) ) < self.inc:
			self.inc = ( 180 - math.fabs(tel.Lat()) )

		self.V_eq = ( ( 2 * math.pi * tel.R() ) /  tel.Rot_p() )

		self.inertAz = math.asin(max(min(math.cos(self.inc / math.cos(tel.Lat())), 1), -1))
		self.VXRot = Tar.T_orb_V * math.sin(self.inertAz) - self.V_eq * math.cos(tel.Lat())
		self.VYRot = Tar.T_orb_V * math.cos(self.inertAz)

		self._Az = math.fmod(math.atan2( self.VXRot , self.VYRot ) +360, 360)
		
		if self.node == "Ascending":    self.Az = self._Az
		elif self.node == "Descending":
			if self._Az <= 90:          self.Az = 180 - self._Az
			elif self._Az >= 270:       self.Az = 540 - self._Az

class Gravity_pitch:
	def __init__(self, Tar, tel):

		self.Tar = Tar
		self.tel = tel

		if tel.R_ap() < Tar.Tar_R:
			self.pitch = ( 85 - ( 1.2 * math.sqrt( tel.orb_speed() - 70 ))) - ( Tar.T_ap_dV / 4.5 )
		else: self.pitch = Tar.T_ap_dV / 4.5


def engine_Actions(tel,eng_to_activate,action):
	for eng in tel.engines:
		if eng.name == eng_to_activate[0]:
			mods = eng.modules
			for mod in mods:
				if mod.name == "ModuleEnginesRF":
					m = mod
					m.set_action(action,True)


