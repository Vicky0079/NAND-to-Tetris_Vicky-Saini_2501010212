import sys
import os

PREDEFINED = {
    'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4,
    'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7,
    'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11, 'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15,
    'SCREEN': 16384, 'KBD': 24576
}

COMP = {
    '0':'0101010', '1':'0111111', '-1':'0111010', 'D':'0001100', 'A':'0110000', '!D':'0001101',
    '!A':'0110001', '-D':'0001111', '-A':'0110011', 'D+1':'0011111', 'A+1':'0110111', 'D-1':'0001110',
    'A-1':'0110010', 'D+A':'0000010', 'D-A':'0010011', 'A-D':'0000111', 'D&A':'0000000', 'D|A':'0010101',
    'M':'1110000', '!M':'1110001', '-M':'1110011', 'M+1':'1110111', 'M-1':'1110010', 'D+M':'1000010',
    'D-M':'1010011', 'M-D':'1000111', 'D&M':'1000000', 'D|M':'1010101'
}

DEST = {'':'000', 'M':'001', 'D':'010', 'MD':'011', 'A':'100', 'AM':'101', 'AD':'110', 'AMD':'111'}

JUMP = {'':'000', 'JGT':'001', 'JEQ':'010', 'JGE':'011', 'JLT':'100', 'JNE':'101', 'JLE':'110', 'JMP':'111'}

def assemble(input_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    clean_lines = []
    symbols = dict(PREDEFINED)
    rom_address = 0
    seen_labels = set()

    for line_num, line in enumerate(lines, 1):
        line = line.split('//')[0].strip()
        if not line: continue

        if line.startswith('(') and line.endswith(')'):
            label = line[1:-1].strip()
            if label in seen_labels:
                print(f"WARNING: Line {line_num}: Duplicate label '{label}'")
            seen_labels.add(label)
            symbols[label] = rom_address
        else:
            clean_lines.append((line_num, line))
            rom_address += 1

    binary_output = []
    next_var_address = 16

    for line_num, line in clean_lines:
        if line.startswith('@'):
            symbol = line[1:].strip()
            if symbol.isdigit():
                address = int(symbol)
            elif symbol in symbols:
                address = symbols[symbol]
            else:
                symbols[symbol] = next_var_address
                address = next_var_address
                next_var_address += 1
            binary_output.append('0' + format(address, '015b'))
        else:
            try:
                dest, comp, jump = '', line, ''
                if '=' in line:
                    dest, line = line.split('=', 1)
                    dest = dest.strip()
                if ';' in line:
                    comp, jump = line.split(';', 1)
                    comp = comp.strip()
                else:
                    comp = line.strip()
                jump = jump.strip()
                binary_output.append('111' + COMP[comp] + DEST[dest] + JUMP[jump])
            except KeyError:
                print(f"Line {line_num}: invalid instruction: {line}")
                sys.exit(1)

    output_file = os.path.splitext(input_file)[0] + '.hack'
    with open(output_file, 'w') as f:
        f.write('\n'.join(binary_output) + '\n')

    # EXTRA FEATURE FOR K=12 (12 mod 3 = 0)
    sym_file = os.path.join(os.path.dirname(os.path.abspath(input_file)), 'symbols.txt')
    with open(sym_file, 'w') as f:
        for sym, addr in sorted(symbols.items(), key=lambda kv: (kv[1], kv[0])):
            f.write(f"{sym} {addr}\n")

    print(f"Successfully assembled {input_file} -> {output_file}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python assembler.py <file.asm>")
        sys.exit(1)
    assemble(sys.argv[1])
