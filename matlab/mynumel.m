function N = mynumel(desctypes)

N = 0;
for i=1:length(desctypes)
    switch desctypes{i}
        case 'l_hist'
            N = N+16;
        case 'c_hist';
            N = N+16;
        case 'h_hist';
            N = N+16;
        case 'rgb_hist';
            N = N+8^3;
        case 'l_layout'
            N = N+64;
        case 'c_layout';
            N = N+64;
        case 'h_layout';
            N = N+64;
        case 'sunhist';
            N = N+27;
        case 'l_high_layout_01'
            N = N+64;
        case 'details_hist_01'
            N = N+3*16;
        case 'details_layout_01'
            N = N+3*64;
        case 'l_high_layout_05'
            N = N+64;
        case 'gabor_hist'
            N = N+2*4*16;
        case 'gabor_layout'
            N = N+2*4*64;
    end
end

