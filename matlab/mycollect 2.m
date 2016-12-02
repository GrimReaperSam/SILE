function [descs, N, ids] = mycollect(name, varargin)
init;

FORCE = opts.FORCE || opts.FORCE_COLLECT;
% keyboard
% FORCE = 1;

% default values
kw = 0;
posnr = 0;

% parse varargin
i = 1;
while i <= size(varargin, 2)
    if isnumeric(varargin{i})
        posnr = varargin{i};
    elseif ischar(varargin{i})
        kw = varargin{i};
    else
        error('mycollect: unrecognized input argument %s', varargin{i});
    end
    i = i+1;
end

fnameall = sprintf(opts.collPath, name, '__all__');
if kw == 0
    fname = fnameall;
else
    kw = lower(kw);
    if posnr > 0
        fname = sprintf(opts.collPath, name, [kw '_' num2str(posnr)]);
    else
        fname = sprintf(opts.collPath, name, kw);
    end
end

% keyboard

fprintf('%s ... ', fname);
if exist(fname, 'file') && ~FORCE
	load(fname, 'descs');
    fprintf('loaded\n');
else
    if exist(fnameall, 'file') && ~FORCE
        fprintf('collecting from m file\n');
        load(fnameall, 'descs', 'ids');
    else
        fprintf('collecting from hd\n');
        % getting all descriptors from hd and put into file
        [tfs, tfsn, ids] = myquery(0);
        
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
        try
	        save(fnameall, 'descs', 'ids', '-v7.3');
        catch
        	directory = regexp(fnameall, '.*\/\d\d\/', 'match');
			directory = directory{1};
			mkdir(directory);
			save(fnameall, 'descs', 'ids', '-v7.3');
			end
        
        if kw == 0
            N = size(descs);
			N = N(1:end-1);
			N = sum(N);
            return;
        end
    end
%     keyboard
    % ids corresponding to the kw
    [tfs, tfsn, ids] = myquery(kw, 'pos', posnr);
    
    descs = descs(tfs);
    ids = ids(tfs);
    try
	    save(fname, 'descs', 'ids');
	catch % create directory if not existant
		directory = regexp(fname, '.*\/\d\d\/', 'match');
		directory = directory{1};
		mkdir(directory);
		save(fname, 'descs', 'ids');
	end

end
N = size(descs);
N = N(1:end-1);
N = sum(N);
