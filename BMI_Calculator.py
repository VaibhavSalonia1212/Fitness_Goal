import math

def calculate_bmi(weight, height, unit_w, unit_h):
    """
    Calculates the Body Mass Index (BMI) with unit conversion.

    Args:
        weight (float): Weight of the person.
        height (float): Height of the person.
        unit_w (str): Unit of weight ('kg' or 'lb').
        unit_h (str): Unit of height ('m' or 'inch').

    Returns:
        float: The BMI value, or 0 if there is an error.
    """
    if unit_w not in ('kg', 'lb'):
        raise ValueError("Invalid weight unit. Please use 'kg' or 'lb'.")
    if unit_h not in ('m', 'inch'):
        raise ValueError("Invalid height unit. Please use 'm' or 'inch'.")

    # Convert weight to kg
    if unit_w == 'lb':
        weight_kg = weight * 0.45359237
    else:
        weight_kg = weight

    # Convert height to meters
    if unit_h == 'inch':
        height_m = height * 0.0254
    else:
        height_m = height

    if height_m <= 0:
        return 0  # Avoid division by zero

    bmi = weight_kg / (height_m ** 2)
    return bmi


def get_bmi_category(bmi):
    """
    Determines the BMI category based on the BMI value.

    Args:
        bmi (float): The BMI value.

    Returns:
        str: The BMI category.
    """
    if bmi <= 0:
        return "Invalid BMI"
    elif bmi < 18.5:
        return "Underweight"
    elif bmi < 24.9:
        return "Normal Weight"
    elif bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"
