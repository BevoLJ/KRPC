from Transfer_UI import TransferUI


class LunarTransfer(TransferUI):
    def __init__(self):
        super().__init__()



    def transfer(self):
            # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
            #               L U N A R                #
            #            T R A N S F E R             #
            # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

        self.ap.engage()
        self.control.throttle = 0

        # ui = TransferUI()

        while self.mode != "XFer":
            print("Hi")


def main():
    LunarTransfer().transfer()

main()
