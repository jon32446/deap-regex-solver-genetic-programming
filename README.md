# Generate regex to match lists using DEAP genetic programming library
Playing around with DEAP's genetic programming library.

## evolve-a-string
Simple adaptation of the DEAP GP tutorial to evolve the given hard-coded string out of a primitive
set composed of the lowercase ASCII characters.

## regex_solver
An attempt to evolve a regex that matches everything in one list while matching nothing in a second
list. Changing to possessive quantifiers avoided catastrophic backtracking and allows this to evolve
for more complex lists and multiple generations.

This is a bit different to normal regex golf since I want it to fully match (all characters) of the
items in the match list while matching zero characters in the avoid list.

```
python regex_solver.py 10000 10 --match arthur marthur --avoid jimmy billy
Running with population N=10000 and generations G=10
to evolve matches for: ['arthur', 'marthur']
and avoid these: ['jimmy', 'billy']

                                    fitness                    
                -----------------------------------------------
gen     nevals  avg     gen     max     min     nevals  std    
0       10000   83.071  0       101     26      10000   6.40665
1       5498    80.2341 1       93      26      5498    9.24212
2       5460    74.867  2       93      8       5460    11.8703
3       5444    67.7622 3       89      8       5444    12.745 
4       5597    61.3353 4       111     0       5597    12.6773
5       5498    56.5689 5       111     0       5498    12.2319
6       5545    54.349  6       101     0       5545    12.1049
7       5489    53.2788 7       94      0       5489    12.7   
8       5397    51.808  8       101     0       5397    13.9786
9       5529    49.4161 9       110     0       5529    16.2798
10      5455    46.1716 10      110     0       5455    19.391 
char_join(regex_star('\\w'), 'r')
(\w)*r
Completed the evolution run with population N=10000 and generations G=10
```

Or without arguments:
```
python regex_solver.py
Running with population N=10000 and generations G=10
to evolve matches for: amazing
and avoid these: terrible

                                    fitness                     
                ------------------------------------------------
gen     nevals  avg     gen     max     min     nevals  std     
0       10000   7.0702  0       11      4       10000   0.855612
1       5483    6.5833  1       11      4       5483    0.795023
2       5451    6.0908  2       9       3       5451    0.919758
3       5291    5.5509  3       11      2       5291    0.969025
4       5489    5.0971  4       11      2       5489    0.975537
5       5394    4.7345  5       11      2       5394    0.987831
6       5509    4.4378  6       10      2       5509    0.993545
7       5544    4.1772  7       10      1       5544    1.04489 
8       5457    3.8806  8       11      1       5457    1.10451 
9       5356    3.5486  9       10      1       5356    1.13156 
10      5635    3.2705  10      10      1       5635    1.20072 
regex_or(regex_plus('n'), regex_or(regex_or('z', 'a'), regex_or('g', 'm')))
((n)+)|(((z)|(a))|((g)|(m)))
Completed the evolution run with population N=10000 and generations G=10
```

