import os

root = "resources"

# Counting each folder for base file
count = 0
for folder in os.listdir(os.path.join(root, "base")):
    count += 1
print(f"Total base folder: {count}")

# Counting each folder for base test
count = 0
for folder in os.listdir(os.path.join(root, "test")):
    count += 1
print(f"Total test folder: {count}")

# Saving the foldernames
foldernames = []
for folder in os.listdir(root):
    foldernames.append(folder)

# Removing duplicates names that occurs from the top foldernames
foldernames.remove("base")
foldernames.remove("test")

# Counting the total number of base files
count_base = 0
for i in range(len(foldernames)):
	count = 0
	for file in os.listdir(os.path.join(root, "base", foldernames[i])):
		count_base += 1
		count += 1
	print(f"Total base file for {foldernames[i]} : {count}")
print(f"Total base file: {count_base}")

# Counting the total number of test files
count_test = 0
for i in range(len(foldernames)):
	count = 0
	for file in os.listdir(os.path.join(root, "test", foldernames[i])):
		count_test += 1
		count += 1
	print(f"Total test file for {foldernames[i]} : {count}")
print(f"Total test file: {count_test}")
