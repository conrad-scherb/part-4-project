%Script which generates and saves data
clc; clear;

%Ask the user how many tests they want to do 
trials = input("How many images would you like to generate?: ");
size = 8;

%For each trail:
for i = 1:trials/2
    
    %Save to file
    fileName = sprintf('Image%d', i);

    %Generate a new image set
    imwrite(createTestImageRandomSignal(size), ("./RandomOffsetData/Signal/" + fileName + ".png"));

    %Generate a new image set
    imwrite(generateRandomDatasetNoSignal(size), ("./RandomOffsetData/NoSignal/" + fileName + ".png"));

end


