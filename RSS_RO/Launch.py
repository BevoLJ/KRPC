import krpc, time, math
import argparse ### T O   A D D ### Parking Orbit, inc
import Telemetry, Flight
from Telemetry import _Telemetry, Target_orb
from Flight import Azumuth_init, Gravity_pitch, engine_Actions

Tar_orb = 175000    # Target parking orbit. N O T E: add arg
inc = 29            # Target inclination.   N O T E: add arg

tel = _Telemetry()
Tar = Target_orb(Tar_orb, tel)
Az = Azumuth_init(Tar, inc, tel)
Pitch = Gravity_pitch(Tar, tel).pitch

cur_stage_engs = tel.cur_stage_engs

engine_Actions(tel,cur_stage_engs,'Activate Engine')