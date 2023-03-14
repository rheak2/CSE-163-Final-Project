Title:
Authors: Giulia Clini, Elizabeth Karas, and Rhea Kulkarni
CSE 163 Project

Step 1: Install Camelot library and ghostscript
    https://camelot-py.readthedocs.io/en/master/user/install.html using pip for camelot and ghostscript
    you do NOT need to install ghostscript for the files to run, but it helps avoid certain warnings. All of our files are processed using flavor='Stream'
    pandas version 1.3.5 helps to avoid warnings, however, warnings do not affect data quality


Step 2: Running python program
    The main.py file.
    You do NOT need to run the process_loc.py file, and the code in that file is not called in any
    other file. This is because Running process_loc.py takes >3 hours to run. The function adds a csv file
    to our folder, and this csv is processed in other files. Processing the csv takes less than 2 seconds.
    To demonstrate how we converted the pdf into a csv file, we included the code in process_loc.py. Running
    the process_big_data() function will sometimes result in warnings. These warnings are due to Camelot reading whitespace on the pdf pages and do not result in any data loss. These are the only warnings you should receive if everything is installed correctly.

    Running the main.py file will run the code to produce the results for each of the research questions. The files rq1.py, rq2.py, and rq3.py detail the code that will run when main.py runs. The folder also includes the testing files for each question.
