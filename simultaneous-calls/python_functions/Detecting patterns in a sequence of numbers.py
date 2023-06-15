def detect_patterns(numbers):
    if len(numbers) < 3:
        return "Sequence too short for pattern detection"

    sequence_info = {
        "arithmetic": None,
        "geometric": None
    }

    arithmetic_difference = numbers[1] - numbers[0]
    geometric_ratio = numbers[1] / numbers[0]

    for i in range(1, len(numbers) - 1):
        if sequence_info["arithmetic"] is not False:
            if numbers[i+1] - numbers[i] == arithmetic_difference:
                sequence_info["arithmetic"] = True
            else:
                sequence_info["arithmetic"] = False

        if sequence_info["geometric"] is not False:
            if numbers[i+1] / numbers[i] == geometric_ratio:
                sequence_info["geometric"] = True
            else:
                sequence_info["geometric"] = False

        if not sequence_info["arithmetic"] and not sequence_info["geometric"]:
            break

    return sequence_info

# Example usage:
sequence = [2, 4, 6, 8, 10]
result = detect_patterns(sequence)
print(result)