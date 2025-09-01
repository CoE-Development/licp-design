import os
import pandas as pd
from bs4 import BeautifulSoup


# Function to extract table data from HTML
def extract_table_data(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    tables = soup.find_all("table", class_="table")

    data = []

    for table in tables:
        caption = table.find("caption")
        if caption:
            table_name = caption.find("strong").text.strip()
            schema_name = caption.find("em").text.strip()

            rows = table.find("tbody").find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                if len(cols) > 1:  # Ensure there are enough columns
                    column_name = cols[0].text.strip()
                    if column_name.startswith("Constraints"):
                        continue
                    data_type = cols[1].text.strip()
                    if data_type in [
                        "Type",
                        "UNIQUE",
                        "PRIMARY KEY",
                        "FOREIGN KEY",
                        "Indexes",
                        "btree",
                    ]:
                        continue
                    data.append(
                        {
                            "Schema": schema_name,
                            "Table Name": table_name,
                            "Column Name": column_name,
                            "Data Type": data_type,
                        }
                    )

    return data


# Main function to process the folder and create an Excel file
def main(folder_path, output_file):
    all_data = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".html"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                html_content = file.read()
                table_data = extract_table_data(html_content)
                all_data.extend(table_data)

    # Create a DataFrame and save to Excel
    df = pd.DataFrame(all_data)
    df.to_excel(output_file, index=False)


# Usage
if __name__ == "__main__":
    folder_path = "./data_dict"  # Update this path
    output_file = "data_dict.xlsx"  # Desired output Excel file name
    main(folder_path, output_file)
