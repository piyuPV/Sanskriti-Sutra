from snowflake_utils import SnowflakeManager
import pandas as pd
from pathlib import Path

def init_snowflake():
    """Initialize Snowflake database with our data"""
    # Initialize Snowflake manager
    sf_manager = SnowflakeManager()
    
    # Create tables
    if not sf_manager.create_tables():
        print("Failed to create tables")
        return
    
    # Load data from CSV files
    assets_path = Path("assets")
    
    # Load quarterly visitors data
    print("Loading quarterly visitors data...")
    if sf_manager.load_quarterly_visitors(assets_path / "Country Quater Wise Visitors.csv"):
        print("Successfully loaded quarterly visitors data")
    else:
        print("Failed to load quarterly visitors data")
    
    # Load art forms data
    print("Loading art forms data...")
    art_forms_df = pd.read_csv(assets_path / "art_forms.csv")
    if sf_manager.load_data_from_csv(art_forms_df, "art_forms"):
        print("Successfully loaded art forms data")
    else:
        print("Failed to load art forms data")
    
    # Load cultural events data
    print("Loading cultural events data...")
    events_df = pd.read_csv(assets_path / "festivals_kaggle.csv")
    if sf_manager.load_data_from_csv(events_df, "cultural_events"):
        print("Successfully loaded cultural events data")
    else:
        print("Failed to load cultural events data")
    
    # Load heritage sites data
    print("Loading heritage sites data...")
    heritage_df = pd.read_csv(assets_path / "WORLD HERITAGE SITES 2024 UPDATED.csv")
    if sf_manager.load_data_from_csv(heritage_df, "heritage_sites"):
        print("Successfully loaded heritage sites data")
    else:
        print("Failed to load heritage sites data")
    
    # Load tourism statistics
    print("Loading tourism statistics...")
    tourism_df = pd.read_csv(assets_path / "foreignVisit.csv")
    if sf_manager.load_data_from_csv(tourism_df, "tourism_statistics"):
        print("Successfully loaded tourism statistics")
    else:
        print("Failed to load tourism statistics")
    
    print("Successfully initialized Snowflake database!")
    
    # Close connection
    sf_manager.close()

if __name__ == "__main__":
    init_snowflake()