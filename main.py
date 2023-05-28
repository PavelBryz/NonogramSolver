from time import sleep

from classess.android_connector import AndroidConnector
from classess.image_processor import ImageProcessor
from classess.nonogram_solver import solver


if __name__ == '__main__':
    android_connector = AndroidConnector()
    while True:
        android_connector.prepare_image()
        image_processor = ImageProcessor(android_connector.prepare_image())
        # Wait until some scenario found. It means that board is loaded
        while image_processor.scenario is None:
            sleep(1)
            image_processor.image = android_connector.prepare_image()
            print("Try to get scenario")
            image_processor.scenario = image_processor.get_scenario()
        board = solver(image_processor.recognize_top_panel(), image_processor.recognize_left_panel(), None)
        print(f"{'Solution':-^30}")
        print(board)
        android_connector.press_boxes(board, image_processor.scenario)
        sleep(7)
        android_connector.click_continue()
        sleep(2)
        android_connector.click_play()

