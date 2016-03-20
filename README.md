# bracket-picker
A project to calculate win probabilities between any two Division 1 NCAA basketball teams to help you fill out your bracket.

#Method
Currently uses Kenpom's Pythagorean win percentage, ESPN's PVA rating derived from BPI, Jeff Sagarin's Predictor ratings, and both AP and Coaches Preseason polls.
Using those sources,  each rating is normalized to have the same mean and standard deviation as Sagarin's Predictor ratings.
The average rating for each team can be used to calculate an expected point spread for each game. Historical point spread data is used to convert the spreads to probabilities.

#Implementation
Currently uses a python script to web scrape the data and store it as a csv file.
All manipulation is currently done in Excel.
Basic user interface is also provided in Excel.

#Future Plans
-Add more sources such as Georgia Tech's LRMC rankings and the NCAA committee's seed rankings.

-Adjust probabilities for travel distance and player injuries.

-Manipulate data directly in Python or R.

-Provide a better interface.