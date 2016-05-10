import krpc, math
from Telemetry import Orb_info, Vessel_info

class Target_orb:
    def __init__(self, Tar_orb, orb):

        self.Tar_orb = Tar_orb
        self.orb = orb

        #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        #        T A R G E T   O R B I T        #
        #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

        self.Tar_R = self.Tar_orb + self.orb.R()
        self.T_V_ap = math.sqrt((2 * self.orb.mu() * self.orb.R_pe() ) / ( self.Tar_R * ( self.orb.R_ap() + self.orb.R_pe() )))
        
        self.T_ap_dV = self.T_V_ap - self.orb.V_ap
        self.T_orb_V = math.sqrt( orb.mu() / self.Tar_R )

class init_Azumuth:
    def __init__(self, Tar, inc, orb):

        self.Tar = Tar
        self.orb = orb
        self.inc = inc

        if self.inc > 0:
            self.node = "Ascending"
        else:
            self.node = "Descending"
            self.inc = math.fabs(self.inc)

        if (math.fabs(orb.Lat())) > self.inc:
            self.inc = math.fabs(orb.Lat())
        if ( 180 - math.fabs(orb.Lat()) ) < self.inc:
            self.inc = ( 180 - math.fabs(orb.Lat()) )

        self.V_eq = ( ( 2 * math.pi * orb.R() ) /  orb.Rot_p() )

        self.inertAz = math.asin(max(min(math.cos(self.inc / math.cos(orb.Lat())), 1), -1))
        self.VXRot = Tar.T_orb_V * math.sin(self.inertAz) - self.V_eq * math.cos(orb.Lat())
        self.VYRot = Tar.T_orb_V * math.cos(self.inertAz)

        self._Az = math.fmod(math.atan2( self.VXRot , self.VYRot ) +360, 360)
        
        if self.node == "Ascending":
            self.Az = self._Az
        elif self.node == "Descending":
            if self._Az <= 90:
                self.Az = 180 - self._Az
            elif self._Az >= 270:
                self.Az = 540 - self._Az

class Gravity_pitch:
    def __init__(self, Tar, orb):

        self.Tar = Tar
        self.orb = orb

#        if orb.Q > 