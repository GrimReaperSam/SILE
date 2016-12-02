function [C] = Cui(LCh)

% cform = makecform('srgb2lab');
% lab = applycform(rgb,cform); 
% cform = makecform('lab2lch');
% LCH = applycform(lab,cform); 
Cab = mean2(LCh(:,:,2));
L = mean2(LCh(:,:,1));
ss = size(LCh);

C = 54.38 + 0.1.*Cab.*(1+ (Cab./L).^(4./3));
C = C./ss(1).*ss(2);%normalizing with the size of the image