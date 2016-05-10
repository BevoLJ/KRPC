import krpc, time, math
import argparse ### T O   A D D ### Parking Orbit, ...
from Telemetry import Orb_info, Vessel_info
from Flight import Target_orb, init_Azumuth

Tar_orb = 250000  # Target parking orbit. NOTE: add arg
inc = 29

class setup:
    def __init__(self):
        self.conn = krpc.connect( name='A4 Launch Program', address='127.0.0.1', rpc_port=50000, stream_port=50001)
        self.KSC = self.conn.space_center
        self.vessel = self.KSC.active_vessel
        self.control = self.vessel.control

orb = Orb_info(setup())
ves = Vessel_info(setup())
Tar = Target_orb(Tar_orb, orb)
Az = init_Azumuth(Tar, inc, orb)

while True:
    print(Az.Az)