import json
import os


class SmilesToxprint:
    def __init__(self, json_path=None):
        if json_path is None:
            # 라이브러리 내부의 JSON 파일 경로 설정
            json_path = os.path.join(os.path.dirname(__file__), '..', 'SMILES-TOXPRINT.json')
        self.data = self._load_json(json_path)

    def _load_json(self, json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_toxprint(self, smiles):
        return self.data.get(smiles, "SMILES not found")


# 사용자 편의를 위해 함수도 제공
def get_toxprint(smiles, json_path=None):
    st = SmilesToxprint(json_path)
    return st.get_toxprint(smiles)
