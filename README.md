# Generative-Adversarial-Network-Pizzas-
A generative adversarial network engineered that utilizes a discriminator and a generator. The GAN can be trained using a Binary Cross Entropy Loss or a Wasserstein Distance Loss to generate replicate images based on input data.

# Overview
This repository contains an implementation of a Generative Adversarial Network (GAN) for generating pizza images and an evaluation model. The GAN is trained on a set of pizza images and learns to generate new images that are similar to the training set. The GAN uses two deep neural networks - a generator and a discriminator - which are trained simultaneously to compete against each other. The generator is tasked with generating realistic images, while the discriminator tries to differentiate between the generated images and real images. Over time, the generator learns to generate realistic images that can fool the discriminator.

#Requirements
numpy
torch
torchvision
PIL
matplotlib
gzip
pickle
logging
requests
cv2
math
random
copy

