import os
import numpy as np 
import shutil 

root = "PINS"
foldernames = []

# Finding all folder
for folder in os.listdir(root):
	foldernames.append(folder)

# Finding all image in 1 folder && count each values
count_list = []
file_per_folder = []
for folder in foldernames:
	files = []
	count = 0
	for file in os.listdir(os.path.join(root, folder)):
		files.append(file)
		count += 1
	file_per_folder.append(files)
	count_list.append(count)

# Splitting data for each folder
os.makedirs(root + '/' + 'base')
os.makedirs(root + '/' + 'test')

# Creating the directory for the base database and testing data
base_dir = os.path.join(root, 'base')
test_dir = os.path.join(root, 'test')

# Splitting data 
j = 0
for filelist in file_per_folder:
	val_count = 0
	os.makedirs(os.path.join(base_dir, foldernames[j]))
	os.makedirs(os.path.join(test_dir, foldernames[j]))
	folder_path_test = os.path.join(test_dir, foldernames[j])
	folder_path_base = os.path.join(base_dir, foldernames[j])
	for i in range(len(filelist)):
		val_count += 1
		if (int(val_count) < count_list[j] * 0.2):
			path = shutil.copy(os.path.join(root, foldernames[j], filelist[i]), folder_path_test)
		else :
			path = shutil.copy(os.path.join(root, foldernames[j], filelist[i]), folder_path_base)
	j += 1


	



