# climateviz.github.io
GT CSE 6242 - DVA - Project Team 214 - Final Project Site

### DESCRIPTION - 
This project vizualizes the similarities/differences between states of the USA from the perspective of merged datasets of the following indicators of climate change: Precipitation, Temperature, Pollution Index, Storm Deaths, Storm Injuries, Pneumonia/Flu Deaths, Lung Cancer Deaths. The user selects at least two indicators of interest, then in the back end, the states are grouped into 4 clusters using the k-means algorithm. Each State is colored according to its parent cluster. The states within a cluster can be perceived as being similarly affected by climate change.
One may investigate the detailed differences among states with repect to indicators by clicking on a few states from the map. To the right, one may see a list of these selections. Click the update button to see a radar chart with this comparison. This tool works best for comparing only a few states. Try picking those that are similar (belonging to the same cluster). Then try picking those that are different. Keep an eye out for any emerging patterns.

Datasets were downloaded from the following locations:
NOAA.gov:{Precipitation, Temperature, Storm Deaths, Storm Injuries}
data.gov:{Pneumonia/Flu Deaths}
CDC.gov:{Pollution Index, Lung Cancer Deaths}
### INSTALLATION  & EXECUTION - 
    Use our website at https://climateviz.github.io/ or to execute the code, simply open index.html. 
    This will call our AWS infrastrcture that runs PCA and K-Means using Python in AWS Lambda.
    
