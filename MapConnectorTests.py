import unittest
import cv2
from MapConnectorFile import MapConnector


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.connector = MapConnector()

    def test_0_load_edges(self):
        self.assertEqual(204, len(self.connector.edges), "You haven't loaded the correct number of edges.")

    # Test #1 is a little annoying after you get it working, so you might wish to uncomment the next line once
    #   you've passed the test.
    # @unittest.skip("Skipping test 1.")
    def test_1_display_path(self):
        """
        Note: this also depends on your having a working load_connection_data() method in MapConnector. If you haven't
        written it yet, you'll see an index error since you are trying to get item 47 from an empty list.

        There are no actual tests in this -- you're just checking that a window shows up with the pink line described.
        """
        edge_nums = [47, 51, 33, 32, 19, 11]
        example_path = []
        for num in edge_nums:
            example_path.append(self.connector.edges[num])
        self.connector.first_city_id = 49
        self.connector.second_city_id = 89
        print("You should see a pink line connecting Helena, MT to San Antonio, TX.")
        self.connector.display_path(example_path, line_color=(128, 128, 255))
        print("Press any key to continue.")
        cv2.waitKey()
        cv2.destroyAllWindows()

    def test_2_print_no_path(self):
        self.assertEqual("No path found.", self.connector.describe_path(None),
                         "If path is None, we should get a message.")

    def test_3_east_west_path_description(self):
        edge_nums = [90, 54, 48, 2]
        path = []
        self.connector.first_city_id = 96
        self.connector.second_city_id = 95
        expected = ("Path found:\n• Madison, WI\n• Minneapolis, MN\n• Bismarck, ND\n• Helena, MT\n• Seattle, WA\n"
                    "total_distance = 103318.0	total_time = 3053590.0")
        print(f"You are starting at city #{self.connector.first_city_id}, which is "
              f"{self.connector.vertices[self.connector.first_city_id]}.")
        print("You're being given a path that includes the following: \n\tCity1\tCity2\tdist\ttime")
        for num in edge_nums:
            path.append((self.connector.edges[num]))
            print(f"\t{self.connector.edges[num]}")
        print(
            f"You are ending at city #{self.connector.second_city_id}, which is "
            f"{self.connector.vertices[self.connector.second_city_id]}.")

        print("-------The computer is expecting the following description -----")
        print(expected)
        print("----------------------------------------------------------------")
        print("Now you are building your own description.")
        result = self.connector.describe_path(path)
        print("------- You described this as ----------------------------------")
        print(result)
        print("----------------------------------------------------------------")
        self.assertEqual(expected, result, "East->West path did not match. You might have the correct cities, but "
                                           "different spacing/punctuation. Be sure to check the comparison.")
        # self.connector.display_path(path, line_color=(128, 128, 255))
        # cv2.waitKey()
        # cv2.destroyAllWindows()

    def test_4_west_east_path_description(self):
        edge_nums = [4, 73, 50, 52, 56, 58, 89, 133, 138, 179, 180]

        path = []
        self.connector.first_city_id = 72
        self.connector.second_city_id = 65
        expected = ("Path found:\n• Portland, OR\n• Boise, ID\n• Salt Lake City, UT\n• Cheyenne, WY\n• Lincoln, NE\n"
                    "• Omaha, NE\n• Des Moines, IA\n• Chicago, IL\n• Toledo, OH\n• Cleveland, OH\n• Buffalo, NY\n"
                    "• Syracuse, NY\ntotal_distance = 156894.0	total_time = 4640760.0")

        print(f"You are starting at city #{self.connector.first_city_id}, which is "
              f"{self.connector.vertices[self.connector.first_city_id]}.")
        print("You're being given a path that includes the following: \n\tCity1\tCity2\tdist\ttime")
        for num in edge_nums:
            path.append((self.connector.edges[num]))
            print(f"\t{self.connector.edges[num]}")
        print(f"You are ending at city #{self.connector.second_city_id}, which is "
              f"{self.connector.vertices[self.connector.second_city_id]}.")

        print("-------The computer is expecting the following description -----")
        print(expected)
        print("----------------------------------------------------------------")
        print("Now you are building your own description.")
        result = self.connector.describe_path(path)
        print("------- You described this as ----------------------------------")
        print(result)
        print("----------------------------------------------------------------")
        self.assertEqual(expected, result,
                         "West->East path did not match. You might have the correct cities, but different "
                         "spacing/punctuation. Be sure to check the comparison.")
        # self.connector.display_path(path, line_color=(128, 128, 255))
        # cv2.waitKey()
        # cv2.destroyAllWindows()

    def test_5_zig_zag_path_description(self):

        edge_nums = [203, 123, 99, 15, 17, 24]

        path = []
        self.connector.first_city_id = 58
        self.connector.second_city_id = 4
        expected = ("Path found:\n• Albuquerque, NM\n• Oklahoma City, OK\n• Little Rock, AR\n• Dallas, TX\n"
                    "• Fort Worth, TX\n• El Paso, TX\n• Tucson, AZ\ntotal_distance = 112256.0	total_time = 3462014.0")
        print(f"You are starting at city #{self.connector.first_city_id}, which is "
              f"{self.connector.vertices[self.connector.first_city_id]}.")
        print("You're being given a path that includes the following: \n\tCity1\tCity2\tdist\ttime")
        for num in edge_nums:
            path.append((self.connector.edges[num]))
            print(f"\t{self.connector.edges[num]}")
        print(
            f"You are ending at city #{self.connector.second_city_id}, which is "
            f"{self.connector.vertices[self.connector.second_city_id]}.")

        print("-------The computer is expecting the following description -----")
        print(expected)
        print("----------------------------------------------------------------")
        print("Now you are building your own description.")
        result = self.connector.describe_path(path)
        print("------- You described this as ----------------------------------")
        print(result)
        print("----------------------------------------------------------------")
        self.assertEqual(expected, result,
                         "ZigZag path did not match. You might have the correct cities, but different "
                         "spacing/punctuation. Be sure to check the comparison.")
        # self.connector.display_path(path, line_color=(128, 128, 255))
        # cv2.waitKey()
        # cv2.destroyAllWindows()

    # NOTE: Tests 6-9 are optimized for DISTANCE, not TIME.

    def test_6_find_very_short_path(self):
        edge_nums = [54, 55]
        expected_path = []
        for num in edge_nums:
            expected_path.append((self.connector.edges[num]))
        self.connector.first_city_id = 53  # Bismark
        self.connector.second_city_id = 79  # Pierre

        result = self.connector.perform_search()
        self.assertEqual(expected_path, result, "Extra Short path did not match expected.")

    def test_7_find_short_path(self):
        edge_nums = [131, 143, 142]
        expected_path = []
        for num in edge_nums:
            expected_path.append((self.connector.edges[num]))
        self.connector.first_city_id = 28  # Chicago
        self.connector.second_city_id = 81  # Memphis

        result = self.connector.perform_search()
        self.assertEqual(expected_path, result, "Short path did not match expected.")

    def test_8_find_medium_path(self):
        edge_nums = [3, 73, 35, 36, 31]
        expected_path = []
        for num in edge_nums:
            expected_path.append((self.connector.edges[num]))
        self.connector.first_city_id = 95  # Seattle
        self.connector.second_city_id = 4  # Tuscon

        result = self.connector.perform_search()
        self.assertEqual(expected_path, result, "Medium path did not match expected.")

    def test_9_find_long_path(self):
        edge_nums = [121, 118, 151, 156, 161, 175, 174, 189, 186, 188, 193]
        expected_path = []
        for num in edge_nums:
            expected_path.append((self.connector.edges[num]))
        self.connector.first_city_id = 21  # Miami
        self.connector.second_city_id = 93  # Montpellier

        result = self.connector.perform_search()
        self.assertEqual(expected_path, result, "Long path did not match expected.")
