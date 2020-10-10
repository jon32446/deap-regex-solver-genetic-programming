# deap-tutorial-genetic-programming
Playing around with DEAP's genetic programming library.

## evolve-a-string
Simple adaptation of the DEAP GP tutorial to evolve the given hard-coded string out of a primitive
set composed of the lowercase ASCII characters.

## regex_solver
An attempt to evolve a regex that matches everything in one list while matching nothing in a second
list. Changing to possessive quantifiers avoided catastrophic backtracking and allows this to evolve
for more complex lists and multiple generations.

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
