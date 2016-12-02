function varargout = mydescribe(id, varargin)
% keyboard
init;
argn = 1;

ALL = 0;
FORCE = opts.FORCE || opts.FORCE_DESCRIBE;
%FORCE = 1;

LD = size(varargin,2);
if (LD == 0)
    ALL = 1;
end

wishlist = '';
for i = 1:LD
    wishlist = [wishlist '<' varargin{i} '>'];
end

prefix = getprefix(id);
dpath = sprintf(opts.descPath, prefix, num2str(id));
fprintf('%s ... ', dpath);

% create mat file if not existant
if ~exist(dpath, 'file')
    image_id = id;
    try
        save(dpath, 'image_id');
    catch % create directory if not existant
        directory = regexp(dpath, '.*\/\d\d\/', 'match');
        directory = directory{1};
        mkdir(directory);
        save(dpath, 'image_id');
    end
end

warning('off', 'MATLAB:load:variableNotFound');

%% descriptor computations
name = 'lab_hist15';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('lab', 'var')
            lab = myget(id, 'cielab');
        end
        [H, W, D] = size(lab);
        lab_ = reshape(lab, H*W, D);
        lab_hist15 = histnd(double(lab_), [[0 15 100]; [-80 15 80]; [-80 15 80]]);
        lab_hist15 = lab_hist15 / sum(lab_hist15(:));
        
        save(dpath, name, '-append');
    end
    varargout{argn} = lab_hist15;
    argn = argn + 1;
end

name = 'lab_hist21';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('lab', 'var')
            lab = myget(id, 'cielab');
        end
        [H, W, D] = size(lab);
        lab_ = reshape(lab, H*W, D);
        lab_hist21 = histnd(double(lab_), [[0 21 100]; [-80 21 80]; [-80 21 80]]);
        lab_hist21 = lab_hist21 / sum(lab_hist21(:));
        
        save(dpath, name, '-append');
    end
    varargout{argn} = lab_hist21;
    argn = argn + 1;
end

name = 'lch_hist15';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('lab', 'var')
            lab = myget(id, 'cielab');
        end
        [H, W, D] = size(lab);
        
        lab_l = lab(:,:,1);
        lab_c = sqrt(lab(:,:,2).^2 + lab(:,:,3).^2);
        lab_h = 180/pi*atan2(lab(:,:,3), lab(:,:,2));
        neg = lab_h < 0;
        lab_h(neg) = lab_h(neg) + 360;
        
        lch_ = [lab_l(:), lab_c(:), lab_h(:)];
        
        lch_hist15 = histnd(double(lch_), [[0 15 100]; [0 15 80]; [0 15 360]]);
        lch_hist15 = lch_hist15 / sum(lch_hist15(:));
        
        save(dpath, name, '-append');
    end
    varargout{argn} = lch_hist15;
    argn = argn + 1;
end

name = 'lch_hist21';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('lab', 'var')
            lab = myget(id, 'cielab');
        end
        [H, W, D] = size(lab);
        
        lab_l = lab(:,:,1);
        lab_c = sqrt(lab(:,:,2).^2 + lab(:,:,3).^2);
        lab_h = 180/pi*atan2(lab(:,:,3), lab(:,:,2));
        neg = lab_h < 0;
        lab_h(neg) = lab_h(neg) + 360;
        
        lch_ = [lab_l(:), lab_c(:), lab_h(:)];
        
        lch_hist21 = histnd(double(lch_), [[0 21 100]; [0 21 80]; [0 21 360]]);
        lch_hist21 = lch_hist21 / sum(lch_hist21(:));
        
        save(dpath, name, '-append');
    end
    varargout{argn} = lch_hist21;
    argn = argn + 1;
end

name = 'lab_hist9';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('lab', 'var')
            lab = myget(id, 'cielab');
        end
        [H, W, D] = size(lab);
        lab_ = reshape(lab, H*W, D);
        lab_hist9 = histnd(double(lab_), [[0 9 100]; [-80 9 80]; [-80 9 80]]);
        lab_hist9 = lab_hist9 / sum(lab_hist9(:));
        
        save(dpath, name, '-append');
    end
    varargout{argn} = lab_hist9;
    argn = argn + 1;
