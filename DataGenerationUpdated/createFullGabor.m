% Creating Gabor Image from array of 64 angles
function Image = createFullGabor(Angles, border, size)
    
    %Defining block size (should be same as gabor width)
    blockSize = 64;

    % Gray square variable for border
    DefaultSqaure = uint8(128*ones(blockSize, blockSize));

    % Create a 12x12 block (96x96 pixels each block)
    count = 1;

    % Option for boarder
    if (border)

        %Initialise Image
        Image = uint8(zeros(blockSize*(size + 4), blockSize*(size + 4)));
        for i=1:(size + 4)
            for ii=1:(size + 4)
    
                % Add border
                if ((i<=2) || (i>=(size + 3))) || ((ii<=2) || (ii>=(size + 3)))
                    
                    % Fill in with a gray square
                    Image( (i*blockSize-blockSize+1):(i*blockSize) , (ii*blockSize-blockSize+1):(ii*blockSize) ) = DefaultSqaure;
    
                else
    
                    %Otherwise add the relavent gabor patch
                    Image( (i*blockSize-blockSize+1):(i*blockSize) , (ii*blockSize-blockSize+1):(ii*blockSize) ) = createSingleGabor(Angles(count), blockSize);
                    count = count + 1;
    
                end
    
            end
        end
    
        %Adding a small white dot in the middle
        Image(((blockSize*(size + 4)/2)-3):((blockSize*(size + 4)/2)+3), ((blockSize*(size + 4)/2)-3):((blockSize*(size + 4)/2)+3)) = 200;
        
    %Option for no border
    else

        %Initialise Image
        Image = uint8(zeros(blockSize*size, blockSize*size));
        for i=1:size
            for ii=1:size
    
                %Otherwise add the relavent gabor patch
                Image( (i*blockSize-blockSize+1):(i*blockSize) , (ii*blockSize-blockSize+1):(ii*blockSize) ) = createSingleGabor(Angles(count), blockSize);
                count = count + 1;

    
            end
        end
    
        %Adding a small white dot in the middle
        Image(((blockSize*size/2)-3):((blockSize*size/2)+3), ((blockSize*size/2)-3):((blockSize*size/2)+3)) = 200;

    end

end

