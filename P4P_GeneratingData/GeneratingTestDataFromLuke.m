% Generating Test data from Luke's data
clc; clear;

%Enter in response data for data pairing
resp{98} = 'jjjjjkjkkjjjkkkjkjjkjjkjjkkjjkkkjkjkkkkj';
resp{99} = 'kkjkkkjkkkkkjjjjjkjkjkkkkkjjkkjjkjkkjjkk';

%Function declaraions
fnAngle2UnitComplex = @(x_deg) complex(cos(x_deg/180*pi), sin(x_deg/180*pi));
fnDoubleTheta = @(z) abs(z).*fnAngle2UnitComplex(2*angle(z)/pi*180);

%Run through all the response blocks
for iiblock = 98:99

  %Get current response data and initialise arrays
  resp_ = resp{iiblock};
  resp__ = [];

  %Go through data in each trial
  for iitrial = 1:length(resp_)

    % Vector resp__ contains 0 (response = no) and 1 (yes)
    currentResponse = 0;
    if (resp_(iitrial) == 'j'), currentResponse = 1; end % ie. This is the response from the user data

    %Read in the signal properties and response from the design NN
    dsgSig = dlmread(sprintf('./stimuli/Block%d/signal_%d_%d',iiblock,iiblock,iitrial));
    dsgSigPlusNoise_ = dlmread(sprintf('./stimuli/Block%d/signal_plus_noise_%d_%d',iiblock,iiblock,iitrial));
    dsgSigPlusNoise = dsgSigPlusNoise_(5,:); % middle frame of 9 (for whatever reason this is the one that changes from signal to Signal+noise
    dsgNoise_ = dlmread(sprintf('./stimuli/Block%d/noise_%d_%d',iiblock,iiblock,iitrial));
    dsgNoise = dsgNoise_(5,:); % middle frame of 9 (again, this is the only one that changes)
    
    % Im guessing this is the "origin seed" of the design
    oriSig_deg = angle(dsgSig(1))/pi*180;

    % This applied the original offset of each signal element to the data, reverting
    % it back to normal (data is still in complex form)
    for jj = 1:64 
      dsgSigPlusNoise(jj) = fnAngle2UnitComplex(angle(dsgSigPlusNoise(jj))/pi*180 - oriSig_deg);
      dsgSig(jj) = fnAngle2UnitComplex(angle(dsgSig(jj))/pi*180 - oriSig_deg);
      dsgNoise(jj) = fnAngle2UnitComplex(angle(dsgNoise(jj))/pi*180 - oriSig_deg);
    end

    %Figure out the angle for the signal plus noise
    Angles = angle(dsgSigPlusNoise)./pi.*180;

    %Generate Gabor patches
    GaborImage = createFullGabor(Angles);

    %Plot the data
    %imshow(GaborImage)
    %title(["Signal: ", num2str(currentResponse)])

    %Save the data to the JSON format
    s.response = currentResponse;
    s.Image = GaborImage;

    %Save to file
    fileName = sprintf('Block%d_Trial%d', iiblock, iitrial);
    fid = fopen(("./ImageData/Block" + num2str(iiblock) + "/" + fileName + ".json"), 'w');
    fprintf(fid, jsonencode(s));
    fclose(fid);
   

  end 

end


