function newDataset = createTestImageRandomSignal(size)
%First generate the signal, by slecting a random "offset angle"
offsetAngle = (-1 -1i) + 2*rand("like", 1i);

%Now generate the signal "pattern", where some signals are flipped
flipped = (rand(size,size) > 0.5);
signalArray = zeros(size,size);
randomOffset = randi([-2, 2]);
for i = 1:size
    for ii = 1:size
        %For the left side of the image:
        if ((i)<=(randomOffset + size/2))
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
noiseArray = (-1 -1i) + 2*rand(size,size,"like", 1i);
noiseArray = 0.7*rand()*noiseArray;

%Commbining Noise and 
signalPlusNoise = noiseArray + signalArray;

%Randomly flipping the image to make horizontal
if rand()<0.5
    signalPlusNoise = rot90(signalPlusNoise);
end

%Return the gabor image
newDataset = createFullGabor((180/pi)*angle(signalPlusNoise(:)), 1, size);

end