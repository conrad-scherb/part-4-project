%Plotting Figure for poster
clc; clear;

%Definining kernel & Neuron numbers
kernels = 7:2:17;
neurons = [64, 32, 16, 8, 4];
[X, Y] = meshgrid(kernels, neurons);
accuracies = [55.2 83.4 91.2 92.4 92.5 90.4;
    54.5 79.2 90.7 92.5 91.2 84.5;
    54.6 78.9 90.2 91.5 73.7 56.7;
    54.1 68.0 88.4 91.7 71.0 55.2;
    54.7 62.6 86.2 91.1 68.3 56.5];

%Create graph
figure;
CO(:,:,1) = ones(6).*linspace(0,0.5,6); % red
CO(:,:,2) = zeros(6); % green
CO(:,:,3) = ones(6)*0.8; % blue
s = surf(X, Y, accuracies, CO(1:5, 1:6, :), FaceAlpha=0.6);
xlabel("Kernel Number"); ylabel("Neuron Number"); zlabel("Validation Accuracy");
xticks([7, 9, 11, 13, 15, 17]); yticks([4, 8, 16 ,32, 64]);
xlim([7, 17]); ylim([4 64]);