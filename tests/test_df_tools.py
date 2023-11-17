import pandas as pd 
import unittest
from src.df_manipulation.df_tools import *

class TestCreateColumnFromMatch(unittest.TestCase):

    def setUp(self):
        # Initialize a DataFrame with sample data for testing
        self.df = pd.DataFrame({'text': ['Hello World', 'hello universe', 
                                         'goodbye world', 'world with Jacuzzi', "GLOB"]})

    def test_single_word(self):
        # Test creating a column based on a single word match
        result_df = create_column_from_match(self.df, 'text', word='hello')
        self.assertIn('hello', result_df.columns)  # Check if 'hello' column is created
        self.assertListEqual(list(result_df['hello']), [1, 1, 0, 0, 0])  # Verify the column values

    def test_words_dictionnary(self):
        # Test creating multiple columns based on a dictionary of words
        words_dict = {'hello_col': ['hello'], 'world_col': ['world', "GLOB"], 'jacuzzi_col': ['jacuzzi']}
        result_df = create_column_from_match(self.df, 'text', words_dictionnary=words_dict)

        # Expected values for each column based on the words_dict and the provided DataFrame
        expected_values_dict = {
            'hello_col': [1, 1, 0, 0, 0],  # 'hello' is in the first two texts
            'world_col': [1, 0, 1, 1, 1],  # 'world' or 'GLOB' is in all but the second text
            'jacuzzi_col': [0, 0, 0, 1, 0]  # 'jacuzzi' is in the fourth text
        }

        # Check for each key in dictionary if the corresponding column is created and verify its values
        for col_name, expected_values in expected_values_dict.items():
            self.assertIn(col_name, result_df.columns)
            self.assertListEqual(list(result_df[col_name]), expected_values)

    def test_invalid_df(self):
        # Test the function with invalid DataFrame input
        with self.assertRaises(TypeError):
            create_column_from_match("not a dataframe", 'text', word='hello')

    def test_invalid_reference_column(self):
        # Test the function with a non-existent column name
        with self.assertRaises(ValueError):
            create_column_from_match(self.df, 'non_existent_column', word='hello')

    def test_no_word_or_dictionnary(self):
        # Test the function without providing a word or a dictionary
        with self.assertRaises(ValueError):
            create_column_from_match(self.df, 'text')

    def test_both_word_and_dictionnary(self):
        # Test the function when both a single word and a dictionary are provided

        with self.assertRaises(ValueError):
            create_column_from_match(self.df, 'text', word='hello', words_dictionnary={'world_col': ['world']})

    def test_invalid_word_type(self):
        # Test the function with a non-string type for the word parameter
        with self.assertRaises(TypeError):
            create_column_from_match(self.df, 'text', word=123)


    def test_invalid_words_dictionnary_type(self):
        # Test the function with an invalid type for the words_dictionnary parameter
        with self.assertRaises(TypeError):
            create_column_from_match(self.df, 'text', words_dictionnary='hello')

    def test_empty_dictionnary(self):
        # Test the function with an empty dictionary
        result_df = create_column_from_match(self.df, 'text', words_dictionnary={})
        self.assertEqual(result_df.shape[1], self.df.shape[1])  # No new columns should be added

class TestCountAmenities(unittest.TestCase):
    def setUp(self):
        # Set up sample data for testing
        self.example_amenities = [
            '["Microwave", "Wifi", "Iron"]',
            '["Iron", "Air conditioning", "Wifi"]',
            '["Wifi", "Heating"]'
        ]
        # Create a DataFrame from the sample data
        self.df_example = pd.DataFrame({'amenities': self.example_amenities})

    def test_basic_count(self):
        # Test if the function correctly counts the frequency of 'Wifi'
        result = count_amenities(self.df_example)
        self.assertEqual(result.loc[result['Amenity'] == 'Wifi', 'Frequency'].values[0], 3)

    def test_data_cleaning(self):
        # Test if the function properly cleans the data (removes quotes)
        result = count_amenities(self.df_example)
        self.assertNotIn('"', result['Amenity'].values)

    def test_sorting(self):
        # Test if the amenities are sorted correctly in descending order of frequency
        result = count_amenities(self.df_example)
        self.assertTrue(result.iloc[0]['Frequency'] >= result.iloc[-1]['Frequency'])

    def test_output_format(self):
        # Test if the output DataFrame is formatted correctly (correct column names)
        result = count_amenities(self.df_example)
        self.assertTrue(set(result.columns) == {'Amenity', 'Frequency'})

if __name__ == '__main__':
    unittest.main()