end

name = 'ab_hist9';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('lab', 'var')
            lab = myget(id, 'cielab');
        end
%         keyboard
        [H, W, D] = size(lab);
        ab_ = reshape(lab(:,:,2:3), H*W, D-1);
        ab_hist9 = histnd(double(ab_), [[-80 9 80]; [-80 9 80]]);
        ab_hist9 = ab_hist9 / sum(ab_hist9(:));
        
        save(dpath, name, '-append');
    end
    varargout{argn} = ab_hist9;
    argn = argn + 1;
end

name = 'ab_hist21';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('lab', 'var')
            lab = myget(id, 'cielab');
        end
%         keyboard
        [H, W, D] = size(lab);
        ab_ = reshape(lab(:,:,2:3), H*W, D-1);
        ab_hist21 = histnd(double(ab_), [[-80 21 80]; [-80 21 80]]);
        ab_hist21 = ab_hist21 / sum(ab_hist21(:));
        
        save(dpath, name, '-append');
    end
    varargout{argn} = ab_hist21;
    argn = argn + 1;
end

name = 'ab_hist31';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('lab', 'var')
            lab = myget(id, 'cielab');
        end
%         keyboard
        [H, W, D] = size(lab);
        ab_ = reshape(lab(:,:,2:3), H*W, D-1);
        ab_hist31 = histnd(double(ab_), [[-80 31 80]; [-80 31 80]]);
        ab_hist31 = ab_hist31 / sum(ab_hist31(:));
        
        save(dpath, name, '-append');
    end
    varargout{argn} = ab_hist31;
    argn = argn + 1;
end

name = 'lch_hist9';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('lab', 'var')
            lab = myget(id, 'cielab');
        end
        [H, W, D] = size(lab);
        
        lab_l = lab(:,:,1);
        lab_c = sqrt(lab(:,:,2).^2 + lab(:,:,3).^2);
        lab_h = 180/pi*atan2(lab(:,:,3), lab(:,:,2));
        neg = lab_h < 0;
        lab_h(neg) = lab_h(neg) + 360;
        
        lch_ = [lab_l(:), lab_c(:), lab_h(:)];
        
        lch_hist9 = histnd(double(lch_), [[0 9 100]; [0 9 80]; [0 9 360]]);
        lch_hist9 = lch_hist9 / sum(lch_hist9(:));
        
        save(dpath, name, '-append');
    end
    varargout{argn} = lch_hist9;
    argn = argn + 1;
end

name = 'ch_hist9';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('lab', 'var')
            lab = myget(id, 'cielab');
        end
        [H, W, D] = size(lab);
        
        lab_c = sqrt(lab(:,:,2).^2 + lab(:,:,3).^2);
        lab_h = 180/pi*atan2(lab(:,:,3), lab(:,:,2));
        neg = lab_h < 0;
        lab_h(neg) = lab_h(neg) + 360;
        
        ch_ = [lab_c(:), lab_h(:)];
        
        ch_hist9 = histnd(double(ch_), [[0 9 80]; [0 9 360]]);
        ch_hist9 = ch_hist9 / sum(ch_hist9(:));
        
        save(dpath, name, '-append');
    end
    varargout{argn} = ch_hist9;
    argn = argn + 1;
end

name = 'ch_hist21';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('lab', 'var')
            lab = myget(id, 'cielab');
        end
        [H, W, D] = size(lab);
        
        lab_c = sqrt(lab(:,:,2).^2 + lab(:,:,3).^2);
        lab_h = 180/pi*atan2(lab(:,:,3), lab(:,:,2));
        neg = lab_h < 0;
        lab_h(neg) = lab_h(neg) + 360;
        
        ch_ = [lab_c(:), lab_h(:)];
        
        ch_hist21 = histnd(double(ch_), [[0 21 80]; [0 21 360]]);
        ch_hist21 = ch_hist21 / sum(ch_hist21(:));
        
        save(dpath, name, '-append');
    end
    varargout{argn} = ch_hist21;
    argn = argn + 1;
