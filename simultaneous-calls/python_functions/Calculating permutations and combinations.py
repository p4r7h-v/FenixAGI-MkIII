def perm_comb(n, r, calc_type='both'):
    '''
    Calculate permutations and/or combinations for a given n and r.

    :param n: int
        The total number of elements in the set
    :param r: int
        The number of elements to be selected from the set
    :param calc_type: str, optional
        The type of calculation - 'permutations', 'combinations' or 'both'
        Default value is 'both'
    :return: tuple
        A tuple containing the calculated permutations and/or combinations
    '''

    import math

    def calculate_permutations(n, r):
        return math.perm(n, r)

    def calculate_combinations(n, r):
        return math.comb(n, r)

    if calc_type == 'both':
        permutations = calculate_permutations(n, r)
        combinations = calculate_combinations(n, r)
        return permutations, combinations
    elif calc_type == 'permutations':
        return calculate_permutations(n, r),
    elif calc_type == 'combinations':
        return calculate_combinations(n, r),
    else:
        raise ValueError("Invalid calc_type. Accepted values: 'permutations', 'combinations', 'both'")