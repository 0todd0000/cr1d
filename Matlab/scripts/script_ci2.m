
clear;  clc
close all



% %(0) Ellipse for a single frame:
% rng(0)
% alpha = 0.05;
% J     = 20;
% x     = randn(J,1);
% y     = randn(J,1);
% 
% Q     = 101;
% efwhm = 20;
% 
% [XY0,theta,IJKL,lambdas] = confidence_ellipse_0d_onesample(x,y,alpha);
% [XY,theta,IJKL,lambdas]  = confidence_ellipse_1d_onesample(x,y,alpha,Q,efwhm);
% XY0 = [XY0; XY0(1,:)];
% XY  = [XY; XY(1,:)];
% 
% 
% plot(x, y, 'ko')
% hold on
% plot(XY0(:,1), XY0(:,2), 'b-')
% plot(XY(:,1), XY(:,2), 'r-')




%(0) Load data:
fname   = '/Users/todd/GitHub/cr1d/Data/walking_grf.mat';
load(fname, 'grfA', 'grfB')

Q          = size(grfA,2);
trials     = 1:50;
% i          = 1:5:Q;
i          = 1:Q;

xAin       = grfA(trials,i,1)';
xBin       = grfB(trials,i,1)';
yAin       = grfA(trials,i,2)';
yBin       = grfB(trials,i,2)';


[gamma,CIseries1,CIseries2]=ci2(xAin,yAin,xBin,yBin,0.95,0,'yes',1);