import csv
import re
import os

md_file = "/Users/stijnsterkenburg/.gemini/antigravity/brain/6f10eb9d-2e1f-4409-b627-09a6216005b0/expanded_stucadoors_enriched.md"
csv_file = "/Users/stijnsterkenburg/.gemini/antigravity/playground/hidden-sun/Stucadoors 2/Stucadoors enriched.csv"

if not os.path.exists(md_file):
    print(f"Error: {md_file} not found")
    exit(1)

with open(md_file, 'r') as f:
    content = f.read()

# Handle cases where the text literal \n is used instead of actual newlines
if '\\n' in content:
    lines = content.split('\\n')
else:
    lines = content.split('\n')

table_lines = [line.strip() for line in lines if line.strip().startswith('|')]

if len(table_lines) > 2:
    data_lines = table_lines[2:]
    
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Bedrijfsnaam", "Beoordeling", "Reviews", "Telefoon", "Email", "Website", "Socials", "Adres"])
        
        for line in data_lines:
            # First remove ALL literal backslashes and pipes meant to escape strings inside cells.
            # E.g. \\|S\\|e\\|m\\|e\\| becomes Seme
            # We can use regex to remove any sequence of backslashes and pipes IF they are not separating columns
            # Wait, easier: `csv.reader` handles escaped characters perfectly.
            
            # Use regex to just completely erase any backslashes and the pipe after them.
            # Match backslashes optionally followed by a pipe
            # But wait, we ONLY want to erase pipes that are escaped
            # The column separator is always ` | ` (space pipe space) or at least `| ` at the start.
            
            # Let's replace any `\|` with an empty string, and `\\|` with empty string.
            clean_line = re.sub(r'\\+\|?', '', line)
            
            # Now split by normal column divider `|`
            cols = [col.strip() for col in clean_line.split('|')]
            
            # Remove empty strings at start/end
            if len(cols) > 0 and cols[0] == '':
                cols = cols[1:]
            if len(cols) > 0 and cols[-1] == '':
                cols = cols[:-1]
                
            cols = [col.strip() for col in cols]
            cols = [c.replace('\\', '') for c in cols]
            cols = [re.sub(r'<br>', ', ', c) for c in cols]
            cols = [re.sub(r'\*\*(.*?)\*\*', r'\1', c) for c in cols]
            cols = [re.sub(r'\*(.*?)\*', r'\1', c) for c in cols]
            cols = [re.sub(r'\[(.*?)\]\((.*?)\)', r'\1 (\2)', c) for c in cols]
            
            if len(cols) > 0:
                writer.writerow(cols)
    print("CSV written successfully.")
else:
    print("No table found.")
