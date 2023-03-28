import cv2
from copy import deepcopy
from enum import Enum
from typing import TypeVar, List, Tuple
import os

import numpy

City_Data = Tuple[int, str, str, int, int]
Edge_Data = Tuple[int, int, float, float]


class ClickHandlerMode(Enum):
    FIRST_CLICK = 0
    SECOND_CLICK = 1
    SEARCHING = 2
    DONE = 3


class MapConnector:

    def __init__(self):
        """
        Loads the map graphic, as well as the files for the cities and the connections between them.

        """
        self.original_map_image: numpy.ndarray = cv2.imread("Major_US_Cities.png")  # by default this reads as color.

        self.load_city_data()
        self.load_connection_data()

        self.current_map: numpy.ndarray = self.draw_cities_and_connections()
        # display the map you just made in a window called "Map"
        cv2.imshow("Map", self.current_map)

    def load_city_data(self):
        """
        opens & reads the data file containing location info about cities into self.vertices.
        :return:
        """
        self.vertices: List[City_Data] = []  # an array of 5-element arrays ("City_Data"s)
        if os.path.exists("City Data with coords.txt"):
            try:
                # city data consists of tab-delimited: id#, city name, state, x-coord, y-coord
                city_data_file = open("City Data with coords.txt", "r")
                for line in city_data_file:
                    parts: List[str] = line.split("\t")
                    city: City_Data = (int(parts[0]), parts[1], parts[2], int(parts[3]), int(parts[4]))
                    self.vertices.append(city)
            except IOError as ioErr:
                print(f"Error reading City Data file: {ioErr}")
            city_data_file.close()
        else:
            print ("Could not find City Data file.")


    def load_connection_data(self):
        """
        opens & reads the data file containing roadway info about city connections into self.edges, a list of undirected edges.
        :return:
        """
        self.edges: List[Edge_Data] = []  # an array of 4-element arrays ("Edge_Data"s)

        if os.path.exists("connections.txt"):
            try:
                # connection data consists of tab-delimited: node1_id, node2_id, distance_in_meters, travel_time_in_seconds
                connection_file = open("connections.txt", "r")
                # -----------------------------------------
                # TODO: You should write the portion of this method that fills
                #       the edge list from the connection_file.


                # -----------------------------------------
            except IOError as ioErr:
                print(f"Error reading Connection Data file: {ioErr}")
            connection_file.close()
        else:
            print ("Could not find Connection Data file.")






    def start_process(self):
        """
        this is essentially our game loop - it sets up the mouse listener,
        and then enters an infinite loop where it waits for the user to select
        the two cities before it performs a search and displays the result.
        :return:
        """
        # if anybody does anything mouse-related in the "Map" window, call self.handle_click.
        cv2.setMouseCallback("Map", self.handle_click)
        self.reset()
        while True:
            while self.click_mode != ClickHandlerMode.SEARCHING:
                cv2.waitKey(1)
            path = self.perform_search()
            self.display_path(path)
            print(self.describe_path(path))

            # TODO: consider the following. No action is required.
            #  Optional: if you would like to save a copy of the graphic that results,
            #  you can say:
            #     cv2.imsave("pickAFilename.png",self.current_map).

            print("Click on screen once to start again.")
            self.click_mode = ClickHandlerMode.DONE

    def reset(self):
        """
        set the image to be shown to be one that shows vertices and edges.
        set the click mode to wait for the first click.
        :return:
        """
        self.current_map = self.draw_cities_and_connections()
        self.click_mode = ClickHandlerMode.FIRST_CLICK

    def draw_city(self, map:numpy.ndarray, city:City_Data, color:Tuple[int,int,int]=(0, 0, 128), size:int=4):
        """
        draws a dot into the graphic "map" for the given city 5-element array
        :param map: the graphic to alter
        :param city: the 5-element array from which to get location info
        :param color: # note: color is BGR, 0-255
        :param size: the radius of the dot for the city
        :return: None
        """
        cv2.circle(img=map, center=(int(city[3]), int(city[4])), radius=size, color=color,
                   thickness=-1)

    def draw_edge(self, map:numpy.ndarray, city1_id:int, city2_id:int, color:Tuple[int,int,int]=(0, 0, 0)):
        """
        draws a line into the graphic "map" for the given connection
        :param map: the graphic to alter
        :param city1_id: the 5-element array for the first city
        :param city2_id: the 5-element array for the second city, to which we connect.
        :param color: note: color is BGR, 0-255
        :return: None
        """
        point1 = (int(self.vertices[city1_id][3]), int(self.vertices[city1_id][4]))
        point2 = (int(self.vertices[city2_id][3]), int(self.vertices[city2_id][4]))
        cv2.line(img=map, pt1=point1, pt2=point2, color=color)  # note color is BGR, 0-255.

    def draw_cities_and_connections(self, draw_cities:bool=True, draw_connections:bool=True) -> numpy.ndarray:
        """
        makes a new graphic, based on a copy of the original map file, with
        the cities and connections drawn in it.
        :param draw_cities:
        :param draw_connections:
        :return: the new copy with the drawings in it.
        """
        map = deepcopy(self.original_map_image)
        if draw_cities:
            for city in self.vertices:
                self.draw_city(map, city)
        if draw_connections:
            for edge in self.edges:
                self.draw_edge(map, int(edge[0]), int(edge[1]))  # note edge is a list of strings,
                # so we have to cast to ints.
        return map

    def display_path(self, path:List[Edge_Data], line_color:Tuple[int,int,int] = (0,255,0)):
        """
        draws the edges that connect the cities in the list of cities in a
         color that makes them obvious. If the path is None, then you should
         display a message that indicates that there is no path.
         You may assume that the self.first_city and self.second_city variables are correct.
         *** Modifies the existing self.current_map graphics variable. ***

        :param path: a list of edges or None, if no path can be found.
        :param line_color: the BGR 0-255 values for the color to draw these lines over the normal black lines.
        :return: None
        """
        # -----------------------------------------
        # TODO: You should write this method
        print("You're supposed to replace this line with code to draw the path found.")


        # -----------------------------------------
        # NOTE: Don't forget to call cv2.imshow to make the screen update:
        cv2.imshow("Map", self.current_map)

    def describe_path(self, path:List[Edge_Data])->str:
        """
        Returns the list of city names corresponding to the items in path, along with the total path length
        (in km or time) of this path. If the path is None (or empty), then you should return a message "No path found."

        :param path: a list of Edges or None, if no path was found
        :return: a string describing the path.
        """

        if path is None or len(path)==0:
            return "No path found."
        result = "Path found:\n"
        # -----------------------------------------
        # TODO: You should write this method


        # -----------------------------------------
        return result

    def find_closest_city(self, pos:Tuple[int,int]) -> int:
        """
        identifies which city is closest to the coordinate given.
        :param pos: the coordinate of interest (x,y)
        :return: the index of the closest city.
        """
        dist = float("inf")
        which_city = None
        counter = 0
        for city in self.vertices:
            d_squared = (pos[0] - int(city[3])) ** 2 + (pos[1] - int(city[4])) ** 2
            if d_squared < dist:
                dist = d_squared
                which_city = counter
            counter += 1
        return which_city

    def handle_click(self, event:int, x:int, y:int, flags:int, param):
        """
        this method gets called whenever the user moves or clicks or does
        anything mouse-related while the mouse is in the "Map" window.
        In this particular case, it will only do stuff if the mouse is being
        released. What it does depends on the self.click_mode enumerated variable.
        :param event: what kind of mouse event was this?
        :param x:
        :param y:
        :param flags: I suspect this will be info about modifier keys (e.g. shift)
        :param param: additional info from cv2... probably unused.
        :return: None
        """
        if event == cv2.EVENT_LBUTTONUP:  # only worry about when the mouse is released inside this window.
            if self.click_mode == ClickHandlerMode.FIRST_CLICK:
                # we were waiting for the user to click on the first city, and she has just done so.
                # identify which city was selected, set the self.first_city_id variable
                # and display the selected city on screen.
                self.first_city_id = self.find_closest_city((x, y))
                cv2.putText(img=self.current_map, \
                            text="from: {0}, {1}".format(self.vertices[self.first_city_id][1],
                                                         self.vertices[self.first_city_id][2]), \
                            org=(0, 400), \
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, \
                            thickness=2, \
                            color=(0, 128, 0), bottomLeftOrigin=False)
                # update the screen with these changes.
                cv2.imshow("Map", self.current_map)
                # now prepare to receive the second city.
                self.click_mode = ClickHandlerMode.SECOND_CLICK
                return

            elif self.click_mode == ClickHandlerMode.SECOND_CLICK:
                # we were waiting for the user to click on the second city, and she has just done so.
                # identify which city was selected, set the self.second_city_id variable
                # and display the selected city on screen.
                self.second_city_id = self.find_closest_city((x, y))
                cv2.putText(img=self.current_map, \
                            text="to: {0}, {1}".format(self.vertices[self.second_city_id][1],
                                                       self.vertices[self.second_city_id][2]), \
                            org=(0, 420), \
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5,
                            thickness=2, \
                            color=(0, 0, 128), bottomLeftOrigin=False)
                # update the screen with these changes
                cv2.imshow("Map", self.current_map)
                # now prepare for the search process. Any further clicks while
                #   the search is in progress will be used to advance the search
                #   step by step.
                self.click_mode = ClickHandlerMode.SEARCHING
                return
            elif self.click_mode == ClickHandlerMode.SEARCHING:
                # advance to the next step
                self.waiting_for_click = False
                return

            elif self.click_mode == ClickHandlerMode.DONE:
                # we just finished the search, and user has clicked, so let's start over
                self.reset()
                cv2.imshow("Map", self.current_map)
                return

    def wait_for_click(self):
        """
        makes the program freeze until the user releases the mouse in the window.
        :return: None
        """
        if (self.click_mode != ClickHandlerMode.SEARCHING)
            raise RuntimeError("You asked to wait_for_click, but it only works in SEARCHING mode. "
                               "(Otherwise the program would freeze indefinitely.)")
        self.waiting_for_click = True
        while self.waiting_for_click:
            cv2.waitKey(1)
            # if the user clicks the mouse, then handle_click() will change the waiting_for_click variable.

    def get_neighbor_edges(self,city:int)->List[Edge_Data]:
        """
        gets a list of all edges that have the given city on one end or the other
        :param city: the id of the city in question
        :return: a list of edge_data values
        """
        result = []
        for edge in self.edges:
            if edge[0] == city or edge[1] == city:
                result.append(edge)
        return result

    def perform_search(self)->List[Edge_Data]:
        """
        finds the shortest path from self.first_city_id to self.second_city_id.
        Whether this is the shortest driving distance or the shortest time duration
        is the programmer's choice. (For testing, use distance.)
        :return: a list of EdgeData's (like what you received in describePath) that represents the path, 
        or None, if no such path can be found.
        """

        result_path:List[Edge_Data] = []
        # -----------------------------------------
        # TODO: You should write this method here.




        # Hint: if you would like to be able to pause after each cycle of the search, consider adding "wait_for_click()" inside your primary loop.
        # ...but be sure to delete it for your finished program!
        # -----------------------------------------
        return result_path
