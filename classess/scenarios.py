from typing import Protocol


class Scenario(Protocol):
    @property
    def start_cell_x(self):
        raise NotImplemented("Method was not implemented")

    @property
    def start_cell_y(self):
        raise NotImplemented("Method was not implemented")

    @property
    def step(self):
        raise NotImplemented("Method was not implemented")

    @property
    def distance_between_panel_element(self):
        raise NotImplemented("Method was not implemented")

    @property
    def size_of_panel_element(self):
        raise NotImplemented("Method was not implemented")

    @property
    def size_of_number(self):
        raise NotImplemented("Method was not implemented")

    @property
    def num_of_elements(self):
        raise NotImplemented("Method was not implemented")

    @property
    def min_len_between_numbers(self):
        raise NotImplemented("Method was not implemented")


class HardLevelScenario(Scenario):
    @property
    def start_cell_x(self):
        return 220

    @property
    def start_cell_y(self):
        return 705

    @property
    def step(self):
        return 57

    @property
    def distance_between_panel_element(self):
        return 6

    @property
    def size_of_panel_element(self):
        return 52

    @property
    def size_of_number(self):
        return 15

    @property
    def num_of_elements(self):
        return 15

    @property
    def min_len_between_numbers(self):
        return 10



class MediumLevelScenario(Scenario):
    @property
    def start_cell_x(self):
        return 220

    @property
    def start_cell_y(self):
        return 705

    @property
    def step(self):
        return 84

    @property
    def distance_between_panel_element(self):
        return 6

    @property
    def size_of_panel_element(self):
        return 80

    @property
    def size_of_number(self):
        return 18

    @property
    def num_of_elements(self):
        return 10

    @property
    def min_len_between_numbers(self):
        return 13

class BasicLevelScenario(Scenario):
    @property
    def start_cell_x(self):
        return 220

    @property
    def start_cell_y(self):
        return 705

    @property
    def step(self):
        return 170

    @property
    def distance_between_panel_element(self):
        return 6

    @property
    def size_of_panel_element(self):
        return 168

    @property
    def size_of_number(self):
        return 20

    @property
    def num_of_elements(self):
        return 5

    @property
    def min_len_between_numbers(self):
        return 13


