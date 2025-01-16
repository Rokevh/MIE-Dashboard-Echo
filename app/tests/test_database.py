"""
NAME:          test_database.py
AUTHOR:        Alan Davies (Lecturer Health Data Science)
EMAIL:         alan.davies-2@manchester.ac.uk
DATE:          24/12/2019
INSTITUTION:   University of Manchester (FBMH)
DESCRIPTION:   Suite of tests for testing the dashboards database
               functionality.
"""

import unittest
from sqlalchemy.sql import func
from app import app, db
from app.database.controllers import Database
from app.database.controllers import PrescribingData, PracticeData

class DatabaseTests(unittest.TestCase):
    """Class for testing database functionality and connection."""
    def setUp(self):
        """Run prior to each test."""
        self.db_mod = Database()

    def tearDown(self):
        """Run post each test."""
        pass

    def test_get_total_number_items(self):
        with app.app_context():
            """Test that the total number of items returns the correct value."""
            self.assertEqual(self.db_mod.get_total_number_items(), 8218165, 'Test total items returns correct value')

    def test_get_average_ACT_Cost(self):
        with app.app_context():
            """Define the min and max ACT costs using SQLAlchemy"""
            ACT_min = int(db.session.execute(db.select(func.min(PrescribingData.items))).first()[0])
            ACT_max = int(db.session.execute(db.select(func.max(PrescribingData.items))).first()[0])
            """Test that the average ACT cost is between the min/max costs"""
            self.assertTrue(ACT_min <= self.db_mod.get_average_ACT_Cost() <= ACT_max)

    def test_get_unique_item_count(self):
        with app.app_context():
            """Test that the total number of unique items is less than or equal to the total number of items in dt"""
            self.assertLessEqual(self.db_mod.get_unique_item_count(), 8218165, 'Test unique items returns correct value')

    def test_get_total_GP_number(self):
        with app.app_context():
            """Test that the total number of GP practices returns the correct value"""
            self.assertEqual(self.db_mod.get_total_GP_number(), 9348, 'Test total GP practices returns correct value')

if __name__ == "__main__":
    unittest.main()