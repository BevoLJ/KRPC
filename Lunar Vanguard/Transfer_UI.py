from Lunar_XFer_Manager import LunarXFerManager
import numpy as np


class TransferUI(LunarXFerManager):

    def __init__(self):
        super().__init__()

        self.LAN = self.conn.add_stream(getattr, self.vessel.orbit, 'longitude_of_ascending_node')
        self.ETA_ap = self.conn.add_stream(getattr, self.vessel.orbit, 'time_to_apoapsis')

        _screen_size = self.conn.ui_extended.rect_transform.size
        _panel_flight = self.conn.ui_extended.add_panel()
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

    def transfer_ui(self, mode):

        self.text_1.content = 'Mode       :  ' + mode
        self.text_2.content = 'Apoapsis   :  %d km' % (self.apoapsis_altitude() / 1000)
        self.text_3.content = 'ETA Ap      :  %d sec' % (self.ETA_ap())
        self.text_4.content = 'Periapsis   :  %d km' % (self.periapsis_altitude() / 1000)
        self.text_5.content = 'true_anomaly           :  %d deg' % self.true_anomaly(self.eccentricity(),
                                                                           self.eccentric_anomaly())
        self.text_6.content = 'Moon True Anomaly:  %d deg' % self.true_anomaly(self.moon_eccentricity(),
                                                                           self.moon_eccentric_anomaly())
        self.text_7.content = 'Period        :  %d mins' % ((self.period()) / 60)
        self.text_8.content = 'LAN             :  %d deg' % (np.rad2deg(self.LAN()))
        self.text_9.content = 'Moon LAN   :  %d deg' % (np.rad2deg(self.moon_LAN()))