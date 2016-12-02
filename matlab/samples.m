function out = samples(type)

switch type
    case {'lab_hist9'}
        l = 100*linspace(1/18, 1-1/18, 9)';
        l = repmat(l, [1 9 9]);
        a = 160*linspace(1/18, 1-1/18, 9)-80;
        a = repmat(a, [9 1 9]);
        b = reshape(160*linspace(1/18, 1-1/18, 9)-80, [1 1 9]);
        b = repmat(b, [9 9 1]);
        
        out = Lab2RGB(l(:), a(:), b(:));

    case {'lab_hist15'}
        l = 100*linspace(1/30, 1-1/30, 15)';
        l = repmat(l, [1 15 15]);
        a = 160*linspace(1/30, 1-1/30, 15)-80;
        a = repmat(a, [15 1 15]);
        b = reshape(160*linspace(1/30, 1-1/30, 15)-80, [1 1 15]);
        b = repmat(b, [15 15 1]);
        
        out = Lab2RGB(l(:), a(:), b(:));

    case {'ab_hist9'}
        l = 70*ones(9);
        a = 160*linspace(1/18, 1-1/18, 9)'-80;
        a = repmat(a, [1 9]);
        b = 160*linspace(1/18, 1-1/18, 9)-80;
        b = repmat(b, [9 1]);
        
        out = Lab2RGB(l(:), a(:), b(:));
    
    case {'ab_hist15'}
        l = 70*ones(15);
        a = 160*linspace(1/30, 1-1/30, 15)'-80;
        a = repmat(a, [1 15]);
        b = 160*linspace(1/30, 1-1/30, 15)-80;
        b = repmat(b, [15 1]);
        
        out = Lab2RGB(l(:), a(:), b(:));
        
    case {'ab_hist21'}
        l = 70*ones(21);
        a = 160*linspace(1/42, 1-1/42, 21)'-80;
        a = repmat(a, [1 21]);
        b = 160*linspace(1/42, 1-1/42, 21)-80;
        b = repmat(b, [21 1]);
        
        out = Lab2RGB(l(:), a(:), b(:));
    
    case {'ab_hist31'}
        l = 70*ones(31);
        a = 160*linspace(1/62, 1-1/62, 31)'-80;
        a = repmat(a, [1 31]);
        b = 160*linspace(1/62, 1-1/62, 31)-80;
        b = repmat(b, [31 1]);
        
        out = Lab2RGB(l(:), a(:), b(:));
	
    case {'lch_hist9'}
        l = 100*linspace(1/18, 1-1/18, 9)';
        l = repmat(l, [1 9 9]);
        c = 80*linspace(1/18, 1-1/18, 9);
        c = repmat(c, [9 1 9]);
        h = reshape(2*pi*linspace(1/18, 1-1/18, 9), [1 1 9]);
        h = repmat(h, [9 9 1]);
        
        a = c.*cos(h);
        b = c.*sin(h);
        
        out = Lab2RGB(l(:), a(:), b(:));
        
    case {'ch_hist9'}
        l = 70*ones(9);
        c = 80*linspace(1/18, 1-1/18, 9)';
        c = repmat(c, [1 9]);
        h = 2*pi*linspace(1/18, 1-1/18, 9);
        h = repmat(h, [9 1]);
        
        a = c.*cos(h);
        b = c.*sin(h);
        
        out = Lab2RGB(l, a, b);
    
    case {'ch_hist21'}
        l = 70*ones(21);
        c = 80*linspace(1/42, 1-1/42, 21)';
        c = repmat(c, [1 21]);
        h = 2*pi*linspace(1/42, 1-1/42, 21);
        h = repmat(h, [21 1]);
        
        a = c.*cos(h);
        b = c.*sin(h);
        
        out = Lab2RGB(l, a, b);
        
    case {'ch_hist31'}
        l = 70*ones(31);
        c = 80*linspace(1/62, 1-1/62, 31)';
        c = repmat(c, [1 31]);
        h = 2*pi*linspace(1/62, 1-1/62, 31);
        h = repmat(h, [31 1]);
        
        a = c.*cos(h);
        b = c.*sin(h);
        
        out = Lab2RGB(l, a, b);
end
