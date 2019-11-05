import os
import shutil
from tqdm import tqdm

"""
Program untuk melakukan ekstraksi seluruh data dari tiap folder menjadi 1 database.
"""

root = os.path.join("resources", "base")
foldernames = []

for folder in tqdm(os.listdir(root)):
    foldernames.append(folder)

folder_path = []
for folder in tqdm(foldernames):
    folder_path.append(os.path.join(root, folder))

for i in tqdm(range(len(folder_path))):
    for file in os.listdir(folder_path[i]):
        path = shutil.copy(os.path.join(folder_path[i], file), root)
