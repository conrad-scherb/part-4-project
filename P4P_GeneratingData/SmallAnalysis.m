%Script which reads in the data 
clc; clear;

%Enter in response data 
resp{98} = 'jjjjjkjkkjjjkkkjkjjkjjkjjkkjjkkkjkjkkkkj';
resp{99} = 'kkjkkkjkkkkkjjjjjkjkjkkkkkjjkkjjkjkkjjkk';

%Function declaraions
fnAngle2UnitComplex = @(x_deg) complex(cos(x_deg/180*pi), sin(x_deg/180*pi));
fnDoubleTheta = @(z) abs(z).*fnAngle2UnitComplex(2*angle(z)/pi*180);
dsgNoiseByType = {[];[];[];[]};

%Run through all the responses
for iiblock = 98:99

  %Get current response data and initialise arrays
  resp_ = resp{iiblock};
  resp__ = [];
  dsgYN = [];

  %Go through data in each trial
  for iitrial = 1:length(resp_)

    % Y and N; one per trial comprising this block (probably 20).
    dsgYN_ = dlmread(sprintf('./stimuli/Block%d/designYN_%d_%d',iiblock,iiblock,iitrial)); %ie. reading in the response for whether there was a signal
    dsgYN = [dsgYN dsgYN_]; % ie. this is the repsonse from the NN

    % Vector resp__ contains 0 (response = no) and 1 (yes)
    resp__ = [resp__, 0];
    if (resp_(iitrial) == 'j'), resp__(end) = 1; end % ie. This is the response from the user data

    % There are 4 types of response: hit, miss, CR, FA.
    if ((resp__(end) == 1) && (resp__(end) == dsgYN(iitrial))), this_type = 1; end % Hit
    if ((resp__(end) == 0) && (resp__(end) ~= dsgYN(iitrial))), this_type = 2; end % False Affirmation (FA)
    if ((resp__(end) == 0) && (resp__(end) == dsgYN(iitrial))), this_type = 3; end % Correct Rejection (CR)
    if ((resp__(end) == 1) && (resp__(end) ~= dsgYN(iitrial))), this_type = 4; end % Miss
    
    %Read in the signal properties and response from the design NN
    dsgSig = dlmread(sprintf('./stimuli/Block%d/signal_%d_%d',iiblock,iiblock,iitrial));
    dsgSigPlusNoise_ = dlmread(sprintf('./stimuli/Block%d/signal_plus_noise_%d_%d',iiblock,iiblock,iitrial));
    dsgSigPlusNoise = dsgSigPlusNoise_(5,:); % middle frame of 9 (for whatever reason this is the one that changes from signal to Signal+noise
    dsgNoise_ = dlmread(sprintf('./stimuli/Block%d/noise_%d_%d',iiblock,iiblock,iitrial));
    dsgNoise = dsgNoise_(5,:); % middle frame of 9 (again, this is the only one that changes)
    
    % Im guessing this is the "origin seed" of the design
    oriSig_deg = angle(dsgSig(1))/pi*180;

    % If the original offset is zero, signals remain the same
    if (dsgYN(iitrial) == 0), oriSig_deg = 0; end

    % This applied the original offset of each signal element to the data, reverting
    % it back to normal (data is still in complex form)
    for jj = 1:64 
      dsgSigPlusNoise(jj) = fnAngle2UnitComplex(angle(dsgSigPlusNoise(jj))/pi*180 - oriSig_deg);
      dsgSig(jj) = fnAngle2UnitComplex(angle(dsgSig(jj))/pi*180 - oriSig_deg);
      dsgNoise(jj) = fnAngle2UnitComplex(angle(dsgNoise(jj))/pi*180 - oriSig_deg);
    end
   
   %This figure here is basically a representation of the signal (black)
   %and noise (red). From this you can pretty easily see the texture
   %boundary (if it exists) in the middle. In the first image all the
   %signal components on the left side are horizontal, while those on the
   %right side are vertical.
   figure; hold on
   subplot(8,8,1)
   for jj = 1:64
    subplot(8,8,jj); hold on
    plot([0 real(dsgSig(jj))],[0 imag(dsgSig(jj))],'-k'); axis square; axis(1.1*[-1 1 -1 1]);
    plot([0 real(dsgNoise(jj))],[0 imag(dsgNoise(jj))],'-r'); axis square; axis(1.1*[-1 1 -1 1]);
    set(gca, 'xtick', [-100 100], 'ytick', [-100 100]);
   end

   %This line then adds tbe noise data to the corresponding data
   dsgNoiseByType{this_type} = vertcat(dsgNoiseByType{this_type}, fnDoubleTheta(dsgNoise));

  end % iitrial

% Overall accuracy for block (represented as the amount per block)
  resp___ = resp__ == dsgYN; 
  sum(resp___)

end % iiblock

%%%
% There are 4 types of response: hit, miss, CR (correct rejection), FA (false affirmation).
%%%%%
va = mean(dsgNoiseByType{4},1) + mean(dsgNoiseByType{1},1) - mean(dsgNoiseByType{2},1) - mean(dsgNoiseByType{3},1); %ie. types 1 & 4 are correct responses by the NN
fnIsotropics = @(x) cos(x) + i*sin(x);
BOOT = 1000;
Bva = zeros(BOOT,length(va));
for iiboot = 1:BOOT
  aa = fnIsotropics(pi*2*(rand(size(dsgNoiseByType{1}))-0.5));
  bb = fnIsotropics(pi*2*(rand(size(dsgNoiseByType{2}))-0.5));
  cc = fnIsotropics(pi*2*(rand(size(dsgNoiseByType{3}))-0.5));
  dd = fnIsotropics(pi*2*(rand(size(dsgNoiseByType{4}))-0.5));
  Bva(iiboot,:) = mean(dd,1) + mean(aa,1) - mean(bb,1) - mean(cc,1);
end

vaz = zeros(1,length(va));
for jj = 1:64
  vaz(jj) = (abs(va(jj)) - mean(abs(Bva(:,jj)))) / std(abs(Bva(:,jj)));
end


