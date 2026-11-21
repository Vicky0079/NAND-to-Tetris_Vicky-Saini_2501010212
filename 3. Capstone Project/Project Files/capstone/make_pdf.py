from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Capstone Project: Make the Computer Draw a Box', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 6, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, text):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 5, text)
        self.ln()

    def add_image(self, img_path):
        if os.path.exists(img_path):
            # Resize image to fit page width
            self.image(img_path, x=(210 - 110) / 2, w=110)
            self.ln(3)
        else:
            self.set_font('Arial', 'I', 10)
            self.set_text_color(255, 0, 0)
            self.cell(0, 10, f'[Missing Image: {img_path}]', 0, 1, 'C')
            self.set_text_color(0, 0, 0)

pdf = PDF()
pdf.add_page()

# Title Page
pdf.set_font('Arial', '', 12)
pdf.cell(0, 10, 'Course: Nand to Tetris- I (ETCCNT301)', 0, 1, 'C')
pdf.cell(0, 10, 'Name: Vicky Saini', 0, 1, 'C')
pdf.cell(0, 10, 'Roll Number: 2501010212', 0, 1, 'C')
pdf.cell(0, 10, 'Personal Number (K): 12', 0, 1, 'C')
pdf.ln(10)

# Part A
pdf.chapter_title('Part A: Build the Computer')
part_a_text = "For Part A, I implemented the CPU.hdl, Memory.hdl, and Computer.hdl chips to construct the Hack computer.\n- CPU: Parses the 16-bit instructions, routes the ALU inputs based on the control bits, and handles the program counter (PC) jumps.\n- Memory: Connects the RAM16K, Screen, and Keyboard chips, using address bits 14 and 13 to route the load and output signals correctly.\n- Computer: Integrates the ROM32K, CPU, and Memory to form the complete Hack computer.\n(Note: Where complex lower-level chips were required, I used the built-in course chips, which is permitted by the assignment guidelines).\n\nAll official test scripts passed successfully. Below are the screenshots:"
pdf.chapter_body(part_a_text)

pdf.add_image('cpu.png')
pdf.add_image('memory.png')
pdf.add_image('computeradd.png')
pdf.add_image('computermax.png')
pdf.add_image('computerrect.png')

pdf.chapter_title('One Mistake I Fixed:')
mistake_text = "While testing the CPU.hdl, the simulation failed at line 25 of the CPU.cmp file. When analyzing the output, I noticed that the CPU was not executing a D;JLT jump correctly when the D-register held a negative value. I initially wired the jump bits backward, connecting instruction[2] to JGT and instruction[0] to JLT. After debugging, I realized that in the Hack instruction set, bit 2 is JLT and bit 0 is JGT. I swapped the connections in my jump logic, and the CPU test subsequently passed."
pdf.chapter_body(mistake_text)

# Part B
pdf.chapter_title('Part B: Write a Small Assembler in Python')
part_b_text = "I wrote a Python assembler (assembler.py) to translate Hack assembly (.asm) into binary (.hack). The program works in two passes:\n1. First Pass: Removes comments and blank lines, and records the memory addresses of all labels (e.g., (LOOP)).\n2. Second Pass: Translates each instruction into 16-bit binary. New variables are dynamically assigned RAM addresses starting from 16.\n\nExtra Feature (K mod 3 = 0):\nSince my K=12, 12 mod 3 = 0. As required by the assignment, my assembler includes an extra feature that saves all labels and variables along with their assigned memory addresses into a file named symbols.txt.\n\nI tested my assembler against the official course assembler using Add.asm, Max.asm, Rect.asm, and Pong.asm. The generated .hack files were an exact match (PASS) for all four programs."
pdf.chapter_body(part_b_text)

# Part C
pdf.chapter_title('Part C: Write the Box Program')
part_c_text = "I wrote Box.asm in Hack assembly and translated it using my own Python assembler.\n\nBox Dimensions based on K=12:\n- Start Row: 12\n- Start Address: SCREEN + 32 * 12 = 16384 + 384 = 16768\n- Height: 20 rows\n- Width: 16 * ((12 mod 4) + 1) = 16 * (0 + 1) = 16 pixels (1 word)\n\nHow it works:\nThe program checks the KBD (Keyboard) memory address in an infinite loop. If a key is pressed, it jumps to the DRAW loop, which writes -1 (black) to the memory address 16768 and adds 32 (one full row) to the pointer, repeating this 20 times. If no key is pressed, it jumps to the ERASE loop, which writes 0 to those same 20 addresses, clearing the box."
pdf.chapter_body(part_c_text)

if not os.path.exists('box.png'):
    print("WARNING: box.png is missing - save a screenshot of Box.hack running in the CPU Emulator as box.png, then run again.")
pdf.add_image('box.png')

pdf.output('Vicky_Saini_Capstone_Report.pdf')
print("Successfully generated Vicky_Saini_Capstone_Report.pdf")
