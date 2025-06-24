import os
from pathlib import Path

input_dir = 'input'
output_dir = 'output'

os.makedirs(output_dir, exist_ok=True)

mes_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.mes')]

for mes_file in mes_files:
    mes_path = os.path.join(input_dir, mes_file)
    out_path = os.path.join(output_dir, f"{Path(mes_file).stem}_extracted.txt")

    with open(mes_path, 'rb') as f:
        mes_data = f.read()

    size = len(mes_data)
    offset = 0x12
    pointers = []

    # Read valid pointers (1 yes, 1 no)
    toggle = True  # True = valid pointer, False = useless
    while offset + 2 <= size:
        ptr = int.from_bytes(mes_data[offset:offset+2], 'big')
        if toggle:
            if ptr >= size or ptr == 0:
                break
            pointers.append(ptr)
        toggle = not toggle
        offset += 2

    # Add end of file as final limit
    pointers.append(size)

    with open(out_path, 'w', encoding='utf-8') as out:
        for i in range(len(pointers) - 1):
            p1 = pointers[i]
            p2 = pointers[i + 1]
            block = mes_data[p1:p2]
            try:
                text = block.decode('shift_jis').strip()
            except UnicodeDecodeError:
                text = f"[ERROR DECODING BLOCK {p1:04X}-{p2:04X}]"

            out.write(f"# Pointer: 0x{p1:04X}\n")
            out.write(text + '\n\n')

    print(f"{mes_file} -> {out_path}")

print("Dump finished.")
