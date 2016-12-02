fig_ferrari_red
init;

kw = 'ferrari';
desc = 'lab_hist9';

[tfs, tfsn] = myquery(kw);
% tfs = tfs .* (pos_ < 5);
sum(tfs)
d_ = mycollect(desc);
d_ = squeeze(d_);
sum(tfsn)


matrix = myzvalues({kw}, desc);


figure(2)
hold off
keyboard

d = d_(:, tfs==1);
dq = quantile(d, [opts.q .5 1-opts.q], 2);
dn = d_(:, tfsn==1);
dnq = quantile(dn, [opts.q .5 1-opts.q], 2);

errorbar([1:16]-.1, dq(:,2), dq(:,1), dq(:,3), 'LineWidth', 2);
hold on
errorbar([1:16]+.1, dnq(:,2), dnq(:,1), dnq(:,3), 'red', 'LineWidth', 2, 'LineStyle', '-.');
plot([-1 -2], [-1 -2], 'LineWidth', 2, 'LineStyle', '--', 'Color', [0 .5 0]);

% keyboard
Ndims = min(size(d));
Z = zeros(1, Ndims);
for i=1:Ndims
    [~, ~, stat] = ranksum(d(i, :), dn(i, :));
	Z(i) = stat.zval;
end

Z
dZ = max(Z) - min(Z)
[a h1 h2] = plotyy(NaN, NaN, 1:16, Z);
% keyboard
% plot(a(2), [0 17], [0 0], 'LineStyle', '--', 'Color', [0 .5 0]);


rgb = gy_histvalues();
for i = 1:16
	plot(i, -.02, '.','MarkerFaceColor', rgb(i,:), 'MarkerEdgeColor', rgb(i,:), 'MarkerSize', 40);
	hold on;
end
plot([.5 16.5], [0 0], 'k');
% keyboard

set(h2, 'LineWidth', 2);
set(h2, 'LineStyle', '--');
set(h2, 'Color', [0 .5 0]);
set(a(1),'Xlim', [.5 16.5]);
set(a(2),'Xlim', [.5 16.5]);
set(a(1),'Ylim', [-.04 .68]);
set(a(2),'Ylim', [-140 135]);

set(a(1),'Xtick', 1:16)
set(a(2),'Xtick', 1:16)
set(a(1),'Ytick', [0 .2 .4 .6])
set(a(2),'Ytick', [-130 -100 -50 0 50 100 130])
% keyboard
box(a(1));


set(a(1), 'FontSize', 16);
set(a(2), 'FontSize', 16);

h = legend(kw, ['not ' kw], 'z', 'Location', 'NorthEast');
set(h, 'FontSize', 16);

% keyboard

% set(hh2, 'LineStyle', '--');
% set(hh2, 'Color', [0 .5 0]);
% set(aa(2),'Xlim', [.5 16.5]);
% set(aa(1),'Xtick', [])
% set(aa(2),'Xtick', [])
% % set(aa(1),'Ytick', [])
% set(aa(2),'Ytick', [])


% keyboard
% set(a(1), 'Ylabel', 'Percent');

xlabel('Characteristic', 'FontSize', 16);

set(get(a(1),'Ylabel'),'String','percent','FontSize', 16);
set(get(a(2),'Ylabel'),'String','z value','FontSize', 16);
plot(gca, [1 11.25], [.655 .655], 'Color', [0 .5 0], 'LineStyle', '-.');
arrow([11 -.015], [11 .655]);
arrow([11 .655], [11 -.015]);
text(11.5, .335, 'dz')


% keyboard

% print('characteristic_example.eps', '-depsc2');
% keyboard

%% single characteristic
edges = linspace(0, .28, 30);
nd = histc(d(1,:), edges);
nd = nd/sum(nd);
ndn = histc(dn(1,:), edges);
ndn = ndn/sum(ndn);
figure(3)
hold off
plot(edges, nd/sum(nd), 'LineWidth', 2)
hold on
plot(edges, ndn, 'r-.', 'LineWidth', 2)
h = legend(kw, ['not ' kw]);
set(h, 'FontSize', 20);
set(gca, 'FontSize', 20);
xlabel('percentage of pixels', 'FontSize', 20);
ylabel('percentage of images', 'FontSize', 20);
xlim([0 .25]);
print('characteristic_example_2.eps', '-depsc2');
[~, ~, stat] = ranksum(d(1,:), dn(1,:));
z_dark = stat.zval


