function [descs, ranks, ids] = mycollect(name)
init;

FORCE = opts.FORCE || opts.FORCE_COLLECT;
% keyboard
% FORCE = 1;

fnameall = sprintf(opts.collPath, name, '__all__');
% keyboard

fprintf('%s ... ', fnameall);
if exist(fnameall, 'file') && ~FORCE
    load(fnameall, 'descs', 'ids', 'ranks');
    fprintf('loaded\n');
else
    fprintf('collecting from hd\n');
    % getting all descriptors from hd and put into file
    [~, ~, ids] = myquery(0);

    first = single(mydescribe(ids(1), name));
    dimensions = size(first);
    for d = length(dimensions)+1:6
        dimensions(d) = 1;
    end
    dimensions(7) = length(ids);
    descs = zeros(dimensions, 'single');
    for i = 1:length(ids)
        fprintf('%d/%d ', i, length(ids));
%             keyboard
        % save descriptors of differen timages along the 7th dimension to have enough other dimensions for any kin of descriptor i want to collect
        descs(:, :, :, :, :, :, i) = single(mydescribe(ids(i), name));
    end

    % compute ranks
    ranks = mexranks(reshape(descs, prod(dimensions(1:end-1)), dimensions(end))');
    ranks = reshape(ranks', dimensions);
    
    try
        save(fnameall, 'descs', 'ids', 'ranks', '-v7.3');
    catch
        directory = regexp(fnameall, '.*\/', 'match');
        directory = directory{1};
        mkdir(directory);
        save(fnameall, 'descs', 'ids', 'ranks', '-v7.3');
    end

end
