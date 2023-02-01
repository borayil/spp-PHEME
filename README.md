# Longitudinal Analysis of Network Data   

Python code for the short programming project course at the University of Groningen by Bora Yilmaz, under the supervision of Mirela Riveni.

This code is used to read, prepare and perform longitudinal analysis, extract key insight values and create Ego graphs on the [PHEME Rumour Dataset](https://www.pheme.eu/2016/06/13/pheme-rumour-dataset-support-certainty-and-evidentiality/). You can find comments on all sections and functions.

In order to run the code and create all of the output (figures and terminal output), run the script by the following command  
`python3 main.py`  

The dataset will be downloaded and extracted, renamed into `PhemeDataset`, at the root level of this project. If there is an error in this, you should manually do this through the official link above.  

The output of each event (images and text files) has it's seperate folder and is saved in the respective `output/event` folder. The process of the script, along with key values are printed out in the terminal. 
