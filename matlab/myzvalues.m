function [matrix, deltarank_kw, deltarank_desc, qs, Nkws] = myzvalues(kws, desctypes)


init;
FORCE = opts.FORCE || opts.FORCE_Z;
FORCE = 1;
% keyboard

% fname = sprintf(opts.compPath, desctype);
matrix = cell(length(desctypes), length(kws));
qs = cell(length(desctypes), length(kws));
nqs = cell(length(desctypes), length(kws));
Nkws = cell(length(desctypes), length(kws));

if nargout >= 2
    delta = zeros(length(desctypes), length(kws));
    deltanames = cell(length(desctypes), length(kws));
    
    deltarank_kw = cell(length(desctypes), length(kws));
    deltarank_desc = cell(length(desctypes), length(kws));
end

dsttype = 'rs';

% keyboard
for d = 1:length(desctypes)
    desctype = desctypes{d};
    if exist('rank_all', 'var');
        clear rank_all;
    end
    
    t_desc = tic;
    for k = 1:length(kws)
        
%         desccnt = mynumel(desctypes(1:d-1)) + 1;
        kw = kws{k};

        fname = sprintf(opts.distPath, dsttype, kw , desctype);
        fprintf('%s', fname);
        
        warning('off', 'MATLAB:load:variableNotFound');
        if exist(fname, 'file') && ~FORCE
           load(fname, 'zvalues', 'q', 'nq', 'Nkw', 'm');
        end
%        keyboard
        if exist('zvalues', 'var') && exist('q', 'var') && exist('Nkw', 'var') && exist('m', 'var') && ~FORCE
           fprintf(' ... loaded\n');
        else % cannot load from file, have to compute distances
            fprintf(' ... computing\n');
            if ~exist('rank_all', 'var');
%            keyboard
                [desc_all, rank_all] = mycollect(desctype);
                ssize = size(rank_all);
                Sbins = ssize(ssize > 1);
                Sbins = Sbins(1:end-1);
                if numel(Sbins) == 1
                	Sbins = [Sbins 1];
                end
                Nbins = prod(ssize(1:end-1));
                Ndesc = ssize(end);
                desc_all = reshape(desc_all, Nbins, Ndesc);
                desc_all = desc_all';
                rank_all = reshape(rank_all, Nbins, Ndesc);
                rank_all = rank_all';
            end
            
            [tfs, tfsn] = myquery(kws{k});
            Nkw = sum(tfs);
            Nkwn = sum(tfsn);
            
            if Nkw < 10
                fprintf('WARNING (mydistances): Only %d image(s) for kws "%s".\n', Nkw, kw);
            end
%             keyboard
%             Nnkw = sum(ntfs);

%             keyboard

            t = tic;
            T = squeeze(sum(rank_all(tfs, :), 1));
            mu_T = Nkw*(Nkw+Nkwn+1)/2;
            sigma_T = sqrt(Nkw*Nkwn*(Nkw+Nkwn+1)/12);
            zvalues = (T - mu_T) / sigma_T;
            
            zvalues = reshape(zvalues, Sbins);
            
            q = quantile(desc_all(tfs, :), [opts.q .5 1-opts.q], 1);
            m = mean(desc_all(tfs, :), 1);
            v = var(desc_all(tfs, :), [], 1);
            q9 = quantile(desc_all(tfs, :), [.1 .2 .3 .4 .5 .6 .7 .8 .9], 1);
            
 %           nq = quantile(desc_all(tfsn, :), [opts.q .5 1-opts.q], 1);
 
            mkpath(fname);
            zkw = kw;
            save(fname, 'zvalues', 'q', 'Nkw', 'zkw', 'm', 'v', 'q9');
                        
            time(k) = toc(t);
        end
        matrix{d, k} = zvalues;
        qs{d, k} = q;
%         nqs{d, k} = nq;
        Nkws{d, k} = Nkw;
        clear q
        clear nq
        clear m
        
        if nargout >= 2
            delta(d, k) = max(zvalues(:)) - min(zvalues(:));
            deltanames{d, k} = [kw '__' desctype '__' num2str(delta(d, k))];
        end
    end
%    mean(time)
    toc(t_desc)
end


% keyboard
if (nargout >= 2)
    % rank for kw
    [~, idx] = sort(delta, 1, 'descend');
    for i = 1:size(delta, 2)
        deltarank_kw(:, i) = deltanames(idx(:, i), i);
    end
    
    % rank for desc
    [~, idx] = sort(delta, 2, 'descend');
    for i = 1:size(delta, 1)
        deltarank_desc(i, :) = deltanames(i, idx(i, :));
    end
end

