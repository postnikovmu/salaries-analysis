# salaries-analysis
A Python script analyzing the average salaries

The project is designed to analyze the average salaries of programmers in Moscow by popular programming languages. 

## Description

This Python script uses public data from the HeadHunter and SuperJob job search platforms. It makes queries to the APIs of these sites to collect data on job openings for the specified programming languages. 

The script analyzes the offered salaries and calculates the average salary for each programming language. The results are then displayed as a table in the console.

## How to Install

To use this script, you need to have Python installed on your computer. You can download the latest version of Python from [official website](https://www.python.org/downloads/).

To install the required dependencies, run the following command:

`pip install -r requirements.txt`

## Setup

1. Create an account on [SuperJob](https://api.superjob.ru/) register your application and SeceretKey will be generated for you, which will be in ["Your Application"](https://api.superjob.ru/info/) section of your account.

2. Create a .env file in the same directory as the script and add the following line:

`SUPER_JOB_KEY=<your_secret_key>`.

## Usage

To use the script, open a terminal or command line and go to the directory where the script is located.

Run the script by running the following command:

`python main.py`.

The console will show you the results of job analysis on [HeadHunter](https://hh.ru/) and [SuperJob](https://superjob.ru/) sites in form of two tables with information about average earnings of programmers in Moscow by popular programming languages.

## Dependencies

This script requires the following Python packages:

- requests==2.32.2
- python-dotenv==1.0.0
- terminaltables==3.1.10
