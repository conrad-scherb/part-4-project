%Fucntion which generates a random dataset 
function newDataset = generateRandomDatasetSignal()

%First generate the signal, by slecting a random "offset angle"
offsetAngle = (-1 -1i) + 2*rand("like", 1i);

%Now generate the signal "pattern", where some signals are flipped
flipped = (rand(8,8) > 0.5);
signalArray = zeros(8,8);
for i = 1:8
    for ii = 1:8
        %For the left side of the image:
        if (i<=4)
            %If the random integer is 1, flip the signal
            if (flipped(i,ii))
                signalArray(i,ii) = offsetAngle;
            else
                signalArray(i,ii) = offsetAngle*-1;
            end
        else
            %For the right side of the image
            if (flipped(i,ii))
                signalArray(i,ii) = offsetAngle*1j;
            else
                signalArray(i,ii) = offsetAngle*1j*-1;
            end
        end
    end
end

%Generate a noise array
noiseArray = (-1 -1i) + 2*rand(8,8,"like", 1i);
noiseArray = 0.7*rand()*noiseArray;

%Commbining Noise and 
signalPlusNoise = noiseArray + signalArray;

%Return the gabor image
newDataset = createFullGabor((180/pi)*angle(signalPlusNoise(:)), 1);

end