end

name = 'ch_hist31';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('lab', 'var')
            lab = myget(id, 'cielab');
        end
        [H, W, D] = size(lab);
        
        lab_c = sqrt(lab(:,:,2).^2 + lab(:,:,3).^2);
        lab_h = 180/pi*atan2(lab(:,:,3), lab(:,:,2));
        neg = lab_h < 0;
        lab_h(neg) = lab_h(neg) + 360;
        
        ch_ = [lab_c(:), lab_h(:)];
        
        ch_hist31 = histnd(double(ch_), [[0 31 80]; [0 31 360]]);
        ch_hist31 = ch_hist31 / sum(ch_hist31(:));
        
        save(dpath, name, '-append');
    end
    varargout{argn} = ch_hist31;
    argn = argn + 1;
end


name = 'l_hist';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('lab', 'var')
            lab = myget(id, 'cielab');
        end
        
        l_hist = myhist(lab(:,:,1), 0, 100, 16);
        
        save(dpath, name, '-append');
    end
    varargout{argn} = l_hist;
    argn = argn + 1;
end

name = 'c_hist';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('lab', 'var')
            lab = myget(id, 'cielab');
        end
            
        lab_c = sqrt(lab(:,:,2).^2 + lab(:,:,3).^2);
        c_hist = myhist(lab_c, 0, 50, 16);
        
        save(dpath, name, '-append');
    end
    varargout{argn} = c_hist;
    argn = argn + 1;
end

name = 'h_hist';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
%         keyboard
        if ~exist('lab', 'var')
            lab = myget(id, 'cielab');
        end
            
        lab_h = 180/pi*atan2(lab(:,:,3), lab(:,:,2));
        neg = lab_h < 0;
        lab_h(neg) = lab_h(neg) + 360;
        
        if ~exist('lab_c', 'var')
            lab_c = sqrt(lab(:,:,2).^2 + lab(:,:,3).^2);
        end
        
        mask = lab_c > 1;
        if sum(sum(mask)) > 16
            h_hist = myhist(lab_h(mask), 0, 360, 16);
        else
            h_hist = zeros(16,1);
        end
        
        save(dpath, name, '-append');
    end
    varargout{argn} = h_hist;
    argn = argn + 1;
end

name = 'rgb_hist';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('srgb', 'var')
            srgb = myget(id, 'srgb');
        end
        [H, W, D] = size(srgb);
        if (D == 1)
            srgb = cat(3, srgb, srgb, srgb);
            D = 3;
            fprintf('WARNING %d: converted to 3-channel color image (mydescribe/%s)\n', id, name);
        end
        rgb = reshape(srgb, H*W, D);
        rgb_hist = histnd(double(rgb), [[0 8 255]; [0 8 255]; [0 8 255]]);
        rgb_hist = rgb_hist / sum(rgb_hist(:));

        save(dpath, name, '-append');
    end
    varargout{argn} = rgb_hist;
    argn = argn + 1;
end

% keyboard
name = 'gy_hist';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('grey', 'var')
        	if ~exist('srgb', 'var')
            	srgb = myget(id, 'srgb');
            end
            grey = mean(srgb, 3);
        end
        
        gy_hist = myhist(grey, 0, 255, 16);
        
        save(dpath, name, '-append');
    end
    varargout{argn} = gy_hist;
    argn = argn + 1;
end

name = 'gy_hist2';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('grey', 'var')
        	if ~exist('srgb', 'var')
            	srgb = myget(id, 'srgb');
            end
            grey = mean(srgb, 3);
        end
        
        gy_hist2 = myhist(grey, 0, 255, 2);
        
        save(dpath, name, '-append');
    end
    varargout{argn} = gy_hist2;
    argn = argn + 1;
