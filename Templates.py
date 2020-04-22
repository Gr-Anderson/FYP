import sqlite3
import json
import cv2
import numpy as np
import matplotlib.pyplot as plt


class Templates:
    """
    A class for templates for ECG signals

    ...

    Methods
    -------
    create_table()
        Creates the templates table in the database if it doesn't already exist
    add_entry_to_database(features_lower, features_higher, combined_seg, x_length, y_length)
        Adds a record to the database
    convert_features_to_percentages(features, length)
        Converts the feature locations to percentages
    query_db(theName)
        Searchs for a name in the database
    does_user_exist(theName)
        Checks to see if user already exists in the database
    get_template()
        Retrieves a template from the database
    template_matching()
        Compares the template in the database with a captured one
    get_start_end_locations(self, feature_x, feature_y, image_width, image_height)
        Uses a feature to determine a area to check for a match
    create_image(biosignal, name):
        Converts a combined segment to a image for template matching
    
    """

    def __init__(self, name):
        """
        Parameters
        ----------
        name : str
            The name of the user
        conn : sqlite3.Connection
            Connection to the SQLite3 database
        c : sqlite3.Cursor
            Cursor for the SQLite3 database
        combined_seg : numpy.ndarray
            Standareised segment, standisating in nesscessary for processing
        featuresX : list
            A list of all the features on the X axis
        featuresY : list
            A list of all the features on the Y axis
        """

        self.name = name
        self.conn = sqlite3.connect("templatesDB.db")
        self.c = self.conn.cursor()
        self.create_table()
        self.combined_seg = []
        self.featuresX = []
        self.featuresY = []

    def create_table(self):
        r"""Creates the templates table in the database if it doesn't already exist

        Checks to see if table for the templates exists and creates it if it doesn't.
        The table contains the name, combined_seg, features along the X axis and 
        features along the Y axis
        """

        self.c.execute(
            """CREATE TABLE IF NOT EXISTS templates 
                                            ( name text,
                                                combined_seg text,
                                                featuresX text,
                                                featuresY text)"""
        )
        self.conn.commit()

    def add_entry_to_database(
        self, features_lower, features_higher, combined_seg, x_length, y_length
    ):
        r"""Adds a record to the database

        Adds a new user to the database. It starts by converting the feature locations
        to percentages for both the lower and higher features. This standardises the 
        locations making matching more accurate. It then adds them to the database,
        combining X axises of both lower and higher features, and doing the
        same for the Y axises. It also sotres the user and the user's standarised
        mean segment.
        
        Parameters
        ----------
        features_lower : tuple
            A tuple containing the positions of lower unique features.
        features_higher : tuple
            A tuple containing the positions of higher unique features.
        combined_seg : numpy.ndarray
            Standareised mean segment, standisatin in nesscessary for processing
        x_length : int
            The length of the X axis
        y_length : int
            The length of the Y axis 
        """
        if self.does_user_exist(self.name) != True:
            thefeaturesLowerX = self.convert_features_to_percentages(
                features_lower[0].tolist(), x_length
            )
            thefeaturesLowerY = self.convert_features_to_percentages(
                features_lower[1].tolist(), y_length
            )
            thefeaturesHigherX = self.convert_features_to_percentages(
                features_higher[0].tolist(), x_length
            )
            thefeaturesHigherY = self.convert_features_to_percentages(
                features_higher[1].tolist(), y_length
            )

            self.c.execute(
                "INSERT INTO templates VALUES (:name, :combined_seg, :featuresX, :featuresY)",
                {
                    "name": self.name,
                    "combined_seg": json.dumps(combined_seg.tolist()),
                    "featuresX": json.dumps(thefeaturesLowerX + thefeaturesHigherX),
                    "featuresY": json.dumps(thefeaturesLowerY + thefeaturesHigherY),
                },
            )

            self.conn.commit()

    def convert_features_to_percentages(self, features, length):
        r"""Converts a feature's location to a percentage

        Converts the location of a feature to a percentage for
        standardisaion. When converted to an image for template matching,
        if there is any slight difference in image size, OpenCV will
        not work. Using the x,y position of a feature as a percentage, rather
        than its true x,y corordinate in relation to the image helps solve this.
        
        Parameters
        ----------
        features : numpy.ndarray
            An array containing the features
        length : int
            The length of the features array
            
        Returns
        -------
        the_row : list
            Returns a list of ints
            
        """

        the_row = []

        for i in features:
            pos_percentage = (i * 100) // length
            the_row.append(int(pos_percentage))

        [int(i) for i in the_row]

        return the_row

    def query_db(self, theName):
        r"""Queries the database with the name provided in arguments

        Queries the database with the name provided in arguments and
        returns the result if there is one.
        
        Parameters
        ----------
        theName : str
            The name used in the query
            
        Returns
        -------
        query_response : tuple
            The result, if any, of the query
            
        """

        self.c.execute(
            "SELECT * FROM templates WHERE name IS (:name)", {"name": theName}
        )
        query_response = self.c.fetchone()
        return query_response

    def does_user_exist(self, theName):
        r"""Queries the database with the name provided in arguments

        Queries the database with the name provided in arguments and
        returns a bool.
        
        Parameters
        ----------
        theName : str
            The name used in the query
            
        Returns
        -------
        bool
            True or false, depending on if name is found in database
        """

        if self.query_db(theName) == None:
            return False
        else:
            return True

    def get_template(self, theName):
        r"""Retrieves template from the database

        Queries the database with the name provided in arguments and
        returns the result if there is one.
        
        Parameters
        ----------
        theName : str
            The name used in the query
            
        Returns
        -------
        combined_seg : list
            The users segment
        featuresX : list
            The X cordinates of the the features
        featuresY : list
            The X cordinates of the the features            
        """

        if self.does_user_exist(theName):
            query_response = self.query_db(theName)
            self.combined_seg = json.loads(query_response[1])
            self.featuresX = json.loads(query_response[2])
            self.featuresY = json.loads(query_response[3])
            return self.combined_seg, self.featuresX, self.featuresY

    def get_start_end_locations(self, feature_x, feature_y):
        r"""Identifies area to check on the template

        The features are a single point on the segment, this function
        takes the area around that point to include in the template match
        to increase its accuracity. It also takes into account where
        the point is, and if its close to an edge to make sure it doesn't
        go out of bounds.
        
        Parameters
        ----------
        feature_x : list
            The cordinates on X axis
        feature_y : list
            The cordinates on Y axis
        image_width : int
            The segments width
        image_height : int
            The segments length
            
        Returns
        -------
        x_start : int
            The starting X cordinate needed for OpenCV
        x_end : int
            The ending X cordinate needed for OpenCV
        y_start : int
            The starting Y cordinate needed for OpenCV
        y_end : type
            The ending Y cordinate needed for OpenCV  
        """

        margin = 10
        print(feature_x, feature_y)

        x_start = feature_x - margin
        y_start = feature_y - margin

        x_end = feature_x + margin
        y_end = feature_y + margin
        print(x_start, y_start, x_end, y_end)
        return x_start, y_start, x_end, y_end

    def create_image(self, biosignal, name):
        r"""Creates an image for OpenCV to use in template matching

        OpenCV requires images for template matching. This converts a
        combined segemnt to image, and saves it to the assets folder.
        
        Parameters
        ----------
        biosignal : Segment.combined_seg
            The segment to to made into an image
        name : str
            The name of segment, either capture or template
            
        """

        plt.figure(num=None, figsize=(10, 5), dpi=80, facecolor="w", edgecolor="k")
        plt.margins(0, 0)
        plt.plot(biosignal, color="#000000", linewidth=1)
        plt.axis("off")
        plt.savefig(
            "./assets/" + name + ".png",
            dpi=150,
            quality=100,
            bbox_inches="tight",
            pad_inches=0,
        )

    def template_matching(self, captured_seg):
        r"""Compares the captured template with the one in the database

        Compares the captured template with the one in the database. Loops
        through each each feature of the captured ECG signal and compares
        it to that in the database.
            
        Returns
        -------
        success_rate : float
            The success rate of the matches
        """

        #         self.featuresY =  [int(i) for i in featuresY]

        self.create_image(self.combined_seg, "template")
        self.create_image(captured_seg, "captured")

        template_ecg = cv2.imread("./assets/template.png", 0)
        captured_ecg = cv2.imread("./assets/captured.png", 0)

        total_matches = 1
        successful_matches = 1

        print("Captured: ", captured_ecg.shape, "\n")
        image_height, image_width = template_ecg.shape

        for x, y in zip(self.featuresX, self.featuresY):

            if x > 10 and x < 90 and y > 10 and y < 90:

                xpos = (image_width // 100) * x
                print(xpos)

                self.get_feature_to_match(template_ecg, xpos, image_height)
        #                 feature_to_match = template_ecg[(xpos - 100):0,(xpos + 100):image_height]
        #                 print("Feature: ", feature_to_match.shape, "\n"))

        #                 ypos = (image_height // 100) * (100 - y)
        #                 x_start, y_start, x_end, y_end = self.get_start_end_locations(xpos, ypos)

        #                 cv2.imshow('Detected',feature_to_match)
        #                 cv2.waitKey(0) & 0xFF
        #                 cv2.destroyAllWindows()
        #                 res = cv2.matchTemplate(captured_ecg,feature_to_match,cv2.TM_CCOEFF_NORMED)

        #                 threshold = 0.9
        #                 loc = np.where( res >= threshold)
        #                 if np.amax(res) > threshold:
        #                     total_matches += 1
        #                     successful_matches += 1
        #                 else:
        #                     total_matches += 1

        success_rate = (successful_matches * 100) / total_matches
        return success_rate

    def get_feature_to_match(self, template_ecg, xpos, image_height):
        print("X: ", (xpos - 100))
        print("X: ", (xpos + 100))
        #         print()
        feature_to_match = template_ecg[(xpos - 100) : 0, (xpos + 100) : image_height]
        print("Feature: ", feature_to_match.shape, "\n")
