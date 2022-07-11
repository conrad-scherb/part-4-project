%Function which creates a single gabor patch (orientation in deg)
function gaborPatch = createSingleGabor(orientation)

    %Defining useful variables
    gaborWidth = 95;
    standDev = 10;
    frequency = 0.03; %cycles per pixel
    phase = 0;

    %Convert units
    angle = orientation*(pi/180);
    radPerPixel = frequency*2*pi;

    %Creating a mesh grid to create the gabor patch
    widthArray = (-gaborWidth/2):(gaborWidth/2);
    [X, Y] = meshgrid(widthArray, widthArray);

    %Creating ramp function and gaussian blur
    rampFunction = sin(angle)*X + cos(angle)*Y;
    gaussianBlur = exp(-((X/standDev).^2)-((Y/standDev).^2));

    %Create the Gabor Patch
    Grating = sin(radPerPixel*rampFunction - phase);
    Gabor = Grating.*gaussianBlur;

    %Creating image from Gaussian Patch
    gaborPatch = uint8(Gabor*255 + 128);

    %Show the patch (optional)
    %figure;
    %imshow(gaborPatch);
    %title(["Orientation: ", num2str(orientation)])

end