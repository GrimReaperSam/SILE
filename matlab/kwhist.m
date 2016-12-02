function [kwh freq] = kwhist()


% keyboard

kwh = cell(1e6,1);
freq = zeros(1e6,1);

lastkw = 1;
mem = [];

% read mirflickr database
fid = fopen('id_kw_mirflickr.txt');
c = textscan(fid, '%u64 %s', 'delimiter', '\t', 'bufsize', 1000000);
fclose(fid);
kws = c{2};

Nkw = length(kws);

for i = 1:Nkw
    mem = progressbar(mem, i, Nkw);

    line = kws{i};
    if strcmp(line, '')
        continue;
    end
    delimiter = '<<';
    pos = regexp(line, delimiter);
    pos = [pos length(line)+1];
    for p = 1:length(pos)-1
        kw = line(pos(p)+2:pos(p+1)-4);
        kw = lower(kw);
        if isempty(kw)
            continue;
        end
        tf = strcmpi(kw, kwh);
        if any(tf)
            idx = find(tf, 1, 'first');
            freq(idx) = freq(idx) + 1;
        else
            if lastkw > length(kwh)
                kwh = [kwh; cell(floor(.1*length(kwh)), 1)];
                freq = [freq; zeros(floor(.1*length(kwh)), 1)];
            end
            kwh{lastkw} = kw;
            freq(lastkw) = 1;
            lastkw = lastkw + 1;
        end
    end
end

kwh = kwh(1:lastkw);
freq = freq(1:lastkw);

[freq idx] = sort(freq, 'descend');
kwh = kwh(idx);