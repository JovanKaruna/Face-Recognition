# Algeo2-Face Recognition
Algeo-Face Recognition by using opencv-python
by : 
## TimDariITB :
- Jovan Karuna Cahyadi  - 13518024 - K3
- Jonathan Yudi Gunawan - 13518084 - K3
- William               - 13518138 - K3 

![Image of Us](https://github.com/JovanKaruna/Algeo2-Face/blob/master/FotoCover.jpg)
## Requirements:
- python 3
- wxpython (GUI Library for Python)
- pubsub
- numpy (vector manipulation optimization)
- opencv-python (image feature extraction)
- tqdm (progress bar)
- imageio 
- pickle
- os
- shutil (untuk membagi file menjadi 2 bagian, base dan test).

> Untuk menginstall requirements diatas dapat menggunakan manager [pip](https://pip.pypa.io/en/stable/).
> ```bash
> pip install module
> ```
> <em>*Ganti <strong>module</strong> menjadi requirements yang diperlukan</em> 

## How to use the program :
### 1. Split the photos into database and test photos
- Run the split.py
### 2. Extract the features from database photos
- Run the extractor.py
### 3. Now you can use the face recognition
- Run the dragndrop.py 
- Drag and drop the image from test photos to the GUI
- Select 2 face recognition method : cosine or euclidian
- Program will query the image and sort based on similarity
- You can match other photos by selecting the button
- Close the program to exit.

## Credits
Program ini dibuat untuk memenuhi salah satu Tugas Besar IF2123 Aljabar Linier dan Geometri Teknik Informatika ITB. 
