FS = 20;
descs = {'c_hist' 'h_hist' 'lbp_hist'};
% descnames = {'graylevel hist' 'chroma hist' 'hue angle hist' 'CIE-ab hist' 'CIE-Lab hist' 'sunhist' 'CIE-LCH hist' 'lightness layout' 'chroma layout' 'hue angle layout' 'details hist' 'gabor filter hist' 'gabor filter layout' 'linear binary pattern hist'};
kws = {'red' 'green' 'blue' 'flower' };

% keyboard


rgb_hue = [0.7624    0.3070    0.4123;
    0.7405    0.3379    0.2920;
    0.6793    0.3876    0.1875;
    0.5875    0.4386    0.1081;
    0.4727    0.4815    0.0911;
    0.3354    0.5133    0.1593;
    0.1352    0.5341    0.2672;
         0    0.5452    0.3934;
         0    0.5477    0.5255;
         0    0.5415    0.6477;
         0    0.5253    0.7425;
         0    0.4970    0.7949;
    0.3483    0.4560    0.7964;
    0.5355    0.4044    0.7473;
    0.6626    0.3509    0.6564;
    0.7377    0.3120    0.5389];

rgb_chroma = [0.4663    0.4664    0.4663;
    0.5021    0.4544    0.4672;
    0.5362    0.4416    0.4681;
    0.5689    0.4278    0.4690;
    0.6004    0.4129    0.4700;
    0.6309    0.3967    0.4710;
    0.6606    0.3791    0.4720;
    0.6896    0.3598    0.4730;
    0.7180    0.3383    0.4741;
    0.7458    0.3143    0.4752;
    0.7733    0.2870    0.4764;
    0.8003    0.2552    0.4775;
    0.8270    0.2166    0.4788;
    0.8534    0.1666    0.4800;
    0.8795    0.0881    0.4813;
    0.9054         0    0.4826];


[matrix, deltarank_kw2, deltarank_desc2, qs2, nqs2] = myzvalues(kws, descs);

chroma = [];
hue = [];
lbp = [];

% keyboard
for i = 1:length(kws)
    chroma(i, :) = matrix{1, i}';
    hue(i, :) = matrix{2, i}';
    lbp(i, :) = matrix{3, i}';
end

figure(1)
subplot(3,1,1)
hold off
h = bar(chroma');
set(h(1),'facecolor','red');
set(h(2),'facecolor','green');
set(h(3),'facecolor','blue');
set(h(4),'facecolor','black');
set(gca, 'FontSize', FS);
xlim([0 17])
ylim([-120 180])
set(gca,'XTick', 1:16, 'FontSize', FS);
title('chroma')
ylabel('z')

hold on
for i = 1:16
	plot(i, -120, '.','MarkerFaceColor', rgb_chroma(i,:), 'MarkerEdgeColor', rgb_chroma(i,:), 'MarkerSize', 40);
	hold on;
end

hl = legend('red', 'green', 'blue', 'flower');
set(hl, 'FontSize', 16)

subplot(3,1,2)
hold off
h = bar(hue');
set(h(1),'facecolor','red');
set(h(2),'facecolor','green');
set(h(3),'facecolor','blue');
set(h(4),'facecolor','black');
set(gca, 'FontSize', FS);
xlim([0 17])
ylim([-100 180])
set(gca,'XTick', 1:16, 'FontSize', FS);
title('hue angle')
ylabel('z')

hold on
for i = 1:16
	plot(i, -100, '.','MarkerFaceColor', rgb_hue(i,:), 'MarkerEdgeColor', rgb_hue(i,:), 'MarkerSize', 40);
	hold on;
end


subplot(3,1,3)
hold off
h = bar(lbp');
set(h(1),'facecolor','red');
set(h(2),'facecolor','green');
set(h(3),'facecolor','blue');
set(h(4),'facecolor','black');
set(gca, 'FontSize', FS);
xlim([0 19])
ylim([-205 200])
set(gca,'XTick', 1:18, 'FontSize', FS);
title('linear binary pattern')
ylabel('z')

hold on
C = -180;
Lx = .2;
Ly = 25;
% keyboard

for i = 2:17
    alpha = (i - 1)/16*2*pi;
    for alpha_steps = linspace(0, alpha, 20*i)
        dx = Lx*cos(alpha_steps);
        dy = Ly*sin(alpha_steps);
        line([i i+dx], [C C+dy], 'Color', 'black', 'LineWidth', 1);
    end
end

for alpha_steps = [0 45 90 135 180 225 270 315]/360*2*pi
    dx = Lx*cos(alpha_steps);
    dy = Ly*sin(alpha_steps);
    line([18 18+dx], [C C+dy], 'Color', 'black', 'LineWidth', 1);
end

