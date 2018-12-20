% adapted from talmo/vid2hdf5.m https://gist.github.com/talmo/d3c6c06a48d416a9848602aff5166e81
% Clean start!
clear all, clc

disp('NOTE THAT THIS IS ASSUMING UINT8!!!')

%% Parameters
% Path to input file
videoPath = 'C:\Users\rldun\Desktop\data 2 upload\20181120_KS\181120_RLD_tierpsy2\181120_FC050_atr+_turning_backlight_on_2-11202018175242.avi'

% Path to output file
% savePath = '..\..\leap\data\examples\072212_163153.clip.h5';
savePath = 'C:\Users\rldun\Desktop\data 2 upload\20181120_KS\181120_RLD_tierpsy2\181120_FC050_atr+_turning_backlight_on_2-11202018175242.hdf5'

%videoPath = 'temp.m4v'
savePath = 'output.hdf5'

% Frames to convert at a time (lower this if your memory is limited)
chunkSize = 1;

% Convert frames to single channel grayscale images (instead of 3 channel RGB)
grayscale = true;

%% Initialize
% Open video for reading
vr = VideoReader(videoPath);

% Check size from first frame
I0 = vr.readFrame();
if grayscale
    I0 = rgb2gray(I0); 
end
frameSize = size(I0);
if numel(frameSize) == 2
    frameSize = [frameSize 1]; 
end

% Reset VideoReader
delete(vr);
vr = VideoReader(videoPath);

% Check if file already exists
if exist(savePath,'file') > 0
    warning(['Overwriting existing HDF5 file: ' savePath])
    delete(savePath)
end

% Create HDF5 file with infinite number of frames and GZIP compression
datasetname = '/mask';
maxframes = floor(vr.duration * vr.framerate);
%h5create(savePath,datasetname,[frameSize(1), frameSize(2), inf],'ChunkSize',[frameSize], 'DataType', 'uint8', 'Deflate',1)
h5create(savePath,datasetname,[frameSize(1), frameSize(2), maxframes],'ChunkSize',[frameSize], 'DataType', 'uint8', 'Deflate', 1)

%% Save
buffer = cell(chunkSize,1);
done = false;
framesRead = 0;
framesWritten = 0;
t0 = tic;
while ~done
    
    % sanity check
    if mod(framesWritten, 100) == 0
        disp(framesWritten); 
    end
    
    % Read next frame
    I = vr.readFrame();
    if grayscale; I = rgb2gray(I); end
    
    % Check if there are any frames left
    done = ~vr.hasFrame();

    % Increment frames read counter and add to the write buffer
    framesRead = framesRead + 1;
    buffer{mod(framesRead-1, chunkSize)+1} = I;
    
    % if we've maxed out our max frames
    if framesRead >= maxframes
        done = 1
    end
    
    % Have we filled the buffer or are there no frames left?
    if mod(framesRead, chunkSize) == 0 || done
        % Concatenate the buffer into an array
        chunk = cat(3, buffer{:});
        
        % Extend the dataset and save to disk
        % need to add singleton to last param if chunkSize = 1
        h5write(savePath, datasetname, chunk, [1 1 framesWritten+1], [size(chunk), 1])
        % otherwise this works
        %h5write(savePath, datasetname, chunk, [1 1 framesWritten+1], [size(chunk)])
        
        % Increment frames written counter
        framesWritten = framesWritten + size(chunk,3);
    end
end
elapsed = toc(t0);
fprintf('Finished writing %d frames in %.2f mins.\n', framesWritten, elapsed/60)

h5disp(savePath)