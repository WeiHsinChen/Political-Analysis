# Political-Analysis 

## Introduction

Political-Analysis program is designed for analyzing the sentiment of tweets for 2016 presidential candidates, and categorizing each tweet based on location. We aggregated these sentiments in order to determine the social sentiment of each candidate across different states, and to determine whether a candidate was perceived in a positive or negative light for certain topics. A Naive Bayes classifier was implemented as our model for both sentiment and domain analysis.

Once our system is incepted, it will keep collecting and analyzing tweets until user terminate it. The system also automatically and regularly generates analysis figures mentioned in the report. Therefore, it is easy for users to manipulate our system. Users just need to compile “twitter_streaming.py” without any parameters and close it by typing “Ctrl + C”. 

We've placed our system's API documentation into its own folder, "API-Level Documentation", which can be viewed in any HTML browser.

## Required setup
* Python 2.7
* Numpy
* Natural Language Toolkit
* Sklearn
* Pandas
* Matlibplot
* Geocoder
* Openpyxl


## Instructions of APIs 
* After a user installs all required packages, he/she can incept the program by simply typing the following command in terminal.
	
* Commands in terminal
		
			'''
			cd "the position of twitter_streaming.py"
			python2.7 twitter_streaming.py
			'''

