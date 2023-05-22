
# short example 2
var x1;
var x2;
var w11 = 1;
var w12 = 3;
var w21 = 1;
var w22 = 2;
var w3 = -1;
var w4 = 1;



minimize obj: ((x1 * 1) + (x2 * 1))*-1 + ((x1 * 1) + (x2 * 2))*1;
s.t. c1: x1 >= 1;
s.t. c2: x1 <= 5;
s.t. c3: x2 >=4;
s.t. c4: x2 <= 6;
s.t. c5: ((x1 * 1) + (x2 * 1))*(-1) + ((x1 * 1) + (x2 * 2))*1 <= 20;
solve;
display x1,x2;