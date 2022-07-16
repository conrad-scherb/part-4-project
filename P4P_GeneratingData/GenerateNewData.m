%Script which generates some new data 
clc; clear;
figure(1);
imshow(uint8(128*ones(768,768)));

%Ask the user how many tests they want to do 
trials = input("How many trails would you like to do?: ");
trialName = input("Name of trial: ", "s");

%For each trail:
for i = 1:trials
    
    %Clear the command window
    clc;

    %Generate a new image set
    currentImage = generateRandomDataset();

    %Show the image set to the user for 0.5s
    imshow(currentImage);
    pause(0.5);
    imshow(uint8(128*ones(768,768)));

    %Get input from user
    currentResponse = input("Was there a signal present? (y/n/NA): ", "s");

    %Save to file
    fileName = sprintf('%s%d_Result=%d', trialName, i, currentResponse);

    %Save data in relavent folder
    if currentResponse=='y'
        
        %Write Image
        imwrite(currentImage, ("./NewImageData/Signal/" + fileName + ".png"));

    elseif currentResponse=='n'
        
        %Write Image
        imwrite(currentImage, ("./NewImageData/NoSignal/" + fileName + ".png"));

    end
    

end

