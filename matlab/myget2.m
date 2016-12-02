function data = myget2(im, type, varargin)

init;

isID = 0;
if numel(im) == 1
    isID = 1;
end


% keyboard
type = lower(type);
switch type
    case {'orig'}
        if isID
            fprintf('myget2: Give back input image!!\n');
            data = im;
        else
            fname = sprintf(opts.origPath, num2str(id));
            fprintf('%s ... ', fname);
            if exist(fname, 'file')
                data = imread(fname);
                fprintf('loaded\n');
            else
                fprintf('\nfailed loading "%s" of id %0.0f (%s)\n', type, id, fname);
            end
        end
        
    case {'srgb'}
        if isID
            fprintf('myget2: Give back input image!!\n');
            data = im;
        else
            fname = sprintf(opts.photoPath, getprefix(id), num2str(id));
            fprintf('%s ... ', fname);
            if exist(fname, 'file')
                data = imread(fname);
                fprintf('loaded\n');
            else
                fprintf('\nfailed loading "%s" of id %0.0f (%s)\n', type, id, fname);
            end
        end
        
    case {'hsv'}
        if isID
            fprintf('hsv ...');
            rgb = myget2(im, 'srgb');
        else
            rgb = im;
        end
        rgb = double(rgb);
        [H, W, D] = size(rgb);
        if D ~= 3
            if isID
                error('error in myget2 compute_hsv for file %d. not a 3 channel image.', im);
            else
                error('error in myget2 compute_hsv for input image. not a 3 channel image.');
            end
        end
        [M i] = max(rgb, [], 3); % max of RGB and the channel in which it occurs
        m = min(rgb, [], 3);
        d = M - m;

        % value
        v = M;

        % saturation
        s(M==0) = 0;
        s(M~=0) = d(M~=0) / M(M~=0);

        % hue
        h(M==0) = -1;
        I = i==1 && M~=0;
        h(I) = (rgb(I + H*W) - rgb(I + 2*H*W)) / delta(I);
        I = i==2 && M~=0;
        h(I) = 2 + (rgb(I + 2*H*W) - rgb(I)) / delta(I);
        I = i==3 && M~=0;
        h(I) = 4 + (rgb(I) - rgb(I + H*W)) / delta(I);

        data = cat(3, h, s, v);
        
	case {'cielab'}
        fprintf('cielab ... ');
        if isID
            rgb = myget2(im, 'srgb');
        else
            rgb = im;
        end
        [H, W, D] = size(rgb);
        if D==1
            rgb = cat(3, rgb, rgb, rgb);
        end
        data = RGB2Lab(rgb);
        
    case {'gaborplanes'}
%         keyboard
        lab_l = myget2(im, 'cielab');
        lab_l = lab_l(:,:,1);
        thetas = pi*[0 1/4 1/2 3/4];
        sizexys = [10 20];
        data = cell(length(sizexys), length(thetas));
        for s = 1:length(sizexys)
            sizexy = sizexys(s);
            freq = 1/sizexy;
            for t = 1:length(thetas)
                theta = thetas(t);
                [G gout] = computegabor(lab_l, sizexy, freq, theta);
                data{s, t} = gout;
            end
        end
        
        case {'msss'}
%         keyboard
        fname = sprintf(opts.charPath, type, getprefix(id), num2str(id), 'jpg');
        fprintf('%s ... ', fname);
        if exist(fname, 'file') && ~opts.FORCE && ~opts.FORCE_MSSS
            data = imread(fname);
            fprintf('loaded\n');
        else
            fprintf('computing %s\n', type);
            im = myget2(id, 'srgb');
            data = uint8(mexmsss(im));
            
            imwrite(data, fname, 'Quality', 75);
        end
        
    otherwise
        error('myget2: type "%s" is not supported\n', type);
end


%% helper functions
function [G out] = computegabor(I, n, f, theta)
[Gx Gy] = meshgrid(-n:n);
G = exp(-(Gx.^2 + Gy.^2)/.5/n^2) .* exp(1i*2*pi*f*(Gx*cos(-theta) + Gy*sin(-theta)));
G = real(G);
G = G / sum(abs(G(:)));

out = imfilter(I, G, 'same', 'replicate');
