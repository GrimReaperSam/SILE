function mkpath(path)

directory = regexp(path, '.*\/', 'match');
directory = directory{1};
if ~exist(directory, 'dir')
    mkdir(directory);
end
