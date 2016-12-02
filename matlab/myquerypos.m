function [tfs ids] = myquerypos(kw, posnr)
% [tfs ids favs Lanno pos kws] = myquery(kw, 'pos', 0)

init;
FORCE = opts.FORCE || opts.FORCE_QUERY;
% FORCE = 1;
% keyboard

kw = lower(kw);


% check for stupidities
if posnr < 0 || round(posnr) ~= posnr
	error('myquery: posnr must be non-negative integer\n');
end


fname = [kw '_' num2str(posnr)];
fname = sprintf(opts.queryPath, fname);
% keyboard

success = 0;
fprintf('%s ... ', fname);
if exist(fname, 'file') && ~FORCE
    try
        load(fname, 'tfs');
        success = 1;
    catch
        success = 0;
    end
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
    
    
    tfs = false(length(ids), 1);

    % buil;d regexp to find kw at specific position (uses lookaheads and lookbehinds)
    if posnr == 0
        regex_poscount = '';
    else
        regex_poscount = ['^\W*?((?<=\W)\w+(?=\W)\W*?){' num2str(posnr-1) '}'];
    end
%       keyboard
    for i = 1:length(ids)
        if negate == false && ~isempty(regexpi(['.' lower(kws{i})], [regex_poscount '\W+?' kw '\W+?']))
            tfs(i) = true;
%                 keyboard
            anno = ['.' lower(kws{i}) '.'];
            anno = strrep(anno, ' <<__flickr__>>', '');
            kwpos = regexp(anno, ['(?<=\W)' kw '(?=\W)']);
            allpos = regexp(anno, '<<');
            pos(i) = sum(allpos < kwpos(1));

        elseif negate == true && isempty(regexpi(['.' lower(kws{i})], ['\W' kw '\W']))
            tfs(i) = true;
        end
    end
    
    % count number of kws in annotation string
    Lanno = zeros(length(ids), 1);
    for i = 1:length(kws)
        if regexpi(kws{i}, '__APN__')
            if regexpi(kws{i}, '^<<__APN__>>$')
                Lanno(i) = 0;
            else
                Lanno(i) = length(regexpi(kws{i}, ',')) + 1;
            end
        else
            Lanno(i) = length(regexpi(kws{i}, '<<')) - 1;
        end
    end
    
    % remove unwanted ids
    for i = 1:length(opts.reject_ids)
        idx = find(ids == opts.reject_ids(i));
        if ~isempty(idx)
            tfs(idx) = false;
        end
    end
	
    if kw ~= 0
        ids = ids(tfs);
        favs = favs(tfs);
        kws = kws(tfs);
        Lanno = Lanno(tfs);
        pos = pos(tfs);
    end
%     keyboard
    save(fname, 'ids', 'tfs', 'favs', 'Lanno', 'kws', 'pos');
    
    fprintf('done\n');
end

if nargout == 2
    varargout{1} = ids;
elseif nargout == 3
    varargout{1} = ids;
    varargout{2} = favs;
elseif nargout == 4
    varargout{1} = ids;
    varargout{2} = favs;
    varargout{3} = Lanno;
elseif nargout == 5
    varargout{1} = ids;
    varargout{2} = favs;
    varargout{3} = Lanno;
    varargout{4} = pos;
elseif nargout == 6
    varargout{1} = ids;
    varargout{2} = favs;
    varargout{3} = Lanno;
    varargout{4} = pos;
    varargout{5} = kws;
end
