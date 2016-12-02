FS = 5;
init;
% descs = {'gy_hist', 'l_hist', 'c_hist', 'h_hist', 'l_layout', 'c_layout', 'h_layout', 'details_hist_01', 'lbp_hist', 'gabor_hist'};
% descs = {'ab_hist21' 'c_hist' 'c_layout' 'details_hist_01' 'gabor_hist' 'gabor_layout' 'gy_hist' 'h_hist' 'h_layout' 'lab_hist9' 'lbp_hist' 'lch_hist9' 'l_hist' 'l_layout' 'sunhist'};
descs = {'gy_hist' 'c_hist' 'h_hist' 'ab_hist21' 'lab_hist9' 'sunhist' 'lch_hist9' 'l_layout' 'c_layout' 'h_layout' 'details_hist_01' 'gabor_hist' 'gabor_layout' 'lbp_hist'};
descnames = {'graylevel hist' 'chroma hist' 'hue angle hist' 'CIE-ab hist' 'CIE-Lab hist' 'sunhist' 'CIE-LCH hist' 'lightness layout' 'chroma layout' 'hue angle layout' 'high frequency hist' 'gabor filter hist' 'gabor filter layout' 'linear binary pattern hist'};
% descs = {'gy_hist'};
kws = {'nature' 'sky' 'blue' 'macro' 'bw' 'flowers' 'flower' 'water' 'red' 'portrait' 'green' 'art' 'hdr' 'light' 'night' 'sunset' 'white' 'film' 'clouds' 'winter' 'street' 'beach' 'people' 'landscape' 'architecture' 'city' 'yellow' 'blackandwhite' 'snow' 'tree' 'black' 'color' 'cat' 'sea' 'urban' 'bokeh' 'trees' 'bird' 'pink' 'spring' 'sun' 'selfportrait' 'animal' 'orange' 'graffiti' 'park' 'photo' 'building' 'statue' 'solitude'};
% kws = opts.kwgeq500;
% kws = cvpr.kws;
keyboard
[matrix, deltarank_kw2, deltarank_desc2, qs2, nqs2] = myzvalues(kws, descs);
Nk = length(kws);
Nd = length(descs);
dz = zeros(size(matrix));

minimum = 1e9;
maximum = 0;

% keyboard

for d = 1:Nd
    for k = 1:Nk
        z = matrix{d, k};        
        dz(d, k) = max(z(:)) - min(z(:));
        
        if dz(d, k) > maximum
            maximum = dz(d, k);
        end
        if dz(d, k) < minimum
            minimum = dz(d, k);
        end
    end
end

figure(21)
SSh = 100;
SSv = 70;
subplot(2,1,1)
hold off
imagesc(imresize(min(150, dz), [SSv SSh].*size(dz), 'nearest'));
axis equal
hold on

for d = 1:Nd
    for k = 1:Nk
        text((k-.5)*SSh, (d-.5)*SSv, num2str(round(dz(d, k))), 'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle', 'FontSize', FS);
    end
end

% xlabel('keyword', 'FontSize', FS);
set(gca,'YTick', linspace(.5*SSv, (Nd-.5)*SSv, Nd), 'FontSize', FS);
set(gca,'YTickLabel', descnames, 'FontSize', FS);
set(gca,'XTick', linspace(.5*SSh, (Nk-.5)*SSh, Nk), 'FontSize', FS);
set(gca,'XTickLabel', kws, 'FontSize', FS);
ylim([1 Nd*SSv]);
xlim([1 Nk*SSh]);
rotateticklabel(gca, 45, FS);
axis ij
colormap hsv_
hC = colorbar('FontSize', FS);
set(hC,'Ytick', [10 30 50 70 90 110 130 150],'YTicklabel', {'10' '30' '50' '70' '90' '110' '130' '150'});
set(gca, 'TickLength', [0 0]);
% title('title');

x1=get(gca,'position');
x=get(hC,'Position');
x(3)=0.01;
set(hC,'Position',x)
set(gca,'position',x1)
print('fig_other_examples.eps', '-depsc2');

%% creates a single plot with the descriptor on the vertical axis and the deltaZ value on the horizontal
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  highest two keywords per descriptor are represented with a crossmark and
%  the keyword is written as text next to it
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% FS = 20;
% XLIM = 120;
% 
% descs = {'gy_hist', 'l_hist', 'c_hist', 'h_hist', 'l_layout', 'c_layout', 'h_layout', 'l_high_layout_01', 'details_hist_01', 'details_layout_01', 'sunhist', 'lbp_hist', 'rgb_hist', 'gabor_hist', 'gabor_layout'};;
% kws = opts.kwgeq100;
% % [matrix, deltarank_kw, deltarank_desc, qs, nqs] = myzvalues(kws, descs);
% Nd = length(descs);
% keyboard
% 
% try
%     close(20)
% end
% figure(20)
% hold off
% for d = 1:2:Nd
%     rectangle('Position',[1,d-.5,XLIM-1,1], 'FaceColor', [.8 .8 .8], 'LineStyle', 'none');
%     hold on
% end
% 
% maximum = 0;
% 
% for d = 1:Nd
%     for k = [1 3]
%         reg = deltarank_desc{d, k};
%         pos = regexpi(reg, '__');
%         kw = reg(1:pos(1)-1);
%         deltaZ = str2double(reg(pos(2)+2:end));
%         if deltaZ > maximum
%             maximum = deltaZ
%         end
%         plot(deltaZ, d, '*', 'MarkerSize', 5);
%         if k==1
%             text(deltaZ, d, [' ' kw], 'Rotation', -45, 'HorizontalAlignment', 'left', 'FontSize', FS)
%         else
%             text(deltaZ, d, [' ' kw], 'Rotation', 45, 'HorizontalAlignment', 'left', 'FontSize', FS)
%         end
%         hold on;
%     end
% end
% 
% xlabel('deltaZ', 'FontSize', FS);
% set(gca,'YTick', 1:Nd, 'FontSize', FS);
% set(gca,'YTickLabel', descs, 'FontSize', FS);
% ylim([0 Nd+1]);
% xlim([0 XLIM]);