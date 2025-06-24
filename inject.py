import os
import struct

input_dir = 'input'
text_dir = 'output'
modified_dir = 'modified'

os.makedirs(modified_dir, exist_ok=True)

txt_files = [f for f in os.listdir(text_dir) if f.endswith('_extracted.txt')]
mes_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.mes')]

print(f".MES files found in input_dir: {mes_files}")
print(f".txt files found in text_dir: {txt_files}")

for txt_file in txt_files:
    base_name = txt_file[:-14]
    mes_file_name = base_name + '.MES'

    if mes_file_name not in mes_files:
        print(f".MES file not found for {txt_file}, skipping.")
        continue

    mes_path = os.path.join(input_dir, mes_file_name)
    txt_path = os.path.join(text_dir, txt_file)
    modified_path = os.path.join(modified_dir, mes_file_name)

    with open(mes_path, 'rb') as f:
        mes_data = bytearray(f.read())

    with open(txt_path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    # Collect the blocks
    blocks = []
    current_text = []
    for line in lines:
        if line.startswith('# Pointer:'):
            if current_text:
                blocks.append('\n'.join(current_text))
                current_text = []
            current_text.append(line)
        else:
            current_text.append(line)
    if current_text:
        blocks.append('\n'.join(current_text))

    # Read the offset of the first original text (pointer at 0x12)
    if len(mes_data) < 0x14:
        print(f"File {mes_file_name} too small to read pointer at 0x12, skipping.")
        continue
    first_text_offset = struct.unpack('>H', mes_data[0x12:0x14])[0]

    # Prepare new texts and pointers
    new_text = bytearray()
    new_pointers = []

    for block in blocks:
        lines = block.splitlines()
        ptr_line = lines[0]
        text_content = '\n'.join(lines[1:]).strip()
        # Aqui está a modificação para ignorar bytes ilegais
        sjis = text_content.encode('shift_jis', errors='ignore') + b'\x00'
        pointer_value = first_text_offset + len(new_text)
        if pointer_value > 0xFFFF:
            print(f"Error: pointer {pointer_value:#06X} bigger than 0xFFFF in {mes_file_name}, aborting this file.")
            break
        new_pointers.append(pointer_value)
        new_text += sjis

    # Build the new file
    out_data = bytearray(mes_data[:first_text_offset])  # header + original table
    out_data += new_text  # new text replaces the old

    # Update the table
    table_off = 0x12
    ptr_idx = 0
    toggle = True
    while table_off + 2 <= first_text_offset and ptr_idx < len(new_pointers):
        if toggle:
            out_data[table_off:table_off+2] = struct.pack('>H', new_pointers[ptr_idx])
            ptr_idx += 1
        toggle = not toggle
        table_off += 2

    with open(modified_path, 'wb') as f:
        f.write(out_data)

    print(f"Modified file saved: {modified_path}")

print("Reinsertion finished.")
