def convert_temperature(temp, from_scale, to_scale):
    """
    Convert a temperature between Celsius, Fahrenheit, and Kelvin scales.

    :param temp: the temperature to convert
    :param from_scale: the scale of the given temperature ('C', 'F', or 'K')
    :param to_scale: the target scale to convert the temperature to ('C', 'F', or 'K')
    :return: the converted temperature
    """
    if from_scale == "C":
        if to_scale == "F":
            return (temp * 9/5) + 32
        elif to_scale == "K":
            return temp + 273.15
        else:
            return temp
    elif from_scale == "F":
        if to_scale == "C":
            return (temp - 32) * 5/9
        elif to_scale == "K":
            return (temp - 32) * 5/9 + 273.15
        else:
            return temp
    elif from_scale == "K":
        if to_scale == "C":
            return temp - 273.15
        elif to_scale == "F":
            return (temp - 273.15) * 9/5 + 32
        else:
            return temp
    else:
        raise ValueError("Invalid temperature scale")

# Function usage example
celsius_to_fahrenheit = convert_temperature(100, "C", "F")
print(celsius_to_fahrenheit)  # Output: 212.0