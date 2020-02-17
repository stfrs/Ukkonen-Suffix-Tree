#!/usr/bin/env python3

##################################################################################################
# Programm-Name:  "ukkonen.py"
# Beschreibung:   Algorithmus zum Aufbau von Suffix-Tree nach Ukkonen (1995).
# Aufruf:         "python3 ukkonen.py STRING_CONSTRUCTION (STRING_CHECK)"
#                  Das dritte Argument STRING_CHECK ist optional.
#                  Wird es beim Aufruf nicht angegeben, wird die Baumstruktur ausgegeben.
#                  Wird es angegeben, teilt das Programm mit ob es ein Infix ist.
# Baumstruktur:   Die Baumstruktur wird folgendermaßen ausgegeben:
#                 - offene Kante mit Label: "-- label --".
#                 - Kante mit Nachfolgeknoten: "-- label --> Node".
#                 - Die ausgehenden Kanten eines Knoten stehen eingerückt in den darauffolgenden Zeilen.
#                 - Alle nicht-eingerückten Kanten sind Kanten von Root.
#
# Autor:          Steffen Freisinger
# Matrikelnr:     11656230
#
# Weitere Infos zum Programm:
# Der Code ist angelehnt an den Pseudocode von Ukkonen (1995).
# Erstellt im Rahmen des Seminars "Algorithmische und formale Aspekte II" von Prof. Dr. Schulz.
# Datum der letzen Änderung: 11.09.2018.
##################################################################################################

import sys

############### Klasse "Node" ###############
class Node:

    def __init__(self):             # Konstruktor für einen Knoten
        self.suffix_pointer = None  # Suffixpointer vom Knoten ausgehend
        self.transitions = {}       # Dictionary mit allen Kanten, die vom Knoten ausgehen (Label:Zielknoten)

    def add_transition(self, edge, aim=None):   # Hinzufügen einer Kante
        self.transitions[edge] = aim            # Ist die Kante offen, ist der Zielknoten = None

    def take_transition(self, word):            # Wird für die Prüfung eines möglichen Infixes benötigt
        for trans, aim in self.transitions.items():
            if len(word) >= len(trans):         # Wort endet nicht innerhalb des Labels
                if trans == word[:len(trans)]:
                    return True, aim, word[len(trans):]
            else:                               # Wort endet innerhalb des Labels
                if word == trans[:len(word)]:
                    return True, None, ''
        return False, None, ''

################ Funktionen ################
def lookup(s, word):            # Baum wird durchlaufen, um zu prüfen ob ein Wort enthalten ist
    found = True
    while word != '':
        if s == None:
            return False
        found, s, word = s.take_transition(word)
    return found

def split_edge(s, k, p):                 # Kante wird an Stelle p aufgeteilt durch Node r
    for trans, aim in s.transitions.items():
        if word[k-1:p] == trans:
            return aim
        if word[k-1:p] == trans[:p-k+1]:
            r = Node()
            del s.transitions[trans]
            s.add_transition(trans[:p-k+1], r)	    # Neue Kanten erstellen	
            r.add_transition(trans[p-k+1:], aim)
            return r

def canonize(s, k, p):      # Knoten s und Index k werden aktualisiert
    if k > p:               # expliziter Knoten
        return (s,k)
    if s == bottom:
        s = root
        k += 1
    found = True
    while found: 
        for trans, aim in s.transitions.items():
            if p-k >= len(trans)-1:                 # s und k werden weiter angepasst
                if trans == word[k-1:len(trans)+k-1]:
                    k = k + len(trans)
                    s = aim
            else:
                if trans[:p-k+1] == word[k-1:p]:
                    return s,k  
        found = False
    return s, k

def check_end_point(s, k, p, c):
    if k <= p:          # impliziter Knoten
        for trans in s.transitions:
            if word[k-1:p]+c == trans[:p-k+2]:
                return True
        return False
    else:               # expliziter Knoten
        for trans in s.transitions:
            if trans[0] == c:
                return True
        return False

def update(s,k,p):      # Routine zur Erweiterung des Baumes um neues Symbol
    c = word[p-1]
    oldr = None
    while check_end_point(s,k,p-1, c) == False:
        if k <= p-1:                # impliziter Knoten
            r = split_edge(s,k,p-1)
        else:                       # expliziter Knoten
            r = s
        r.add_transition(word[p-1:len(word)-1])
        if oldr != None:
            oldr.suffix_pointer = r
        oldr = r
        s, k = canonize(s.suffix_pointer, k, p-1)
    if oldr != None:
        oldr.suffix_pointer = s
    return canonize(s,k,p)

def print_tree(node, m):            # Ausgabe des Suffix-Baumes auf stdout
    for trans, aim in node.transitions.items():
        if aim == None:
            print(m*2*'\t', "--", trans, "--")
        if aim != None:
            print(m*2*'\t',"--", trans, "--> Node")
            m+=1
            print_tree(aim, m)
            m-=1
    print()

################## Main ##################

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Call: python3", sys.argv[0], "String_to_build_Tree", "(String_to_check)")
        sys.exit()
    if len(sys.argv) == 2:
        show_tree = True
    else:
        show_tree = False
        check_word = sys.argv[2]

word = sys.argv[1] + '$'

bottom = Node()         # Erstellung von bottom und root
root = Node()

for char in word:
    if char not in bottom.transitions:
        bottom.add_transition(char, root)   # Zuweisung von Transitions mit allen Buchstaben des Wortes

root.suffix_pointer = bottom        # Zuweisung des Suffix-Pointers

s = root
i = 0          # Initialisierung der Variablen für die Hauptroutine
k = 1

while word[i] != '$':     # Hauptroutine
    i += 1
    s,k = update(s,k,i)

##### Ausgabe #####

if show_tree == True:     # Ausgabe der Baumstruktur
    print_tree(root, 0)
else:                     # Prüfung eines möglichen Infixes
    if lookup(root, check_word):
        print("'", check_word, "'", "is Infix")
    else:
        print("'", check_word, "'", "is NO Infix")