end

name = 'gy_hist4';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('grey', 'var')
        	if ~exist('srgb', 'var')
            	srgb = myget(id, 'srgb');
            end
            grey = mean(srgb, 3);
        end
        
        gy_hist4 = myhist(grey, 0, 255, 4);
        
        save(dpath, name, '-append');
    end
    varargout{argn} = gy_hist4;
    argn = argn + 1;
end

name = 'gy_hist8';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('grey', 'var')
        	if ~exist('srgb', 'var')
            	srgb = myget(id, 'srgb');
            end
            grey = mean(srgb, 3);
        end
        
        gy_hist8 = myhist(grey, 0, 255, 8);
        
        save(dpath, name, '-append');
    end
    varargout{argn} = gy_hist8;
    argn = argn + 1;
end

name = 'gy_hist16';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('grey', 'var')
        	if ~exist('srgb', 'var')
            	srgb = myget(id, 'srgb');
            end
            grey = mean(srgb, 3);
        end
        
        gy_hist16 = myhist(grey, 0, 255, 16);
        
        save(dpath, name, '-append');
    end
    varargout{argn} = gy_hist16;
    argn = argn + 1;
end

name = 'gy_hist32';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('grey', 'var')
        	if ~exist('srgb', 'var')
            	srgb = myget(id, 'srgb');
            end
            grey = mean(srgb, 3);
        end
        
        gy_hist32 = myhist(grey, 0, 255, 32);
        
        save(dpath, name, '-append');
    end
    varargout{argn} = gy_hist32;
    argn = argn + 1;
end

name = 'gy_hist64';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('grey', 'var')
        	if ~exist('srgb', 'var')
            	srgb = myget(id, 'srgb');
            end
            grey = mean(srgb, 3);
        end
        
        gy_hist64 = myhist(grey, 0, 255, 64);
        
        save(dpath, name, '-append');
    end
    varargout{argn} = gy_hist64;
    argn = argn + 1;
end

name = 'gy_hist128';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('grey', 'var')
        	if ~exist('srgb', 'var')
            	srgb = myget(id, 'srgb');
            end
            grey = mean(srgb, 3);
        end
        
        gy_hist128 = myhist(grey, 0, 255, 128);
        
        save(dpath, name, '-append');
    end
    varargout{argn} = gy_hist128;
    argn = argn + 1;
end

name = 'gy_hist256';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('grey', 'var')
        	if ~exist('srgb', 'var')
            	srgb = myget(id, 'srgb');
            end
            grey = mean(srgb, 3);
        end
        
        gy_hist256 = myhist(grey, 0, 255, 256);
        
        save(dpath, name, '-append');
    end
    varargout{argn} = gy_hist256;
    argn = argn + 1;
end


name = 'l_layout';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('lab', 'var')
            lab = myget(id, 'cielab');
        end
        l_layout = sample8x8(lab(:,:,1));
        l_layout = l_layout - min(l_layout(:));
        l_layout = l_layout / max(l_layout(:));

        save(dpath, name, '-append');
    end
    varargout{argn} = l_layout;
    argn = argn + 1;
end

name = 'c_layout';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('lab', 'var')
            lab = myget(id, 'cielab');
        end
        if ~exist('lab_c', 'var')
            lab_c = sqrt(lab(:,:,2).^2 + lab(:,:,3).^2);
        end
        
        c_layout = sample8x8(lab_c);
        c_layout = c_layout - min(c_layout(:));
        c_layout = c_layout / max(c_layout(:));

        save(dpath, name, '-append');
    end
    varargout{argn} = c_layout;
    argn = argn + 1;
end
% keyboard
name = 'h_layout';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('lab', 'var')
            lab = myget(id, 'cielab');
        end
        if ~exist('lab_h', 'var')
            lab_h = 180/pi*atan2(lab(:,:,3), lab(:,:,2));
            neg = lab_h < 0;
            lab_h(neg) = lab_h(neg) + 360;
        end
        if ~exist('lab_c', 'var')
            lab_c = sqrt(lab(:,:,2).^2 + lab(:,:,3).^2);
        end
        mask = lab_c > 1;
        
        h_layout = h_sample8x8(lab_h, mask);

        save(dpath, name, '-append');
    end
    varargout{argn} = h_layout;
    argn = argn + 1;
