# save searches and their template paths
# input date in YYYY-MM-DD format -> add to guidelines

import requests
import json
import random
import os
import mysql.connector

dir_path = ""

def getInput(inputSearch):
    possibleQueries = generateQueries(filterInput(inputSearch), inputSearch)
    if(inputSearch.upper() != "" or filterInput(inputSearch) != "ERROR"):
        imageDownloader(possibleQueries, inputSearch)
    createDB()

def filterInput(inputSearch):
    # Text which user input can be a camera type, sol, rover name, date or status
    global dir_path

    cameraTypes = ["FHAZ", "RHAZ", "MAST", "CHEMCAM", "MAHLI", "MARDI", "NAVCAM", "PANCAM", "MINITES"]
    if(inputSearch in cameraTypes):
        result = "camera"
        dir_path = "processed-images/originals/camera"

    elif(inputSearch.isdigit()):
        result = "sol"
        dir_path = "processed-images/originals/sol"

    elif(inputSearch.lower() == "curiosity" or inputSearch.lower() == "opportunity" or inputSearch.lower() == "spirit"):
        result = "rover"
        dir_path = "processed-images/originals/rover"

    elif(len(inputSearch) == 10):
        if(validateDate(inputSearch)):
            result = "date"
            dir_path = "processed-images/originals/earth-date"
        else:
            result = "ERROR"

    elif(inputSearch.lower()=="active" or inputSearch.lower()=="complete" or inputSearch.lower()=="inactive"):
        result = "status"
        dir_path = "processed-images/originals/status"

    else:
        result = "ERROR"

    return result

def validateDate(textDate):

    if(textDate.find("-")>0):
        delim = "-"
    elif(textDate.find("/")>0):
        delim = "/"
    elif(textDate.find(".")>0):
        delim = "."

    year, month, day = textDate.split(delim)
    year = int(year)
    month = int(month)
    day = int(day)

    def checkDay(month, day):
        
        if(month==1 and day in range(1,32)):
            status = True
        elif(month==2 and day in range(1,29)):
            status = True
        elif(month==3 and day in range(1,32)):
            status = True
        elif(month==4 and day in range(1,31)):
            status = True
        elif(month==5 and day in range(1,32)):
            status = True
        elif(month==6 and day in range(1,31)):
            status = True
        elif(month==7 and day in range(1,32)):
            status = True
        elif(month==8 and day in range(1,32)):
            status = True
        elif(month==9 and day in range(1,31)):
            status = True
        elif(month==10 and day in range(1,32)):
            status = True
        elif(month==11 and day in range(1,31)):
            status = True
        elif(month==12 and day in range(1,32)):
            status = True

        return status

    # spirit and curiosity launch year = 2003
    if(year >= 2003 and month in range(1,13) and checkDay(month, day)):
        return True
    else:
        return False

def generateQueries(inputType, inputSearch):
    possibleQueries = {}

    sols = []
    for i in range(3):
        n = random.randint(0, 3000)
        sols.append(str(n))

    curiosityQ = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=" + sols[0] + "&camera=" + inputSearch + "&api_key=Iy6ndQpWKECX5adXsiHgPvbIef9KyZ2QtvruNThl"
    opportunityQ = "https://api.nasa.gov/mars-photos/api/v1/rovers/opportunity/photos?sol=" + sols[1] + "&camera=" + inputSearch + "&api_key=Iy6ndQpWKECX5adXsiHgPvbIef9KyZ2QtvruNThl"
    spiritQ = "https://api.nasa.gov/mars-photos/api/v1/rovers/spirit/photos?sol=" + sols[2] + "&camera=" + inputSearch + "&api_key=Iy6ndQpWKECX5adXsiHgPvbIef9KyZ2QtvruNThl"
    
    if(inputType == "camera"):
        if(inputSearch.upper() == "FHAZ" or inputSearch.upper == "RHAZ" or inputSearch == "NAVCAM"):
            # present in all 3 rovers

            queries = [curiosityQ, opportunityQ, spiritQ]

            #f = open("test.txt", "w")
            for query in queries:
                response = requests.get(query)
                
                if(response.status_code == 200):
                    jsonData = json.loads(response.text)
                    dictData = jsonData

                    i = 0
                    for val in dictData.values():
                        for l in val:
                            possibleQueries[i] = l
                            i += 1
                            #f.write(str(l) + "\n")
                    
                elif(response.status_code == 404):
                    #f.write("Error connecting to API")
                    return
                
                else:
                    #f.write("An unidentified error occured")
                    return

            #f.write(str(possibleQueries[2]['img_src']))
            #f.close()

        elif(inputSearch.upper() == "PANCAM" or inputSearch.upper() == "MINITES"):
            # present in opportunity and spirit

            queries = [opportunityQ, spiritQ]

            #f = open("test.txt", "w")
            for query in queries:
                response = requests.get(query)
                
                if(response.status_code == 200):
                    jsonData = json.loads(response.text)
                    dictData = jsonData

                    i = 0
                    for val in dictData.values():
                        for l in val:
                            possibleQueries[i] = l
                            i += 1
                            #f.write(str(l) + "\n")
                    
                elif(response.status_code == 404):
                    #f.write("Error connecting to API")
                    return
                
                else:
                    #f.write("An unidentified error occured")
                    return

            #f.close()

        else:
            queries = [curiosityQ]

            #f = open("test.txt", "w")
            for query in queries:
                response = requests.get(query)
                
                if(response.status_code == 200):
                    jsonData = json.loads(response.text)
                    dictData = jsonData

                    i = 0
                    for val in dictData.values():
                        for l in val:
                            possibleQueries[i] = l
                            i += 1
                            #f.write(str(l) + "\n")
                    
                elif(response.status_code == 404):
                    #f.write("Error connecting to API")
                    return
                
                else:
                    #f.write("An unidentified error occured")
                    return
            #f.close()

    return possibleQueries

def imageDownloader(possibleQueries, inputSearch):
    randomImageSources = []
    randomImageIndexes = []
    count = 1

    if(len(possibleQueries) > 0):
        for i in range(0, 3):
            n = random.randint(0, len(possibleQueries)-1)
            randomImageIndexes.append(n)
    
    for i in randomImageIndexes:
        randomImageSources.append(str(possibleQueries[i]['img_src']))   

    if (dir_path != ""):
        for path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, path + "/" + inputSearch.upper())):
                count += 1

    for url in randomImageSources:
        r = requests.get(url)
        open(dir_path + "/" +  inputSearch.upper() + " - " + str(count) + ".png", 'wb').write(r.content)
        count += 1

def createDB():
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Root1234$"
    )

    f = open("test.txt", "w")
    f.write(str(db))
    f.close()
# def createDB():
#     marsapp.app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///Mars_Imagery.db'
#     db = SQLAlchemy(marsapp.app)

#     class ImageInfo(db.Model):
#         image_id = db.Column(db.Integer, primary_key = True)
#         sol = db.Column(db.Integer, nullable = False)
#         camera = db.Column(db.String(10), nullable = False)
#         path = db.Column(db.String(150), nullable = False)
#         earth_date = db.Column(db.Date, nullable = False)
#         rover_name = db.Column(db.String(100), nullable = False)
#         landing_date = db.Column(db.Date, nullable = False)
#         launch_date = db.Column(db.Date, nullable = False)
#         status = db.Column(db.String(50), nullable = False)

#     class SearchImage(db.Model):
#         search_text = db.Column(db.String(150), nullable = False)
#         image1 = db.Column(db.Integer, nullable = False)
#         image2 = db.Column(db.Integer, nullable = False)
#         image3 = db.Column(db.Integer, nullable = False)