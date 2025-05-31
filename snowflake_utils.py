import os
from dotenv import load_dotenv
import snowflake.connector
import pandas as pd
from snowflake.connector.pandas_tools import write_pandas
import json

# Load environment variables
load_dotenv()


class SnowflakeManager:
    def __init__(self):
        self.conn = None
        self.connect()

    def connect(self):
        """Establish connection to Snowflake"""
        try:
            self.conn = snowflake.connector.connect(
                user=os.getenv('SNOWFLAKE_USER'),
                password=os.getenv('SNOWFLAKE_PASSWORD'),
                account=os.getenv('SNOWFLAKE_ACCOUNT'),
                warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
                database=os.getenv('SNOWFLAKE_DATABASE'),
                schema=os.getenv('SNOWFLAKE_SCHEMA'),
                role=os.getenv('SNOWFLAKE_ROLE')
            )
            print("Successfully connected to Snowflake!")
        except Exception as e:
            print(f"Error connecting to Snowflake: {str(e)}")
            self.conn = None

    def create_tables(self):
        """Create necessary tables in Snowflake"""
        if not self.conn:
            return False

        try:
            cursor = self.conn.cursor()

            # Create quarterly_visitors table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS quarterly_visitors (
                    id INT AUTOINCREMENT,
                    country VARCHAR(255),
                    year INT,
                    quarter VARCHAR(10),
                    visitor_percentage FLOAT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create art_forms table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS art_forms (
                    id INT AUTOINCREMENT,
                    name VARCHAR(255),
                    region VARCHAR(100),
                    description TEXT,
                    history TEXT,
                    artists TEXT,
                    image_url VARCHAR(500),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create cultural_events table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cultural_events (
                    id INT AUTOINCREMENT,
                    name VARCHAR(255),
                    date DATE,
                    location VARCHAR(255),
                    description TEXT,
                    type VARCHAR(100),
                    region VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create heritage_sites table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS heritage_sites (
                    id INT AUTOINCREMENT,
                    name VARCHAR(255),
                    location VARCHAR(255),
                    latitude FLOAT,
                    longitude FLOAT,
                    description TEXT,
                    historical_significance TEXT,
                    image_url VARCHAR(500),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create tourism_statistics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tourism_statistics (
                    id INT AUTOINCREMENT,
                    year INT,
                    state VARCHAR(100),
                    foreign_visitors INT,
                    domestic_visitors INT,
                    growth_rate FLOAT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cursor.close()
            return True
        except Exception as e:
            print(f"Error creating tables: {str(e)}")
            return False

    def process_quarterly_visitors(self, df):
        """Process and transform quarterly visitors data"""
        # Melt the dataframe to convert quarters into rows
        quarters = [col for col in df.columns if 'quarter' in col.lower()]
        melted_df = pd.melt(
            df,
            id_vars=['Country of Nationality'],
            value_vars=quarters,
            var_name='quarter_year',
            value_name='visitor_percentage'
        )

        # Extract year and quarter from quarter_year column
        melted_df['year'] = melted_df['quarter_year'].str.extract(
            r'(\d{4})').astype(int)
        melted_df['quarter'] = melted_df['quarter_year'].str.extract(
            r'(\d{1})st|(\d{1})nd|(\d{1})rd|(\d{1})th').fillna('').apply(lambda x: ''.join(x))

        # Clean up the dataframe
        final_df = melted_df[['Country of Nationality',
                              'year', 'quarter', 'visitor_percentage']]
        final_df.columns = ['country', 'year', 'quarter', 'visitor_percentage']

        return final_df

    def load_quarterly_visitors(self, csv_path):
        """Load quarterly visitors data from CSV to Snowflake"""
        if not self.conn:
            return False

        try:
            # Read CSV
            df = pd.read_csv(csv_path)

            # Process the data
            processed_df = self.process_quarterly_visitors(df)

            # Load to Snowflake
            success, nchunks, nrows, _ = write_pandas(
                self.conn,
                processed_df,
                'QUARTERLY_VISITORS',
                database=os.getenv('SNOWFLAKE_DATABASE'),
                schema=os.getenv('SNOWFLAKE_SCHEMA')
            )
            return success
        except Exception as e:
            print(f"Error loading quarterly visitors data: {str(e)}")
            return False

    def get_quarterly_visitors(self, country=None, year=None):
        """Get quarterly visitors data with optional filters"""
        query = "SELECT * FROM quarterly_visitors"
        conditions = []

        if country:
            conditions.append(f"country = '{country}'")
        if year:
            conditions.append(f"year = {year}")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        return self.execute_query(query)

    def execute_query(self, query):
        """Execute a query and return results as a pandas DataFrame"""
        if not self.conn:
            return None

        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(results, columns=columns)
            cursor.close()
            return df
        except Exception as e:
            print(f"Error executing query: {str(e)}")
            return None

    def close(self):
        """Close the Snowflake connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
