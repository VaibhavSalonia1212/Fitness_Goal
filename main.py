# main.py
from BMI_Calculator import calculate_bmi, get_bmi_category
from supplement_recommender import recommend_supplements, load_supplement_data
from clean_data import clean_supplement_data  # Import the cleaning function

def main():
    """
    Main function to run the BMI and Supplement Recommender.
    This function orchestrates the data cleaning, user input, BMI calculation,
    and supplement recommendation processes.
    """
    print("Welcome to the BMI and Supplement Recommender!")

    # --- Data Cleaning Step ---
    print("\n--- Preparing Data ---")
    #  Explicitly define the input and output filepaths.
    raw_data_filepath = "data/bodybuilding_nutrition_products.csv"
    cleaned_data_filepath = "data/cleaned_supplements_order_data.csv"
    if not clean_supplement_data(input_filepath=raw_data_filepath,
                                 output_filepath=cleaned_data_filepath):
        print("Data cleaning failed. Exiting.")
        return
    print("Data preparation complete.")
    # --- End Data Cleaning Step ---

    try:
        # Get user input
        weight = float(input("Enter your weight(kg/lb): "))
        unit_w = input("Enter weight unit (kg/lb): ").lower()
        height = float(input("Enter your height(m/inch): "))
        unit_h = input("Enter height unit (m/inch): ").lower()

        # Calculate BMI and get category
        bmi_value = calculate_bmi(weight, height, unit_w, unit_h)
        bmi_category = get_bmi_category(bmi_value)

        print(f"\nYour BMI is: {bmi_value:.2f}")
        print(f"Which puts you in the: {bmi_category} category.")

        goal = input(
            "\nWhat is your fitness goal? (Lose Weight, Gain Muscle, Maintain Weight/General Health): ").strip()

        # Load supplement data (this will now read from the cleaned file)
        available_categories = load_supplement_data(filepath=cleaned_data_filepath)  # Pass the cleaned file path
        if not available_categories:
            print(
                "No available product categories loaded. Cannot provide category-specific recommendations.")
            return

        # Get supplement recommendations
        supplement_advice = recommend_supplements(bmi_category, goal, available_categories)
        print("\n--- Supplement Recommendations ---")
        print(supplement_advice)

    except ValueError as e:
        print(f"Input Error: {e}. Please enter valid numeric values and units.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