end
% keyboard

name = 'sunhist';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('lab', 'var')
            lab = myget(id, 'cielab');
        end
        if ~exist('lab_c', 'var')
            lab_c = sqrt(lab(:,:,2).^2 + lab(:,:,3).^2);
        end
        if ~exist('lab_h', 'var')
            lab_h = 180/pi*atan2(lab(:,:,3), lab(:,:,2));
            neg = lab_h < 0;
            lab_h(neg) = lab_h(neg) + 360;
        end
        sunhist = mexsunhist(cat(3, lab(:,:,1), lab_c, lab_h));
        sunhist = sunhist / sum(sunhist(:));

        save(dpath, name, '-append');
    end
    varargout{argn} = sunhist;
    argn = argn + 1;
end

name = 'l_high_layout_01';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('lab', 'var')
            lab = myget(id, 'cielab');
        end
        lab_l = lab(:,:,1);
        [l_blur_01 ss] = compute_l_blur(lab_l, 0.1);
        
        l_high_01 = abs(lab_l(ss:end-ss, ss:end-ss) - l_blur_01(ss:end-ss, ss:end-ss));
        
        l_high_layout_01 = sample8x8(l_high_01);
        l_high_layout_01 = l_high_layout_01 - min(l_high_layout_01(:));
        l_high_layout_01 = l_high_layout_01 / max(l_high_layout_01(:));
        
        save(dpath, name, '-append');
    end
    varargout{argn} = l_high_layout_01;
    argn = argn + 1;
end
% DO NOT SEPARATE THE BLOCK OF CODE ABOVE AND BELOW THIS LINE. THEY MUST
% STAY TOGETHER TO ASSURE THAT THE VARIABLE ss DOES NOT CHANGE.
% keyboard
name = 'details_hist_01';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('lab', 'var')
            lab = myget(id, 'cielab');
        end
        lab_l = lab(:,:,1);
        if ~exist('l_high_01', 'var')
            [l_blur_01 ss] = compute_l_blur(lab_l, 0.1);
            l_high_01 = abs(lab_l(ss:end-ss, ss:end-ss) - l_blur_01(ss:end-ss, ss:end-ss));
        end
        lab_l_crop = lab_l(ss:end-ss, ss:end-ss);
        
        pos = lab_l_crop <= 100/3;
        if sum(pos(:)) > numel(lab_l_crop)/100
            details_hist_01(:,1) = myhist(l_high_01(pos), 0, 40, 16);
        else
            details_hist_01(:,1) = zeros(1,16);
        end
        pos = lab_l_crop > 100/3 & lab_l_crop <= 200/3;
        if sum(pos(:)) > numel(lab_l_crop)/100
            details_hist_01(:,2) = myhist(l_high_01(pos), 0, 40, 16);
        else
            details_hist_01(:,2) = zeros(1,16);
        end
        pos = lab_l_crop > 200/3;
        if sum(pos(:)) > numel(lab_l_crop)/100
            details_hist_01(:,3) = myhist(l_high_01(pos), 0, 40, 16);
        else
            details_hist_01(:,3) = zeros(1,16);
        end
        
        save(dpath, name, '-append');
    end
    varargout{argn} = details_hist_01;
    argn = argn + 1;
