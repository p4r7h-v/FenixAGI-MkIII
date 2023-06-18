import argparse

def parse_command_line_args():
    parser = argparse.ArgumentParser(description='Parse command line arguments.')

    parser.add_argument('-i', '--input', type=str, required=True, help='Input file')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode')

    args = parser.parse_args()

    return args

# Example usage
if __name__ == "__main__":
    arguments = parse_command_line_args()
    print("Input file:", arguments.input)
    print("Output file:", arguments.output)
    print("Verbose mode:", arguments.verbose)