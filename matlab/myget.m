function data = myget(id, type, varargin)

init;
% keyboard
type = lower(type);
switch type
    case {'orig'}
        fname = sprintf(opts.origPath, num2str(id));
        fprintf('%s ... ', fname);
        if exist(fname, 'file')
            data = imread(fname);
            fprintf('loaded\n');
        else
            fprintf('\nfailed loading "%s" of id %0.0f (%s)\n', type, id, fname);
        end
        
    case {'srgb'}
        fname = sprintf(opts.photoPath, getprefix(id), num2str(id));
        fprintf('%s ... ', fname);
        if exist(fname, 'file')
            data = imread(fname);
            fprintf('loaded\n');
        else
            fprintf('\nfailed loading "%s" of id %0.0f (%s)\n', type, id, fname);
        end
        
    case {'hsv'}
        fprintf('computing %s for %d\n', type, id);
        data = compute_hsv(id);
        
        
    case {'bf5d_2_10'}
        try
            fname = sprintf(opts.charPath, type, num2str(id), 'jpg');
            fprintf('%s ... ', fname);
            if exist(fname, 'file') && ~opts.FORCE
                data = imread(fname);
                fprintf('loaded\n');
            else
                fprintf('computing %s\n', type);
                data = compute_bf5d(id, 2, 10);
                imwrite(data, fname, 'Quality', 75);
            end
        catch
            fprintf('error in myget %s for file %s\n', type, fname);
        end
        
	case {'cielab_ps'}
        fname = sprintf(opts.charPath, type, num2str(id), 'tif');
        fprintf('%s ... ', fname);
        if exist(fname, 'file')
            data = imread(fname);
            fprintf('loaded\n');
        else
            fprintf('\nfailed loading "%s" of id %0.0f (%s)\n', type, id, fname);
        end

	case {'cielabm'}
        fname = sprintf(opts.labPath, num2str(id), 'mat');
        fprintf('%s ... ', fname);
        if exist(fname, 'file')
            load(fname);
            fprintf('loaded\n');
        else
            fprintf('computing %s\n', type);
            data = compute_cielab(id);
            save(fname, 'data');
        end
        
	case {'cielab'}
        fname = sprintf(opts.charPath, type, getprefix(id), num2str(id), 'mat');
        fprintf('%s ... ', fname);
        if exist(fname, 'file')
            load(fname);
            fprintf('loaded\n');
        else
            fprintf('computing %s\n', type);
            rgb = myget(id, 'srgb');
            [H, W, D] = size(rgb);
            if D==1
                rgb = cat(3, rgb, rgb, rgb);
            end
            keyboard
            data = srgb2xyz(rgb);
            data = xyz2lab(data);
            
%             keyboard
%             save(fname, 'data');
        end
        
    case {'l_blur'}
%         keyboard
        ss = varargin{1};
        fname = sprintf(opts.charPath, [type '/' num2str(ss)], getprefix(id), num2str(id), 'jpg');
        fprintf('%s ... ', fname);
        if exist(fname, 'file') && ~opts.FORCE && ~opts.FORCE_BLUR
            data = imread(fname);
            fprintf('loaded\n');
        else
            fprintf('computing %s\n', type);
            data = compute_l_blur(id, ss);
            imwrite(data, fname, 'Quality', 90);
            data = imread(fname);
        end
%         keyboard
        data = double(data)/255;
        f = fspecial('gaussian', 5, 1);
        data = conv2(data, f, 'same');

    case {'l_high'}
        keyboard
%         fprintf('computing %s for %d\n', type, id);
        ss = varargin{1};
        l_blur = double(myget(id, 'l_blur', ss));
        
        l = myget(id, 'cielab');
        l = l(:,:,1);
        l = double(l)/100;
        
        [H, W] = size(l);        
        ss = ss/100*sqrt(H^2 + W^2); % range in percent of the image diagonal
        ss = round(3*ss);
        if ss == 0
            fprintf('myget / l_high: ss is equal to zero since image too small (h,w) = (%d,%d)\n', H, W)
            fprintf('SKIP image %0.0f\n', id);
            error();
            data = 0;
        else
            data = abs(l(ss:H-ss, ss:W-ss) - l_blur(ss:H-ss, ss:W-ss));
        end
        
    case {'gaborplanes'}
%         keyboard
        lab_l = myget(id, 'cielab');
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
            im = myget(id, 'srgb');
            data = uint8(mexmsss(im));
            
            imwrite(data, fname, 'Quality', 75);
        end
        
    otherwise
        error('myget: type "%s" is not supported\n', type);
end


%% helper functions
function [G out] = computegabor(I, n, f, theta)
[Gx Gy] = meshgrid(-n:n);
G = exp(-(Gx.^2 + Gy.^2)/.5/n^2) .* exp(1i*2*pi*f*(Gx*cos(-theta) + Gy*sin(-theta)));
G = real(G);
G = G / sum(abs(G(:)));

out = imfilter(I, G, 'same', 'replicate');

function out = compute_bf5d(id, ss, sv)
im = myget(id, 'srgb');
[H, W, D] = size(im);
if D == 1
    im = cat(3, im, im, im);
elseif D ~= 3
    fprintf('WARNING (compute_bf5d, myget): image %d has %d channels. using only the first\n', id, size(im, 3));
    im = im(:,:,1);
    im = cat(3, im, im, im);
end
ss = ss/100*sqrt(H^2 + W^2); % range in percent of the image diagonal
out = bilateralfilter(im, ss, sv);


function out = compute_l_blur(id, ss)
l = myget(id, 'cielab');
l = double(l(:,:,1))/100;
[H, W] = size(l);
ss = ss/100*sqrt(H^2 + W^2); % range in percent of the image diagonal
f = fspecial('gaussian', round(6*ss), ss);
out = conv2(l, f, 'same');


function hsv = compute_hsv(id)
rgb = myget(id, 'srgb');
rgb = double(rgb);
[H, W, D] = size(rgb);
if D ~= 3
	error('error in myget compute_hsv for file %d. not a 3 channel image.', id);
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

hsv = cat(3, h, s, v);


function out = compute_l_high(id, ss)
l = myget(id, 'cielab');
l = double(l(:,:,1))/255;
[H, W] = size(l);
ss = ss/100*sqrt(H^2 + W^2); % range in percent of the image diagonal
f = fspecial('gaussian', round(6*ss), ss);
out = l - conv2(l, f, 'same');


function out = compute_cielab(id)
im = myget(id, 'srgb');
im = im2double(im);
if size(im, 3) == 1
    im = cat(3, im, im, im);
elseif size(im, 3) ~= 3
    fprintf('WARNING: image %d has %d channels. repeating the first channel 3 times.\n', id, size(im, 3));
    im = im(:,:,1);
    im = cat(3, im, im, im);
end
srgb2lab = makecform('srgb2lab');
out = applycform(im, srgb2lab);
