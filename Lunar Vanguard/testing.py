from Launch_Manager import LaunchManager
import time


class Testing(LaunchManager):

    def __init__(self):
        super().__init__()

        self.target_orbit_inc = 28

        self.lAz_data = self.azimuth_init()

        self.main()

        while True:
            time.sleep(1)

    def main(self):
        # print(self.lAz_data)
        print("Test all things")
        print(self.azimuth_init2(self.lAz_data))


Testing()
