import pandas as pd

DISCLAIMER = """
IMPORTANT DISCLAIMER: The following supplement recommendations are for informational purposes only and are NOT medical advice. Always consult with a healthcare professional, registered dietitian, or certified nutritionist before taking any supplements. Supplements can interact with medications and may have side effects.
"""

def load_supplement_data(filepath="bodybuilding_nutrition_products.csv"):
    """
   
    """
    try:
        # Assuming the first row is headers based on your image
        df = pd.read_csv(filepath)
        # Extract unique product categories for potential recommendations
        if 'product_category' in df.columns:
            return df['product_category'].unique().tolist()
        else:
            print(f"Warning: 'product_category' column not found in {filepath}.")
            return []
    except FileNotFoundError:
        print(f"Error: {filepath} not found. Supplement data cannot be loaded.")
        return []
    except pd.errors.EmptyDataError:
        print(f"Error: {filepath} is empty.")
        return []
    except Exception as e:
        print(f"An error occurred while loading supplement data: {e}")
        return []

def recommend_supplements(bmi_category, goal, available_categories):
    """
    Provides supplement recommendations based on BMI category, goal,
    and *available product categories* from your data.
    """
    recommendations = []
    # Convert available categories to a set for faster lookup
    available_categories_set = set(c.lower() for c in available_categories)

    # --- Recommendation Logic ---
    # This logic maps goals to general supplement types.
    # We then check if these types exist in your 'product_category' data.

    if goal.lower() == "lose weight":
        recommendations.append("For weight loss, consider supplements that aid satiety or metabolism.")
        if "protein" in available_categories_set:
            recommendations.append("- Protein powder (helps with satiety and muscle preservation).")
        if "l-carnitine" in available_categories_set: # Example: If you have L-Carnitine
            recommendations.append("- L-Carnitine (often associated with fat metabolism, consult a professional).")
        if "fiber" in available_categories_set: # Example: If you have fiber supplements
            recommendations.append("- Fiber supplements (aids digestion and fullness).")
        if not any(cat in available_categories_set for cat in ["protein", "l-carnitine", "fiber"]):
             recommendations.append("  (No specific weight loss supplements found in your data, but protein/fiber are generally recommended).")


    elif goal.lower() == "gain muscle":
        recommendations.append("For muscle gain, focus on supplements that support muscle growth and recovery.")
        if "protein" in available_categories_set:
            recommendations.append("- Protein powder (essential for muscle repair and growth).")
        if "creatine" in available_categories_set:
            recommendations.append("- Creatine (can improve strength and power).")
        if "bcaa" in available_categories_set or "bcaas" in available_categories_set:
            recommendations.append("- BCAAs (Branch Chain Amino Acids) may aid in muscle recovery.")
        if "pre-workout" in available_categories_set:
            recommendations.append("- Pre-workout (for energy and focus during training).")
        if not any(cat in available_categories_set for cat in ["protein", "creatine", "bcaa", "bcaas", "pre-workout"]):
             recommendations.append("  (No specific muscle gain supplements found in your data, but protein/creatine are generally recommended).")


    elif goal.lower() in ["maintain weight", "general health"]:
        recommendations.append("For general health and maintenance, consider foundational supplements.")
        if "multivitamin" in available_categories_set:
            recommendations.append("- A good quality multivitamin.")
        if "omega-3" in available_categories_set or "fish oil" in available_categories_set:
            recommendations.append("- Omega-3 fatty acids (for heart and brain health).")
        if "vitamin d" in available_categories_set:
            recommendations.append("- Vitamin D (especially if you have limited sun exposure).")
        if not any(cat in available_categories_set for cat in ["multivitamin", "omega-3", "fish oil", "vitamin d"]):
             recommendations.append("  (No specific general health supplements found in your data, but multivitamins/omega-3 are generally recommended).")

    # Add a fallback if no specific goal recommendations were made
    if not recommendations:
        recommendations.append("No specific supplement recommendations available for your goal or from your loaded data at this time.")
        recommendations.append("General recommendations might include protein, multivitamins, and omega-3s for overall well-being.")

    return "\n".join(recommendations) + "\n\n" + DISCLAIMER

# Example usage (for testing purposes, if you were to run this file directly)
if __name__ == "__main__":
    # Create a dummy CSV for testing
    dummy_data = {
        'supplier_name': ['Supplier A', 'Supplier B', 'Supplier C'],
        'product_category': ['Protein', 'L-Carnitine', 'Creatine'],
        'product_description': ['Whey Protein', 'L-Carnitine Liquid', 'Creatine Monohydrate'],
        'product_price': [30.0, 15.0, 25.0]
        # ... other columns as per your image
    }
    dummy_df = pd.DataFrame(dummy_data)
    dummy_df.to_csv('data/supplements_order_data.csv', index=False)

    print("--- Testing load_supplement_data ---")
    available_cats = load_supplement_data()
    print(f"Available categories: {available_cats}")

    print("\n--- Testing recommend_supplements ---")
    print("\nGoal: Lose Weight, Category: Overweight")
    print(recommend_supplements("Overweight", "Lose Weight", available_cats))

    print("\nGoal: Gain Muscle, Category: Normal weight")
    print(recommend_supplements("Normal weight", "Gain Muscle", available_cats))

    print("\nGoal: General Health, Category: Normal weight")
    print(recommend_supplements("Normal weight", "General Health", available_cats))

    # Clean up dummy file
    import os
    os.remove('data/supplements_order_data.csv')