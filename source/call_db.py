import os
import sqlite3


def options_in_db(type_: str = "croptown"):
    db_path = os.path.join(os.getcwd(), "web_options.db")
    option_conn = sqlite3.connect(db_path)
    option_cur = option_conn.cursor()
    
    # Extract all attr elements
    option_cur.execute("SELECT DISTINCT attr FROM data;")
    
    unique_attr = [i[0] for i in option_cur.fetchall()] # as the fetch results are list of tuples

    # As a key(attr)-value(List of tuple) structure
    all_options = {}
    for attr_ in unique_attr:
        # query
        options_query = f'SELECT value, label FROM data WHERE type = ? AND attr = ?;'

        # Extract for each attr
        option_cur.execute(options_query, (type_, attr_))

        # Saving to dictionary
        all_options[attr_] = option_cur.fetchall()
    
    option_conn.close()

    return all_options

class Option():
    def __init__(self, dict_):
        self.year = dict_['accountingyear']
        self.item = dict_['item']
        self.crop = dict_['crop']
        self.city = dict_['city']
    
    def value_dict(self, attribute: str, reverse: bool = False) -> dict:
        if hasattr(self, attribute):
            if reverse:
                return {i[1]: i[0] for i in getattr(self, attribute)}
            else:
                return {i[0]: i[1] for i in getattr(self, attribute)}
        raise AttributeError(f"'Option' object has no attribute '{attribute}'")
    
