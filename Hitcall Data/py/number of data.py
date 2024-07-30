import os
import glob
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 현재 파일(1.py)의 디렉토리 경로를 가져옴
current_dir = os.path.dirname(__file__)

# folder1에 있는 data.txt 파일의 경로를 설정
file_path = os.path.join(current_dir, '..', 'Hitcall', 'ToxCast_v.4.1_Hitcall_v.2_smiles.xlsx')



# 데이터 일부를 샘플링하여 읽기 (1000개의 행, 100개의 열)
df = pd.read_excel(file_path)

# 각 어세이마다 결측값을 제외한 실제 데이터의 개수를 계산
non_missing_counts = df.notna().sum()

# 히스토그램 생성 (1000개 단위로 끊어서)
plt.figure(figsize=(10, 6))
sns.histplot(non_missing_counts, bins=range(0, int(non_missing_counts.max()) + 1000, 1000), kde=False, color='blue')
plt.title('Histogram of Assay Counts by Data Size (1000-unit bins)')
plt.xlabel('Number of Non-Missing Data Points')
plt.ylabel('Number of Assays')

save_path = os.path.join(current_dir, '..', 'image', 'distribution',
                                 'histogram_assay_counts_by_data_size.png')

plt.savefig(save_path)
