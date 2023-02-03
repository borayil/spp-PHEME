# Longitudinal Analysis and Visualization of Network Data (with PHEME Rumour Dataset) 

Python code for the short programming project (spp) course at the University of Groningen by Bora Yilmaz, under the supervision of Mirela Riveni. This code and it's output is used in the project's report for the analysis.

This code is used to read, prepare and perform longitudinal analysis, extract key insight values and create Ego graphs on the [PHEME Rumour Dataset](https://www.pheme.eu/2016/06/13/pheme-rumour-dataset-support-certainty-and-evidentiality/). You can find comments on all sections and functions.

To install required modules, you can run  
`pip3 install -r requirements`  

In order to run the code and create all of the output (figures and terminal output), run the script by the following command  
`python3 main.py`  

If not present, the dataset will be downloaded, extracted and renamed into `PhemeDataset`. If there is an error in this download, the program will notify you. Then you can manually do this through the official page, [PHEME Rumour Dataset](https://www.pheme.eu/2016/06/13/pheme-rumour-dataset-support-certainty-and-evidentiality/).

The process of the script, along with key values are printed out in the terminal. The output of each event (images and text files) has it's seperate folder and is saved in the respective `output/event` folder. Please check the [report PDF](REPORT.pdf) itself to see an example of each outputs explanation.
