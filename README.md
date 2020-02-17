# Ukkonen-Suffix-Tree
### Python-script generating suffix trees in linear time, using the method of Esko Ukkonen (1992)

The program can by called in 2 different ways, both using python3:
1. With one string as argument: The suffix tree will be created and the tree structure will be printed to std::out.
2. With two strings as arguments: The tree will be created based on the first string. Then it will be tested, wheter the second string is a part of the first string. The result of the matching will be printed to std::out.

The python-script itself contains additional information (as comments) regarding the tree structure and the program.
 
For an explanation of the algorithm, read:
http://web.stanford.edu/~mjkay/gusfield.pdf

The Original Paper by Ukkonen:
E. Ukkonen: Constructing suffix trees on-line in linear time. Proc. Information Processing 92, Vol. 1, IFIP Transactions A-12, 484-492, Elsevier 1992
