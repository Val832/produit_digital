import pandas as pd 
import unittest
from src.df_manipulation.df_tools import *

class TestCreateColumnFromMatch(unittest.TestCase):

    def setUp(self):
        # Initialize a DataFrame with sample data for testing
        self.df = pd.DataFrame({'text': ['Hello World', 'hello universe', 
                                         'goodbye world', 'world with Jacuzzi']})
    
    def test_single_word(self):
        # Test creating a column based on a single word match
        result_df = create_column_from_match(self.df, 'text', word='hello')
        self.assertIn('hello', result_df.columns)  # Check if 'hello' column is created
        self.assertListEqual(list(result_df['hello']), [1, 1, 0, 0])  # Verify the column values

    def test_words_list(self):
        # Test creating multiple columns based on a list of words
        result_df = create_column_from_match(self.df, 'text', 
                                             words_list=['hello', 'world', 'jacuzzi'])
        # Check for each word if the corresponding column is created and verify its values
        for word in ['hello', 'world', 'jacuzzi']:
            self.assertIn(word, result_df.columns)
        self.assertListEqual(list(result_df['hello']), [1, 1, 0, 0])
        self.assertListEqual(list(result_df['world']), [1, 0, 1, 1])
        self.assertListEqual(list(result_df['jacuzzi']), [0, 0, 0, 1])
    
    def test_invalid_df(self):
        # Test the function with invalid DataFrame input
        with self.assertRaises(TypeError):
            create_column_from_match("not a dataframe", 'text', word='hello')
    
    def test_invalid_reference_column(self):
        # Test the function with a non-existent column name
        with self.assertRaises(ValueError):
            create_column_from_match(self.df, 'non_existent_column', word='hello')
    
    def test_no_word_or_list(self):
        # Test the function without providing a word or a list of words
        with self.assertRaises(ValueError):
            create_column_from_match(self.df, 'text')
    
    def test_both_word_and_list(self):
        # Test the function when both a single word and a list of words are provided
        with self.assertRaises(ValueError):
            create_column_from_match(self.df, 'text', word='hello', words_list=['world'])
    
    def test_invalid_word_type(self):
        # Test the function with a non-string type for the word parameter
        with self.assertRaises(TypeError):
            create_column_from_match(self.df, 'text', word=123)
    
    def test_invalid_words_list_type(self):
        # Test the function with an invalid type for the words_list parameter
        with self.assertRaises(TypeError):
            create_column_from_match(self.df, 'text', words_list='hello')
    
    def test_invalid_element_in_words_list(self):
        # Test the function with a non-string element in the words list
        with self.assertRaises(TypeError):
            create_column_from_match(self.df, 'text', words_list=['hello', 123])


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

