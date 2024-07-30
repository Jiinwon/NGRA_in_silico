import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

# 현재 파일(1.py)의 디렉토리 경로를 가져옴
current_dir = os.path.dirname(__file__)

# folder1에 있는 data.txt 파일의 경로를 설정
file_path = os.path.join(current_dir, '..', 'Hitcall', 'ToxCast_v.4.1_Hitcall_v.2.xlsx')


df = pd.read_excel(file_path, skiprows=1)

# 데이터프레임의 3번째 열부터 사용
df = df.iloc[:, 2:]

# 어세이 이름 리스트 가져오기
assay_list = df.columns.tolist()


# 0의 비율 계산
zero_ratios = []
high_zero_ratio_assays = {}
high_zero_ratio_threshold = 99.98

for assay in assay_list:
    # 결측값 제외한 데이터에서 0의 비율 계산
    valid_data = df[assay].dropna()
    zero_ratio = (valid_data == 0).mean() * 100
    zero_ratios.append(zero_ratio)
    if zero_ratio > high_zero_ratio_threshold:
        high_zero_ratio_assays[assay] = zero_ratio


# 99.7%를 넘어가는 어세이의 개수
high_zero_ratio_count = len(high_zero_ratio_assays)

# 결과 출력
print(f"0 비율이 {high_zero_ratio_threshold}%를 넘어가는 어세이의 개수: {high_zero_ratio_count}")
print(f"0 비율이 {high_zero_ratio_threshold}%를 넘어가는 어세이의 리스트와 비율:")
print(high_zero_ratio_assays)
# 박스플롯 그리기
plt.figure(figsize=(10, 6))
plt.boxplot(zero_ratios)
plt.title('Boxplot of 0 Ratios for Each Assay')
plt.ylabel('0 Ratio (%)')

# 박스플롯을 파일로 저장
# folder1에 있는 data.txt 파일의 경로를 설정
save_path = os.path.join(current_dir, '..', 'image','distribution', 'boxplot_zero_ratios.png')
plt.savefig(save_path)
