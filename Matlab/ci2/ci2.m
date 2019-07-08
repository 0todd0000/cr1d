function [gamma,CIseries1,CIseries2]=myCI2(xAin,yAin,xBin,yBin,p,g,plotsyes,tshade)
% output: overlap of two bivariate times-series (0 no overlap; 1 overlap); option: plots
% input: xAin,yAin,xBin,yBin: two xy series 1 and 2; n>=3 trials in columns (same n within series, but n can be different between series 1 and 2)
% input: time-points in rows same length: n>=2; good if before have removed outliers & offset normalised
% input: p is probability for confidence-interval of ellipse (e.g. 0.95)
% input: g is timelag from 0 (exact match) to g forward & backwards (so if any of series A overlaps B-g to B+g then identified as overlap) 
% input: option: plotsyes as 'yes' for plots; tshade=1 to r (e.g. 10 shade every 10th quads on plots to show any time diff between series)
% See accompanying paper for explanations: Mullineaux DR. CI2 for creating and comparing confidence-intervals 
% for time-series bivariate plots Gait Posture. 2017;xx
% ------------------------------------------------------------------------
[r,~]=size(xAin);
m=r-1; %connecting current to next CI to create quadrilaterals reduces size by 1
%-------STAGE1&2 ELLIPSE AND ELLIPSE CONFIDENCE INTERVALS-----------------
% calculate 2D CI for each bivariate series A and B
[x1A,y1A,x2A,y2A]=ellipseCIts(xAin,yAin,p);
[x1B,y1B,x2B,y2B]=ellipseCIts(xBin,yBin,p);
CIseries1=[x1A,y1A,x2A,y2A];
CIseries2=[x1B,y1B,x2B,y2B];
% ------STAGE3 CONVEX HULL, AND PLOT OPTION-------------------------------
% create quadrilaterals for series 1 and 2 (and option to plot data)
switch plotsyes % creates figure where option selected
    case 'yes'; figure; hold on; 
end
% create matrices before loop (5 points as 4 corners +1 to close quadrilateral) 
Px1=NaN(5,m); Py1=NaN(5,m); Px2=NaN(5,m); Py2=NaN(5,m);
for T=1:m; % T is t, but use capital version for plots
[Px1(:,T),Py1(:,T)]=convexquad([x1A(T:T+1,1);x2A(T:T+1,1)],[y1A(T:T+1,1);y2A(T:T+1,1)]);
[Px2(:,T),Py2(:,T)]=convexquad([x1B(T:T+1,1);x2B(T:T+1,1)],[y1B(T:T+1,1);y2B(T:T+1,1)]);
    switch plotsyes
        case 'yes'
fill(Px1(:,T),Py1(:,T),'w','FaceAlpha',0.0,'EdgeColor','none')
fill(Px2(:,T),Py2(:,T),'w','FaceAlpha',0.0,'EdgeColor','none')
TT=mod(T,tshade); % shade/colour every tshade quad to see any time-lag between series
        if TT<=0
fill(Px1(:,T),Py1(:,T),'k','FaceAlpha',1,'EdgeColor','none')
fill(Px2(:,T),Py2(:,T),'k','FaceAlpha',.5,'EdgeColor','none')
        end
axis equal; % NOTE: if series different units, then normalise scales for this to look ok
plot([x1A,x2A],[y1A,y2A],'k');
plot([x1B,x2B],[y1B,y2B],'k','LineStyle','--');
    end
end
 
% ------STAGE4 OVERLAP OF QUADRILATERALS--------------------------------
% finds overlap of all quadrilaterals from series1 with all quadrilaterals from series2
beta1=zeros(m,1); %Series 1; default zeros is no overlap
beta2=zeros(m,1); %Series 2; default zeros is no overlap (beta1 and beta2 will be same if no timelag)
Q=NaN(2,16); R=NaN(2,16);S=NaN(2,16);T=NaN(2,16);%16 to compare 4 vectors of quad1 to 2
for t=1:m
% STAGE4a: create combinations of the 16 vectors; series1 vectors
Q(1,:)=[repmat(Px1(1,t),1,4),repmat(Px1(2,t),1,4),repmat(Px1(3,t),1,4),repmat(Px1(4,t),1,4)];
Q(2,:)=[repmat(Py1(1,t),1,4),repmat(Py1(2,t),1,4),repmat(Py1(3,t),1,4),repmat(Py1(4,t),1,4)];
R(1,:)=[repmat(Px1(2,t),1,4),repmat(Px1(3,t),1,4),repmat(Px1(4,t),1,4),repmat(Px1(1,t),1,4)];
R(2,:)=[repmat(Py1(2,t),1,4),repmat(Py1(3,t),1,4),repmat(Py1(4,t),1,4),repmat(Py1(1,t),1,4)];
    for hh=t-g:1:t+g
        h=hh; %these few lines to adjust indexes to stay within ranges 
        if hh<=0
        h=1;
            elseif hh>=m
                h=m;
        end
