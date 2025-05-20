# clean_data.py
import pandas as pd

def clean_supplement_data(input_filepath="bodybuilding_nutrition_products.csv",
                          output_filepath="cleaned_supplements_order_data.csv"):
    """
    Loads raw supplement order data, cleans it by handling null values,
    and saves the cleaned data to a new CSV file.

    Cleaning steps:
    1. Drop rows where 'product_category' is null (as this is crucial for recommendations).
    2. Fill numeric columns' nulls with 0 (e.g., price, discount, taxes).
    3. Fill other object/string columns' nulls with an empty string or 'Unknown'.
    4. Convert 'product_category' to string type (just in case).
    """
    print(f"Attempting to load data from: {input_filepath}")
    try:
        df = pd.read_csv(input_filepath)
        print(f"Raw data loaded. Shape: {df.shape}")

        # --- Cleaning Logic ---

        # 1. Drop rows where 'product_category' is null
        # This column is essential for recommendations, so rows without it are problematic.
        initial_rows = df.shape[0]
        df.dropna(subset=['product_category'], inplace=True)
        dropped_rows = initial_rows - df.shape[0]
        if dropped_rows > 0:
            print(f"Dropped {dropped_rows} rows due to null 'product_category'.")

        # 2. Fill nulls in numeric columns with 0
        numeric_cols = ['product_price', 'shipping_price', 'discount', 'subtotal', 'taxes', 'total_price']
        for col in numeric_cols:
            if col in df.columns:
                if df[col].isnull().any():
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                    print(f"Filled nulls in '{col}' with 0.")

        # 3. Fill nulls in other string/object columns with 'Unknown' or empty string
        for col in df.columns:
            if df[col].dtype == 'object' and df[col].isnull().any():
                df[col].fillna('Unknown', inplace=True) # Or ''
                print(f"Filled nulls in '{col}' with 'Unknown'.")

        # 4. Ensure product_category is string type
        if 'product_category' in df.columns:
            df['product_category'] = df['product_category'].astype(str)
            print("Ensured 'product_category' column is string type.")

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
    print("Running data cleaning script...")
    # Create a dummy CSV with nulls for testing
    dummy_data_with_nulls = {
        'supplier_name': ['A', 'B', None, 'D'],
        'product_category': ['Protein', 'L-Carnitine', None, 'Creatine'],
        'product_description': ['Whey', 'Liquid', 'Amino', None],
        'product_price': [30.0, None, 25.0, 40.0],
        'shipping_price': [2.0, 1.5, None, 3.0]
    }
    dummy_df_with_nulls = pd.DataFrame(dummy_data_with_nulls)
    dummy_df_with_nulls.to_csv('supplements_order_data.csv', index=False)
    print("Created dummy CSV with nulls for demonstration.")

    clean_supplement_data()
    print("\nCleaning complete. Check 'cleaned_supplements_order_data.csv'")

    # Clean up dummy file
    import os
    os.remove('supplements_order_data.csv')
    os.remove('cleaned_supplements_order_data.csv') # Remove cleaned version too