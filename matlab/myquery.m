function [tfs, tfsn, ids, idsn, pos, N] = myquery(kw)
% [tfs ids favs Lanno pos kws] = myquery(kw)

init;
FORCE = opts.FORCE || opts.FORCE_QUERY;
% FORCE = 1;
% keybo0ard

if kw == 0
    fname = sprintf(opts.queryPath, '__all__');
else
    fname = sprintf(opts.queryPath, kw);
end
% keyboard

success = 1;
fprintf('%s ... ', fname);
if exist(fname, 'file') && ~FORCE
    try
        load(fname, 'tfs', 'ids', 'tfsn', 'idsn', 'pos', 'N');
    end
end
if ~(exist('tfs', 'var') && exist('ids', 'var') && exist('tfsn', 'var') && exist('idsn', 'var'))
    success = 0;
end

if success == 1
	fprintf('loaded\n');
else
    fprintf('querying ... ');
    timer = tic;
    % read flickr database
    fid = fopen('./id_kw_mirflickr.txt');
    c = textscan(fid, '%u64 %s', 'delimiter', '\t', 'bufsize', 100000);
    fclose(fid);
    ids = c{1}; kws = c{2};
    
    N = nan(length(ids), 1);
    for i = 1:length(kws)
        tmp = strfind(kws{i}, '<<');
        N(i) = length(tmp);
%         keyboard
    end

    if kw == 0
        tfs = true(length(ids), 1);
        tfsn = false(length(ids), 1);
        idsn = [];
    else
        tfs = false(length(ids), 1);
    	tfsn = true(length(ids), 1);
        pos = nan(length(ids), 1);
    	
%       keyboard
        for i = 1:length(ids)
            regpos = regexpi(['.' lower(kws{i})], ['\W+?' kw '\W+?']);
            if ~isempty(regpos)
                tfs(i) = true;
                tfsn(i) = false;
%                 keyboard
                tmp = kws{i}(1:regpos(1));
                tmp = strfind(tmp, '<<');
                pos(i) = length(tmp) + 1;
            end
        end
    end
	
    % remove unwanted ids
    for i = 1:length(opts.reject_ids)
        idx = find(ids == opts.reject_ids(i));
        if ~isempty(idx)
            tfs(idx) = false;
            tfsn(idx) = false;
            pos(idx) = nan;
        end
    end
	
    if kw~=0
        idsn = ids(tfsn);
        ids = ids(tfs);
    end
    
%     keyboard
    save(fname, 'tfs', 'ids', 'tfsn', 'idsn', 'pos', 'N');
    
    timer = toc(timer);
    fprintf('%3.1f s\n', timer);
end

