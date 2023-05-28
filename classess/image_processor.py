from PIL.Image import Image
import classess.numbers_recognition as numbers_recognition


class ImageProcessor:
    def __init__(self, image: Image):
        self.image = image
        self.scenario = self.get_scenario()

    def get_scenario(self):
        return numbers_recognition.get_scenario(self.image.crop(box=(350, 140, 750, 200)))

    """Next 2 functions defensively might be written better, but I'm tired"""

    def crop_top_panel(self):
        """Crop the image to extract the top panel."""
        top_panel = self.image.crop(box=(196, 477, 1066, 667))
        top_panel.save(r"images\tp.png")
        return top_panel

    def crop_left_panel(self):
        """Crop the image to extract the left panel."""
        left_panel = self.image.crop(box=(12, 678, 186, 1542))
        left_panel.save(r"images\lp.png")
        return left_panel

    def recognize_numbers_in_panel(self, top_panel):
        """Recognize the numbers in the top panel."""
        return numbers_recognition.recognize_numbers(top_panel, self.scenario.size_of_number)

    def process_recognized_numbers_top(self, recognized_numbers):
        """
        Processes the list of recognized numbers from the top panel of the image.

        Args:
            recognized_numbers: list[tuple(int, int, int), int] - List of recognized numbers, where each number is a
            tuple with its coordinates and its numerical value.

        Returns:
            List of processed numbers where each number is in a format [(coordinate_x, coordinate_y), value].
        """

        # The size of an individual element on the panel, retrieved from the scenario
        size_of_el = self.scenario.size_of_panel_element

        # Initialize an empty list to store processed numbers
        numbers = []

        # Process each number from the recognized numbers list
        while recognized_numbers:
            found = False  # Flag to mark if a number has been processed

            # Pop an element from the list for processing
            el = recognized_numbers.pop()

            # Check each existing processed number in the numbers list
            for kv in numbers:

                # If the x-coordinate of the popped element lies within the range of an existing number's
                # x-coordinate (± half the size of the element)
                # and y-coordinate lies within the range of ±3 of the existing number's y-coordinate
                if kv[0][0] - (size_of_el / 2) < el[0][0] < kv[0][0] + (size_of_el / 2) \
                        and kv[0][1] - 3 < el[0][1] < kv[0][1] + 3:

                    # If x coordinate of left el bigger, then it must be first digit of number
                    if el[0][0] > kv[0][0]:
                        kv[1] = kv[1] * 10 + el[1]
                    else:
                        kv[1] = el[1] * 10 + kv[1]

                    # Mark that a number has been processed and merged
                    found = True

            # If the popped element's coordinates do not lie within the range of any existing number
            # Append it as a new number to the list
            if not found:
                numbers.append([(el[0][0], el[0][1]), el[1]])

        # Return the list of processed numbers
        return numbers


    def group_numbers_into_elements_top(self, numbers):
        """Group the numbers into their respective elements in the top panel."""
        size_of_el = self.scenario.size_of_panel_element
        dist_between_el = self.scenario.distance_between_panel_element
        num_of_el = self.scenario.num_of_elements
        tpn = []

        for i in range(num_of_el):
            tmp = [number for number in numbers if
                   size_of_el * i + dist_between_el * i < number[0][0] < size_of_el * (i + 1) + dist_between_el * i]
            tmp.sort(key=lambda x: x[0][1])
            tpn.append([el[1] for el in tmp])

        return tpn

    def group_numbers(self, recognized_numbers):
        """Group the numbers based on their proximity to other numbers."""
        size_of_el = self.scenario.size_of_panel_element
        numbers = []

        while recognized_numbers:
            found = False
            el = recognized_numbers.pop()

            for kv in numbers:
                if kv[0] - (size_of_el / 2) < el[0][1] < kv[0] + (size_of_el / 2):
                    kv[1].append(el)
                    found = True

            if not found:
                numbers.append([el[0][1], [el]])

        return numbers

    def group_numbers_into_elements_left(self, numbers):
        """
        Groups the processed numbers into their respective elements in the left panel.

        Args:
            numbers: List of processed numbers where each number is in a format [(coordinate_x, coordinate_y), value].

        Returns:
            List of numbers grouped by elements in the left panel.
        """

        # Extract the number of elements in the scenario
        num_of_el = self.scenario.num_of_elements

        # Minimum distance between two numbers (used to determine whether two numbers are part of the same group)
        min_len_btw_num = self.scenario.min_len_between_numbers

        # Initialize an empty list to store groups of numbers
        lpn = []

        # Iterate over the range of elements
        for i in range(num_of_el):

            # If the group contains only one number
            if len(numbers[i][1]) == 1:

                # Append the number to the group list and proceed to the next group
                lpn.append([numbers[i][1][0][1]])
                continue

            # Initialize an empty group
            lpn.append([])

            # Iterate over the numbers in the current group
            while numbers[i][1]:

                # If there are more than one number and the distance between two consecutive numbers is less than the minimum
                if len(numbers[i][1]) > 1 and numbers[i][1][1][0][0] - numbers[i][1][0][0][2] < min_len_btw_num:

                    # Merge the two numbers and append them to the group
                    lpn[i].append(numbers[i][1][0][1] * 10 + numbers[i][1][1][1])

                    # Remove the two numbers from the original list
                    numbers[i][1].pop(0)
                    numbers[i][1].pop(0)
                else:
                    # If the above condition is not satisfied, append the number as it is to the group
                    lpn[i].append(numbers[i][1].pop(0)[1])

        # Return the groups of numbers
        return lpn

    def recognize_top_panel(self):
        """Main function to recognize numbers in the top panel."""
        top_panel = self.crop_top_panel()
        recognized_numbers = self.recognize_numbers_in_panel(top_panel)
        numbers = self.process_recognized_numbers_top(recognized_numbers)
        numbers.sort(key=lambda x: x[0][0])
        return self.group_numbers_into_elements_top(numbers)

    def recognize_left_panel(self):
        """Main function to recognize numbers in the left panel."""
        left_panel = self.crop_left_panel()
        recognized_numbers = self.recognize_numbers_in_panel(left_panel)
        recognized_numbers.sort(key=lambda x: x[0][1])
        numbers = self.group_numbers(recognized_numbers)
        numbers.sort(key=lambda x: x[0])
        [number[1].sort(key=lambda x: x[0][0]) for number in numbers]
        return self.group_numbers_into_elements_left(numbers)