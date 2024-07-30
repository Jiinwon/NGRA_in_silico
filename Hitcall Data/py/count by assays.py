import os
import pandas as pd
import glob
import matplotlib.pyplot as plt

# 현재 파일(1.py)의 디렉토리 경로를 가져옴
current_dir = os.path.dirname(__file__)

# folder1에 있는 data.txt 파일의 경로를 설정
performance_files_pattern = os.path.join(current_dir, '..', 'Performance', '*.xlsx')
hitcall_file_path = os.path.join(current_dir, '..', 'Hitcall', 'ToxCast_v.4.1_Hitcall_v.3_countdata.xlsx')



# Load all performance files and extract sheet names
performance_files = glob.glob(performance_files_pattern)
performance_sheet_names = []
for file in performance_files:
    excel = pd.ExcelFile(file)
    performance_sheet_names.extend(excel.sheet_names)

# Remove duplicates
performance_sheet_names = list(set(performance_sheet_names))

# Load the hitcall file
hitcall_df = pd.read_excel(hitcall_file_path)

# Extract assay names and counts from the hitcall Excel file
assay_data = hitcall_df[['assays', 'count']].copy()

# Filter the assays used in the research
filtered_assay_data = assay_data[assay_data['assays'].isin(performance_sheet_names)]

# Sort the filtered data by count in descending order
sorted_assay_data = filtered_assay_data.sort_values(by='count', ascending=False).reset_index(drop=True)

# Function to create and save histogram
def plot_histogram(data, chunk_idx):
    num_bins = 10
    bin_edges = pd.cut(data['count'], bins=num_bins, retbins=True)[1]
    plt.figure(figsize=(10, 6))
    plt.hist(data['count'], bins=bin_edges, edgecolor='black', alpha=0.7)
    plt.title(f'Assay Data Count Distribution - Chunk {chunk_idx + 1}')
    plt.xlabel('Data Count')
    plt.ylabel('Number of Assays')
    plt.xticks(rotation=90)
    plt.grid(axis='y')
    plt.tight_layout()
    save_path = os.path.join(current_dir, '..', 'image', 'distribution', f'countdata_by_assays_chunk_{chunk_idx + 1}.png')
    plt.savefig(save_path)


# Split the data into chunks of 100 and plot histograms for each chunk
chunk_size = 100
num_chunks = (len(sorted_assay_data) + chunk_size - 1) // chunk_size  # Calculate the number of chunks

for i in range(num_chunks):
    chunk_data = sorted_assay_data[i * chunk_size:(i + 1) * chunk_size]
    plot_histogram(chunk_data, i)

# Display the sorted assay data
sorted_assay_data.head()
