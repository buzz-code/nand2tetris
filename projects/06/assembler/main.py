import sys
from assembler import Assembler

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <input.asm>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not input_file.endswith('.asm'):
        print("Error: Input file must be an .asm file")
        sys.exit(1)

    output_file = input_file.replace('.asm', '.hack')
    try:
        assembler = Assembler()
        assembler.assemble(input_file, output_file)
    except FileNotFoundError:
        print(f"Error: Could not open file {input_file}")
        sys.exit(1)

if __name__ == "__main__":
    main()