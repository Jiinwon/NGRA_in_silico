import os
import glob
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 현재 파일(1.py)의 디렉토리 경로를 가져옴
current_dir = os.path.dirname(__file__)

# folder1에 있는 data.txt 파일의 경로를 설정
file_pattern = os.path.join(current_dir, '..', 'Performance', '*.xlsx')

# .xlsx 파일 목록을 가져옴
file_paths= glob.glob(file_pattern)


# 각 파일의 데이터를 저장할 리스트 초기화
data_list = []

# 각 파일의 데이터를 읽어 리스트에 추가
for file_path in file_paths:
    excel_data = pd.ExcelFile(file_path)
    sheet_names = excel_data.sheet_names

    # 각 파일의 각 시트 데이터를 딕셔너리에 저장
    for sheet in sheet_names:
        data = pd.read_excel(file_path, sheet_name=sheet)
        data['Assay'] = sheet  # 시트 이름을 Assay 열로 추가
        data_list.append(data)

# 모든 데이터를 하나의 데이터프레임으로 병합
all_data = pd.concat(data_list, ignore_index=True)

# Assay별 고유 색상 지정
assay_list = all_data['Assay'].unique()
palette = sns.color_palette("husl", len(assay_list))
assay_colors = dict(zip(assay_list, palette))


# 박스플롯을 생성할 함수 정의
def create_boxplot(data, x, y, title, output_file):
    plt.figure(figsize=(16, 10))
    sns.boxplot(data=data, x=x, y=y, palette=assay_colors)
    plt.title(title)
    plt.xlabel('Assay')
    plt.ylabel('AUC')
    plt.xticks(rotation=90)  # x축 레이블 회전
    plt.savefig(output_file)
    plt.close()

# 박스플롯 생성 및 저장
save_path = os.path.join(current_dir, '..', 'image', 'boxplot', 'UC_Boxplot_by_Assay.png')
# 박스플롯 생성 및 저장
create_boxplot(all_data, 'Assay', 'AUC', 'AUC Distribution by Assay', save_path)

# 각 파일의 데이터를 저장할 리스트 초기화
data_list = []

# 각 파일의 데이터를 읽어 리스트에 추가
for file_path in file_paths:
    excel_data = pd.ExcelFile(file_path)
    sheet_names = excel_data.sheet_names

    # 각 파일의 각 시트 데이터를 딕셔너리에 저장
    for sheet in sheet_names:
        data = pd.read_excel(file_path, sheet_name=sheet)
        data['Assay'] = sheet  # 시트 이름을 Assay 열로 추가
        data_list.append(data)

# 모든 데이터를 하나의 데이터프레임으로 병합
all_data = pd.concat(data_list, ignore_index=True)

# FP와 Algorithm 열을 병합하여 새로운 열 생성
all_data['FP_Algorithm'] = all_data['FP'] + ' - ' + all_data['Algorithm']

# FP-Algorithm별 고유 색상 지정
fp_algorithm_list = all_data['FP_Algorithm'].unique()
palette = sns.color_palette("husl", len(fp_algorithm_list))
fp_algorithm_colors = dict(zip(fp_algorithm_list, palette))


# 박스플롯을 생성할 함수 정의
def create_boxplot(data, x, y, title, output_file):
    plt.figure(figsize=(16, 10))
    sns.boxplot(data=data, x=x, y=y, palette=fp_algorithm_colors)
    plt.title(title)
    plt.xlabel('FP-Algorithm Combination')
    plt.ylabel('AUC')
    plt.xticks(rotation=90)  # x축 레이블 회전
    plt.savefig(output_file)
    plt.close()

# 박스플롯 생성 및 저장
save_path = os.path.join(current_dir, '..', 'image', 'boxplot', 'AUC_Boxplot_by_FP_Algorithm.png')

create_boxplot(all_data, 'FP_Algorithm', 'AUC', 'AUC Distribution by FP-Algorithm', save_path)
