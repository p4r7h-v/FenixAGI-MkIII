def identify_genetic_patterns(dna_sequence):
    if not all(nucleotide in 'ACGT' for nucleotide in dna_sequence):
        return "Invalid DNA sequence. Make sure it contains only A, C, G, and T."

    nucleotide_count = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
    for nucleotide in dna_sequence:
        nucleotide_count[nucleotide] += 1

    patterns = []
    pattern_length = 3
    for i in range(len(dna_sequence) - pattern_length + 1):
        pattern = dna_sequence[i:i + pattern_length]
        if pattern not in patterns:
            patterns.append(pattern)

    return nucleotide_count, patterns