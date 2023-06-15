import zlib

def compress_file(file, mode):
    if mode not in ('compress', 'decompress'):
        raise ValueError("Invalid mode. Choose either 'compress' or 'decompress'.")

    # Read input file
    with open(file, 'rb') as input_file:
        input_data = input_file.read()

    # Compress or decompress input data
    if mode == 'compress':
        output_data = zlib.compress(input_data)
        output_file = file + '.compressed'
    else:
        output_data = zlib.decompress(input_data)
        output_file = file.replace('.compressed', '')

    # Write output file
    with open(output_file, 'wb') as outf:
        outf.write(output_data)

    print(f"File {mode}ed successfully: {output_file}")