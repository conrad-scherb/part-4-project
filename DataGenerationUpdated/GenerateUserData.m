%Script which generates some new data 
clc; clear;
figure(1);
size = 10;
imshow(uint8(128*ones(size*64+64*4,size*64+64*4)));

%Ask the user how many tests they want to do 
trials = input("How many trails would you like to do?: ");
trialName = input("Name of trial: ", "s");

%For each trail:
for i = 1:trials
    
    %Clear the command window
    clc;

    %Determine whether to generate a signal or no signal
    if (rand() > 0.5)

        %Generate a signal dataset
        currentImage = generateRandomDatasetSignal(size);
        signal = true;

    else

        %Generate a non-signal dataset
        currentImage = generateRandomDatasetNoSignal(size);
        signal = false;

    end

    %Show the image set to the user for 0.5s
    imshow(currentImage);
    pause(0.75);
    imshow(uint8(128*ones(size*64+64*4,size*64+64*4)));

    %Get input from user
    currentResponse = input(("(Trial " + num2str(i) + ") Was there a signal present? (y/n/NA): "), "s");

    %Save to file
    fileName = sprintf('%s%d_Result=%d', trialName, i, currentResponse);

    %Save data in relavent folder
    if currentResponse=='y'
        
        %Determine classification of response
        if signal
            
            %Save image as a hit
            imwrite(currentImage, ("./UserDataLarge/Hit/" + fileName + ".png"));

        else

            %Save image as a hit
            imwrite(currentImage, ("./UserDataLarge/Miss/" + fileName + ".png"));

        end

    elseif currentResponse=='n'
        
        %Determine classification of response
        if signal
            
            %Save image as a hit
            imwrite(currentImage, ("./UserDataLarge/FalseAffirmation/" + fileName + ".png"));

        else

            %Save image as a hit
            imwrite(currentImage, ("./UserDataLarge/CorrectRejection/" + fileName + ".png"));

        end

    end
    

end

