import time
from UI_Panel import FlightUI
from Operation import Operations


class FlightControl(FlightUI):

    def __init__(self):
        super().__init__()

    def launch(self):

        mode = "Launch"
        self.ap.engage()
        self.control.throttle = 1
        self.ap.target_pitch_and_heading(90, 90)
        self.control.activate_next_stage()
        ui = FlightUI()

        while mode != "Orbit":

            if mode == "Launch":
                if self.twr() > 1:
                    self.ap.target_pitch_and_heading(90, 90)
                    self.control.activate_next_stage()
                    print(mode)
                    mode = "Booster Stage"

            if mode == "Booster Stage":
                if self.vessel_speed() < 80: self.ap.target_pitch_and_heading(90, 90)
                else: self.ap.target_pitch_and_heading(self.pitch(), 90)

                if self.eng_status() == "Flame-Out!":
                    self.control.activate_next_stage()
                    print(mode)
                    mode = "Mid Stage"

            if mode == "Mid Stage":
                self.ap.target_pitch_and_heading(self.pitch(), 90)
                if self.eng_status() == "Flame-Out!":
                    self.control.activate_next_stage()
                    print(mode)
                    mode = "Upper Stage"

            if mode == "Upper Stage":
                if self.vessel_speed() < 2400: self.ap.target_pitch_and_heading(self.pitch(), 90)
                else: self.ap.target_pitch_and_heading(5, 90)

                if self.stage_deltav() < 100:
                    self.control.activate_next_stage()
                    while self.eng_status() != "Flame-Out!": time.sleep(.5)
                    self.control.activate_next_stage()
                    while self.eng_status() != "Flame-Out!": time.sleep(.5)
                    print(mode)
                    mode = "Cruise"

            if mode == "Cruise":
                if self.time_to_burn(self.ut, self.ETA_ap(), self.maneuver_burn_time(self.circ_dv())) < 1:
                    self.control.activate_next_stage()
                    print(mode)
                    mode = "Orbital Insertion"

            if mode == "Orbital Insertion":
                self.ap.target_pitch_and_heading(0, 90)
                if self.circ_dv() < 1:
                    print(mode)
                    mode = "Orbit"

            time.sleep(.4)
            ui.gravity_turn()

    def launch_ui(self):
        screen_size = self.conn.ui.rect_transform.size
        panel = self.conn.ui.add_panel()
        rect = panel.rect_transform
        rect.size = (200, 50)
        rect.position = (400 - (screen_size[0] / 2), 100)

        button = panel.add_button("Launch")
        button.rect_transform.position = (0, 0)

        button_clicked = self.conn.add_stream(getattr, button, 'clicked')

        while True:
            if button_clicked():
                panel.remove()
                self.launch()

            time.sleep(0.4)


def flight_ui_testing():
    ui = FlightUI()
    while True:
        ui.gravity_turn()
        time.sleep(.4)


def main():
    # FlightControl().launch()
    # Testing().test()
    # launch_ui()
    flight_ui_testing()

main()