end
% DO NOT SEPARATE THE BLOCK OF CODE ABOVE AND BELOW THIS LINE. THEY MUST
% STAY TOGETHER TO ASSURE THAT THE VARIABLE ss DOES NOT CHANGE.
name = 'details_layout_01';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('lab', 'var')
            lab = myget(id, 'cielab');
        end
        lab_l = lab(:,:,1);
        if ~exist('l_high_01', 'var')
            [l_blur_01 ss] = compute_l_blur(lab_l, 0.1);
            l_high_01 = abs(lab_l(ss:end-ss, ss:end-ss) - l_blur_01(ss:end-ss, ss:end-ss));
        end
        lab_l_crop = lab_l(ss:end-ss, ss:end-ss);        
        
        details = zeros(size(l_high_01));
        pos = lab_l_crop <= 100/3;
        details(pos) = l_high_01(pos);
        details_layout_01(:,:,1) = sample8x8(details);
        details_layout_01(:,:,1) = details_layout_01(:,:,1) - min(min(details_layout_01(:,:,1)));
        details_layout_01(:,:,1) = details_layout_01(:,:,1) / max(max(details_layout_01(:,:,1)));
        
        details = zeros(size(l_high_01));
        pos = lab_l_crop > 100/3 & lab_l_crop <= 200/3;
        details(pos) = l_high_01(pos);
        details_layout_01(:,:,2) = sample8x8(details);
        details_layout_01(:,:,2) = details_layout_01(:,:,2) - min(min(details_layout_01(:,:,2)));
        details_layout_01(:,:,2) = details_layout_01(:,:,2) / max(max(details_layout_01(:,:,2)));
        
        details = zeros(size(l_high_01));
        pos = lab_l_crop > 200/3;
        details(pos) = l_high_01(pos);
        details_layout_01(:,:,3) = sample8x8(details);
        details_layout_01(:,:,3) = details_layout_01(:,:,3) - min(min(details_layout_01(:,:,3)));
        details_layout_01(:,:,3) = details_layout_01(:,:,3) / max(max(details_layout_01(:,:,3)));
        
        save(dpath, name, '-append');
    end
    varargout{argn} = details_layout_01;
    argn = argn + 1;
end
% DO NOT SEPARATE THE BLOCK OF CODE ABOVE AND BELOW THIS LINE. THEY MUST
% STAY TOGETHER TO ASSURE THAT THE VARIABLE ss DOES NOT CHANGE.
name = 'l_high_layout_05';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('lab', 'var')
            lab = myget(id, 'cielab');
        end
        lab_l = lab(:,:,1);
        [l_blur_05 ss] = compute_l_blur(lab_l, 0.5);
        
        l_high_05 = abs(lab_l(ss:end-ss, ss:end-ss) - l_blur_05(ss:end-ss, ss:end-ss));
        
        l_high_layout_05 = sample8x8(l_high_05);
        l_high_layout_05 = l_high_layout_05 - min(l_high_layout_05(:));
        l_high_layout_05 = l_high_layout_05 / max(l_high_layout_05(:));
        
        save(dpath, name, '-append');
    end
    varargout{argn} = l_high_layout_05;
    argn = argn + 1;
end
% keyboard


name = 'gabor_hist';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('gaborplanes', 'var')
            gaborplanes = myget(id, 'gaborplanes');
        end
        
        Nbins = 16;
        gabor_hist = zeros([Nbins size(gaborplanes)]);
        for s = 1:size(gaborplanes, 1) %size
            for t = 1:size(gaborplanes, 2) %theta
                gabor_hist(:, s, t) = myhist(abs(gaborplanes{s, t}), 0, 16, Nbins);
            end
        end
        
        save(dpath, name, '-append');
    end
    varargout{argn} = gabor_hist;
    argn = argn + 1;
end

name = 'gabor_layout';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('gaborplanes', 'var')
            gaborplanes = myget(id, 'gaborplanes');
        end
        
        gabor_layout = zeros([8, 8, size(gaborplanes)]);
        for s = 1:size(gaborplanes, 1) %size
            for t = 1:size(gaborplanes, 2) %theta
                layout = sample8x8(abs(gaborplanes{s, t}));
                layout = layout - min(layout(:));
                layout = layout / max(layout(:));
                gabor_layout(:, :, s, t) = layout;
            end
        end
