import sqlite3
import json
import cv2

class Templates:
    
    def __init__(self):
        self.conn = sqlite3.connect('templatesDB.db')
        self.c = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS templates 
                                            ( name text,
                                                mean_segment text,
                                                featuresLowerX text,
                                                featuresLowerY text,
                                                featuresHigherX text,
                                                featuresHigherY text)""")
        self.conn.commit()
        
    def convert_features_to_percentages(self, features, length):
        the_row = []

        for value in features:
            pos_percentage = (value * 100) // length
            the_row.append(pos_percentage)
            
        return the_row
    
    def add_entry_to_database(self, features_lower, features_higher, theName, standardised_mean_segment,
                              x_length, y_length):
            
        if self.does_user_exist(theName) != True:
            self.thefeaturesLowerX = self.convert_features_to_percentages(features_lower[0].tolist(), x_length)
            self.thefeaturesLowerY = self.convert_features_to_percentages(features_lower[1].tolist(), y_length)
            self.thefeaturesHigherX = self.convert_features_to_percentages(features_higher[0].tolist(), x_length)
            self.thefeaturesHigherY = self.convert_features_to_percentages(features_higher[1].tolist(), y_length)

            self.c.execute("INSERT INTO templates VALUES (:name, :mean_segment, :featuresLowerX, :featuresLowerY, :featuresHigherX, :featuresHigherY)",
                                                {'name': theName,
                                                 'mean_segment': json.dumps(standardised_mean_segment.tolist()),
                                                 'featuresLowerX': json.dumps(self.thefeaturesLowerX),
                                                 'featuresLowerY': json.dumps(self.thefeaturesLowerY),
                                                 'featuresHigherX': json.dumps(self.thefeaturesHigherX),
                                                 'featuresHigherY': json.dumps(self.thefeaturesHigherY)})

            
            self.conn.commit()

    def query_db(self, theName):
        self.c.execute("SELECT * FROM templates WHERE name IS (:name)", {'name': theName})
        query_response=(self.c.fetchall()) # change this on fetchone        
        return query_response
    
    def does_user_exist(self, theName):
        if self.query_db(theName) == []:
            return False
        else:
            return True
        
    def get_template(self, theName):
        self.does_user_exist(theName)
        query_response = self.query_db(theName)
        standardised_mean_segment = json.loads(query_response[0][1])
        featuresLowerX = json.loads(query_response[0][2])
        featuresLowerY = json.loads(query_response[0][3])
        featuresHigherX = json.loads(query_response[0][4])
#         featuresHigherY = "TEST TEST TEST"
        featuresHigherY = json.loads(query_response[0][5])
        return standardised_mean_segment, featuresLowerX, featuresLowerY, featuresHigherX, featuresHigherY

    
    
    def template_matching(self, featuresLowerX, featuresLowerY, featuresHigherX, featuresHigherY):
        x_cors = featuresLowerX + featuresHigherX
        y_cors = featuresLowerY + featuresHigherY
        y_cors =  [int(i) for i in y_cors]
     
        db_template_ecg = cv2.imread("./assets/db_template.png", 0)
        captured_ecg = cv2.imread("./assets/TEST_standardised_mean_segment.png", 0)

        
        total_matches = 0
        successful_matches = 0
        
        for x,y in zip(x_cors, y_cors):
            
            
            if x > 10 and x < 90 and y > 10 and y < 90 :

                image_width, image_height = db_template_ecg.shape        
                feature_x, feature_y = self.get_feature_location(db_template_ecg, x, y, image_width, image_height)
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
            
            
    def get_feature_location(self, db_template_ecg, x, y, image_width, image_height):
        
        feature_x = (image_width // 100) * x
        feature_y = (image_height // 100) * y
        return feature_x, feature_y
    
    def get_feature_from_template(self, db_template_ecg, x_start, x_end, y_start, y_end):
        feature_to_match = db_template_ecg[x_start:y_start,x_end:y_end]
#         feature_to_match = db_template_ecg[70:500,160:570]
#         print(feature_to_match.shape)
        return feature_to_match
    
    
    def show_image(self):
        cv2.imshow('Detected',captured_ecg)
        cv2.waitKey(0) & 0xFF
        cv2.destroyAllWindows()
    
# TEST_templates = Templates()
# TEST_the_name = 'Sam'
# TEST_templates.add_entry_to_database(TEST_features_lower, TEST_features_higher, TEST_the_name,
#                                      TEST_standardised_mean_segment, len(TEST_combined_seg), 
#                                      len(TEST_standardised_mean_segment))
# TEST_query_response = TEST_templates.query_db(TEST_the_name)
# TEST_standardised_mean_segment, TEST_featuresLowerX, TEST_featuresLowerY, TEST_featuresHigherX, TEST_featuresHigherY = TEST_templates.get_template(TEST_the_name)

# TEST_templates.template_matching(TEST_featuresLowerX, TEST_featuresLowerY, TEST_featuresHigherX, TEST_featuresHigherY)
