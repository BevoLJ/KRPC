import sys
import threading
import time

from PyQt5 import QtWidgets

from PyQt_GUI import UiForm
# from Testing_GUI import UiForm
from Telemetry import Telemetry
from Flight import lift_off, gravity_turn

tel = Telemetry()
print(tel.vessel_speed())
# self.twr = self.thrust() / ((self.mu() / ((self.alt() + self.R_eq()) ** 2)) * self.mass())


def launch():
    lift_off()
    print("Gravity Turn")
    gravity_turn()


def Threading():
    gui_thread = threading.Thread(group=None, target=gui, name="GUI Thread")
    gui_thread.start()
    launch()
    # print(tel.vessel_velocity_vector())



def gui():
    app = QtWidgets.QApplication(sys.argv)
    form = QtWidgets.QWidget()
    unused = UiForm(form)
    form.show()
    sys.exit(app.exec_())

Threading()
