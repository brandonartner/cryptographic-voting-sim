# Cryptographic Voting System
A terminal application that use cryptographic principles to facilitate simulated secure voting in 
segmentated organizations. The system allows for designing simple to complex organizational structures 
and generating secure votes tied to each member. There is also functionality to simulate a voting 
session, where users can intiate a vote and vote on the active vote. When a vote is succesful the 
document gains a digital signature, which can be verified later. Disclaimer: In its current state
this is not a secure system.<br/>
<br/>

## Documentation

[For detailed documentation of the project.](https://htmlpreview.github.com/brandonartner/SecretSharingProject/blob/master/build/html/index.html)

## Required Libraries:
```
pip install fuzzyfinder
pip install pycrypto
```

## Usage:
### Constructing an organization:
```
python TreeMaker.py
```
or (for testing purposes)
```
python TreeMaker.py < config.txt
```
### Simulating a vote:
```
python VoteSim.py
```
or (for testing purposes)
```
python VoteSim.py < vote_sim1.txt
```

## To-Do:
- [X] Implement Legrangian Polynomial Interpolation
- [X] Update Polynomial Interpolation to Neville's Method, to allow for incremental construction of data
- [X] Implement Voter class
- [X] Create a REPL for creating tree structure<br/>
- [X] Create the Tree object made by the REPL<br/>
- [X] Figure out exactly how the world works (within the confines of our project)<br/>
  - [ ] Should we have one master document set at the root level? or<br/>
  - [X] Have each subgroup have its own subdocument set?<br/>
- [ ] Create visualization for audience
- [X] Implement key validation function
- [X] Implement add single node function
- [ ] ~~Turn the toolkit into a class~~
  - [ ] Rework toolkit to actually make sense (its basically a bunch of repeated functions).
- [X] Fix the key_to_data and data_to_key functions so upward propogations is possible
- [ ] Create GUI
- [X] Implement Voter class concept into ThresTree

## Critical To-Do
- [ ] Fix ascii art in the README
<br/>
A..................B<br/>
M--->M---~--->M---(H)<br/>
|....s........s....|<br/>
|....|........|....v<br/>
|....|........|....^<br/>
|....|........|....|<br/>
H---PrK......PuK----<br/>
<br/>
Active Branches:<br/>
<br/>
