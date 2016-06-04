from Boot import BootUp


class EngineManager(BootUp):

    def __init__(self):
        super().__init__()

    # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
    #   E N G   M o d R F   A C T I O N S    #
    # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

    @staticmethod
    def engine_actions(eng_to_activate, action):
        for _eng in eng_to_activate:
            _mods = _eng.modules
            for _mod in _mods:
                if _mod.name == "ModuleEnginesRF":
                    _mod.set_action(action, True)

    def active_next_stage_engines(self):
        _stage = self.get_active_engine().decouple_stage
        for _eng in self.engines:
            if _eng.decouple_stage == (_stage - 1): _eng.engine.active = True

    def eng_status(self):
        _mod = self.get_active_engine().modules
        for _m in _mod:
            if _m.name == "ModuleEnginesRF":
                return _m.get_field("Status")

    def get_active_engine(self):
        for _eng in self.engines:
            if _eng.engine.active: return _eng

    def eng_list_tuples(self):
        _list_eng_tuples = []
        for _part in self.engines:
            _eng_tup = (_part.stage, _part)
            _list_eng_tuples.append(_eng_tup)
        _list_eng_tuples.sort()

        return _list_eng_tuples

    def current_stage_engs(self):
        _stage_num_set = set()
        _englist = []
        _list_eng_tuples = self.eng_list_tuples
        for _part in self.engines:
            _stage_num_set.update(str(_part.stage))
        _num_stages = len(_stage_num_set)

        _next_stage_engs_list = [item for item in _list_eng_tuples if item[0] == _num_stages]

        while len(_next_stage_engs_list) > 0:
            _eng = _next_stage_engs_list.pop()
            _englist.append(_eng[1])

        return _englist

    def next_stage_isp(self):
        for _en in self.current_stage_engs():
            return _en.engine.vacuum_specific_impulse

    def next_stage_thrust(self):
        for _en in self.current_stage_engs():
            return _en.engine.max_thrust * 1000

    @staticmethod
    def _example_(_list):
        for item in _list:
            return item

    # def liquid_engs(self):
    #
    #     _liquid = []
    #     for _eng in self.engines:
    #         if _eng.engine.can_restart:
    #             if _eng.stage == _stage:
    #                 _liquid.append(_eng)
    #     return _liquid
    #
    # def ullage(self, ullage_method):
    #     self.control.throttle = 0
    #     self.engine_actions(self.liquid_engs(cur_stage()), 'Shutdown Engine')
    #     time.sleep(1.5)
    #     if ullage_method == "Solid":
    #         self.control.activate_next_stage()
    #     time.sleep(1)
    #     self.control.throttle = 1
    #     while self.prop_status() == "Very Unstable":
    #         time.sleep(0.2)
    #     time.sleep(1)
    #     self.engine_actions(liquid_engs(cur_stage()), 'Activate Engine')
