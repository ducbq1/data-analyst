from __future__ import absolute_import

import torch
from torch import nn
from torch.nn import functional as F
from torch.autograd import Variable
import torchvision
from IPython.core.debugger import set_trace


__all__ = ['ResNet50','ResNet50_7Stripe','ResNet18']

class ResNet50(nn.Module):
	def __init__(self, num_classes, **kwargs):
		super(ResNet50, self).__init__()		
		resnet50 = torchvision.models.resnet50(pretrained=True)
		# for param in resnet50.parameters():
		# 	param.requires_grad=False # or param.requires_grad_(False)      
		self.base = nn.Sequential(*list(resnet50.children())[:-2])
		self.feat_dim = 2048
		self.classifier = nn.Linear(self.feat_dim, num_classes)

	def forward(self, x):
		b = x.size(0)				
		x = self.base(x)		
		x = F.avg_pool2d(x, x.size()[2:])
		f = x.view(b, self.feat_dim)		
		y = self.classifier(f)		
		return y, f	

class ResNet50_7Stripe(nn.Module):
	def __init__(self, num_classes, **kwargs):
		super(ResNet50_7Stripe, self).__init__()		
		resnet50 = torchvision.models.resnet50(pretrained=True)
		self.base = nn.Sequential(*list(resnet50.children())[:-2])
		self.feat_dim = 14336
		self.classifier = nn.Linear(self.feat_dim, num_classes)
	def forward(self, x):
		b = x.size(0)				
		x = self.base(x)		
		f = F.avg_pool2d(x, (1,7))		# [2048,7,1]
		f = f.view(b,self.feat_dim)		# [14336]		
		y = self.classifier(f)
		return y, f	

class ResNet18(nn.Module):
	def __init__(self, num_classes, **kwargs):
		super(ResNet18, self).__init__()		
		resnet18 = torchvision.models.resnet18(pretrained=True)
		# for param in resnet50.parameters():
		# 	param.requires_grad=False # or param.requires_grad_(False)      
		self.base = nn.Sequential(*list(resnet18.children())[:-2])
		self.feat_dim = 512
		self.classifier = nn.Linear(self.feat_dim, num_classes)

	def forward(self, x):
		b = x.size(0)				
		x = self.base(x)		
		x = F.avg_pool2d(x, x.size()[2:])
		f = x.view(b, self.feat_dim)		
		y = self.classifier(f)		
		return y, f	