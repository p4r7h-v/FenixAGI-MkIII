import calendar

def create_calendar(year, month):
    try:
        cal = calendar.month(year, month)
        print(cal)
    except (ValueError, TypeError):
        print("Invalid input. Please enter valid year and month.")

# Example usage
create_calendar(2022, 9) # September 2022