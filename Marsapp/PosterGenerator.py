# save searches and their template paths
# input date in YYYY-MM-DD format -> add to guidelines

import requests
import json
import random
import os
import mysql.connector
import textwrap
import tensorflow as tf
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from skimage.color import rgb2lab, lab2rgb
from skimage.io import imsave

db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Root1234$",
        database = "MarsImagery"
    )

dir_path = ""

def getInput(inputSearch):
    possibleQueries = generateQueries(filterInput(inputSearch), inputSearch)
    if(inputSearch.upper() != "" or filterInput(inputSearch) != "ERROR"):
        imageDownloader(possibleQueries, inputSearch)

    # resizeImages()
    # colorImages("processed-images/resized/FHAZ - 1.png")


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

            #f.write(str(possibleQueries[2]['img_src']))
            #f.close()

        elif(inputSearch.upper() == "PANCAM" or inputSearch.upper() == "MINITES"):
            # present in opportunity and spirit

            queries = [opportunityQ, spiritQ]

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

        else:
            # present in curiosity only
            queries = [curiosityQ]

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

    return possibleQueries


def imageDownloader(possibleQueries, inputSearch):
    randomImageSources = []
    randomImageIndexes = []
    image_ids = []
    count = 1

    if(len(possibleQueries) > 0):
        for i in range(0, 3):
            n = random.randint(0, len(possibleQueries)-1)
            randomImageIndexes.append(n)
    
    for i in randomImageIndexes:
        if(checkForExistingImages(str(possibleQueries[i]['id']))):
            randomImageSources.append(str(possibleQueries[i]['img_src']))
        else:
            image_ids.append(str(possibleQueries[i]['id']))

    if (dir_path != ""):
        for path in os.listdir(dir_path):
            find_search = path.split()[0]

            if(find_search == inputSearch.upper()):
                count += 1

    for url in randomImageSources:
        r = requests.get(url)
        path = dir_path + "/" +  inputSearch.upper() + " - " + str(count) + ".png"
        open(path, 'wb').write(r.content)
        image_id = possibleQueries[randomImageSources.index(url)]["id"]
        if(checkForExistingImages(image_id) == True):
            updateImageTable(possibleQueries, randomImageSources.index(url), path)
        image_ids.append(image_id)
        count += 1

    updateSearchTable(inputSearch.upper(), image_ids)


def updateImageTable(possibleQueries, i, path_to_image):
    cursor = db.cursor()
    add_to_image_table_Q = "INSERT INTO image_info(image_id, sol, camera, path, earth_date, rover_name, rover_landing_date, rover_launch_date, status) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (str(possibleQueries[i]['id']),
            str(possibleQueries[i]['sol']),
            str(possibleQueries[i]['camera']['name']),
            path_to_image,
            str(possibleQueries[i]['earth_date']),
            str(possibleQueries[i]['rover']['name']),
            str(possibleQueries[i]['rover']['landing_date']),
            str(possibleQueries[i]['rover']['launch_date']),
            str(possibleQueries[i]['rover']['status']))
    cursor.execute(add_to_image_table_Q, values)
    db.commit()


def updateSearchTable(search_text, image_ids):
    cursor = db.cursor()
    add_to_search_table_Q = "INSERT INTO search_image(search_text, image1, image2, image3) values(%s, %s, %s, %s)"
    
    if (len(image_ids) > 0):
        values = (search_text, 
        str(image_ids[0]), 
        str(image_ids[1]), 
        str(image_ids[2]))

        cursor.execute(add_to_search_table_Q, values)
        db.commit()


def checkForExistingImages(image_id):
    cursor = db.cursor()
    cursor.execute("SELECT image_id from image_info where image_id = " + str(image_id))
    result = cursor.fetchall()
    if(len(result) == 0):
        return True
    else:
        return False


def resizeImages():
    for filename in os.listdir("processed-images/originals/camera"):
        path = "processed-images/originals/camera/"
        image = Image.open(path + filename)
        new_image = image.resize((256, 256))
        newpath = "processed-images/resized/"
        new_image.save(newpath + filename)


