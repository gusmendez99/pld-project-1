# Lexical Analyzer

Project 1 - Programming Languages Design course

## :ledger: Index

- [Lexical Analyzer](#lexical-analyzer)
  - [:ledger: Index](#ledger-index)
  - [:beginner: About](#beginner-about)
    - [:rocket: Features](#rocket-features)
  - [:zap: Usage](#zap-usage)
    - [:electric_plug: Installation](#electric_plug-installation)
    - [:package: Run](#package-run)
  - [:camera: Gallery](#camera-gallery)
  - [:star2: Author](#star2-author)
  - [:lock: License](#lock-license)

##  :beginner: About
The project consists of the implementation of the basic algorithms of FA and Regexs. Generally speaking, the program will accept as input a regex **r** and a string **w**. From the regular expression **r** an NFA will be built, which will then be transformed into an DFA. On the other hand, also using the same regular expression **r**, an FDA will be generated directly. With these automata it will be determined whether or not the string **w** belongs to **L(r)**.

### :rocket: Features
- [X] Thompson Construction Algorithm Implementation
- [X] Implementation of Subset Construction algorithm
- [X] Implementation of the DFA Construction algorithm given a regular expression r.
- [X] Simulation of an NFA
- [X] Simulation of an DFA


## :zap: Usage


###  :electric_plug: Installation
- Install `requirements.txt` on your venv
- You must install Graphviz for NFA & DFA digrapgh visualization

###  :package: Run
`python main.py`

##  :camera: Gallery
![terminal](https://github.com/gusmendez99/pld-project-1/blob/main/images/terminal.png?raw=true)

NFA & DFA

![nfa](https://github.com/gusmendez99/pld-project-1/blob/main/images/nfa.png?raw=true)

![dfa](https://github.com/gusmendez99/pld-project-1/blob/main/images/dfa.png?raw=true)

## :star2: Author
Gustavo Méndez

##  :lock: License
MIT