import time
from All_the_things import *

spin_solids = "SnubOtron"


def main():

    mode = "Launch"
    ap.engage()
    control.throttle = 1
    ap.target_pitch_and_heading(90, 90)
    control.activate_next_stage()

    while mode != "Orbit":

        if mode == "Launch":
            if twr() > 1:
                ap.target_pitch_and_heading(90, 90)
                control.activate_next_stage()
                mode = "Lower Stage"

        if mode == "Lower Stage":
            if vessel_speed() < 100:
                ap.target_pitch_and_heading(90, 90)
            else:
                ap.target_pitch_and_heading(pitch(vessel_speed()), 90)

            if eng_status(spin_solids) == "Flame-Out!":
                control.activate_next_stage()
                mode = "Upper Stage"

        if mode == "Upper Stage":
            if stage_deltav("SXTAJ10") > 500:
                ap.target_pitch_and_heading(pitch(vessel_speed()), 90)

            elif stage_deltav("SXTAJ10") > 100:
                ap.target_pitch_and_heading(-1, 90)

            else:
                control.activate_next_stage()
                while eng_status(spin_solids) != "Flame-Out!":
                    time.sleep(.5)
                control.activate_next_stage()
                while eng_status(spin_solids) != "Flame-Out!":
                    time.sleep(.5)
                mode = "Cruise"

        if mode == "Cruise":
            # if ETA_ap() > 30:
                # KSC.warp_to(KSC.ut + ETA_ap() - 15, max_rails_rate=10.0, max_physics_rate=4.0)
            if ETA_ap() < 5:
                control.activate_next_stage()
                mode = "Payload"

        if mode == "Payload":
            if periapsis() < 150000:
                if eng_status(spin_solids) == "Flame-Out!":
                    control.activate_next_stage()
            else:
                mode = "Orbit"

        time.sleep(.5)

main()
