% Creating Gabor Image from array of 64 angles
function Image = createFullGabor(Angles)

    % Gray square variable for border
    DefaultSqaure = uint8(128*ones(96, 96));

    %Initialise Image
    Image = uint8(zeros(96*12, 96*12));

    % Create a 12x12 block (96x96 pixels each block)
    count = 1;
    for i=1:12
        for ii=1:12

            % Add border
            if ((i<=2) || (i>=11)) || ((ii<=2) || (ii>=11))
                
                % Fill in with a gray square
                Image( (i*96-95):(i*96) , (ii*96-95):(ii*96) ) = DefaultSqaure;

            else

                %Otherwise add the relavent gabor patch
                Image( (i*96-95):(i*96) , (ii*96-95):(ii*96) ) = createSingleGabor(Angles(count));
                count = count + 1;

            end

        end
    end

    %Adding a small white dot in the middle
    Image(572:581, 572:581) = 200;

end

