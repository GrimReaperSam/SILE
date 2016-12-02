function myimport

init;

f_database = 'id_fav_kw_flickr.txt';
database = fopen(f_database, 'w');
keyboard
for i = 1:1e6
	folder = num2str(floor((i-1)/10000)+1);
	sourcefile = ['./web/images/' folder '/im' num2str(i) '.jpg'];
	
	prefix = num2str(getprefix(i));
	targetfile = sprintf(opts.photoPath, prefix, num2str(i));
	
	tagfile = ['./web/meta/tags/' folder '/tags' num2str(i) '.txt'];
	fid = fopen(tagfile);
    c = textscan(fid, '%s');
    fclose(fid);
    tags = c{1};
    
	fprintf(database, '%0.0f\t', i);
	for t = 1:length(tags)
		fprintf(database, ' <<%s>>', tags{t});
	end
	fprintf(database, '\r');
	
	if exist(sourcefile, 'file')
		fprintf('move %s -> %s\n', sourcefile, targetfile);
	    try
			movefile(sourcefile, targetfile);
		catch % create directory if not existant
			directory = regexp(targetfile, '.*\/\d\d\/', 'match');
			directory = directory{1};
			mkdir(directory);
			movefile(sourcefile, targetfile);
		end
	else
		fprintf('File not found %s', sourcefile);
	end
end
fclose(database);	