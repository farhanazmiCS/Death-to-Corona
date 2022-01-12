# Death to Corona

## App Demo
Click [here](https://death-to-corona.herokuapp.com/) to try the app yourself!

## Video Demo
Click [here](https://youtu.be/Qs_rJFs2Ewc) to view the youtube demo!

## About this app
A simple web application using tools such as HTML, CSS, JavaScript, SQL as well as Python that lets a user perform a risk-assessment for the coronavirus as well as lookup the nearest vaccination drives given an input location. The main application was written in Python using a micro-web framework called Flask, which contains the functions `home`, which are the lines of code to allow the homepage to function, `riskAssessment`, which performs all the actions for the risk-assessment function, and `getVaccinated`, which performs all the actions for the get vaccinated function.

## Function Definitions `app.py`
### Home

The home function used is to load up the `home.html` webpage, which gives the user access to the other web pages and other health advisories.
### RiskAssessment

The primary function of the `riskAssessment` function is to allow the user to roughly gauge on his/her likelihood of getting the coronavirus based on several factors, such as medical condition, gender and symptoms. The `riskAssessment` function has two methods of HTML requests, `GET` and `POST`. If the request method is `GET`, it loads up `diagnose.html`, which renders all of the questions for the risk assessment. If the request method is `POST`, a series of actions would happen upon form submission. It follows this sequence:
1. The application would classify the user options based on a points system.
2. The application will then decide which webpage to load. At the lower points bound, `lowrisk.html` will load, at the upper bound, `highrisk.html` will load, and `moderaterisk.html` will load at the middle bound.

**_Note: The risk assessment is only meant to be a guide, and is NOT medically endorsed by a professional. Each option carries different points. Based on research, certain symptoms carry a greater likelihood of being infected for the coronavirus. The points, which are assigned to each option, are stored in a SQLite database along with the options, and a search query will be called when needed. The points are then added up to load up the respective "risk" pages._**

### getVaccinated
* The purpose of the `getVaccinated` function is to allow the user to search for locations of vaccination drives in Singapore so that users can be better informed of where they can proceed to to get vaccinated for the coronavirus.
* The `getVaccinated` function can be requested via two methods, `GET` and `POST`.
* If the HTTP request method is `GET`, the application loads `tested.html` page.
* The webpage allows the user to input a Singapore postcode, which only allows numerical values up to six digits to be considered valid input. If the user input is NULL or None, the webpage would prompt the user to fill up the empty input field, with the aid of JQuery (JavaScript). 
* When the user presses the __search__ button, the application submits the form via `POST`, and will retrieve the user's longitude and latitude based on the postcode, using a free, open-source API called OneMap. 
* If the user inputs a postcode that is not valid, on form submission, an error message in red would appear reminding the user to input a valid Singapore postcode.
* Once the API returns the user's longitude and latitude, the Haversine method is used for calculating distance. The Haversine method takes four input values, Long1, Long2, Lat1 and Lat2, with Long1 and Lat1 being the user's input location, and the remaining two values being the location of the vaccination drive. The information of the vaccination drives are stored in a database, containing their names, addresses as well as longitude and latitude values, which are needed for computation. These information are imported from a CSV file, via a python program `import.py`. After calculations, the application returns the distance between the user's input and the vaccination drive in kilometers, and stores them in a list called `distance_info`.
* The list is then sorted by distance, in ascending order, as a variable called `distance_sorted`. The variable is parsed into the HTML page `tested.html`, where the names, addresses and the distance of the vaccination drive from the user's location is displayed, using a `FOR` loop expressed in Jinja format, in the order from nearest to furthest.

## Databases

### `options.db`
* `options.db` is a SQLite database that contains five tables, one for each question. 
* Each table has two columns, one for the option in string text and the other column being the number of points that particular option carries in integer format. 
* As the application runs, a search query is performed to see a match with the database. 
* If a match is found, the corresponding number of points is added into the total. The total number of points is then used to classify the user into the three risk levels.

### `vaccine.db`
* `vaccine.db` is a SQLite database that contains the information of the vaccine drives.
* Information such as the name, address, x and y coordinates, longitude and latitude, as well as the zone which the vaccination drive is located at are stored in this database.

## HTML and CSS Files

### `home.html`
* `home.html` is the homepage of the web application. 
* It allows the user access to the other functions of the application, such as the risk-assessment form and the locations for vaccinations. This homepage was developed using tools such as Bootstrap 5.0 and HTML. 
* When loaded, users are greeted with a large "carousel", a Bootstrap UI component, which would "slide-over" while showing images and links to the other functionalities of the web application. 
* When the user scrolls down, the user would see advice on how to stay safe from the coronavirus. These were created using Bootstrap's "grid-column", which sets limitations on the column width when viewed on both desktop and mobile. The icons were implemented using an icon set called font-awesome.
* Lastly, at the bottom of this page, is the footer, which contains the developer's name.

### `diagnose.html`
* `diagnose.html` loads the risk-assessment form which contains the questions that the user can answer to determine the user's risk level of getting the coronavirus. 
* The entire form is grouped into a Bootstrap 5.0 form class called "needs-validation". The reasoning is that this class would be used in some JavaScript function that would prevent the form from being submitted if the form is incomplete. This is applicable for questions 1 to 4, where the input type is radio. 
* For the final question, JQuery, a JavaScript library, was used for validating a checkbox-like input. 
* Another function where JavaScript was used was for preventing "contradicting" checkboxes from being pressed at the same time. For example, when clicking on one of the "symptom" boxes such as "running nose" or "cough", the "no symptoms" box automatically gets disabled, and vice-versa.
* On submission of the form, if the form does not return any validation errors (i.e unanswered questions), the form would load either of the three "risk" html pages, `lowrisk.html`, `moderaterisk.html` or `highrisk.html` depending on the results of the user's answers.

### `getlocation.html`
* This html page contains an empty field where the user can input a Singapore postcode to determine the nearest vaccination location.
* The form also checks whether a postcode has been typed in. If not, with the aid of JavaScript, will return an invalid response message.
* In addition, the form also validates the input, only allowing numerical values to be typed.

### `tested.html`
* On submission of the `getlocation.html` form, `tested.html` would return the results via the `/getvaccinated` path of `app.py`.
* Since the values are returned in a list of dictionaries, Jinja syntax was used to execute a `for` loop in the `tested.html` page to display the name, address and the distance from the user's location. 
* The data is sorted from nearest to furthest, with information at the top being the nearest location from the user.

### `lowrisk.html`, `moderaterisk.html`, `highrisk.html`
* One of the three risk pages (low, moderate and high risk) will render on the submission of the `diagnose.html` form. 
* If the total number of points is __less than five__, `lowrisk.html` is loaded. 
* If the total number of points is __five or greater but less than eight__, moderate.html is loaded. 
* Any result that __returns eight or greater__ loads `highrisk.html`.

### `styles.css`
The overall styling was done on styles.css.

## Other Files

### `locations.csv`
Contains the data of the vaccination drives in csv. To be imported into the `vaccine.db` database.

### `import.py`
Used to import the data from the `locations.csv` file to the `vaccine.db` database.
