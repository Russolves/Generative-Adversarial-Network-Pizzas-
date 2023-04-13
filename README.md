# GAN Image Generation with FID score evaluation
This repository contains the code for generating fake pizza images using Generative Adversarial Networks (GAN) and evaluating them using the Frechet Inception Distance (FID) score.

The code is written in Python 3 and uses the PyTorch deep learning framework.

# Overview
This repository contains an implementation of a Generative Adversarial Network (GAN) for generating pizza images and an evaluation model. The GAN is trained on a set of pizza images and learns to generate new images that are similar to the training set. The GAN uses two deep neural networks - a generator and a discriminator - which are trained simultaneously to compete against each other. The generator is tasked with generating realistic images, while the discriminator tries to differentiate between the generated images and real images. Over time, the generator learns to generate realistic images that can fool the discriminator.

# Getting Started
1. Clone repository to your local machine
2. Install the required dependencies by running the following command: pip3 install -r requirements.txt
3. Navigate to the repository folder.
4. Open the Jupyter notebook hw7_evaluation.ipynb.
5. Execute the cells in the notebook in the order they appear.

# Files and Folders
The repository contains the following files and folders:
- hw7_evaluation.ipynb: Jupyter notebook containing the code for generating fake pizza images and evaluating them using the FID score.
- requirements.txt: List of Python packages required to run the code.
- pizzas/train: Folder within pizzas containing the real pizza images used for training the GAN.
- pizzas/eval: Folder within pizzas containing the real pizza images used for evaluating the FID score.
- fake_pizzas_bce: Folder containing the fake pizza images generated using the GAN with Binary Cross Entropy (BCE) loss.
- fake_pizzas_wasserstein: Folder containing the fake pizza images generated using the GAN with Wasserstein distance.

# How it W
The code in hw7_evaluation.ipynb uses a GAN to generate fake pizza images. The generator is trained on a dataset of real pizza images, and the discriminator is trained to distinguish between real and fake pizza images. Once trained, the generator is used to generate fake pizza images, which are then evaluated using the FID score.

The mydataloader class is used to load the real pizza images into the PyTorch dataloader. The Discriminator and Generator classes define the architectures of the discriminator and generator networks, respectively. The generate_fake_pizzas function generates a specified number of fake pizza images using the trained generator and saves them in the fake_pizzas_bce and fake_pizzas_wasserstein folders. The display_image_grid function generates a 4x4 grid of fake pizza images and saves it in the repository folder. The list_directories and fid_score_calculator functions are used to calculate the FID score for the generated images.

# Findings
After executing the cells in the Jupyter notebook, the code generates 1000 fake pizza images using the GAN with BCE loss and 1000 fake pizza images using the GAN with Wasserstein distance. The generated images are saved in the fake_pizzas_bce and fake_pizzas_wasserstein folders, respectively. The display_image_grid function generates a 4x4 grid of fake pizza images for each GAN and saves it in the repository folder. The fid_score_calculator function calculates the FID score for each set of generated images.

The FID score for the generated images using the GAN with BCE loss is 49.94. The FID score for the generated images using the GAN with Wasserstein distance is 52.44.

# Requirements
- numpy
- torch
- torchvision
- PIL
- matplotlib
- gzip
- pickle
- logging
- requests
- cv2
- math
- random
- copy