Complex example:
```
python regex_solver.py 2000 300 --threads 16 --match mary patricia linda barbara elizabeth jennifer maria susan margaret dorothy lisa nancy karen betty helen sandra donna carol ruth sharon michelle laura sarah kimberly deborah jessica shirley cynthia angela --avoid james john robert michael william david richard charles joseph thomas christopher daniel paul mark donald george kenneth steven edward brian ronald anthony kevin jason matthew gary timothy jose larry
Running with population N=2000 and generations G=300
to evolve matches for: ['mary', 'patricia', 'linda', 'barbara', 'elizabeth', 'jennifer', 'maria', 'susan', 'margaret', 'dorothy', 'lisa', 'nancy', 'karen', 'betty', 'helen', 'sandra', 'donna', 'carol', 'ruth', 'sharon', 'michelle', 'laura', 'sarah', 'kimberly', 'deborah', 'jessica', 'shirley', 'cynthia', 'angela']
and avoid these: ['james', 'john', 'robert', 'michael', 'william', 'david', 'richard', 'charles', 'joseph', 'thomas', 'christopher', 'daniel', 'paul', 'mark', 'donald', 'george', 'kenneth', 'steven', 'edward', 'brian', 'ronald', 'anthony', 'kevin', 'jason', 'matthew', 'gary', 'timothy', 'jose', 'larry']

                                    fitness                    
                -----------------------------------------------
gen     nevals  avg     gen     max     min     nevals  std    
0       2000    1100.05 0       1134    654     2000    60.6105
1       1085    1065.95 1       1128    648     1085    92.1146
2       1145    1013.11 2       1134    648     1145    120.777
3       1106    944.02  3       1150    648     1106    132.877
4       1110    880.639 4       1150    648     1110    123.257
5       1133    846.681 5       1135    648     1133    122.547
6       1140    815.956 6       1139    592     1140    137.844
7       1098    766.861 7       1139    592     1098    145.347
8       1094    728.71  8       1135    576     1094    147.025
9       1062    708.583 9       1135    576     1062    141.98 
10      1129    704.845 10      1144    571     1129    146.476
20      1071    642.115 20      1150    560     1071    150.087
30      1112    609.757 30      1138    497     1112    136.998
40      1086    538.082 40      1160    430     1086    125.045
50      1110    472.471 50      1155    356     1110    131.241
60      1138    407.446 60      1128    323     1138    129.815
70      1119    380.557 70      1192    299     1119    139.355
80      1098    355.658 80      1128    281     1098    142.96 
90      1102    332.233 90      1126    272     1102    139.639
100     1145    326.124 100     1146    264     1145    142.617
120     1070    305.197 120     1128    244     1070    137.64 
140     1094    242.583 140     1128    170     1094    148.801
160     1109    202.402 160     1126    114     1109    154.408
180     1109    153.297 180     1117    89      1109    163.243
200     1144    143.851 200     1126    71      1144    164.024
220     1108    119.216 220     1126    62      1108    158.053
240     1077    105.962 240     1102    52      1077    155.098
260     1101    115.225 260     1126    50      1101    172.283
280     1090    125.172 280     1128    50      1090    192.398
300     1097    127.058 300     1144    50      1097    198.275
join(regex_or('t', regex_or('t', regex_or(join(regex_plus('s'), regex_or(join(join(regex_or('t', join(regex_or(regex_or(join(join(regex_or(join('\\w', 'e'), regex_optional('k')), '.'), '.'), join('\\w', '.')), '\\w'), '.')), '.'), '.'), regex_star(regex_or(join(regex_optional('a'), '.'), regex_optional('k'))))), join(join(join(join('.', 'g'), '.'), join(regex_or('t', join(regex_or(regex_or(join(join(regex_or(join('\\w', 'e'), '\\w'), '.'), '.'), 'r'), '\\w'), join('.', '\\w'))), '.')), regex_or('t', regex_or(join(regex_or(join(join(regex_or('c', regex_or('d', join('\\w', '\\w'))), regex_or(join(join(join(join('.', '.'), '.'), '.'), '\\w'), regex_plus('s'))), regex_or(join('\\w', '.'), join(regex_star('.'), '.'))), join(regex_star(join('\\w', regex_or('n', 'h'))), regex_or(join(regex_or('h', join('k', regex_or(join('.', '\\w'), join('\\w', '.')))), 'e'), regex_or(join(regex_or(regex_star('y'), join('.', 'a')), 'e'), '\\w')))), regex_or(regex_plus(join(regex_or(join(regex_or(regex_star('y'), join('k', 'a')), 'e'), '\\w'), 'o')), regex_star('.'))), join('\\w', 'w'))))))), regex_or(regex_or(regex_or(regex_or(regex_or(join(regex_or('g', join(regex_or(regex_or(join(regex_optional('o'), '.'), regex_or(join('h', 'e'), '\\w')), '\\w'), 't')), regex_or('h', 'x')), regex_plus(join(regex_or(join(join(regex_optional('a'), '.'), regex_plus(join(regex_or('y', regex_or(join('.', '\\w'), join('\\w', '.'))), join(regex_or('y', regex_or(join('.', '\\w'), join('\\w', '.'))), 'c')))), regex_plus(regex_or('\\w', join('\\w', '.')))), 'c'))), join(regex_optional('a'), '.')), join('\\w', '\\w')), '\\w'), join('\\w', '\\w')))
(t)|((t)|(((s)++((t)|((((\we)|((k)?+)..)|(\w.))|(\w).)..)|((((a)?+.)|((k)?+))*+))|(.g.(t)|((((\we)|(\w)..)|(r))|(\w).\w).(t)|((((c)|((d)|(\w\w))(....\w)|((s)++)(\w.)|((.)*+.))|((\w(n)|(h))*+((h)|(k(.\w)|(\w.))e)|((((y)*+)|(.a)e)|(\w)))(((((y)*+)|(ka)e)|(\w)o)++)|((.)*+))|(\ww)))))((((((g)|((((o)?+.)|((he)|(\w)))|(\w)t)(h)|(x))|((((a)?+.((y)|((.\w)|(\w.))(y)|((.\w)|(\w.))c)++)|(((\w)|(\w.))++)c)++))|((a)?+.))|(\w\w))|(\w))|(\w\w)
Completed the evolution run with population N=2000 and generations G=300
        match   | avoid
        -----   | -----
       mary ✅  | james ✅
   patricia ✅  | john ✅
      linda ✅  | robert ✅
    barbara ✅  | michael ✅
  elizabeth ✅  | william ✅
   jennifer ✅  | david ✅
      maria ✅  | richard ✅
      susan ✅  | charles ✅
   margaret ✅  | joseph ✅
    dorothy ✅  | thomas ✅
       lisa ✅  | christopher ✅
      nancy ✅  | daniel ✅
      karen ✅  | paul ✅
      betty ✅  | mark ✅
      helen ✅  | donald ✅
     sandra ✅  | george ✅
      donna ✅  | kenneth ✅
      carol ❌  | steven ❌
       ruth ✅  | edward ✅
     sharon ✅  | brian ✅
   michelle ✅  | ronald ✅
      laura ✅  | anthony ✅
      sarah ✅  | kevin ✅
   kimberly ✅  | jason ✅
    deborah ✅  | matthew ✅
    jessica ✅  | gary ❌
    shirley ✅  | timothy ❌
    cynthia ✅  | jose ✅
     angela ✅  | larry ✅
```
