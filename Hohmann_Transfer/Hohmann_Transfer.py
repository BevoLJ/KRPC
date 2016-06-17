import time
# import numpy as np
from UI import UI
from Orbit_Manager import OrbitManager


class LaunchControl(UI):
    def __init__(self):
        super().__init__()

        # self.mode = "Testing"
        self.mode = "Launch Prep"
        self.camera.mode = self.CameraMode.free
        self.falafels = True

    def launch(self):
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        #              L A U N C H               #
        #             P R O G R A M              #
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

        self.ap.engage()
        ui = UI()

        while self.mode == "Launch Prep":
            if self.control.get_action_group(9): self.mode = "Launch"; self.control.activate_next_stage()
            time.sleep(1)

        while self.mode != "Orbit":
            self.pitch_and_heading()

            if self.mode == "Launch":
                self.control.throttle = 1
                _twr = self.twr_calc(self.thrust(), self.mass(), self.altitude(), self.radius_eq, self.mu)
                if _twr > 1:
                    self.lAz_data = self.azimuth_init()
                    self.control.activate_next_stage()
                    self.mode = "Booster Stage"

            if self.mode == "Booster Stage":

                if (self.altitude() > 80000) and (self.falafels is True):
                    self.control.activate_next_stage()
                    self.falafels = False

                self.flameout("Upper Stage")

            if self.mode == "Upper Stage":

                if self.eng_status(self.get_active_engine(), "Status") == "Flame-Out!":
                    self.control.throttle = 0
                    time.sleep(1.5)
                    self.control.activate_next_stage()
                    self.control.rcs = True
                    self.mode = "Cruise"

            if self.mode == "Cruise":
                if self.time_to_burn(self.ETA_ap(), self.maneuver_burn_time(self.circ_dv())) < 5:
                    self.ullage_rcs()
                    self.mode = "Orbit Insertion"

            if self.mode == "Orbit Insertion":
                self.control.rcs = False
                if (self.circ_dv() < 10) or (self.orbital_period(self.parking_orbit_alt + self.radius_eq,
                                                                 self.mu) < self.period()):
                    self.control.throttle = 0
                    self.mode = "Orbit"

            if self.circ_dv() > 500: time.sleep(.1)

            ui.gravity_turn(self.mode)

        self.control.rcs = True
        self.ap.disengage()
        self.control.sas = True
        time.sleep(2)


class HohmannTransfer(OrbitManager):
    def __init__(self):
        super().__init__()

        self.mode = "LEO"
        # self.mode = "Testing"
        self.hoh_xfer = []
        self.camera.mode = self.CameraMode.free

    def transfer(self):
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        #             H O H M A N N              #
        #            T R A N S F E R             #
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

        self.control.rcs = False
        self.control.throttle = 0
        time.sleep(1)
        self.ap.reference_frame = self.vessel.orbital_reference_frame
        self.ap.target_direction = (0, 1, 0)
        self.ap.engage()
        print(self.mode)
        ui = UI()

        while self.mode != "Xfered":

            if self.mode == "LEO":
                _hoh_xfer_dv = self.transfer_injection_dv(self.mu, self.semi_major_axis(), self.target_orbit_radius)
                _time_to_burn = self.time_to_burn(self.ETA_pe(), self.maneuver_burn_time(_hoh_xfer_dv))

                if _time_to_burn > 120: self.KSC.warp_to(self.ut() + _time_to_burn - 90)
                elif _time_to_burn > 34: self.fix_aoa(_time_to_burn, self.maneuver_burn_time(_hoh_xfer_dv))
                elif _time_to_burn < 5: self.ullage_rcs(); self.mode = "Xfer Burn"

            if self.mode == "Xfer Burn":
                self.control.rcs = False
                if self.apoapsis_radius() > self.target_orbit_radius:
                    self.control.throttle = 0
                    time.sleep(1)
                    self.mode = "Xfer Cruise"

            if self.mode == "Xfer Cruise":
                _time_to_burn = self.time_to_burn(self.ETA_ap(), self.maneuver_burn_time(self.circ_dv()))

                if _time_to_burn > 120: self.KSC.warp_to(self.ut() + _time_to_burn - 90)
                elif _time_to_burn > 34: self.fix_aoa(_time_to_burn, self.maneuver_burn_time(self.circ_dv()))
                elif _time_to_burn < 5:
                    self.ullage_rcs()
                    self.mode = "Final Burn"

            if self.mode == "Final Burn":
                self.control.rcs = False
                if (self.circ_dv() < 10) or (self.orbital_period(self.target_orbit_radius, self.mu) < self.period()):
                    self.control.throttle = 0
                    time.sleep(1)
                    self.mode = "Xfered"

            time.sleep(.05)
            ui.transfer(self.mode)

        print("Done")


def main():
    LaunchControl().launch()
    HohmannTransfer().transfer()


main()
