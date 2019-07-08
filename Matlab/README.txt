The accompanying MATLAB code was downloaded on 2019.07.08 from:
https://www.sciencedirect.com/science/article/pii/S0966636216307160
(see Appendix A. Supplementary data)

The supplementary data are in Word (DOCX) format. This code was converted to the MATLAB (.m) files indicated below.


1.  ci2.m
Description: All code.
Notes: Copy-and-pasted from the supplementary DOCX file. 

2. ellipse.m
Description: Only the "ellipse" function
Notes:
a) Copy-and-pasted from ci2.m to allow access to this function from external scripts.
b) Command added to compute lengths of semi axes::
    axes_lengths = sort( diag( k * sqrt(lambdas) ), 'descend');

