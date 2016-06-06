import time
from Launch_Manager import LaunchManager


class LaunchUI(LaunchManager):

    def __init__(self):
        super().__init__()

        self.LAN = self.conn.add_stream(getattr, self.vessel.orbit, 'longitude_of_ascending_node')

        # S E C O N D A R Y   O R B I T A L   E L E M E N T S

        self.apoapsis_altitude = self.conn.add_stream(getattr, self.vessel.orbit, 'apoapsis_altitude')
        self.periapsis_altitude = self.conn.add_stream(getattr, self.vessel.orbit, 'periapsis_altitude')
        self.apoapsis_radius = self.conn.add_stream(getattr, self.vessel.orbit, 'apoapsis')
        self.periapsis_radius = self.conn.add_stream(getattr, self.vessel.orbit, 'periapsis')
        self.ETA_ap = self.conn.add_stream(getattr, self.vessel.orbit, 'time_to_apoapsis')

        _screen_size = self.conn.ui.rect_transform.size
        _panel_flight = self.conn.ui.add_panel()
        _rect = _panel_flight.rect_transform
        _rect.size = (260, 200)
        _rect.position = (50 - (_screen_size[0] / 2), 350)

        self.text_1 = _panel_flight.add_text("")
        self.text_1.rect_transform.position = (40, 80)
        # self.text_1.color = (1, 1, 1)
        self.text_1.size = 13
        self.text_2 = _panel_flight.add_text("")
        self.text_2.rect_transform.position = (40, 60)
        # self.text_1.color = (1, 1, 1)
        self.text_2.size = 12
        self.text_3 = _panel_flight.add_text("")
        self.text_3.rect_transform.position = (40, 45)
        # self.text_1.color = (1, 1, 1)
        self.text_3.size = 12
        self.text_4 = _panel_flight.add_text("")
        self.text_4.rect_transform.position = (40, 20)
        # self.text_1.color = (1, 1, 1)
        self.text_4.size = 12
        self.text_5 = _panel_flight.add_text("")
        self.text_5.rect_transform.position = (40, -5)
        # self.text_1.color = (1, 1, 1)
        self.text_5.size = 12
        self.text_6 = _panel_flight.add_text("")
        self.text_6.rect_transform.position = (40, -20)
        # self.text_1.color = (1, 1, 1)
        self.text_6.size = 12
        self.text_7 = _panel_flight.add_text("")
        self.text_7.rect_transform.position = (40, -35)
        # self.text_1.color = (1, 1, 1)
        self.text_7.size = 12
        self.text_8 = _panel_flight.add_text("")
        self.text_8.rect_transform.position = (40, -60)
        # self.text_1.color = (1, 1, 1)
        self.text_8.size = 12
        self.text_9 = _panel_flight.add_text("")
        self.text_9.rect_transform.position = (40, -75)
        # self.text_1.color = (1, 1, 1)
        self.text_9.size = 12
        self.text_10 = _panel_flight.add_text("")
        self.text_10.rect_transform.position = (40, -90)
        # self.text_1.color = (1, 1, 1)
        self.text_10.size = 12

    def gravity_turn(self, mode):

        self.text_1.content = 'Mode       :  ' + mode
        self.text_2.content = 'Apoapsis  :  %d km' % (self.apoapsis_altitude() / 1000)
        self.text_3.content = 'ETA Ap      :  %d sec' % (self.ETA_ap())
        self.text_4.content = 'Periapsis    :  %d km' % (self.periapsis_altitude() / 1000)
        self.text_6.content = 'Circ dV    :  %d m/s' % (self.circ_dv())
        self.text_8.content = 'Stage dV   :  %d m/s' % (self.stage_dv())
        self.text_9.content = 'Burn Time    :  %d sec' % (self.maneuver_burn_time(self.circ_dv()))
        self.text_10.content = 'LAN        :  %d sec' % (self.maneuver_burn_time(self.LAN()))

        if mode == "Mid Stage" or "Upper Stage":
            self.text_5.content = 'Ap dV      :  %d m/s' % (self.target_apoapsis_speed_dv() / 3)
        elif mode == "Orbital Insertion":
            self.text_5.content = 'Ap dV      :  %d m/s' % (self.target_apoapsis_speed_dv())
        else: self.text_5.content = 'Ap dV      :  %d m/s' % (self.target_apoapsis_speed_dv() / 5)

        if self.Q() < 30:
            self.text_7.content = 'Azimuth         :  %d' % (self.azimuth(self.lAz_data))
        else:
            self.text_7.content = 'Q               :  %d' % (self.Q())

    def launch_ui(self):
        _mode = "Pre-Flight Checks"
        _screen_size = self.conn.ui.rect_transform.size
        _panel = self.conn.ui.add_panel()
        _rect = _panel.rect_transform
        _rect.size = (200, 140)
        _rect.position = (400 - (_screen_size[0] / 2), 110)
        # Testing ui.messages
        self.conn.ui.message("Launch Mode: " + _mode, 5.0, self.conn.ui.MessagePosition.top_center)

        _text_1 = _panel.add_text("Enter Target Inclination")
        _text_1.rect_transform.position = (5, 50)
        _text_1.size = 14
        _text_1 = _panel.add_text("Enter Target Orbit in Km")
        _text_1.rect_transform.position = (5, 5)
        _text_1.size = 14

        _target_orbit_inc = _panel.add_input_field()
        _target_orbit_inc.rect_transform.position = (0, 35)

        _target_orbit_alt = _panel.add_input_field()
        _target_orbit_alt.rect_transform.position = (0, -15)
        _launch_button = _panel.add_button("Launch")
        _launch_button.rect_transform.position = (0, -50)

        _button_clicked = self.conn.add_stream(getattr, _launch_button, 'clicked')

        while _mode == "Pre-Flight Checks":
            if _button_clicked():
                self.target_orbit_inc = (float(_target_orbit_inc.value))
                self.target_orbit_alt = (float(_target_orbit_alt.value) * 1000)
                _mode = "Launch"
                _button_clicked.clicked = False
            time.sleep(0.4)

        self.control.activate_next_stage()
        _panel.remove()
        return _mode
