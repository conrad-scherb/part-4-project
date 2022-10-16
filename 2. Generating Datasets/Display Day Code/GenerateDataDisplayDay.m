%Script which generates some new data 
clc; clear;
figure(1);
imshow(uint8(128*ones(size*64+64*4,size*64+64*4)));

%For each trail:
while(1)
    
    %Clear the command window
    clc;

    %Generate Random Size of image
    rng = rand();
    if (rng < 0.33)
        size = 6;
    elseif (rng > 0.66)
        size = 8;
    else
        size = 10;
    end

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
    pause(0.5);
    imshow(uint8(128*ones(size*64+64*4,size*64+64*4)));

    %Get input from user
    currentResponse = input(("(Trial " + num2str(i) + ") Was there a signal present? (y/n/NA): "), "s");

    %Show User the answer
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

