def find_genetic_patterns(dna_sequence, pattern):
    """
    Find the occurrences of a given genetic pattern in a DNA sequence.
    
    Args:
    dna_sequence (str): The DNA sequence to search for the pattern.
    pattern (str): The pattern we are looking for in the DNA sequence.

    Returns:
    A list containing the starting indices of the pattern occurrences in the DNA sequence.
    """
    pattern_length = len(pattern)
    sequence_length = len(dna_sequence)
    
    # Initialize result list
    pattern_indices = []

    # Iterate through the DNA sequence
    for i in range(sequence_length - pattern_length + 1):
        # Extract a substring of the same length as the pattern
        current_substring = dna_sequence[i:i + pattern_length]

        # Check if it is the desired pattern, and if so, add the index to the list
        if current_substring == pattern:
            pattern_indices.append(i)

    return pattern_indices

# Test the function
dna_seq = "ATGCAGTAGCTAGTAGCGTAGCAGTAG"
search_pattern = "TAG"
results = find_genetic_patterns(dna_seq, search_pattern)

print(f"Pattern '{search_pattern}' found at indices: {results}")