nd = histc(d(11,:), edges);
nd = nd/sum(nd);
ndn = histc(dn(11,:), edges);
ndn = ndn/sum(ndn);
figure(4)
hold off
plot(edges, nd/sum(nd), 'LineWidth', 2)
hold on
plot(edges, ndn, 'r-.', 'LineWidth', 2)
h = legend(kw, ['not ' kw]);
set(h, 'FontSize', 20);
set(gca, 'FontSize', 20);
xlabel('percentage of pixels', 'FontSize', 20);
ylabel('percentage of images', 'FontSize', 20);
xlim([0 .25]);
inter = interp1(edges, nd, .05);
intern = interp1(edges, ndn, .05);
plot([.05 .05], [0 max(inter, intern)], 'k--');
plot([0 .05], [inter inter], 'k--');
plot([0 .05], [intern intern], 'k--');
plot(.05, inter, '.', 'MarkerSize', 20, 'MarkerFaceColor', 'blue', 'MarkerEdgeColor', 'blue');
plot(.05, intern, '.', 'MarkerSize', 20, 'MarkerFaceColor', 'red', 'MarkerEdgeColor', 'red');
inter
intern

print('characteristic_example_16.eps', '-depsc2');
[~, ~, stat] = ranksum(d(12,:), dn(12,:));
z_bright = stat.zval

% keyboard
%% example with deltaR = 0
kw = 'statue';

[tfs, tfsn] = myquery(kw);
% tfs = tfs .* (pos_ < 5);
sum(tfs)
d_ = mycollect('gy_hist');
d_ = reshape(d_, 16, 1e6);
sum(tfsn)

figure(5)
hold off
keyboard

d = d_(:, tfs==1);
dq = quantile(d, [opts.q .5 1-opts.q], 2);
dn = d_(:, tfsn==1);
dnq = quantile(dn, [opts.q .5 1-opts.q], 2);

errorbar([1:16]-.1, dq(:,2), dq(:,1), dq(:,3), 'LineWidth', 2);
hold on
errorbar([1:16]+.1, dnq(:,2), dnq(:,1), dnq(:,3), 'red', 'LineWidth', 2, 'LineStyle', '-.');
plot([-1 -2], [-1 -2], 'LineWidth', 2, 'LineStyle', '--', 'Color', [0 .5 0]);

% keyboard
Ndims = min(size(d));
Z = zeros(1, Ndims);
for i=1:Ndims
    [~, ~, stat] = ranksum(d(i, :), dn(i, :));
	Z(i) = stat.zval;
end

Z
dZ = max(Z) - min(Z)
[a h1 h2] = plotyy(NaN, NaN, 1:16, Z);
% keyboard
% plot(a(2), [0 17], [0 0], 'LineStyle', '--', 'Color', [0 .5 0]);


rgb = gy_histvalues();
for i = 1:16
	plot(i, -.007, '.','MarkerFaceColor', rgb(i,:), 'MarkerEdgeColor', rgb(i,:), 'MarkerSize', 40);
	hold on;
end
plot([.5 16.5], [0 0], 'k');


set(h2, 'LineWidth', 2);
set(h2, 'LineStyle', '--');
set(h2, 'Color', [0 .5 0]);
set(a(1),'Xlim', [.5 16.5]);
set(a(2),'Xlim', [.5 16.5]);
set(a(1),'Ylim', [-.014 .25]);
set(a(2),'Ylim', [-140 135]);

set(a(1),'Xtick', 1:16)
set(a(2),'Xtick', 1:16)
set(a(1),'Ytick', [0 .1 .2])
set(a(2),'Ytick', [-130 -100 -50 0 50 100 130])

box(a(1));


set(a(1), 'FontSize', 16);
set(a(2), 'FontSize', 16);

h = legend(kw, ['not ' kw], 'z', 'Location', 'NorthEast');
set(h, 'FontSize', 16);

% keyboard

% set(hh2, 'LineStyle', '--');
% set(hh2, 'Color', [0 .5 0]);
% set(aa(2),'Xlim', [.5 16.5]);
% set(aa(1),'Xtick', [])
% set(aa(2),'Xtick', [])
% % set(aa(1),'Ytick', [])
% set(aa(2),'Ytick', [])


% keyboard
% set(a(1), 'Ylabel', 'Percent');

xlabel('Characteristic', 'FontSize', 16);

set(get(a(1),'Ylabel'),'String','percent','FontSize', 16);
set(get(a(2),'Ylabel'),'String','z value','FontSize', 16);

% plot(gca, [1 14.25], [.118 .118], 'Color', [0 .5 0], 'LineStyle', '-.');
% arrow([14 .088], [14 .118]);
% arrow([14 .158], [14 .128]);
% text(14.5, .103, 'dz')


function rgb = gy_histvalues()
rgb = linspace(1/32, 1-1/32, 16);
rgb = [rgb' rgb' rgb'];