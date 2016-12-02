%% still produces some bullshit

keyboard
desc_all = mycollect('h_hist');
ssize = size(rank_all);
Sbins = ssize(ssize > 1);
Sbins = Sbins(1:end-1);
if numel(Sbins) == 1
    Sbins = [Sbins 1];
end
Nbins = prod(ssize(1:end-1));
Ndesc = ssize(end);
desc_all = reshape(desc_all, Nbins, Ndesc);
% desc_all = desc_all';
                
[tfs, tfsn, ids, idsn, pos, N] = myquery('red');



figure(1)
cmap = jet;

hold off
for p = 1:10
    tfsp = tfs & (pos == p);
    Nkw = sum(tfsp);
    Nkwn = length(tfs) - Nkw;
    
    zvalues = zeros(16, 1);
    for d = 1:16
        
        [p,h,stats] = ranksum(desc_all(tfsp, d), desc_all(tfsn, d));
        zvalues(d) = stats.zval;
    end
    keyboard
    plot(zvalues, 'color', cmap(round(63*(p-1)/9+1), :));
    hold on;
end

