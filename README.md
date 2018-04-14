# SecretSharingProject
Project to implement a secret sharing application.<br/>
<br/>
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
- [ ] Implement key validation function
- [X] Implement add single node function
- ~~[ ] Turn the toolkit into a class~~
- [X] Fix the key_to_data and data_to_key functions so upward propogations is possible
- [ ] Create GUI
- [ ] Implement Voter class concept into ThresTree

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
- Django_App: Not actually making a Django app but this branch has all the new stuff.s<br/>
