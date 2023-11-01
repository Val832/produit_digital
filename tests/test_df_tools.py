import pandas as pd 
import unittest
from src.df_manipulation.df_tools import create_column_from_match

class TestCreateColumnFromMatch(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({'text': ['Hello World', 'hello universe', 
                                         'goodbye world', 'world with Jacuzzi']})
    
    def test_single_word(self):
        result_df = create_column_from_match(self.df, 'text', word='hello')
        self.assertIn('hello', result_df.columns)
        self.assertListEqual(list(result_df['hello']), [1, 1, 0, 0])
    
    def test_words_list(self):
        result_df = create_column_from_match(self.df, 'text', 
                                             words_list=['hello', 'world', 'jacuzzi'])
    
        for word in ['hello', 'world', 'jacuzzi']:
            self.assertIn(word, result_df.columns)
        self.assertListEqual(list(result_df['hello']), [1, 1, 0, 0])
        self.assertListEqual(list(result_df['world']), [1, 0, 1, 1])
        self.assertListEqual(list(result_df['jacuzzi']), [0, 0, 0, 1])
    
    def test_invalid_df(self):
        with self.assertRaises(TypeError):
            create_column_from_match("not a dataframe", 'text', word='hello')
    
    def test_invalid_reference_column(self):
        with self.assertRaises(ValueError):
            create_column_from_match(self.df, 'non_existent_column', word='hello')
    
    def test_no_word_or_list(self):
        with self.assertRaises(ValueError):
            create_column_from_match(self.df, 'text')
    
    def test_both_word_and_list(self):
        with self.assertRaises(ValueError):
            create_column_from_match(self.df, 'text', word='hello', words_list=['world'])
    
    def test_invalid_word_type(self):
        with self.assertRaises(TypeError):
            create_column_from_match(self.df, 'text', word=123)
    
    def test_invalid_words_list_type(self):
        with self.assertRaises(TypeError):
            create_column_from_match(self.df, 'text', words_list='hello')
    
    def test_invalid_element_in_words_list(self):
        with self.assertRaises(TypeError):
            create_column_from_match(self.df, 'text', words_list=['hello', 123])
    
if __name__ == '__main__':
    unittest.main()

