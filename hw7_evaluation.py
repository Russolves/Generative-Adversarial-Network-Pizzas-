# -*- coding: utf-8 -*-
"""hw7_evaluation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fYHwZcCeaJzmaC1o1097_jcksF8Urp5s
"""

# Importing the necessary libraries
import numpy as np
import sys,os,os.path
import torch
import torch.nn as nn
import torch.nn.functional
import torchvision                  
import torchvision.transforms as tvt
from torchvision.utils import make_grid, save_image
import torch.optim as optim          
import numpy as np
from PIL import ImageFilter
import numbers
import re
import cv2
import math
import random
import copy
import matplotlib.pyplot as plt
import gzip
import pickle
import logging
import requests
import torch.autograd as autograd
from torch.optim.lr_scheduler import StepLR

import torchvision.transforms as tvt
import numpy as np
import os
import argparse
import matplotlib.pyplot as plt
from PIL import Image
from torch.utils.data import DataLoader, Dataset

# Installing pytorch-fid
!pip3 install pytorch-fid
from pytorch_fid.fid_score import calculate_activation_statistics, calculate_frechet_distance
from pytorch_fid.inception import InceptionV3

# Implementing the class for customized dataloader
class mydataloader(torch.utils.data.DataLoader):
  def __init__(self):
    self.image_path = os.listdir()
    self.transform = tvt.Compose([tvt.ToTensor(), tvt.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

  def __len__(self):
    return len(self.image_path)
  
  def __getitem__(self, idx):
    temp_image = Image.open(self.image_path[idx])
    temp_image = self.transform(temp_image).to(dtype = torch.float64)
    return temp_image

# Discriminator class for 64x64 RGB images (see fc1 for image dimensions)
class Discriminator(nn.Module):
  def __init__(self):
    super(Discriminator, self).__init__()
    self.conv1 = nn.Conv2d(3, 16, 3, padding = 1)
    self.conv2 = nn.Conv2d(16, 64, 3, padding=1)
    self.conv3 = nn.Conv2d(64, 32, 3, padding=1) 
    self.pool1 = nn.Conv2d(16, 16, 4, stride=2, padding=1)
    self.pool2 = nn.Conv2d(64, 64, 4, stride=2, padding=1)
    self.pool3 = nn.Conv2d(32, 32, 4, stride=2, padding=1)

    self.fc1 = nn.Linear((32*8*8), 256)
    self.fc2 = nn.Linear(256, 1)

  def forward(self, x):
    x = self.pool1(torch.nn.functional.relu(self.conv1(x)))
    x = self.pool2(torch.nn.functional.relu(self.conv2(x)))
    x = self.pool3(torch.nn.functional.relu(self.conv3(x)))
    x = x.view(-1, (32*8*8))
    x = torch.nn.functional.relu(self.fc1(x))
    x = torch.sigmoid(self.fc2(x))
    return x

# Generator class for generating images that are of RGB and of 64x64
class Generator(nn.Module):
    def __init__(self):
        super(Generator, self).__init__()
        self.convt1 = nn.ConvTranspose2d(256, 64, 4, stride=1)  #With random noise vectors of size 256x1x1
        self.bn1 = nn.BatchNorm2d(64)
        self.convt2 = nn.ConvTranspose2d(64, 32, 4, stride=2, padding=1)
        self.bn2 = nn.BatchNorm2d(32)
        self.convt3 = nn.ConvTranspose2d(32, 16, 4, stride=2, padding=1)
        self.bn3 = nn.BatchNorm2d(16)
        self.convt4 = nn.ConvTranspose2d(16, 8, 4, stride=2, padding=1)
        self.bn4 = nn.BatchNorm2d(8)
        self.convt5 = nn.ConvTranspose2d(8, 3, 4, stride=2, padding=1)
        self.tanh = nn.Tanh()

    def forward(self, x):
        x = torch.nn.functional.relu(self.bn1(self.convt1(x)))
        x = torch.nn.functional.relu(self.bn2(self.convt2(x)))
        x = torch.nn.functional.relu(self.bn3(self.convt3(x)))
        x = torch.nn.functional.relu(self.bn4(self.convt4(x)))
        x = self.tanh(self.convt5(x))
        return x

# Navigation to correct directory
# If using Google Drive
os.chdir("/content/drive/MyDrive/BME 64600/hw7")
print(os.getcwd())
os.listdir()

# Function for generating 1k images of fake pizza from noise vectors using trained generator
def generate_fake_pizzas(netG, netD, num_fake, gan_type="bce", batch_size = 10):
  # Check if cuda is available
  print(torch.cuda.is_available())
  device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
  # Load models
  with torch.no_grad():
    netG.load_state_dict(torch.load('/content/drive/MyDrive/BME 64600/hw7/netG_' + gan_type))
    netD.load_state_dict(torch.load('/content/drive/MyDrive/BME 64600/hw7/netD_' + gan_type))
    if torch.cuda.is_available():
        netG.cuda()
        netD.cuda()

  os.chdir("/content/drive/MyDrive/BME 64600/hw7/pizzas")

  # Create directory for fake images
  fake_img_directory = "fake_pizzas_" + gan_type
  if not os.path.exists(fake_img_directory):
    os.makedirs(fake_img_directory)
  os.chdir("/content/drive/MyDrive/BME 64600/hw7/pizzas/fake_pizzas_" + gan_type)

  # Generate fake images
  for i in range(num_fake // batch_size):
    print(f"Generating batch {i + 1} out of {num_fake // batch_size}")
    noise = torch.randn(batch_size, 256, 1, 1, device = device) #Randomly sampled noise vectors
    fake_images = netG(noise) #Generating fake images
    for j in range(batch_size):
      img_np = fake_images[j].cpu().detach().numpy()
      img_np = np.transpose(img_np, (1, 2, 0))  # Change shape to (H, W, C), since plt accepts (M, N, 3) format
      img_np = (img_np + 1) / 2  # Normalize image values to [0, 1] range
      plt.imsave(f"fake_pizza_{i * batch_size + j}.png", img_np)

# Call the function
netG = Generator()
netD = Discriminator()

num_fake = 1000 #Change this to generate different numbers of images
generate_fake_pizzas(netG, netD, num_fake, "bce")
# Do the same thing for wasserstein GAN
generate_fake_pizzas(netG, netD, num_fake, "wasserstein")

# Display the 4x4 image grid of generated images
def display_image_grid(netG, gan_type, nrow = 4):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    # Load the generator model
    netG.load_state_dict(torch.load("/content/drive/MyDrive/BME 64600/hw7/netG_" + gan_type))
    netG.to(device)
    noise = torch.randn(nrow * nrow, 256, 1, 1, device=device)  # Randomly sampled noise vectors
    fake_images = netG(noise)  # Generating fake images
    grid = make_grid(fake_images, nrow=nrow, normalize=True, scale_each=True)
    # Save the 4x4 image
    os.chdir("/content/drive/MyDrive/BME 64600/hw7")
    save_image(grid, f"4x4_Image_for_{gan_type}.png")

    # Showing the output
    grid_np = grid.cpu().detach().numpy()
    plt.imshow(np.transpose(grid_np, (1, 2, 0)))
    plt.axis('off')
    plt.show()

# Call on function and generate images
netG = Generator()
# netD = Discriminator()
# Using BCE
display_image_grid(netG, "bce", 4)
# Using Wasserstein Distance
display_image_grid(netG, "wasserstein", 4)

os.chdir("/content/drive/MyDrive/BME 64600/hw7/pizzas") #Navigate to correct directory

# Function to get list of files within a given path
def list_directories(path, gan_type = "real"):
  base_path = os.path.abspath(path)
  # print(base_path)
  if gan_type == "real":
    return [base_path + "/" + d for d in os.listdir(base_path)]
  elif gan_type == "bce":
    return [base_path + "/" + d for d in os.listdir(base_path)]
  elif gan_type == "wasserstein":
    return [base_path + "/" + d for d in os.listdir(base_path)]
  else:
    raise Exception("Please specify gan_type!")
    return None

# Function to calculate Frechet Distance
def fid_score_calculator(gan_type, dims = 2048):
  device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
  # Get the paths to the images
  file_path = os.getcwd()
  real_path = file_path + "/eval/"
  fake_path = file_path + "/fake_pizzas_" + gan_type + "/"
  # Get list
  real_paths = list_directories(real_path, "real")
  fake_paths = list_directories(fake_path, gan_type)
  # print(real_paths)
  # print(fake_paths)

  # Calculate FIDs
  block_idx = InceptionV3.BLOCK_INDEX_BY_DIM[dims]
  model = InceptionV3([block_idx]).to(device)
  m1, s1 = calculate_activation_statistics(real_paths, model, device = device)
  m2, s2 = calculate_activation_statistics(fake_paths, model, device = device)
  fid_value = calculate_frechet_distance(m1, s1, m2, s2)
  print(f"FID score for {gan_type} GAN: {fid_value:.2f}")
  return fid_value

fid_value_bce = fid_score_calculator("bce")
fid_value_wasserstein = fid_score_calculator("wasserstein")