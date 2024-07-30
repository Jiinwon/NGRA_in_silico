import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import glob


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

# FP와 Algorithm 열을 병합하여 새로운 열 생성
all_data['FP_Algorithm'] = all_data['FP'] + ' - ' + all_data['Algorithm']

# 데이터 개수 파일 불러오기
count_data = pd.read_excel('Hitcall/ToxCast_v.4.1_Hitcall_v.3_countdata.xlsx', header=None)

# 데이터 개수 순서대로 Assay 정렬
count_data.columns = count_data.iloc[0]
count_data = count_data.drop(count_data.index[0])
count_data.columns = ['Assay', 'Count']
sorted_assays = count_data.sort_values(by='Count', ascending=False)['Assay'].tolist()


# 실제로 존재하는 Assay 열만 사용하도록 필터링
existing_assays = [assay for assay in sorted_assays if assay in all_data['Assay'].unique()]


# 히트맵을 생성할 함수 정의
def create_heatmap(data, title, output_file, annot=False):
    plt.figure(figsize=(20, 15))
    heatmap = sns.heatmap(data, annot=annot, cmap='coolwarm', fmt=".2f" if annot else None, linewidths=.5)
    plt.title(title)
    plt.xlabel('Assay')
    plt.ylabel('FP-Algorithm Combination')
    plt.savefig(output_file)
    plt.close()


# 클러스터 맵을 생성할 함수 정의
def create_clustermap(data, title, output_file):
    cluster_map = sns.clustermap(data, cmap='coolwarm', linewidths=.5, figsize=(20, 15), method='average',
                                 metric='euclidean')
    plt.title(title)
    cluster_map.savefig(output_file)
    plt.close()





# 데이터 확인 및 히트맵 생성
pivot_table = all_data.pivot_table(index='FP_Algorithm', columns='Assay', values='AUC')

# Assay를 100개씩 나누어 히트맵 및 클러스터맵 생성
for i in range(0, len(existing_assays), 100):
    sub_assays = existing_assays[i:i + 100]
    sub_pivot_table = pivot_table[sub_assays]
    if not sub_pivot_table.empty:
        # 히트맵 생성 및 저장 (AUC 값 표시)
        save_path = os.path.join(current_dir, '..', 'image', 'heatmap', f'AUC_Heatmap_with_values_part_{i // 100 + 1}.png')
        create_heatmap(sub_pivot_table, f'AUC Heatmap with Values (Part {i // 100 + 1})',
                       save_path, annot=True)

        # 히트맵 생성 및 저장 (AUC 값 미표시)
        save_path = os.path.join(current_dir, '..', 'image', 'heatmap',
                                 f'AUC_Heatmap_without_values_part_{i // 100 + 1}.png')
        create_heatmap(sub_pivot_table, f'AUC Heatmap without Values (Part {i // 100 + 1})',
                       save_path, annot=False)

        # 클러스터 맵 생성 및 저장
        save_path = os.path.join(current_dir, '..', 'image', 'heatmap',
                                 f'AUC_Clustermap_part_{i // 100 + 1}.png')
        create_clustermap(sub_pivot_table, f'AUC Clustermap (Part {i // 100 + 1})',
                          save_path)


