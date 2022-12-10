Names: Noa Don and Antonio Escallon

Noteworthy resources: We used the class slides as well as a couple of Youtube videos (https://www.youtube.com/watch?v=1IQOtJ4NI_0 and https://www.youtube.com/watch?v=FuTRucXB9rA&t=679s) to get more familiar with information gain. 
Additionally, we were struggling at a certain point to pass certain basic autograder tests, and after talking about our general approaches, we realized we should be getting the parent entropy at each level of the recursion tree, not of the global dataset. 
we also talked about how when we we found the left and right children datasets, we initially planned on calling the funciton recursively everytime we found a higher information gain, but Ido helped us realize that would cause many unnecessary recursive calls because we only want to run the algorithm once we've officially found the highest information gain

Other notes: we believe everything is working correctly