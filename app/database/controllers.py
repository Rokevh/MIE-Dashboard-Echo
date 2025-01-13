"""
NAME:          database\controllers.py
AUTHOR:        Alan Davies (Lecturer Health Data Science)
EMAIL:         alan.davies-2@manchester.ac.uk
DATE:          17/12/2019
INSTITUTION:   University of Manchester (FBMH)
DESCRIPTION:   Contains the Database class that contains all the methods used for accessing the database
"""

from sqlalchemy.sql import func
from flask import Blueprint

from app import db
from app.database.models import PrescribingData, PracticeData

database = Blueprint('dbutils', __name__, url_prefix='/dbutils')

class Database:
    """Class for managing database queries."""
    
    def convert_tuple_list_to_raw(self, tuple_list):
        """Helper function to convert results from tuple list to plain list."""
        order_row = [tuple(row) for row in tuple_list]
        return  [item for i in order_row for item in i]
    
    def get_total_number_items(self):
        """Return the total number of prescribed items."""
        result = int(db.session.execute(db.select(func.sum(PrescribingData.items))).first()[0])
        return result
    
    def get_unique_item_count(self):
        result = len(db.session.execute(db.select(PrescribingData.BNF_code).distinct()).all())
        return result
    
    def get_average_ACT_Cost(self):
        """Return the average number of ACT cost."""
        avg_act_cost = float(db.session.execute(db.select(func.avg(PrescribingData.ACT_cost))).first()[0]) 
        result = round(avg_act_cost,2)
        return result
    
    def get_total_GP_number(self):
        '''Use practice dt to find the number of unique gp practices'''
        result = len(db.session.execute(db.select(PracticeData.practice_code).distinct()).all())
        print(result)
        return result
            
    def get_prescribed_items_per_pct(self):
        """Return the total items per PCT."""
        result = db.session.execute(db.select(func.sum(PrescribingData.items).label('item_sum')).group_by(PrescribingData.PCT)).all()
        return self.convert_tuple_list_to_raw(result)

    def get_distinct_pcts(self):
        """Return the distinct PCT codes."""
        result = db.session.execute(db.select(PrescribingData.PCT).distinct()).all()
        return self.convert_tuple_list_to_raw(result)

    def get_n_data_for_PCT(self, pct, n):
        """Return all the data for a given PCT."""
        return db.session.query(PrescribingData).filter(PrescribingData.PCT == pct).limit(n).all()