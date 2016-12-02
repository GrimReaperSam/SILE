function mycollect_mirimport()
% import edge histogram and homogeneous texture descriptors that are
% available on the mireflickr website
init;

% keyboard

descs = {'eh' 'ht'};
N = [150 43];

for d = 1:length(descs)
    name = descs{d};
    directory = ['./DB/mirlickr_precomputed/' name '/'];
    fnameall = sprintf(opts.collPath, name, '__all__')
    

    dimensions = N(d);
    for dd = length(dimensions)+1:6
        dimensions(dd) = 1;
    end
    dimensions(7) = 1e6;
    descs = zeros(dimensions, 'single');
    
%     keyboard
    fprintf('reading text files ...    ');
    t = tic;
    %loop over 100 files
    for f = 1:100
        fprintf('\b\b\b%3.0f', f);
        fid = fopen([directory name num2str(f) '.txt'], 'r');
        for i = 1:1e4
            data = fscanf(fid, '%f', N(d));
            idx = (f-1)*1e4+i;
            descs(:, :, :, :, :, :, idx) = single(data);
        end
        fclose(fid);
        
    end
    fprintf('\b\b\b%fs\n', toc(t));
    
    fprintf('compute ranks ... ');
    t = tic;
    % compute ranks
    ranks = mexranks(reshape(descs, prod(dimensions(1:end-1)), dimensions(end))');
    ranks = reshape(ranks', dimensions);
    fprintf('%fs\n', toc(t));
    
    fprintf('saving to %s ... ', fnameall);
    ids = uint64(1:1e6)';
    t = tic;
    try
        save(fnameall, 'descs', 'ids', 'ranks', '-v7.3');
    catch
        directory = regexp(fnameall, '.*\/', 'match');
        directory = directory{1};
        mkdir(directory);
        save(fnameall, 'descs', 'ids', 'ranks', '-v7.3');
    end
    fprintf('%fs\n', toc(t));
end