%         keyboard 
        
        save(dpath, name, '-append');
    end
    varargout{argn} = gabor_layout;
    argn = argn + 1;
end

name = 'lbp_hist';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('lab', 'var')
            lab = myget(id, 'cielab');
        end
%         keyboard
        lbp_hist = double(mexlbp(lab(:,:,1)));
        lbp_hist = lbp_hist/sum(lbp_hist);
        
        save(dpath, name, '-append');
    end
    varargout{argn} = lbp_hist;
    argn = argn + 1;
end

name = 'khist';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('lab', 'var')
            lab = myget(id, 'cielab');
        end
        
        khist = mexkhist(lab);
        
        save(dpath, name, '-append');
    end
    varargout{argn} = khist;
    argn = argn + 1;
end

name = 'khist500';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('lab', 'var')
            lab = myget(id, 'cielab');
        end
        
        khist500 = mexkhist500(lab);
        
        save(dpath, name, '-append');
    end
    varargout{argn} = khist500;
    argn = argn + 1;
end

name = 'khist_layout';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('lab', 'var')
            lab = myget(id, 'cielab');
        end
        
        ii = round(linspace(1, size(lab,1)+1, 4));
        jj = round(linspace(1, size(lab,2)+1, 4));
        
        khist_layout = zeros(3, 3, 1000, 'single');
        
        for i = 1:3
            for j = 1:3
                khist_layout(i, j, :) = mexkhist(lab(ii(i):ii(i+1)-1, jj(j):jj(j+1)-1, :));
            end
        end
        
        save(dpath, name, '-append');
    end
    varargout{argn} = khist_layout;
    argn = argn + 1;
end

% keyboard
name = 'reinhard';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('srgb', 'var')
            srgb = myget(id, 'srgb');
        end
        [H, W, D] = size(srgb);
        if (D == 1)
            srgb = cat(3, srgb, srgb, srgb);
            D = 3;
            fprintf('WARNING %d: converted to 3-channel color image (mydescribe/%s)\n', id, name);
        end
        rgb = double(reshape(srgb, H*W, D))';
        
        RGB2LMS = [.3811 .5783 .0402; .1967 .7244 .0782; .0241 .1288 .8444];
        LMS2LAlphaBeta = [1/sqrt(3) 0 0;0 1/sqrt(6) 0; 0 0 1/sqrt(2)]*[1 1 1; 1 1 -2; 1 -1 0];
        
        LMS = log(RGB2LMS*rgb);
        LAlhaBeta = LMS2LAlphaBeta*LMS;
        
        reinhard = [mean(LAlhaBeta, 2); var(LAlhaBeta, [], 2)];
        
        save(dpath, name, '-append');
    end
    varargout{argn} = reinhard;
    argn = argn + 1;
end

name = 'kristyn';
if ~isempty(strfind(wishlist, ['<' name '>'])) || ALL
    wishlist = strrep(wishlist, ['<' name '>'], '');
    fprintf('%s ... ', name);
    load(dpath, name);
    if ~exist(name, 'var') || FORCE
        if ~exist('lab', 'var')
            lab = myget(id, 'cielab');
        end
        lab_l = lab(:,:,1);
        lab_c = sqrt(lab(:,:,2).^2 + lab(:,:,3).^2);
        lab_h = 180/pi*atan2(lab(:,:,3), lab(:,:,2));
        neg = lab_h < 0;
        lab_h(neg) = lab_h(neg) + 360;
        lch = cat(3, lab_l, lab_c, lab_h);
		
        kristyn = zeros(17, 1);
        
        % lightness statistics
        kristyn(1) = mean(lab_l(:));
        kristyn(2) = median(lab_l(:));
        kristyn(3) = std(lab_l(:));
        kristyn(4) = skewness(lab_l(:));

        % chroma statistics        
        kristyn(5) = mean(lab_c(:));
        kristyn(6) = std(lab_c(:));
        kristyn(7) = busyness(lab_c);
        
        % colorfulness
        Cab = mean2(lab_c);
		L = mean2(lab_l);
		ss = size(lab_l);
		C = 54.38 + 0.1.*Cab.*(1+ (Cab./L).^(4./3));
		C = C./ss(1).*ss(2);%normalizing with the size of the image

        kristyn(8) = C;
        
        % 3D sunhist statistics
        N = size(lab,1)*size(lab,2);
        
        kristyn(9) = sum(lab_c(:)<=20)/N;
        kristyn(10) = sum(lab_l(:)<=40 & lab_c(:)<=20)/N;
        kristyn(11) = sum(lab_l(:)>40 & lab_l(:)<=70 & lab_c(:)<=20)/N;
        kristyn(12) = sum(lab_l(:)>70 & lab_c(:)<=20)/N;
        kristyn(13) = sum(lab_c(:)>20 & lab_c(:)<=50)/N;
        kristyn(14) = sum(lab_c(:)>50)/N;
        
        
        % texture statistics
        kristyn(15) = busyness(lab_l);
        p = histc(lab_l(:), linspace(0, 100, 100))/N;
        p = p(~isnan(p));
        kristyn(16) = -sum(p.*log2(p));
