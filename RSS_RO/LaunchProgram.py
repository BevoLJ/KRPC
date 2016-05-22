import threading
import sys

from PyQt5 import QtWidgets
from Flight import GravityTurn, OrbitalInsertion, ap_v_dv
from PyQt_GUI import UiForm
# from Telemetry import Readings


def grav_turn():
    # \todo\ P.I.D Control
    GravityTurn.lift_off()
    print("Gravity Turn: ")
    GravityTurn.gravity_start()
    print("entering MaxQ: ")
    GravityTurn.max_q()
    print("Passed MaxQ: ")
    GravityTurn.gravity_finish()
    orbital_insertion()


def orbital_insertion():

    OrbitalInsertion.start_insertion()
    print("Ullage Complete: ")
    OrbitalInsertion.orb_insertion()
    print("Orbit Complete: ")
    orbital_insertion()


def threading_function():
    gui_thread = threading.Thread(group=None, target=gui, name="GUI Thread")
    gui_thread.start()
    # grav_turn()
    # orbital_insertion()
    testing()
    # debug_parts()


def gui():
    app = QtWidgets.QApplication(sys.argv)
    # noinspection PyArgumentList
    form = QtWidgets.QWidget()
    # \todo\ Not use unused vars
    # noinspection PyUnusedLocal
    unused = UiForm(form)
    form.show()
    sys.exit(app.exec_())


def testing():
    # pitch = (84 - (1.2 * math.sqrt(tel.vessel.orbit.speed))) - (tar.T_ap_dV / 4.5)
    print(ap_v_dv()/5)


# def debug_parts():
#     print("testing")
#     _liquid_engs = liquid_engs(cur_stage())
#     # list_modules(_liquid_engs)
#     list_actions(_liquid_engs)


threading_function()
