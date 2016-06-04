from Operation import Operations


class FlightUI(Operations):

    def __init__(self):
        super().__init__()

        _screen_size = self.conn.ui.rect_transform.size
        _panel_flight = self.conn.ui.add_panel()
        _rect = _panel_flight.rect_transform
        _rect.size = (250, 200)
        _rect.position = (50 - (_screen_size[0] / 2), 350)

        self.text_1 = _panel_flight.add_text("")
        self.text_1.rect_transform.position = (40, 70)
        # self.text_1.color = (1, 1, 1)
        self.text_1.size = 13
        self.text_2 = _panel_flight.add_text("")
        self.text_2.rect_transform.position = (40, 40)
        # self.text_1.color = (1, 1, 1)
        self.text_2.size = 12
        self.text_3 = _panel_flight.add_text("")
        self.text_3.rect_transform.position = (40, 25)
        # self.text_1.color = (1, 1, 1)
        self.text_3.size = 12
        self.text_4 = _panel_flight.add_text("")
        self.text_4.rect_transform.position = (40, 0)
        # self.text_1.color = (1, 1, 1)
        self.text_4.size = 12
        self.text_5 = _panel_flight.add_text("")
        self.text_5.rect_transform.position = (40, -25)
        # self.text_1.color = (1, 1, 1)
        self.text_5.size = 12
        self.text_6 = _panel_flight.add_text("")
        self.text_6.rect_transform.position = (40, -40)
        # self.text_1.color = (1, 1, 1)
        self.text_6.size = 12
        self.text_7 = _panel_flight.add_text("")
        self.text_7.rect_transform.position = (40, -55)
        # self.text_1.color = (1, 1, 1)
        self.text_7.size = 12
        self.text_8 = _panel_flight.add_text("")
        self.text_8.rect_transform.position = (40, -70)
        # self.text_1.color = (1, 1, 1)
        self.text_8.size = 12
        self.text_9 = _panel_flight.add_text("")
        self.text_9.rect_transform.position = (40, -85)
        # self.text_1.color = (1, 1, 1)
        self.text_9.size = 12

    def gravity_turn(self, mode):

        self.text_1.content = 'Mode       :  ' + mode
        self.text_2.content = 'Apoapsis  :  %d km' % (self.apoapsis_altitude() / 1000)
        self.text_3.content = 'ETA Ap      :  %d sec' % (self.ETA_ap())
        self.text_4.content = 'Periapsis    :  %d km' % (self.periapsis_altitude() / 1000)
        self.text_6.content = 'Circ dV    :  %d m/s' % (self.circ_dv())
        self.text_7.content = 'Q               :  %d' % (self.Q())
        self.text_8.content = 'Stage dV   :  %d m/s' % (self.stage_deltav())
        self.text_9.content = 'Burn Time    :  %d sec' % (self.maneuver_burn_time(self.circ_dv()))

        if mode == "Mid Stage" or "Upper Stage":
            self.text_5.content = 'Ap dV      :  %d m/s' % (-self.target_apoapsis_speed_dv() / 3)
        elif mode == "Orbital Insertion":
            self.text_5.content = 'Ap dV      :  %d m/s' % (-self.target_apoapsis_speed_dv())
        else: self.text_5.content = 'Ap dV      :  %d m/s' % (-self.target_apoapsis_speed_dv() / 5)

