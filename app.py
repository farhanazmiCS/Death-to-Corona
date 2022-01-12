from cs50 import SQL
from flask import Flask, render_template, request
from flask_session import Session
from tempfile import mkdtemp
from geopy import distance
from operator import itemgetter

# OneMap API
from onemapsg import OneMapClient

# The demo uses my email and password, register with OneMap to access /tested function
Client = OneMapClient("YOUR_EMAIL", "YOUR_PASSWORD")

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///options.db")
dbloc = SQL("sqlite:///vaccine.db")

@app.route("/")
def home():
    """Display self-diagnose link, tips and get tested"""
    return render_template("home.html")

@app.route("/riskassessment", methods=["GET", "POST"])
def riskAssessment():
    """Gets the user to do a self-diagnosis quiz"""
    if request.method == "POST":

        total = 0

        # Store information of form into a dict
        information = {"age": [] , "condition": [] ,"gender": [], "symptoms": [], "travelled": []}

        # Retrieve answer for questions (radio)
        question_ONE = request.form.get("age")
        question_TWO = request.form.get("medical")
        question_THREE = request.form.get("gender")
        question_FIVE = request.form.get("travel")

        # add to information dictionary to use this data later
        information["age"].append(question_ONE)
        information["condition"].append(question_TWO)
        information["gender"].append(question_THREE)
        information["travelled"].append(question_FIVE)

        # Question four returns a list of all checked elements
        question_FOUR = request.form.getlist("symptoms")

        # Loop through the list of checked elements to gain access to individual elements and
        # store them in a dictionary
        for symptom in question_FOUR:
            information["symptoms"].append(symptom)

        # Retrieve points from database
        get_point_one = db.execute("SELECT * FROM one WHERE options = ?", information["age"])
        # db.execute returns a list of dictionaries. This command returns first row and a specific column
        point_one = get_point_one[0]["points"]
        # Tally to total
        total += point_one

        get_point_two = db.execute("SELECT * FROM two WHERE options = ?", information["condition"])
        point_two = get_point_two[0]["points"]
        total += point_two

        get_point_three = db.execute("SELECT * FROM three WHERE options = ?", information["gender"])
        point_three = get_point_three[0]["points"]
        total += point_three

        get_point_four = db.execute("SELECT SUM(points) as totalpoints FROM four WHERE options in (?)", information["symptoms"])
        point_four = get_point_four[0]["totalpoints"]
        total += point_four

        get_point_five = db.execute("SELECT * FROM five WHERE options = ?", information["travelled"])
        point_five = get_point_five[0]["points"]
        total += point_five

        if total < 5:
            return render_template("lowrisk.html")

        elif total < 8 and total > 4:
            return render_template("moderaterisk.html")

        else:
            return render_template("highrisk.html")

    elif request.method == "GET":

        return render_template("diagnose.html")

@app.route("/getvaccinated", methods=["GET", "POST"])
def getVaccinated():
    """Returns a list of nearby clinics where the user can get vaccinated"""
    if request.method == "GET":
        return render_template("getlocation.html")

    elif request.method == "POST":

        # Declare an empty list to insert our distance values
        distance_info = []

        # Search query and execution
        location = request.form.get("location")
        try:
            execute = Client.search(location)
            ex = execute["results"][0]
        except:
            invalid_response = "The postal code you entered does not exist."
            return render_template("getlocation.html", invalid=invalid_response)

        # Retrieve longitude and latitude data of user to compare with database
        longitude = float(ex["LONGITUDE"])
        latitude = float(ex["LATITUDE"])

        coordinates = (latitude, longitude)
        # https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
        # Haversine formula
        # Approximate radius of earth in KM
        R = 6373.0

        # Call database to lookup the longitude and latitude values
        getLongandLat = dbloc.execute("SELECT * FROM locations")
        for row in getLongandLat:
            longitude2 = row["longitude"]
            latitude2 = row["latitude"]
            coordinates2 = (latitude2, longitude2)

            dist = distance.distance(coordinates, coordinates2).km
            row["distance"] = round(dist, 2)

            distance_info.append(row)

        distance_sorted = sorted(distance_info, key=itemgetter('distance'))

        return render_template("tested.html", info=distance_sorted)
