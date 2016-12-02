function centers = make_kmeans_hist()

% keyboard
path(path, './code/kmeanspp');

[~, ~, ids] = myquery(0);
ids = ids(randperm(length(ids)));

Ntot = 900;
Ncenters = 500;

Nsubpx = 1000;
Nstep = 30;

Nsubcenter = 0;
subcenters = zeros(Nstep*Nsubpx, 3);

for i = 1:Nstep:Ntot
    fprintf('i=%d\n', i);
    Npx = 0;
    labs = zeros(Nstep*Nsubpx, 3);

    for ii = i:min(i+Nstep-1, Ntot)
        lab = myget(ids(ii), 'cielab');
        Nlab = size(lab);
        Nlab = Nlab(1) * Nlab(2);
        lab = reshape(lab, [Nlab 3]);
        idx = randperm(Nlab);
        idx = idx(1:Nsubpx);
        lab = lab(idx, :);
        labs(Npx+1:Npx+Nsubpx, 1:3) = lab;
        Npx = Npx + Nsubpx;
    end
%     keyboard
    labs = labs(1:Npx, :);
%     [f c] = litekmeans(labs', Ncenters);
    [L c] = kmeanspp(labs', Ncenters);
    subcenters(Nsubcenter+1:Nsubcenter+Ncenters, :) = c';
    Nsubcenter = Nsubcenter + Ncenters;
end

subcenters = subcenters(1:Nsubcenter, :);

[f c] = kmeanspp(subcenters', Ncenters);
centers = c';

