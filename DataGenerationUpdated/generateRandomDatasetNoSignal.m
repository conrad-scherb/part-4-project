%Fucntion which generates a random dataset
function newDataset = generateRandomDatasetNoSignal(size)

%Generate a noise array
noiseArray = (-1 -1i) + 2*rand(size,size,"like", 1i);
noiseArray = rand()*noiseArray;

%Return the gabor image
newDataset = createFullGabor((180/pi)*angle(noiseArray(:)), 1, size);

end

