# clean_data.py
import pandas as pd
import os  # Import os for file operations

def clean_supplement_data(input_filepath="data/supplements_order_data.csv",
                          output_filepath="data/cleaned_supplements_order_data.csv"):
    """
    Loads raw supplement order data, cleans it by handling null values and ensuring
    'product_category' is always a string, and saves the cleaned data.

    Cleaning steps:
    1. Drop rows where 'product_category' is explicitly null/NaN.
    2. Explicitly convert 'product_category' to string type for all values.
       This handles cases where categories might be numbers (e.g., 123, 45.0) in the raw data.
       It will convert 123.0 to "123".
    3. Fill any remaining nulls in 'product_category' (after string conversion) with 'Unknown'.
    4. Fill nulls in numeric columns with 0.
    5. Fill other object/string columns' nulls with 'Unknown'.
    """
    print(f"Attempting to load data from: {input_filepath}")
    try:
        df = pd.read_csv(input_filepath)
        print(f"Raw data loaded. Shape: {df.shape}")

        # --- Cleaning Logic ---

        # 1. Drop rows where 'product_category' is explicitly null/NaN
        initial_rows = df.shape[0]
        if 'product_category' in df.columns:
            df.dropna(subset=['product_category'], inplace=True)
            dropped_rows = initial_rows - df.shape[0]
            if dropped_rows > 0:
                print(f"Dropped {dropped_rows} rows due to null 'product_category'.")
        else:
            print("Warning: 'product_category' column not found in raw data. Skipping specific cleaning for it.")
            # If column not found, can't clean it. Proceed with other cleaning.

        # 2. Explicitly convert 'product_category' to string type for all values
        if 'product_category' in df.columns:
            # Convert all values in 'product_category' to string.
            df['product_category'] = df['product_category'].astype(str)

            # Optional: Refine numeric strings (e.g., "1.0" -> "1")
            df['product_category'] = df['product_category'].apply(
                lambda x: str(int(float(x))) if isinstance(x, str) and x.replace('.', '', 1).isdigit() and '.' in x else x
            )
            print("Ensured 'product_category' column is string type and refined numeric strings.")

        # 3. Fill any remaining nulls in 'product_category' with 'Unknown'
        if 'product_category' in df.columns and df['product_category'].isnull().any():
            df['product_category'].fillna('Unknown', inplace=True)
            print("Filled any remaining nulls in 'product_category' with 'Unknown'.")

        # 4. Fill nulls in numeric columns with 0
        numeric_cols = ['product_price', 'shipping_price', 'discount', 'subtotal', 'taxes', 'total_price',
                        'verified_buyer_number']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                if df[col].isnull().any():
                    print(f"Filled nulls/non-numeric in '{col}' with 0.")

        # 5. Fill nulls in other string/object columns with 'Unknown'
        for col in df.columns:
            if df[col].dtype == 'object' and df[col].isnull().any():
                df[col].fillna('Unknown', inplace=True)
                print(f"Filled remaining nulls in object column '{col}' with 'Unknown'.")

        print(f"Cleaned data shape: {df.shape}")
        df.to_csv(output_filepath, index=False)
        print(f"Cleaned data saved to: {output_filepath}")
        return True

    except FileNotFoundError:
        print(f"Error: Input file not found at {input_filepath}")
        return False
    except pd.errors.EmptyDataError:
        print(f"Error: Input file {input_filepath} is empty.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during data cleaning: {e}")
        return False


if __name__ == "__main__":
    # Example usage when running clean_data.py directly
    print("Running data cleaning script for demonstration...")
    # Create a dummy CSV with mixed types and nulls for testing
    # IMPORTANT:  Use 'supplements_order_data.csv' to match what main.py expects.
    dummy_raw_data_filepath = 'data/supplements_order_data.csv'
    dummy_cleaned_data_filepath = 'data/cleaned_supplements_order_data.csv'
    dummy_data_with_nulls = {
        'supplier_name': ['A', 'B', None, 'D', 'E', 'F', 'G'],  # NOW 7 elements to match others
        'product_category': ['Protein', 'L-Carnitine', None, 'Creatine', 123.0, 'Pre-Workout',
                             789],  # 7 elements
        'product_description': ['Whey', 'Liquid', 'Amino', None, 'Bar', 'Energy', None],  # 7 elements
        'product_price': [30.0, None, 25.0, 40.0, 10.0, 35.0, 20.0],  # 7 elements
        'shipping_price': [2.0, 1.5, None, 3.0, 1.0, 2.5, 1.8],  # 7 elements
        'top_flavor_rated': ['Chocolate', 'Lemon', None, 'Vanilla', 'Strawberry', 'Grape', 'Orange'],  # 7 elements
        'verified_buyer_number': [100, 50, None, 200, 75, 120, None]  # 7 elements
    }
    dummy_df_with_nulls = pd.DataFrame(dummy_data_with_nulls)
    # Corrected file name here
    dummy_df_with_nulls.to_csv(dummy_raw_data_filepath, index=False)
    print(
        "Created dummy CSV with nulls and mixed product_category types for demonstration:", dummy_raw_data_filepath)

    # Call the cleaning function, using the correct filepaths
    clean_supplement_data(input_filepath=dummy_raw_data_filepath,
                          output_filepath=dummy_cleaned_data_filepath)
    print("\nCleaning complete. Check 'data/cleaned_supplements_order_data.csv'")

    # Clean up dummy files
    if os.path.exists(dummy_raw_data_filepath):
        os.remove(dummy_raw_data_filepath)
        print(f"Removed dummy raw file: {dummy_raw_data_filepath}")
    if os.path.exists(dummy_cleaned_data_filepath):
        os.remove(dummy_cleaned_data_filepath)
        print(f"Removed dummy cleaned file: {dummy_cleaned_data_filepath}")
