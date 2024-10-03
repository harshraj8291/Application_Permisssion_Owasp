import fitz  # PyMuPDF
import pandas as pd

def extract_manifest_analysis(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()

    # Debug: print the first 500 characters of the text to verify content
    print("Start of document text:", text[:500])

    start_idx = text.find("MANIFEST ANALYSIS")
    end_idx = text.find("CODE ANALYSIS", start_idx)
    if start_idx == -1 or end_idx == -1:
        print("Manifest analysis section not found.")
        return []

    # Debug: Print text around the start index to verify the correct section
    print("Extracted section start text:", text[start_idx:start_idx+500])

    section_text = text[start_idx:end_idx]
    lines = section_text.split('\n')

    data = []
    current_entry = {'NO': '', 'ISSUE': '', 'SEVERITY': '', 'DESCRIPTION': ''}

    for line in lines:
        line = line.strip()
        parts = line.split()
        if 'NO' in line and parts[0].isdigit():
            if current_entry['NO']:
                data.append([current_entry['NO'], current_entry['ISSUE'], current_entry['SEVERITY'], current_entry['DESCRIPTION']])
                current_entry = {'NO': '', 'ISSUE': '', 'SEVERITY': '', 'DESCRIPTION': ''}
            current_entry['NO'] = parts[0]
        elif 'ISSUE:' in line:
            current_entry['ISSUE'] = line.partition('ISSUE:')[2].strip()
        elif 'SEVERITY:' in line:
            current_entry['SEVERITY'] = line.partition('SEVERITY:')[2].strip()
        elif 'DESCRIPTION:' in line:
            current_entry['DESCRIPTION'] = line.partition('DESCRIPTION:')[2].strip()

    if current_entry['NO']:
        data.append([current_entry['NO'], current_entry['ISSUE'], current_entry['SEVERITY'], current_entry['DESCRIPTION']])

    return data

def save_to_csv(data, output_file):
    df = pd.DataFrame(data, columns=['NO', 'ISSUE', 'SEVERITY', 'DESCRIPTION'])
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")

pdf_path = r'C:\Users\ANAM KHAN\Documents\Data Science\.vscode\minor2project\pdfreports\com.despdev.quitsmoking-2.20-APK4Fun.com_report.pdf'
output_csv = r'C:\Users\ANAM KHAN\Documents\Data Science\.vscode\minor2project\manifest_analysis.csv'

manifest_data = extract_manifest_analysis(pdf_path)
if manifest_data:
    save_to_csv(manifest_data, output_csv)
else:
    print("No data was extracted.")
