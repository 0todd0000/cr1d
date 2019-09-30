function [XY,theta,IJKL,lambdas]=cellipse_0d_onesample(x,y,alpha) %calculates ellipse
%Input: x and y are 1 column each; p probability to scale ellipse, e.g. 0.95
%Output: XY: ellipse data; theta: axes angles; IJKL/lambdas: eigen vectors/values
%modified from: https://github.com/0todd0000/cr1d
ABCD    = cov(x,y); %2x2 covariance matrix of x and y
[IJKL,lambdas]=eig(ABCD); %scaled eigen vectors and values
p          = 2;
n          = length(x); %number of time-points used to create circle intervals
df         = [p, n-p];
F_crit     = spm1d.rft1d.f.isf0d(alpha, df);
T2_crit    = 2/(n-2) * F_crit / (n/(n-1));
scale      = sqrt(lambdas * T2_crit);
c          = linspace(0,(2*pi)/n*(n-1),n)'; %circle intervals; bias if use (0,2*pi,n)
XYcentered = [cos(c),sin(c)]* scale *IJKL; %ellipse around [0,0]
XY=(XYcentered+repmat([mean(x),mean(y)],n,1)); %ellipse around [meanx, meany]
theta=atan2(IJKL(2,:),IJKL(1,:)); % ellipse axes angles
end