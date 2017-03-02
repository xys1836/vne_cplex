\ENCODING=ISO-8859-1
\Problem name: Transportation Problem

Minimize
 Minimize_Cost#0: 35 x11 + 30 x12 + 40 x13 + 32 x14 + 37 x21 + 40 x22 + 42 x23
                  + 25 x24 + 40 x31 + 15 x32 + 20 x33 + 28 x34
Subject To
 c1: x11 + x12 + x13 + x14 <= 1200
 c2: x21 + x22 + x23 + x24 <= 1000
 c3: x31 + x32 + x33 + x34 <= 800
 c4: x11 + x21 + x31 >= 1100
 c5: x12 + x22 + x32 >= 400
 c6: x13 + x23 + x33 >= 750
 c7: x14 + x24 + x34 >= 750
End
