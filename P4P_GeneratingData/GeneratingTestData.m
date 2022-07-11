% Script for running and creating images
clc; clear;

%Generating list of angles
Angles = linspace(1,360,64);

%Generate the Gabor patch
GaborImage = createFullGabor(Angles);

%Show the image
imshow(GaborImage);