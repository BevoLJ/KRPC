from Operation import Operations


class FlightUI(Operations):

    def __init__(self):
        super().__init__()

        self.screen_size = self.conn.ui.rect_transform.size
        self.panel_flight = self.conn.ui.add_panel()
        self.rect = self.panel_flight.rect_transform
        self.rect.size = (150, 200)
        self.rect.position = (50 - (self.screen_size[0] / 2), 350)

        self.text_1 = self.panel_flight.add_text("")
        self.text_1.rect_transform.position = (40, -20)
        # self.text_1.color = (1, 1, 1)
        self.text_1.size = 12
        self.text_2 = self.panel_flight.add_text("")
        self.text_2.rect_transform.position = (20, -20)
        # self.text_1.color = (1, 1, 1)
        self.text_2.size = 12

    def gravity_turn(self):
        self.text_1.content = 'ap_v_dv: %d kN' % (self.apoapsis_v_dv() / 1000)
        self.text_2.content = 'circ_dv: %d kN' % (self.circ_dv() / 1000)


