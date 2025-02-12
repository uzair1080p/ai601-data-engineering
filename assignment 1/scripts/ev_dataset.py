import requests
import zipfile
import os
import csv


dataset_url = "https://www.kaggle.com/api/v1/datasets/download/sahirmaharajj/electric-vehicle-population?datasetVersionNumber=2"
download_path = "datasets/raw/archive.zip"
extract_path = "datasets/raw/"
csv_filename = "Electric_Vehicle_Population_Data.csv"
cleaned_csv_filename = "cleaned_ev_data.csv"

def download_dataset():

    response = requests.get(dataset_url, stream=True)
    with open(download_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)
    print("Dataset downloaded successfully.")

def extract_dataset():

    with zipfile.ZipFile(download_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    print("Dataset extracted successfully.")

def clean_dataset():

    input_file = os.path.join(extract_path, csv_filename)
    output_file = os.path.join(extract_path, cleaned_csv_filename)
    
    with open(input_file, mode="r", encoding="utf-8") as infile, open(output_file, mode="w", newline="", encoding="utf-8") as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ["Make", "Model", "Model Year", "Electric Range", "State"]
        
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            if all(row[field] for field in fieldnames): 
                try:
                    if int(row["Electric Range"]) > 100: 
                        writer.writerow({field: row[field] for field in fieldnames})
                except ValueError:
                    continue  

    print("Dataset cleaned and saved.")


download_dataset()
extract_dataset()
clean_dataset()