S(1,:)=repmat(Px2(1:4,h)',1,4); %series2 vectors
S(2,:)=repmat(Py2(1:4,h)',1,4);
T(1,:)=repmat([Px2(2:4,h)',Px2(1,h)],1,4);
T(2,:)=repmat([Py2(2:4,h)',Py2(1,h)],1,4);
% STAGE4b: test intersect of all 16 vectors
W=segmentcross(Q,R,S,T); 
% STAGE4bi: if no intersect, now check if quadrilateral 2 not inside quadrilateral 1
        if W<=0  %skips this section if already know there is an overlap
% find which quadrilaterals has lowest y value, and subtract min y from all y's
% order so only need check 2 is inside 1 (and no need to check reverse that 1 inside 2)
Z=[Px1(1:4,t)',Px2(1:4,h)';Py1(1:4,t)',Py2(1:4,h)'];
[~,mincol]=min(Z(2,:));
Z=Z-repmat(Z(:,mincol),1,8);                       
            if mincol>=5 %switch series 1 and 2 for that with minimum
            Z=[Z(:,5:8),Z(:,1:4)];
            end
% check all points quad2ofZ are not between 2nd and 4th angles (QtoR and QtoT) of quad1ofZ (i.e. outside sides of quad1ofZ)
            alpha=atan2(Z(2,:),Z(1,:)); % QQ,QR,QS,QT are angles of quad1ofZ
            alphatest=sum(sign(alpha(5:8)-repmat(alpha(2),1,4)))+sum(sign(repmat(alpha(4),1,4)-alpha(5:8))); %will give 8 if all points between angles QR and QT 
            if alphatest<=7 %as not all 8 + then one quad can't be inside the other 
            W=0;
            else
% STAGE4bii: if all 8 between, check if quad1Q to quad2Q crosses quad1RS or quad1ST
                Q2=[Z(:,1),Z(:,1)]; % [quad1ofZ Q, quad1ofZ Q]
                R2=[Z(:,5),Z(:,5)]; % [quad2 ofZ Q, quad2 ofZ Q]
                S2=[Z(:,2),Z(:,3)]; % [quad1ofZ R, quad1ofZ S]
                T2=[Z(:,3),Z(:,4)]; % [quad1ofZ S, quad1ofZ T]
                W=segmentcross(Q2,R2,S2,T2);
                if W>=1 %if crosses=1, then outside quadrilateral, i.e. no overlap
                W=0;
                else
                W=1; %i.e. no cross, so quad2ofZ within quad1ofZ, so quads overlap
                end
            end
        end
    beta1(t)=beta1(t)+W; % STAGE4c
    beta2(h)=beta2(h)+W;
    end
end
gamma=isfinite(1./(beta1+beta2)); % STAGE4d
%-------------------------------------------------------------------------
switch plotsyes
    case 'yes'% plots traces with shading/colour showing where no overlap
fill(Px1(:,gamma),Py1(:,gamma),'k','FaceAlpha',.2,'EdgeColor','none')
fill(Px2(:,gamma),Py2(:,gamma),'k','FaceAlpha',.2,'EdgeColor','none')
end
%-------------------------------------------------------------------------
end % end of main function
%=========================================================================

%%
%Modified by T.Pataky 2019.07.08
%-------STAGE1 ELLIPSE----------------------------------------------------
function [XY,theta,IJKL,lambdas]=ellipse(x,y,alpha,Q,efwhm) %calculates ellipse
%Input: x and y are 1 column each; p probability to scale ellipse, e.g. 0.95
%Output: XY: ellipse data; theta: axes angles; IJKL/lambdas: eigen vectors/values
%modified from: https://github.com/0todd0000/ci1d
ABCD    = cov(x,y); %2x2 covariance matrix of x and y
[IJKL,lambdas]=eig(ABCD); %scaled eigen vectors and values
p          = 2;
n          = length(x); %number of time-points used to create circle intervals
df         = [p, n-p];
F_crit     = spm1d.rft1d.f.isf(alpha, df, Q, efwhm);
T2_crit    = 2/(n-2) * F_crit / (n/(n-1));
scale      = sqrt(lambdas * T2_crit);
c          = linspace(0,(2*pi)/n*(n-1),n)'; %circle intervals; bias if use (0,2*pi,n)
XYcentered = [cos(c),sin(c)]* scale *IJKL; %ellipse around [0,0]
XY=(XYcentered+repmat([mean(x),mean(y)],n,1)); %ellipse around [meanx, meany]
theta=atan2(IJKL(2,:),IJKL(1,:)); % ellipse axes angles
end

%%
%Modified by T.Pataky 2019.07.08
%-------STAGE2 ELLIPSE CONFIDENCE INTERVALS-------------------------------
function [CI1x,CI1y,CI2x,CI2y]=ellipseCIts(x,y,p) %calculates ellipse CI
% input: x and y data in 1 column; p probability scaling for ellipse, e.g. 0.95
% output: two CI for bivariate time-series. CI relative to direction of time-series
[r,~]=size(x);
k=(-2*log(1-p))^.5; %chi scales ellipse (e.g. otherwise 95% would be 85.35%)
% find angle of general direction of time-series movement
Xmean=mean(x,2); Ymean=mean(y,2);
Xchange=diff(Xmean); Xchange=[Xchange;Xchange(1,end)]; %repeat final point
Ychange=diff(Ymean); Ychange=[Ychange;Ychange(1,end)];
phi=atan2(Ychange,Xchange);
% preset variables before loop
Q     = r;
resx  = x - mean(x,2);
resy  = y - mean(y,2);
res   = [resx resy]';
efwhm = spm1d.geom.fwhm(res);
CI1x=NaN(r,1); CI1y=NaN(r,1); CI2x=NaN(r,1); CI2y=NaN(r,1);
    for t=1:r 
[~,thetas,IJKL,lambdas]=ellipse(x(t,:),y(t,:),p, Q, efwhm);% retrieve ellipse analysis
omega2=thetas(2)-phi(t); %make ellipse angle relative to direction angle
omega1=omega2+pi(); %find second angle relative to direction
%calculate first and second CI (i.e. positions on ellipse relative to direction)
CI1=k*[cos(omega1),sin(omega1)]*sqrt(lambdas)*IJKL; %matrix order correct to work
CI1x(t)=CI1(1); CI1y(t)=CI1(2);
CI2=k*[cos(omega2),sin(omega2)]*sqrt(lambdas)*IJKL;
CI2x(t)=CI2(1); CI2y(t)=CI2(2);
    end
CI1x=CI1x+Xmean; CI1y=CI1y+Ymean; CI2x=CI2x+Xmean; CI2y=CI2y+Ymean;% add mean to CI
end

%%
%-------STAGE3 CONVEX HULL------------------------------------------------
function [Px,Py]=convexquad(Mx,My) %convex hull of 4 points (similar to Graham's scan)
% input: 4 x-points in 1 column; 4 y-points in 1 column;  
% output: x y in convex order (creates quadrilateral, triangle if 1 point inside hull)
[ymint]=find(My<=min(My)); % find min y
if length(ymint)>=2 % if >1 min(My), find min(My) with min(Mx)
[~,ymint2]=min(Mx(ymint));
ymint=ymint(ymint2);
end
Nx=Mx-repmat(Mx(ymint,1),4,1); %subtract x for min-y point from all x points 
Ny=My-repmat(My(ymint,1),4,1); %subtract min-y  from all y points 
O=atan2(Ny,Nx); %calculate angle (range will be 0 to 180)
[~,korder]=sort(O); %sort on angle (small to large; i.e. anti-clockwise)
    Px=Mx(korder); Px=[Px;Px(1)]; %add first point at end to close shape
    Py=My(korder); Py=[Py;Py(1)];
%check if convex (i.e. if third point within quadrilateral replace else keep)
Q=[Px(1,1);Py(1,1)]; R=[Px(3,1);Py(3,1)]; %convex, so QR is points 1 and 3
S=[Px(2,1);Py(2,1)]; T=[Px(4,1);Py(4,1)]; %convex, so ST is points 2 and 4
W=segmentcross(Q,R,S,T); %test if QR intercepts ST
    if W<=0; %convex will intercept (>=1), but if 0 no intercept so replace p3 with p4
    Px(3,1)=Px(4,1); Py(3,1)=Py(4,1);
    end
end

%%
%-------STAGE3d & 4b & 4bii SEGMENT INTERSECT-----------------------------
function W=segmentcross(Q,R,S,T) %calculates intersect of QR and ST using Cramer's rule
% input: four points (QRST, x row 1, y row 2); columns n pairs of coordinates
% output: 0 if no intersection between any n pairs; 1 if any pair of vectors intersect
QR=R-Q; ST=T-S; RT=T-R; % create vectors from points
U=(ST(1,:).*RT(2,:)-ST(2,:).*RT(1,:))./(QR(1,:).*ST(2,:)-QR(2,:).*ST(1,:)); 
V=(QR(1,:).*RT(2,:)-QR(2,:).*RT(1,:))./(QR(1,:).*ST(2,:)-QR(2,:).*ST(1,:)); 
U=(U<1) & (U>0); % reduces to 0 (not meet criteria) or 1 (meets criteria)
V=(V<1) & (V>0);
W=sum(sum(U+V,1)>=2); %reduces to 1 (both criteria=1) else 0, then sums for single value
end
%=========================================================================