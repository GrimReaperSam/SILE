function delta_example

keyboard
init;

snowdark = mean(imread('./snow_799999999.jpg'), 3);

histogram = myhist(snowdark, 0, 255, 16);

load('/Volumes/alindner/mirflickr/DB/distances/rs/dark/gy_hist.mat');
qdark = q';
zdark = zvalues';

load('/Volumes/alindner/mirflickr/DB/distances/rs/snow/gy_hist.mat');
qsnow = q';
zsnow = zvalues';


figure(12)
hold off

h1 = subplot(3,1,1);
hold off

% dnq = quantile(dn, [opts.q .5 1-opts.q], 2);

errorbar([1:16]-.1, qdark(:,2), qdark(:,1), qdark(:,3), 'k--', 'LineWidth', 2);
hold on
errorbar([1:16]+.1, qsnow(:,2), qsnow(:,1), qsnow(:,3), 'b-', 'LineWidth', 2);

plot(histogram, 'r-.', 'LineWidth', 2);

% keyboard
Z = zvalues'
% keyboard
neg = zsnow < 0;
delta_snow(neg) = max(0, histogram(neg) - qsnow(neg,1));
delta_snow(~neg) = max(0, qsnow(~neg, 3) - histogram(~neg));

neg = zdark < 0;
delta_dark(neg) = max(0, histogram(neg) - qdark(neg, 1));
delta_dark(~neg) = max(0, qdark(~neg, 3) - histogram(~neg));


% keyboard
% plot(a(2), [0 17], [0 0], 'LineStyle', '--', 'Color', [0 .5 0]);


rgb = gy_histvalues();
for i = 1:16
	plot(i, -.03, '.','MarkerFaceColor', rgb(i,:), 'MarkerEdgeColor', rgb(i,:), 'MarkerSize', 30);
	hold on;
end
plot([.5 16.5], [0 0], 'k');


set(gca, 'Xlim', [.5 16.5]);
set(gca,'Ylim', [-.06 .4]);

set(gca,'Xtick', 1:16)
set(gca,'Ytick', [0 .3 .6])


set(gca, 'FontSize', 16);

h = legend('concept dark', 'concept snow', 'input image', 'Location', 'North');
set(h, 'FontSize', 16);


xlabel('Characteristic', 'FontSize', 16);

set(get(gca,'Ylabel'),'String','percent','FontSize', 16);

ax = get(h1, 'Position');
set(h1, 'Position', ax+[0 0 0 .08]);

subplot(3,1,2);
hold off
plot(delta_snow, 'b-', 'LineWidth', 2);
hold on
plot(delta_dark, 'k--.', 'LineWidth', 2);

% rgb = l_histvalues();
% for i = 1:16
% 	plot(i, -.018, '.','MarkerFaceColor', rgb(i,:), 'MarkerEdgeColor', rgb(i,:), 'MarkerSize', 40);
% 	hold on;
% end
% plot([.5 16.5], [0 0], 'k');


% h = legend('snow image', 'dark image', 'Location', 'North');

set(h, 'FontSize', 16);
set(get(gca,'Ylabel'),'String','Delta','FontSize', 16);
set(gca,'Xtick', 1:16)
set(gca, 'Xlim', [.5 16.5]);
set(gca,'Ytick', [0 .2 .4 .6])
set(gca, 'Ylim', [0 .4]);
set(gca, 'FontSize', 16);
xlabel('Characteristic', 'FontSize', 16);
% keyboard


subplot(3,1,3);
hold off
plot([.5 16.5], [0 0], 'k');
hold on
plot(delta_snow.*zsnow, 'b-', 'LineWidth', 2);
plot(delta_dark.*zdark, 'k--.', 'LineWidth', 2);


set(h, 'FontSize', 16);
set(get(gca,'Ylabel'),'String','ZDelta','FontSize', 16);
set(gca,'Xtick', 1:16)
set(gca, 'Xlim', [.5 16.5]);
set(gca,'Ytick', [-10 10 30 50]);
set(gca, 'Ylim', [- 15 30]);
set(gca, 'FontSize', 16);
xlabel('Characteristic', 'FontSize', 16);


% print('delta_example.eps', '-depsc2');

keyboard

figure(13)
hold off

SS = [.1 .5 1 2];
cmap = cool;
style = {'-', '--', ':', '-.'};
smax = 5;
% keyboard
for i = 1:length(SS)
    S = SS(i);
    ZD = S*zsnow.*delta_snow;
    pos = ZD > 0;
    deriv = 0;
    deriv(pos) = 1./(1 + abs(ZD(pos)));
    deriv(~pos) = 1 + abs(ZD(~pos));
    centers = linspace(255/32, 255*31/32, 16);
    deriv = interp1(centers, deriv, 0:255, 'linear', 'extrap');
    deriv = max(deriv, 1/smax);
    deriv = min(deriv, smax);
    
    map = cumsum(deriv);
    map = map - min(map);
    map = map/max(map)*255;

    plot(map, 'LineWidth', 2, 'Color', cmap(round(i*64/length(SS)), :), 'Linestyle', style{1+mod(i-1, 4)});
    hold on
end

axis equal
xlim([0 255]);
ylim([0 255]);
set(gca, 'FontSize', 16);
plot(0:255, 0:255, 'k');
legend({'0.5' '1' '2' '4' 'identity'}, 'FontSize', 16, 'Location', 'SouthEast');
xlabel('input value', 'FontSize', 16);
ylabel('output value', 'FontSize', 16);


% print('mapping_example.eps', '-depsc2');


function rgb = gy_histvalues()
rgb = linspace(1/32, 1-1/32, 16);
rgb = [rgb' rgb' rgb'];



function h = myhist(in, min, max, n)
% histogram weith n equidistant bins in the interval [min max]
% values outside the interval are added to the closest bin at the border
h = histc(in(:), [-inf linspace(min, max, n+1) inf]);
h = [h(1)+h(2); h(3:end-3); h(end-2)+h(end-1)+h(end)];
h = h / sum(h);