def colorImages(image_to_be_coloured):
    model = tf.keras.models.load_model("Image Colorization - Model 1")

    color_me = []
    color_me.append(tf.keras.utils.img_to_array(tf.keras.utils.load_img(image_to_be_coloured)))
    color_me = np.array(color_me, dtype=float)
    color_me = rgb2lab(1.0/255 * color_me)[:,:,:,0]
    color_me = color_me.reshape(color_me.shape + (1,))

    # Predict Images
    output = model.predict(color_me)
    output = output * 128

    # Save Results
    for i in range(len(output)):
        cur = np.zeros((256, 256, 3))
        cur[:,:,0] = color_me[i][:,:,0]
        cur[:,:,1:] = output[i]
    imsave("processed-images/colored-results/" + image_to_be_coloured.split("/")[-1] + ".png", lab2rgb(cur)*255)


def createPosterTemp1(title, arr_image_paths, dict_image_data, description, src):
    # initialize template
    temp1 = Image.new('RGB', (1920, 1080), color=(0,0,0))
    
    # Add title
    text1 = ImageDraw.Draw(temp1)
    font = ImageFont.truetype("arial.ttf", 50)
    text1.text((910, 40), title, fill=(255, 255, 255), font=font)
    
    # Get Images
    img1 = Image.open(arr_image_paths[0])
    img1 = img1.resize((256, 256))
    img2 = Image.open(arr_image_paths[1])
    img2 = img2.resize((256, 256))
    img3 = Image.open(arr_image_paths[2])
    img3 = img3.resize((256, 256))

    # Add images to template
    temp1.paste(img1, (1000, 150))
    temp1.paste(img2, (1306, 150))
    temp1.paste(img3, (1612, 150))

    # Add field names
    fieldFont = ImageFont.truetype("arial.ttf", 25)
    sol = ImageDraw.Draw(temp1)
    sol.text((700, 450), "Sol", fill=(255, 255, 255), font=fieldFont)

    earth_date = ImageDraw.Draw(temp1)
    earth_date.text((700, 520), "Date of Image (Earth)", fill = (255, 255, 255), font=fieldFont)

    rover_name = ImageDraw.Draw(temp1)
    rover_name.text((700, 590), "Rover Name", fill = (255, 255, 255), font=fieldFont)

    rover_landing_date = ImageDraw.Draw(temp1)
    rover_landing_date.text((700, 660), "Rover Landing Date", fill = (255, 255, 255), font=fieldFont)

    rover_launch_date = ImageDraw.Draw(temp1)
    rover_launch_date.text((700, 730), "Mission Launch Date", fill = (255, 255, 255), font=fieldFont)

    status = ImageDraw.Draw(temp1)
    status.text((700, 800), "Status of Mission", fill = (255, 255, 255), font=fieldFont)

    # add description
    ques = ImageDraw.Draw(temp1)
    descTitleFont = ImageFont.truetype("arial.ttf", 30)
    ques.text((50, 150), "What is FHAZ?", fill = (255, 255, 255), font=descTitleFont)

    desc = ImageDraw.Draw(temp1)
    descFont = ImageFont.truetype("arial.ttf", 20)
    descText = textwrap.fill(text=description, width=60)
    desc.text((50, 230), descText, fill = (255, 255, 255), font=descFont, spacing=15)

    # Add sources
    source = ImageDraw.Draw(temp1)
    source.text((50, 1000), "Sources: " + src, fill = (255, 255, 255), font=descFont)

    # Save Poster
    temp1.save("processed-images/posters/T1" + title.upper() + ".png")


def getDataForPoster(inputSearch):
    cursor = db.cursor()
    cursor.execute("SELECT image1, image2, image3 FROM search_image WHERE search_text=" + inputSearch.upper())
    get_img_ids = cursor.fetchall()
    chosen_img_ids = random.randint(0, len(get_img_ids))

    image_data = {}

    # returns this [(283128, 283129, 283130), (282224, 282225, 282224)]

getDataForPoster("\"FHAZ\"")