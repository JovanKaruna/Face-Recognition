import os

root = "PINS"

count = 0
for folder in os.listdir(os.path.join(root, "base")):
    count += 1
print(f"Total base folder: {count}")

count = 0
for folder in os.listdir(os.path.join(root, "test")):
    count += 1
print(f"Total test folder: {count}")

foldernames = []
for folder in os.listdir(root):
    foldernames.append(folder)

count_base = 0
for i in range(len(foldernames)):
    for file in os.listdir(os.path.join(root, "base", foldernames[i])):
        count_base += 1
print(f"Total base file: {count_base}")

count_test = 0
for i in range(len(foldernames)):
    for file in os.listdir(os.path.join(root, "test", foldernames[i])):
        count_test += 1
print(f"Total test file: {count_test}")
