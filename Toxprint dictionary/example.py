import sys
import os

# 현재 디렉토리의 부모 디렉토리를 경로에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'smiles_toxprint')))

from smiles_toxprint import get_toxprint

#사용예시
smiles = "OC(=O)C(F)(OC(F)(F)C(F)(OC(F)(F)C(F)(OC(F)(F)C(F)(F)C(F)(F)F)C(F)(F)F)C(F)(F)F)C(F)(F)F"
toxprint = get_toxprint(smiles)

print(len(toxprint))
