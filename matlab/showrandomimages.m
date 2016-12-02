function ids = showrandomimages(kw1, varargin)

i = 1;
n = 1;
kw2 = '';
while i <= size(varargin, 2)
    if isnumeric(varargin{i})
        n = varargin{i};
    else
        kw2 = varargin{i};
    end
    i = i+1;
end

[~, ids] = myquery(kw1, kw2);
N = length(ids);
fprintf('%s+%s: %d images\n', kw1, kw2, N);
if n > N
    n = N;
end

r = randperm(N);
ids = ids(r(1:n));

sqrtn = ceil(sqrt(n));

figure(111);
hold off;
for i = 1:n
    id = ids(i);
    subplot(sqrtn, sqrtn, i);
    imagesc(myget(id, 'srgb'));
    axis off;
    axis equal;
    title(num2str(id));
end
