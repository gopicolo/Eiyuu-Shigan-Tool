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
    last_ptr = -1

    # Read valid pointers (1 yes, 1 no)
    toggle = True  # True = valid pointer, False = useless
    while offset + 2 <= size:
        ptr = int.from_bytes(mes_data[offset:offset+2], 'big')
        if toggle:
            if ptr == 0x302C:
                print(f"Pointer 0x302C found at offset 0x{offset:04X}. Stopping pointer reading.")
                break
            if ptr >= size or ptr == 0:
                break
            if ptr < last_ptr:
                print(f"Pointer 0x{ptr:04X} smaller than previous 0x{last_ptr:04X} at offset 0x{offset:04X}. Stopping pointer reading.")
                break
            pointers.append(ptr)
            last_ptr = ptr
        toggle = not toggle
        offset += 2

    # Add end of file as final limit
    pointers.append(size)

    with open(out_path, 'w', encoding='utf-8') as out:
        skip_next = False
        for i in range(len(pointers) - 1):
            p1 = pointers[i]
            p2 = pointers[i + 1]
            block = mes_data[p1:p2]
            try:
                text = block.decode('shift_jis').strip()
            except UnicodeDecodeError:
                text = f"[ERROR DECODING BLOCK {p1:04X}-{p2:04X}]"

            # Verifica o caso especial
            if (mes_file.upper() == "S09.MES" and
                p1 == 0x3C49 and
                text.startswith("[ERROR DECODING BLOCK 3C49-3C81]")):

                out.write(f"# Pointer: 0x3C49\n")
                out.write("%t<《店主》>\n")
                out.write("「そうか、ボビンに限って無断で仕事を休むような子じゃないと思ってたよ\n")
                out.write(f"# Pointer: 0x3C81\n")
                out.write("とにかくご苦Jさま。\n")
                out.write("報酬は、依頼屋に振り込んでおいたから、そっちで受けとってくれ」%p ")
                skip_next = True
                continue

            if skip_next:
                skip_next = False
                continue

            out.write(f"# Pointer: 0x{p1:04X}\n")
            out.write(text)

            # Adiciona \n\n apenas se não for o último bloco
            if i < len(pointers) - 2:
                out.write('\n\n')

    print(f"{mes_file} -> {out_path}")

print("Dump finished.")
