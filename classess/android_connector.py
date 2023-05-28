from PIL.Image import Image
from com.dtmilano.android.viewclient import ViewClient
from classess.scenarios import Scenario


class AndroidConnector:
    def __init__(self):
        self.device, self.serialno = ViewClient.connectToDeviceOrExit()
        self.vc = ViewClient(self.device, self.serialno)

    def prepare_image(self):
        scr: Image = self.device.takeSnapshot(reconnect=True)
        scr.save(r"images\scr.png")
        return scr

    def press_boxes(self, board, scenario: Scenario):
        """
        Here we press on squares that match solution
        :param board:
        :param scenario:
        :return:
        """
        scx = scenario.start_cell_x
        scy = scenario.start_cell_y
        step = scenario.step
        for x in range(board.shape[0]):
            for y in range(board.shape[1]):
                if board[y, x] == 1:
                    self.vc.click(scx + step * x, scy + step * y)

    def click_continue(self):
        self.vc.click(500, 2200)

    def click_play(self):
        self.vc.click(500, 2200)

