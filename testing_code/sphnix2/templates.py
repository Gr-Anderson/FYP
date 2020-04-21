class Templates:
    """
    A class for templates for ECG signals

    ...

    Methods
    -------
    create_table()
        Creates the templates table in the database if it doesn't already exist
    add_entry_to_database(self, features_lower, features_higher, standardised_mean_segment, x_length, y_length)
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
    get_feature_location(self, x, y, image_width, image_height)
        ddddd
    get_feature_from_template(self, db_template_ecg, x_start, x_end, y_start, y_end)
        sssssss
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
            Connection for the SQLite3 database
        standardised_mean_segment : numpy.ndarray
            Standareised mean segment, standisatin in nesscessary for processing
        featuresX : list
            A list of all the features on the X axis
        featuresY : list
            A list of all the features on the Y axis
        """

        self.name = name
        self.conn = sqlite3.connect('templatesDB.db')
        self.c = self.conn.cursor()
        self.create_table()
        self.standardised_mean_segment = []
        self.featuresX = []
        self.featuresY = []
    
    def create_table(self):
        r"""Creates the templates table in the database if it doesn't already exist

        Checks to see if table for the templates exists and creates it if it doesn't.
        The table contains the name, mean_segment, features along the X axis and 
        features along the Y axis
        """
        self.c.execute("""CREATE TABLE IF NOT EXISTS templates 
                                            ( name text,
                                                mean_segment text,
                                                featuresX text,
                                                featuresY text)""")
        self.conn.commit()
    
    
    def add_entry_to_database(self, features_lower, features_higher, standardised_mean_segment,
                          x_length, y_length):
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
        standardised_mean_segment : numpy.ndarray
            Standareised mean segment, standisatin in nesscessary for processing
        x_length : int
            The length of the X axis
        y_length : int
            The length of the Y axis 
        """
        if self.does_user_exist(self.name) != True:
            thefeaturesLowerX = self.convert_features_to_percentages(features_lower[0].tolist(), x_length)
            thefeaturesLowerY = self.convert_features_to_percentages(features_lower[1].tolist(), y_length)
            thefeaturesHigherX = self.convert_features_to_percentages(features_higher[0].tolist(), x_length)
            thefeaturesHigherY = self.convert_features_to_percentages(features_higher[1].tolist(), y_length)

            self.c.execute("INSERT INTO templates VALUES (:name, :mean_segment, :featuresX, :featuresY)",
                                                {'name': self.name,
                                                 'mean_segment': json.dumps(standardised_mean_segment.tolist()),
                                                 'featuresX': json.dumps(thefeaturesLowerX + thefeaturesHigherX),
                                                 'featuresY': json.dumps(thefeaturesLowerY + thefeaturesHigherY)})


            self.conn.commit()
        
        
    def convert_features_to_percentages(self, features, length):
        r"""Converts a feature's location to a percentage

        Converts the location of a feature to a percentage for
        standardisaion. Standardisation helps with template matching.
        
        Parameters
        ----------
        features : numpy.ndarray
            description
        length : int
            The length of the features
            
        Returns
        -------
        the_row : list
            Returns a list of ints
            
        """
        
        the_row = []

        for value in features:
            pos_percentage = (value * 100) // length
            the_row.append(pos_percentage)
            
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
        
        self.c.execute("SELECT * FROM templates WHERE name IS (:name)", {'name': theName})
        query_response=(self.c.fetchone())        
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
        
        if self.query_db(theName) == []:
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
        standardised_mean_segment : list
            The users segment
        featuresX : list
            The X cordinates of the the features
        featuresY : list
            The X cordinates of the the features            
        """
        
        if self.does_user_exist(theName):
            query_response = self.query_db(theName)
            self.standardised_mean_segment = json.loads(query_response[1])
            self.featuresX = json.loads(query_response[2])
            self.featuresY = json.loads(query_response[3])
            return self.standardised_mean_segment, self.featuresX, self.featuresY
    
    
    def template_matching(self):
        r"""Compares the captured template with the one in the database

        Compares the captured template with the one in the database. Loops
        through each each feature of the captured ECG signal and compares
        it to that in the database.
            
        Returns
        -------
        success_rate : float
            The success rate of the matches
        """
        
        self.featuresY =  [int(i) for i in featuresY]
     
        db_template_ecg = cv2.imread("./assets/db_template.png", 0)
        captured_ecg = cv2.imread("./assets/TEST_standardised_mean_segment.png", 0)

        
        total_matches = 0
        successful_matches = 0
        
        for x,y in zip(self.featuresX, self.featuresY):
            
            if x > 10 and x < 90 and y > 10 and y < 90 :

                image_width, image_height = db_template_ecg.shape        
                feature_x, feature_y = self.get_feature_location(x, y, image_width, image_height)
                x_start, x_end, y_start, y_end = self.get_start_end_locations(feature_x, feature_y, image_width, image_height)

                feature_to_match = self.get_feature_from_template(db_template_ecg, x_start, x_end, y_start, y_end)

                w, h = feature_to_match.shape[::-1]
                res = cv2.matchTemplate(captured_ecg,feature_to_match,cv2.TM_CCOEFF_NORMED)

                threshold = 0.9      
                loc = np.where( res >= threshold)
                if np.amax(res) > threshold:
                    total_matches += 1
                    successful_matches += 1
                else:
                    total_matches += 1

        success_rate = (successful_matches * 100) / total_matches
        return success_rate
    

    
    def get_start_end_locations(self, feature_x, feature_y, image_width, image_height):
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
        
        if feature_x < margin:
            x_start = feature_x
        else:
            x_start = feature_x - margin

        if feature_x > image_width:
            x_end = image_width
        else:
            x_end = feature_x + margin  

        if feature_y < margin:
            y_start = 0
        else:
            y_start = feature_y - margin

        if feature_y > image_height:
            y_end = image_height
        else:
            y_end = feature_y + margin
            
        return x_start, x_end, y_start, y_end
            
            
    def get_feature_location(self, x, y, image_width, image_height):
        r"""Converts a feature location to a percentage

        Converts a feature location to a percentage for standardisaion.
        Standardisation makes template matching more accurate.
        
        Parameters
        ----------
        x : int
            description
        y : int
            description
        image_width : int
            description
        image_height : int
            description
            
        Returns
        -------
        feature_x : int
            description
        feature_y : int
            description
        """
        
        feature_x = (image_width // 100) * x
        feature_y = (image_height // 100) * y
        return feature_x, feature_y
    
    def get_feature_from_template(self, db_template_ecg, x_start, x_end, y_start, y_end):
        r"""Gets feature from template to check

        Converts a feature location to a percentage for standardisaion.
        Standardisation makes template matching more accurate.
        
        Parameters
        ----------
        name : type
            description
            
        Returns
        -------
        name : type
            description
            
        """
        
        feature_to_match = db_template_ecg[x_start:y_start,x_end:y_end]
        return feature_to_match