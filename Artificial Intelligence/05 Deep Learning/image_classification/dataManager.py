import os
import sys
import cv2 as cv
import numpy as np
import os.path as osp
from PIL import Image
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from torchvision import datasets, models, transforms
sys.path.append("./libs")  # Adds higher directory to python modules path.
from utils import mkdir_if_missing, write_json, read_json


from IPython.core.debugger import set_trace

def read_image(img_path):
	"""Keep reading image until succeed. This can avoid IOError incurred by heavy IO process."""
	got_img = False
	while not got_img:
		try:            
			img = Image.open(img_path).convert('RGB')			
			got_img = True
		except IOError:
			print("IOError incurred when reading '{}'. Will redo. Don't worry. Just chill.".format(img_path))
			pass
	return img

class AfosrDataset(Dataset):
	def __init__(self,img_dir, annotation_file_path,
		transform=None,
		use_albumentations=False,):
		self.img_dir = img_dir
		self.annotation_file_path = annotation_file_path        
		self.transform = transform
		self.use_albumentations = use_albumentations

		self.images = []
		self.labels = []

		with open(self.annotation_file_path) as f:
			subject_dirs = [_.strip() for _ in f.readlines()]
			for subject_dir in subject_dirs:
				subject_dir_path = os.path.join(self.img_dir, subject_dir)
				for timestamp_dir in sorted(os.listdir(subject_dir_path)):
					timestamp_dir_path = os.path.join(subject_dir_path, timestamp_dir)
					for mhi_file in filter(lambda _: _.endswith('.jpg'),
											 sorted(os.listdir(timestamp_dir_path))):
						label = int(os.path.splitext(mhi_file)[0]) - 1
						mhi_file = os.path.join(subject_dir, timestamp_dir, mhi_file)
						self.images.append((mhi_file, subject_dir))
						self.labels.append(label)
		
	def __len__(self):		
		return len(self.images) 		
		
	def __getitem__(self, idx):	
		mhi_file, subject = self.images[idx]
		mhi_path = os.path.join(self.img_dir, mhi_file)	
		img = read_image(mhi_path)
		if self.transform is not None:
			img = self.transform(img)										
		return img, self.labels[idx]

if __name__ == '__main__':
	data_dir='/mnt/works/projectComvis/AFOSR-2020/MotionHistoryImage/MHI_images'
	data_list='/home/nhquan/datasets/afosr2022/split_by_subjectid/train.txt'			
	scaler = transforms.Resize((224, 224))
	normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
		std=[0.229, 0.224, 0.225])    
	transforms= transforms.Compose([
		scaler,
		transforms.ToTensor()
		#normalize		
		])   
			
	train_dataset = AfosrDataset(data_dir,data_list,transform=transforms) 
	train_loader = DataLoader(train_dataset, batch_size=64, shuffle=False, num_workers=2)	  
	#### preview imgae  
	cv.namedWindow('image',cv.WINDOW_NORMAL)
	for i, batch in enumerate(train_loader):		
		imgs=batch[0]
		pids=batch[1]
		for i in range(len(imgs)):			
			image=imgs[i].permute(1,2,0).numpy()       
			print (pids[i].numpy())
			cv.imshow('image',cv.cvtColor(image, cv.COLOR_RGB2BGR))
			if cv.waitKey(50)==27:
				cv.destroyAllWindows()	
				sys.exit()  
	