# bikalories 🚴🏿‍♂️🔥
Cycling training data analysis project.

## Motivation and Goal
Biking has become my favorite hobby since the beggining of the COVID-19 pandemic in 2020 when this was one of the only outdoor activities allowed. Since then, I have been using the Mi's [Zepp Life App](https://play.google.com/store/apps/details?id=com.xiaomi.hm.health&hl=pt_BR&gl=US&pli=1) to keep track of my biking workouts, registering routes using my phone's GPS and the calories burnt in each one of them. The years and the pandemic urgency passed, but my love for biking has only grown - and so did the amount of training data I have been collecting.

I know that I have become a better cyclist since I started to practice the sport more often, but I had not yet put any effort to translate this improvement into numbers and data. All I knew was that I had a bunch of data sitting on the Zepp Life's cloud just waiting to be explorated. Hence, I decided to use some Python 🐍 to draw more informed conclusions about this sport that has become my biggest passion.

## Data Collection
The data used in the project has two main types: **training route data** and **training metadata**

* **Route Data:** The training route data was collected using the [Zepp Life App](https://play.google.com/store/apps/details?id=com.xiaomi.hm.health&hl=pt_BR&gl=US&pli=1) during the period of Sep/2020 until Jan/2023. The Zepp Life App allows users to download their training route data as [GPX files](https://pt.wikipedia.org/wiki/GPX), but one can only export data from one train at a time, which makes it infeasible to export data from hundreds of workouts manually. Therefore, the [Mi-Fit-and-Zepp-workout-exporter](https://github.com/rolandsz/Mi-Fit-and-Zepp-workout-exporter) repository was used. This exporter automates the exportation of one user's data from all their workouts using the application's API endpoint made for requests for single workouts' data exportation.

* **Traning Metadata**: the training metadata, on the other hand, was much easier to export because Zepp Life has a feature that exports one user's training metadata from all of their trainings recorded at once. This feature is implemented sending a compressed file to the user's registered email in the application.

## Workouts Evolution
The following metrics were used to evaluate each workout:
* Average Speed
* Off Slope Maximum Speed
* Distance Traveled at Off Slope Maximum Speed
* Off Slope Maximum Accelerations
* Total Time Under Off Slope Acceleration
