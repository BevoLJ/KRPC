# import time
from Launch_Manager import LaunchManager
from Orbit_Manager import OrbitManager


class UI(LaunchManager, OrbitManager):

    def __init__(self):
        super().__init__()

        self.LAN = self.conn.add_stream(getattr, self.vessel.orbit, 'longitude_of_ascending_node')
        self.ETA_ap = self.conn.add_stream(getattr, self.vessel.orbit, 'time_to_apoapsis')

        _screen_size = self.conn.ui_extended.rect_transform.size
        _panel_flight = self.conn.ui_extended.add_panel()
        _rect = _panel_flight.rect_transform
        _rect.size = (260, 200)
        _rect.position = (50 - (_screen_size[0] / 2), 350)

        # _screen_size = self.conn.ui.RectTransform.size
        # _canvas_flight = self.conn.ui.add_canvas()
        # _panel_flight = _canvas_flight.add_panel()
        # _rect = _panel_flight.rect_transform
        # _rect.size = (260, 200)
        # _rect.position = (-830, 300)
        # _rect.position = (50 - (_screen_size[0]), 350)

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
        self.text_4.rect_transform.position = (40, 25)
        # self.text_1.color = (1, 1, 1)
        self.text_4.size = 12
        self.text_5 = _panel_flight.add_text("")
        self.text_5.rect_transform.position = (40, 10)
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
        self.text_8.rect_transform.position = (40, -55)
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
        self.text_2.content = 'Apoapsis   :  %d km' % (self.apoapsis_altitude() / 1000)
        self.text_3.content = 'ETA Ap      :  %d sec' % (self.ETA_ap())
        self.text_4.content = 'Periapsis   :  %d km' % (self.periapsis_altitude() / 1000)
        self.text_5.content = 'Q                :  %d kPa' % (self.Q())
        self.text_6.content = 'Azimuth     :  %d deg' % (self.azimuth(self.lAz_data))
        self.text_7.content = 'Pitch          :  %d deg' % (self.pitch())
        self.text_8.content = 'Ap dV        :  %d m/s' % (self.target_apoapsis_speed_dv())
        self.text_9.content = 'Circ dV          :  %d m/s' % (self.circ_dv())
        self.text_10.content = 'Circ Burn Time:  %d sec' % (self.maneuver_burn_time(self.circ_dv()))

    def transfer(self, mode):

        self.text_1.content = 'Mode       :  ' + mode
        self.text_2.content = 'Apoapsis   :  %d km' % (self.apoapsis_altitude() / 1000)
        self.text_3.content = 'ETA Ap      :  %d sec' % (self.ETA_ap())
        self.text_4.content = 'Periapsis   :  %d km' % (self.periapsis_altitude() / 1000)
        self.text_5.content = 'ETA Pe      :  %d sec' % (self.ETA_pe())
        if mode == "LEO Cruise" or "Transfer Burn":
            _hoh_xfer_dv = self.transfer_injection_dv(self.mu, self.semi_major_axis(), self.target_orbit_radius)
            self.text_9.content = 'Xfer dV          :  %d m/s' % _hoh_xfer_dv
            self.text_10.content = 'Xfer Burn Time:  %d sec' % (self.maneuver_burn_time(_hoh_xfer_dv))
        if mode == "Transfer Cruise" or "Final Burn":
            self.text_9.content = 'Circ dV          :  %d m/s' % (self.circ_dv())
            self.text_10.content = 'Circ Burn Time:  %d sec' % (self.maneuver_burn_time(self.circ_dv()))
