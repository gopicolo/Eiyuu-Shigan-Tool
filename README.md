
# Eiyuu Shigan - Gal Act Heroism (Saturn) Text Extraction and Reinsertion Tool

This tool was created by **gopicolo** for extracting and reinserting text in the game **Eiyuu Shigan - Gal Act Heroism** for Sega Saturn.

---

## What this tool does

- Extracts text from `.MES` files in the game’s data, decoding Shift-JIS encoded text blocks.
- Outputs extracted text to easy-to-edit `.txt` files.
- Allows you to modify the extracted text files.
- Reinjects the modified text back into the original `.MES` files, updating pointers correctly.

---

## How to use

1. **Prepare folders**  
   - Put the original `.MES` files in a folder named `input`  
   - Files with the `.MSG` extension are also `.MES` files — you just need to rename them to `.MES` before using the tool.  
   - Extracted text files will be generated inside the `output` folder  
   - Modified `.MES` files will be saved in the `modified` folder  

2. **Extract text**  
   Run the extraction script. It will read all `.MES` files from `input` and create corresponding `_extracted.txt` files inside `output`.

3. **Keep line length limits in mind**  
   The English text lines should not exceed **34 characters** each.  
   If a sentence is longer, you must manually insert line breaks to avoid cutting words mid-line.  
   For example,  
   ```
   It is a vast land that has been developed by adventurers, for adventurers.
   ```  
   should be rewritten as:  
   ```
   It is a vast land that has been
   developed by adventurers, for
   adventurers.
   ```

4. **Edit text**  
   Open the `_extracted.txt` files in the `output` folder and edit the text as needed.  
   *Do not change the lines starting with `# Pointer:`.*

5. **Reinsert text**  
   Run the reinsertion script. It will read the edited text files from `output` and update the original `.MES` files, saving the modified versions into the `modified` folder.

---

## Font information

The font used by the game is Shift-JIS based, and stored in the file ASC8_16.FNT.
You can edit the font to add new characters (such as accented letters) if needed for your translation.
The font can be opened and viewed in Crystal Tile 2 with the following settings:

Width: 8

Height: 16

Tile form: 1BPP Solid

## Notes

- The tool works specifically with **Eiyuu Shigan - Gal Act Heroism (Saturn)** file structure and encoding.
- Make backups of your original files before running any script.
- The scripts assume the text encoding is Shift-JIS.
- If you encounter errors during reinsertion, check that text lengths and pointer values do not exceed file limits.

---

If you have any questions or feedback, feel free to reach out!
