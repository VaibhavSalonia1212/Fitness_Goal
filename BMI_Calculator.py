def calculate_bmi(weight, height, unit_w="kg", unit_h="m"):
    """Calculates BMI based on weight and height."""
    if unit_w.lower() == "lb" and unit_h.lower() == "inch":
        bmi = (weight / (height ** 2)) * 703
    elif unit_w.lower() == "kg" and unit_h.lower() == "m":
        bmi = weight / (height ** 2)
    else:
        raise ValueError("Invalid units. Please use 'kg'/'m' or 'lb'/'inch'.")
    return bmi

def get_bmi_category(bmi):
    """Returns the BMI category."""
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    elif bmi >= 30:
        return "Obese"