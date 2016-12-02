path(path, '/Users/ajl/Documents/epfl/LCAV2/mirflickr/');

init

kws = opts.kwgeq500;
Nk = length(kws);
descs = {'gy_hist' 'c_hist' 'h_hist' 'ab_hist21' 'lab_hist9' 'sunhist' 'lch_hist9' 'l_layout' 'c_layout' 'h_layout' 'details_hist_01' 'gabor_hist' 'gabor_layout' 'lbp_hist'};
Nd = length(descs);

% matrix = myzvalues(kws, descs);

cmap = hsv_;

%% write output
fid = fopen('z_values.html', 'w');
fprintf(fid, '<table cellspacing="0" cellpadding="1" border="1" width="300" >\n');
for k = 1:Nk
    fprintf(fid, '<tr>\n');
    fprintf(fid, '<td>%s</td>\n', kws{k});
    for d = 1:Nd
        z = matrix{d, k};        
        dz = max(z(:)) - min(z(:));
        c = min(150, dz);
        c = round(c/150*63)+1;
        
        r = dec2hex(round(255*cmap(c,1)));
        g = dec2hex(round(255*cmap(c,2)));
        b = dec2hex(round(255*cmap(c,3)));
        
        if length(r) == 1
            r = ['0' r];
        end
        if length(g) == 1
            g = ['0' g];
        end
        if length(b) == 1
            b = ['0' b];
        end
        hex = ['#' r g b];
        fprintf(fid, '<td style="background-color:#%s;">%3.0f</td>\n', hex, dz);
    end
    fprintf(fid, '</tr>\n');
end

fclose(fid);
