import sqlite3
import json
from datetime import datetime
from typing import Optional, Dict, List

class UserDatabase:
    def __init__(self, db_name: str = "bot_user.db"):
        self.db_name = db_name
        self.init_database()

    def init_database(self):

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            # таблица пользователей
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                           user_id INTEGER PRIMARY KEY,
                           username TEXT,
                           firstname TEXT,
                           lastname TEXT,
                           created_at TEXT DEFAULT CURRENT_TIMESTAMP
                                       )
''')
            # таблица расcчетов
            cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS calculations (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           user_id INTEGER,
                           birth_date TEXT,
                           gender TEXT,
                           country TEXT,
                           life_expectancy REAL,
                           days_lived INTEGER,
                           calculation_date TEXT DEFAULT CURRENT_TIMESTAMP,
                           FOREIGN KEY (user_id) REFERENCES users (user_id)
                           )
''')
            conn.commit()

    def add_user(self, user_id: int, username: str = None, first_name: str = None, last_name: str = None):

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO users (user_id, username, firtst_name, last_name)
                VALUES (?, ?, ?, ?)''', (user_id, username, first_name, last_name))
        conn.commit()
    
    def save_calculation(self, user_id:  int, birth_date: str, gender: str, country: str, life_expectancy:float, days_lived: int):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO calculations (user_id, birth_date, gender, country, life_expectancy, 
                           days_lived)
                           VALUES(?, ?, ?, ?, ?,?)''', (user_id, birth_date, gender, country, 
                                                              life_expectancy, days_lived))
        conn.commit()


    def get_user_calculations(self, user_id: int) -> List[Dict]:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM calculations
                WHERE user_id = ?
                ORDER BY calculation_date DESC
''', (user_id,))

        calculations = []
        for row in cursor.fetchall():
            calculations.append({
                'id' : row[0],
                'birth_date': row[2],
                'gender' : row[3],
                'country' : row[4],
                'life_expectancy' : row[5],
                'days_lived' : row[6],
                'calculation_date': row[7]
            })        
        return calculations
    

    def get_user_stats(self, user_id: int) -> Dict:

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute('SELECT COUNT(*) FROM calculations WHERE user_id = ?', (user_id,))

            total_calculations = cursor.fetchall()[0]

            cursor.execute('''
                SELECT country, life_expectancy, calculation_date
                FROM calculations
                WHERE user_id = ?
                
''', (user_id,))
            
            last_calc = cursor.fetchone()

            return {
                'total_calculations' : total_calculations,
                'last_country' : last_calc[0] if last_calc else None,
                'last_life_expectancy' : last_calc[1] if last_calc  else None,
                'last_calculation_date' : last_calc[2] if last_calc else None
            }
        
db = UserDatabase()
