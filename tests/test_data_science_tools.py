import unittest
import pandas as pd
import logging
from sklearn.datasets import make_regression
from sklearn.feature_selection import mutual_info_regression


from src.data_science.models.data_science_tools import *

class TestDataFunctions(unittest.TestCase):
    
    def test_detect_columns(self):
        """
        Test the 'detect_columns' function.
        """
        # Creating a sample DataFrame
        data = pd.DataFrame({
            'ID': [1, 2, 3],
            'Listing URL': ['url1', 'url2', 'url3'],
            'Space': ['space1', 'space2', 'space3'],
            'Price': ['$100', '$200', '$300']
        })
        
        # Testing the 'detect_columns' function with select=True and nodollar=True
        processed_data = detect_columns(data, select=True, nodollar=True)
        
        # Expected Checks
        
        # Checking for column name changes
        expected_columns = ['listing_url', 'space', 'price']
        self.assertEqual(list(processed_data.columns), expected_columns)
        
        # Checking price transformation (removing '$')
        expected_prices = [100.0, 200.0, 300.0]
        self.assertEqual(list(processed_data['price']), expected_prices)
        
        # Checking index
        self.assertEqual(processed_data.index.name, 'id')
        
    def test_delete_na(self):
        """
        Test the 'delete_na' function.
        """
        # Test data with missing values and values in the 'price' column
        data = pd.DataFrame({
            'column1': [1, 2, None, 4],
            'column2': [5, None, 7, 8],
            'price': [50, 100, 150, None]  # Missing value in 'price'
        })
        
        # Recording logs during the test
        logs = []
        def log_catcher(record):
            logs.append(record.getMessage())
        
        logging.basicConfig(format='%(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        logger.addHandler(logging.StreamHandler())
        logger.addFilter(log_catcher)
        
        # Calling the 'delete_na' function
        result = delete_na(data, vars=['column1', 'column2'], s=100)
        
        # Expected Checks
        
        # Checking missing value removal
        self.assertTrue(result['column1'].notnull().all())
        self.assertTrue(result['column2'].notnull().all())
        
        # Checking filtering on the 'price' column
        self.assertTrue((result['price'] < 100).all())
    
    def test_make_mi_scores(self):
        """
        Test the 'make_mi_scores' function.
        """
        # Generating test data
        X, y = make_regression(n_samples=100, n_features=5, noise=0.1, random_state=42)
        X = pd.DataFrame(X, columns=['feature1', 'feature2', 'feature3', 'feature4', 'feature5'])
        y = pd.Series(y, name='target')
        
        # Calling the 'make_mi_scores' function
        mi_scores = make_mi_scores(X, y)
        
        # Expected Checks
        
        # Checking if scores are numbers
        self.assertTrue(all(isinstance(score, (int, float))) for score in mi_scores)
        
        # Checking scores' length
        self.assertEqual(len(mi_scores), X.shape[1])
        

if __name__ == '__main__':
    unittest.main()