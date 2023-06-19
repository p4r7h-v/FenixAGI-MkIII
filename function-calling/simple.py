import openai
import json
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)  # <--- add this line

def get_current_humidity(location):
    """Get the current humidity in a given location"""
    humidity_info = {
        "location": location,
        "humidity": "60%",  # Example hard coded value
    }
    return json.dumps(humidity_info)


def get_current_wind_speed(location, unit="mph"):
    """Get the current wind speed in a given location"""
    wind_speed_info = {
        "location": location,
        "wind_speed": "10",
        "unit": unit,  # Example hard coded value
    }
    return json.dumps(wind_speed_info)

# Step 1, send model the user query and what functions it has access to
def run_conversation():
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[{"role": "user", "content": "What's the wind like in Boston?"}],
        functions=[
            {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            },
            {
                "name": "get_current_humidity",
                "description": "Get the current humidity in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                    },
                    "required": ["location"],
                },
            },
            {
                "name": "get_current_wind_speed",
                "description": "Get the current wind speed in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["kph", "mph"]},
                    },
                    "required": ["location"],
                },
            }
        ],
        function_call="auto",
    )

    message = response["choices"][0]["message"]
    print(message)

    if message.get("function_call"):
        function_name = message["function_call"]["name"]

        if function_name == "get_current_weather":
            function_response = get_current_weather(
                location=message.get("location"),
                unit=message.get("unit"),
            )
        elif function_name == "get_current_humidity":
            function_response = get_current_humidity(
                location=message.get("location"),
            )
        elif function_name == "get_current_wind_speed":
            function_response = get_current_wind_speed(
                location=message.get("location"),
                unit=message.get("unit"),
            )
        else:
            return "Unknown function: " + function_name

        second_response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=[
                {"role": "user", "content": "What is the weather like in Boston?"},
                message,
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                },
            ],
        )
        return second_response

print(run_conversation())
