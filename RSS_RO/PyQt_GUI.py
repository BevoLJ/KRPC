import threading
from PyQt5 import QtCore, QtWidgets
from Telemetry import Telemetry, TargetOrb
from Flight import azimuth_init, gravity_pitch

Tar_orb = 175000
inc = 29

tel = Telemetry()
tar = TargetOrb(Tar_orb)
Az = azimuth_init(tar)
Pitch = gravity_pitch(tar)


class UiForm(object):
    # noinspection PyArgumentList
    def __init__(self, form):
        super().__init__()
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        #           G U I  L A Y O U T           #
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

        form.setObjectName("Form")
        form.resize(612, 360)
        form.setMinimumSize(QtCore.QSize(400, 230))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.main_layout.setObjectName("main_layout")

        self.Mode_Section = QtWidgets.QHBoxLayout()
        self.Mode_Section.setObjectName("Mode_Section")
        self.mode_label = QtWidgets.QLabel(form)
        self.mode_label.setObjectName("mode_label")
        self.Mode_Section.addWidget(self.mode_label)
        self.setMode_label = QtWidgets.QLabel(form)
        self.setMode_label.setObjectName("setMode_label")
        self.Mode_Section.addWidget(self.setMode_label)
        self.main_layout.addLayout(self.Mode_Section)

        self.LCD_Section = QtWidgets.QHBoxLayout()
        self.LCD_Section.setObjectName("LCD_Section")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.left_lvl_1 = QtWidgets.QLabel(form)
        self.left_lvl_1.setObjectName("left_lvl_1")
        self.verticalLayout_7.addWidget(self.left_lvl_1)
        self.left_lbl_2 = QtWidgets.QLabel(form)
        self.left_lbl_2.setObjectName("left_lbl_2")
        self.verticalLayout_7.addWidget(self.left_lbl_2)
        self.left_lbl_3 = QtWidgets.QLabel(form)
        self.left_lbl_3.setObjectName("left_lbl_3")
        self.verticalLayout_7.addWidget(self.left_lbl_3)
        self.left_lbl_4 = QtWidgets.QLabel(form)
        self.left_lbl_4.setObjectName("left_lbl_4")
        self.verticalLayout_7.addWidget(self.left_lbl_4)
        self.left_lbl_5 = QtWidgets.QLabel(form)
        self.left_lbl_5.setObjectName("left_lbl_5")
        self.verticalLayout_7.addWidget(self.left_lbl_5)
        self.left_lbl_6 = QtWidgets.QLabel(form)
        self.left_lbl_6.setObjectName("left_lbl_6")
        self.verticalLayout_7.addWidget(self.left_lbl_6)
        self.LCD_Section.addLayout(self.verticalLayout_7)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.left_lcd_1 = QtWidgets.QLCDNumber(form)
        self.left_lcd_1.setObjectName("left_lcd_1")
        self.verticalLayout_6.addWidget(self.left_lcd_1)
        self.left_lcd_2 = QtWidgets.QLCDNumber(form)
        self.left_lcd_2.setObjectName("left_lcd_2")
        self.verticalLayout_6.addWidget(self.left_lcd_2)
        self.left_lcd_3 = QtWidgets.QLCDNumber(form)
        self.left_lcd_3.setObjectName("left_lcd_3")
        self.verticalLayout_6.addWidget(self.left_lcd_3)
        self.left_lcd_4 = QtWidgets.QLCDNumber(form)
        self.left_lcd_4.setObjectName("left_lcd_4")
        self.verticalLayout_6.addWidget(self.left_lcd_4)
        self.left_lcd_5 = QtWidgets.QLCDNumber(form)
        self.left_lcd_5.setObjectName("left_lcd_5")
        self.verticalLayout_6.addWidget(self.left_lcd_5)
        self.left_lcd_6 = QtWidgets.QLCDNumber(form)
        self.left_lcd_6.setObjectName("left_lcd_6")

        self.verticalLayout_6.addWidget(self.left_lcd_6)
        self.LCD_Section.addLayout(self.verticalLayout_6)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.right_lbl_1 = QtWidgets.QLabel(form)
        self.right_lbl_1.setObjectName("right_lbl_1")
        self.verticalLayout_5.addWidget(self.right_lbl_1)
        self.right_lbl_2 = QtWidgets.QLabel(form)
        self.right_lbl_2.setObjectName("right_lbl_2")
        self.verticalLayout_5.addWidget(self.right_lbl_2)
        self.right_lbl_3 = QtWidgets.QLabel(form)
        self.right_lbl_3.setObjectName("right_lbl_3")
        self.verticalLayout_5.addWidget(self.right_lbl_3)
        self.right_lbl_4 = QtWidgets.QLabel(form)
        self.right_lbl_4.setObjectName("right_lbl_4")
        self.verticalLayout_5.addWidget(self.right_lbl_4)
        self.right_lbl_5 = QtWidgets.QLabel(form)
        self.right_lbl_5.setObjectName("right_lbl_5")
        self.verticalLayout_5.addWidget(self.right_lbl_5)
        self.right_lbl_6 = QtWidgets.QLabel(form)
        self.right_lbl_6.setObjectName("right_lbl_6")
        self.verticalLayout_5.addWidget(self.right_lbl_6)
        self.LCD_Section.addLayout(self.verticalLayout_5)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.right_lcd_1 = QtWidgets.QLCDNumber(form)
        self.right_lcd_1.setObjectName("right_lcd_1")
        self.verticalLayout_4.addWidget(self.right_lcd_1)
        self.right_lcd_2 = QtWidgets.QLCDNumber(form)
        self.right_lcd_2.setObjectName("right_lcd_2")
        self.verticalLayout_4.addWidget(self.right_lcd_2)
        self.right_lcd_3 = QtWidgets.QLCDNumber(form)
        self.right_lcd_3.setObjectName("right_lcd_3")
        self.verticalLayout_4.addWidget(self.right_lcd_3)
        self.right_lcd_4 = QtWidgets.QLCDNumber(form)
        self.right_lcd_4.setObjectName("right_lcd_4")
        self.verticalLayout_4.addWidget(self.right_lcd_4)
        self.right_lcd_5 = QtWidgets.QLCDNumber(form)
        self.right_lcd_5.setObjectName("right_lcd_5")
        self.verticalLayout_4.addWidget(self.right_lcd_5)
        self.right_lcd_6 = QtWidgets.QLCDNumber(form)
        self.right_lcd_6.setObjectName("right_lcd_6")
        self.verticalLayout_4.addWidget(self.right_lcd_6)
        self.LCD_Section.addLayout(self.verticalLayout_4)
        self.LCD_Section.setStretch(1, 1)
        self.LCD_Section.setStretch(3, 1)

        self.main_layout.addLayout(self.LCD_Section)
        self.editing_section = QtWidgets.QHBoxLayout()
        self.editing_section.setObjectName("editing_section")
        self.parkingOrbit_section = QtWidgets.QVBoxLayout()
        self.parkingOrbit_section.setObjectName("parkingOrbit_section")
        self.parkingOrbit_label = QtWidgets.QLabel(form)
        self.parkingOrbit_label.setObjectName("parkingOrbit_label")
        self.parkingOrbit_section.addWidget(self.parkingOrbit_label)
        self.parkingOrbit_line_edit = QtWidgets.QLineEdit(form)
        self.parkingOrbit_line_edit.setObjectName("parkingOrbit_line_edit")
        self.parkingOrbit_section.addWidget(self.parkingOrbit_line_edit)
        self.editing_section.addLayout(self.parkingOrbit_section)
        self.Inc_section = QtWidgets.QVBoxLayout()
        self.Inc_section.setObjectName("Inc_section")
        self.inclination_label = QtWidgets.QLabel(form)
        self.inclination_label.setObjectName("inclination_label")
        self.Inc_section.addWidget(self.inclination_label)
        self.inclination_line_edit = QtWidgets.QLineEdit(form)
        self.inclination_line_edit.setObjectName("inclination_line_edit")
        self.Inc_section.addWidget(self.inclination_line_edit)
        self.editing_section.addLayout(self.Inc_section)
        self.checkBox_section = QtWidgets.QVBoxLayout()
        self.checkBox_section.setObjectName("checkBox_section")
        self.booster_checkbox = QtWidgets.QCheckBox(form)
        self.booster_checkbox.setObjectName("booster_checkbox")
        self.checkBox_section.addWidget(self.booster_checkbox)
        self.something_checkbox = QtWidgets.QCheckBox(form)
        self.something_checkbox.setObjectName("something_checkbox")
        self.checkBox_section.addWidget(self.something_checkbox)
        self.editing_section.addLayout(self.checkBox_section)
        self.button_sections = QtWidgets.QVBoxLayout()
        self.button_sections.setObjectName("button_sections")
        self.launch_button = QtWidgets.QPushButton(form)
        self.launch_button.setObjectName("launch_button")
        self.button_sections.addWidget(self.launch_button)
        self.abort_button = QtWidgets.QPushButton(form)
        self.abort_button.setObjectName("abort_button")
        self.button_sections.addWidget(self.abort_button)
        self.editing_section.addLayout(self.button_sections)
        self.main_layout.addLayout(self.editing_section)
        self.main_layout.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.main_layout)

        self.translate_ui(form)
        QtCore.QMetaObject.connectSlotsByName(form)

        self.my_timer = QtCore.QTimer()
        # noinspection PyUnresolvedReferences
        self.my_timer.timeout.connect(self.display_updater)
        self.my_timer.start(200)

    # noinspection PyArgumentList,PyTypeChecker
    def translate_ui(self, form):
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        #               T E X T                  #
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

        _translate = QtCore.QCoreApplication.translate
        form.setWindowTitle(_translate("Form", "Form"))
        self.mode_label.setText(_translate("Form",
                                           "<html><head/><body><p align=\"right\"><span style=\" font-size:12pt; "
                                           "font-weight:600; text-decoration: underline;\">Current Mode:"
                                           "</span></p></body></html>"))
        self.setMode_label.setText(_translate("Form",
                                              "<html><head/><body><p><span style=\" font-size:12pt; "
                                              "font-weight:600;\">Mode</span></p></body></html>"))
        self.parkingOrbit_label.setText(_translate("Form", "Parking Orbit"))
        self.inclination_label.setText(_translate("Form", "Inclination"))
        self.booster_checkbox.setText(_translate("Form", "Boosters"))
        self.something_checkbox.setText(_translate("Form", "Something"))
        self.launch_button.setText(_translate("Form", "Launch"))
        self.abort_button.setText(_translate("Form", "Abort"))

        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        #         L C D    L A B E L S           #
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

        self.left_lvl_1.setText(_translate("Form", "Apoapsis"))
        self.left_lbl_2.setText(_translate("Form", "Periapsis"))
        self.left_lbl_3.setText(_translate("Form", "Altitude"))
        self.left_lbl_4.setText(_translate("Form", "Speed"))
        self.left_lbl_5.setText(_translate("Form", "Pitch"))
        self.left_lbl_6.setText(_translate("Form", "Heading"))
        self.right_lbl_1.setText(_translate("Form", "Ap ETA"))
        self.right_lbl_2.setText(_translate("Form", "Pe ETA"))
        self.right_lbl_3.setText(_translate("Form", "Q"))
        self.right_lbl_4.setText(_translate("Form", "TWR"))
        self.right_lbl_5.setText(_translate("Form", "Set Pitch"))
        self.right_lbl_6.setText(_translate("Form", "Set Heading"))

    def display_updater(self):
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        #                 L C D                  #
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

        self.left_lcd_1.display(tel.apoapsis())
        self.left_lcd_2.display(float(tel.periapsis()))
        self.left_lcd_3.display(float(tel.alt()))
        self.left_lcd_4.display(float(tel.vessel_speed()))
        self.left_lcd_5.display(float(tel.vessel_pitch()))
        self.left_lcd_6.display(float(tel.heading()))
        self.right_lcd_1.display(float(tel.ETAap()))
        self.right_lcd_2.display(float(tar.T_ap_dV / 4.5))
        self.right_lcd_3.display(tel.Q())
        self.right_lcd_4.display(Telemetry().twr)
        self.right_lcd_5.display(gravity_pitch(tar))
        self.right_lcd_6.display(azimuth_init(tar))

        self.setMode_label.setText(
            "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Mode</span></p></body></html>")
