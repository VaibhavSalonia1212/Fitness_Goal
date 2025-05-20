# main.py (Updated section)
from BMI_Calculator import calculate_bmi, get_bmi_category
from supplement_recommender import recommend_supplements, load_supplement_data
from clean_data import clean_supplement_data # Import the cleaning function

def main():
    print("Welcome to the BMI and Supplement Recommender!")

    # --- Data Cleaning Step ---
    print("\n--- Preparing Data ---")
    if not clean_supplement_data(): # This cleans and saves to cleaned_supplements_order_data.csv
        print("Data cleaning failed. Exiting.")
        return
    print("Data preparation complete.")
    # --- End Data Cleaning Step ---

    try:
        # ... rest of your existing main function ...
        weight = float(input("Enter your weight: "))
        unit_w = input("Enter weight unit (kg/lb): ").lower()
        height = float(input("Enter your height: "))
        unit_h = input("Enter height unit (m/inch): ").lower()

        bmi_value = calculate_bmi(weight, height, unit_w, unit_h)
        bmi_category = get_bmi_category(bmi_value)

        print(f"\nYour BMI is: {bmi_value:.2f}")
        print(f"Which puts you in the: {bmi_category} category.")

        goal = input("\nWhat is your fitness goal? (Lose Weight, Gain Muscle, Maintain Weight/General Health): ").strip()

        # Load supplement data (this will now read from the cleaned file)
        available_categories = load_supplement_data()
        if not available_categories:
            print("No available product categories loaded. Cannot provide category-specific recommendations.")
            # Optionally, provide very generic advice here if no categories are found.
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