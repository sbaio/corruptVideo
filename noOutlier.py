# -*- coding: utf-8 -*-
import cv2
import numpy as np
from matplotlib import pyplot as plt

from scipy.spatial.distance import pdist,squareform
from itertools import combinations

cap = cv2.VideoCapture("corrupted_video.mp4")
ret, frame = cap.read()

frames = []
hists = np.array([]).reshape(256,0)

# ------ get all the frames and calculate their histograms -----
while(ret):
	#frame = cv2.resize(frame,None,fx=0.1, fy=0.1, interpolation = cv2.INTER_CUBIC)
	frames.append(frame)
	hist = cv2.calcHist([frame],[0],None,[256],[0,256])
	hists = np.append(hists,hist/65536.,axis=1)
	ret, frame = cap.read()

hists = hists.transpose()
Y = squareform(pdist(hists, 'euclidean'))

N = np.argsort(Y, axis=1)

# ----- sort min method ---- 
# pair similarity bewteen inliers histograms
pd = pdist(hists, 'euclidean')
ind = np.argsort(pd)
li = list(combinations(np.arange(hists.shape[0]),2))
count_list = [0 for i in range(hists.shape[0])]


couples_list = []

for k in ind:
	i,j = li[k]
	

	possible_indexes_i = N[i][1:20]
	
	if count_list[i]< 2 and count_list[j]<2 and j in possible_indexes_i:
		couples_list.append([i,j])
		count_list[i] += 1
		count_list[j] += 1
		
	if len(couples_list)==(hists.shape[0]-1):
		break

ones_indices = [i for i,j in enumerate(count_list) if j==1]

chains = []
for c,start_index in enumerate(ones_indices):
	print '-------> start index , %d'%start_index
	find_index = start_index
	chain = [start_index]
	while 1:
		a = [(index,couple) for index,couple in enumerate(couples_list) if find_index in couple]
		if not a:
			break
		#print find_index
		i = a[0][1].index(find_index)
		find_index = a[0][1][1-i]
		chain.append(find_index)
		couples_list[a[0][0]]=[]
	print ' -----> chain %d'%c 
	print chain
	chains.append(chain)


for i in chains[1]:
	img = cv2.resize(frames[i],None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
	cv2.imshow('Video',img)
	cv2.waitKey(0)
cv2.destroyAllWindows()
print 'finished'