%         keyboard
        rfilter = rangefilt(lab_l);
        R = mean(rfilter(:));
        kristyn(17) = R;
        
        save(dpath, name, '-append');
    end
    varargout{argn} = kristyn;
    argn = argn + 1;
end

if length(wishlist) >= 1
    error('unsupprted descriptor types: %s\n', wishlist);
end

fprintf('\n');
warning('on', 'MATLAB:load:variableNotFound');


%% helper functions
function h = myhist(in, min, max, n)
% histogram weith n equidistant bins in the interval [min max]
% values outside the interval are added to the closest bin at the border
h = histc(in(:), [-inf linspace(min, max, n+1) inf]);
h = [h(1)+h(2); h(3:end-3); h(end-2)+h(end-1)+h(end)];
h = h / sum(h);


function out = sample8x8(in)
% initialize
N = 8;
[H, W, D] = size(in);
out = zeros(N, N, D);

% get indexes for N^2 tiles
I = round(linspace(1, H+1, N+1));
J = round(linspace(1, W+1, N+1));

for i = 1:N
    for j = 1:N
        out(i, j, :) = mean(mean(in(I(i):I(i+1)-1, J(j):J(j+1)-1)));
    end
end


function out = h_sample8x8(in, mask)
% initialize
N = 8;
[H, W, D] = size(in);
out = zeros(N, N, D);

% get indexes for N^2 tiles
I = round(linspace(1, H+1, N+1));
J = round(linspace(1, W+1, N+1));

% convert to pi-angles and mark low chroma values (reject for averaged hue angle)
in = in/180*pi;
in(mask == 0) = -1;

for i = 1:N
    for j = 1:N
        patch = in(I(i):I(i+1)-1, J(j):J(j+1)-1);
        x = sum(cos(patch(patch>=0)));
        y = sum(sin(patch(patch>=0)));
        alpha = 180/pi*atan2(y, x);
        if alpha < 0
            alpha = alpha + 360;
        end
        out(i, j, :) = alpha;
    end
end


function [out ss] = compute_l_blur(in, ss)
[H, W] = size(in);
ss = ss/100*sqrt(H^2 + W^2); % range in percent of the image diagonal
ss = round(3*ss);
if ss == 0
	error('mydescribe / compute_l_blur: ss is equal to zero since image too small (h,w) = (%d,%d)\n', H, W)
end
f = fspecial('gaussian', round(6*ss), ss);
out = conv2(in, f, 'same');


% functions from kristyn
function value = busyness(im_lab)
BW = edge(im_lab(:,:,1),'sobel',0.04);
se = strel('diamond',5);
BWdill = imdilate(BW, se);
BWFill = imfill(BWdill,'holes');
BWerode = imerode(BWFill,se);
ss = size(im_lab);
value = (length(find(BWerode == 1))./(ss(1).*ss(2))) .*100;


