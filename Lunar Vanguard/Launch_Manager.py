import numpy
from Operation import Operations
from numba import jit


class LaunchManager(Operations):

    def __init__(self):
        super().__init__()

        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        #         S E T   H E A D I N G          #
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

    def pitch_and_heading(self):

        if self.vessel_speed() < 80:
            self.ap.target_pitch_and_heading(90, 90)
        elif self.vessel_speed() < 2200 or (self.apoapsis_altitude() < (self.target_orbit_alt * .92)):
            self.ap.target_pitch_and_heading(self.gravity_pitch(), self.azimuth_init())
        else:
            self.ap.target_pitch_and_heading(self.insertion_pitch() / 3.5, self.azimuth_init())

    def gravity_pitch(self):
        _t_ap_dv = self.target_apoapsis_speed_dv()
        _speed = self.vessel_speed()

        @jit(nopython=True)
        def pitch_calcs():
            _pitch = (90 - (1.22 * numpy.sqrt(_speed))) + (_t_ap_dv / 6)
            return _pitch
        return pitch_calcs()

    def insertion_pitch(self):
        _circ_dv = self.circ_dv()
        _t_ap_dv = self.target_apoapsis_speed_dv()

        @jit(nopython=True)
        def pitch_calcs():
            if _circ_dv > 2000:
                return _t_ap_dv / 3
            elif _circ_dv > 1000:
                return _t_ap_dv / 2
            else:
                if _t_ap_dv >= 0:
                    return min(_t_ap_dv / 6, 10)
                else:
                    return max(_t_ap_dv / 6, -10)

        return pitch_calcs()

    # /todo/ BROKEN! Need to fix
    def azimuth_init(self):

        _R_eq = self.radius_eq
        _inc = float(self.target_orbit_inc)
        _lat = self.latitude()
        _to = float(self.target_orbit_alt)
        _µ = self.gravitational_parameter
        _Rot_p = self.rotational_period()
        node = "Ascending"

        if _inc < 0:
            node = "Descending"
            _inc = numpy.fabs(_inc)

        if (numpy.fabs(_lat)) > _inc:
            _inc = numpy.fabs(_lat)
        if (180 - numpy.fabs(_lat)) < _inc:
            _inc = (180 - numpy.fabs(_lat))

        @jit(nopython=True)
        def Az_calcs():
            velocity_eq = (2 * numpy.pi * _R_eq) / _Rot_p
            t_orb_v = numpy.sqrt(_µ / (_to + _R_eq))

            inert_az = numpy.arcsin(max(min(numpy.cos(_inc / numpy.cos(_lat)), 1), -1))
            _VXRot = t_orb_v * numpy.sin(inert_az) - velocity_eq * numpy.cos(_lat)
            _VYRot = t_orb_v * numpy.cos(inert_az)

            return numpy.fmod(numpy.arctan2(_VXRot, _VYRot) + 360, 360)

        _az = Az_calcs()

        # This is wrong.  Should return just _az
        # need to figure out why it always returns 0
        if node == "Ascending":
            return _az + 90  # I should not need the +90 here

        if node == "Descending":
            if _az <= 90:
                return 180 - _az
            elif _az >= 270:
                return 540 - _az
