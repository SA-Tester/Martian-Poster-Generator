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
    
    if(inputSearch != None or inputSearch != "ERROR"):
        imageDownloader(possibleQueries, inputSearch.upper())
        getDataForPosterTemp1("\"" + inputSearch + "\"")
    
    
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
        n = random.randint(0, 2500)
        sols.append(str(n))

    curiosityQ = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=" + sols[0] + "&camera=" + inputSearch + "&api_key=Iy6ndQpWKECX5adXsiHgPvbIef9KyZ2QtvruNThl"
    opportunityQ = "https://api.nasa.gov/mars-photos/api/v1/rovers/opportunity/photos?sol=" + sols[1] + "&camera=" + inputSearch + "&api_key=Iy6ndQpWKECX5adXsiHgPvbIef9KyZ2QtvruNThl"
    spiritQ = "https://api.nasa.gov/mars-photos/api/v1/rovers/spirit/photos?sol=" + sols[2] + "&camera=" + inputSearch + "&api_key=Iy6ndQpWKECX5adXsiHgPvbIef9KyZ2QtvruNThl"
    
    if(inputType == "camera"):
        if(inputSearch.upper() == "FHAZ" or inputSearch.upper == "RHAZ" or inputSearch == "NAVCAM"):
            # present in all 3 rovers

            queries = [curiosityQ, opportunityQ, spiritQ]

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


def resizeImages(img_path):
    filename = img_path.split("/")[-1]
    image = Image.open(img_path)
    new_image = image.resize((256, 256))
    newpath = "processed-images/resized/"
    new_image.save(newpath + filename)
    return (newpath + filename)

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
    path = "processed-images/colored-results/" + image_to_be_coloured.split("/")[-1] + ".png"
    return path


def createPosterTemp1(title, arr_image_paths, dict_image_data, description, src):
    # resize original images
    resized_image_paths = []
    for img_path in arr_image_paths:
        resized_image_paths.append(resizeImages(img_path))
    
    coloured_image_paths = []
    for img_path in resized_image_paths:
        coloured_image_paths.append(colorImages(img_path))

    # initialize template
    temp1 = Image.new('RGB', (1920, 1080), color=(0,0,0))
    
    # Add title
    text1 = ImageDraw.Draw(temp1)
    font = ImageFont.truetype("arial.ttf", 50)
    text1.text((910, 40), title[1 : -1], fill=(255, 255, 255), font=font)
    
    # Get Images
    if(len(coloured_image_paths) > 0):
        img1 = Image.open(coloured_image_paths[0])
        img1 = img1.resize((256, 256))
        img2 = Image.open(coloured_image_paths[1])
        img2 = img2.resize((256, 256))
        img3 = Image.open(coloured_image_paths[2])
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

    if (len(dict_image_data)>0):
        # Row 1 - Sol
        sol_data_1 = ImageDraw.Draw(temp1)
        sol_data_1.text((1100, 450), str(dict_image_data[0]['sol']), fill=(255, 255, 255), font=fieldFont)

        sol_data_2 = ImageDraw.Draw(temp1)
        sol_data_2.text((1400, 450), str(dict_image_data[1]['sol']), fill=(255, 255, 255), font=fieldFont)

        sol_data_3 = ImageDraw.Draw(temp1)
        sol_data_3.text((1700, 450), str(dict_image_data[2]['sol']), fill=(255, 255, 255), font=fieldFont)

        # Row 2 - Earth Date
        ed_1 = ImageDraw.Draw(temp1)
        ed_1.text((1070, 520), str(dict_image_data[0]['earth_date']), fill=(255, 255, 255), font=fieldFont)

        ed_2 = ImageDraw.Draw(temp1)
        ed_2.text((1370, 520), str(dict_image_data[1]['earth_date']), fill=(255, 255, 255), font=fieldFont)

        ed_3 = ImageDraw.Draw(temp1)
        ed_3.text((1670, 520), str(dict_image_data[2]['earth_date']), fill=(255, 255, 255), font=fieldFont)

        # Row 3 - Rover Name
        rover1 = ImageDraw.Draw(temp1)
        rover1.text((1070, 590), str(dict_image_data[0]['rover_name']), fill=(255, 255, 255), font=fieldFont)

        rover2 = ImageDraw.Draw(temp1)
        rover2.text((1370, 590), str(dict_image_data[1]['rover_name']), fill=(255, 255, 255), font=fieldFont)

        rover3 = ImageDraw.Draw(temp1)
        rover3.text((1670, 590), str(dict_image_data[2]['rover_name']), fill=(255, 255, 255), font=fieldFont)

        # Row 4 - Rover Landing Date
        r_land_1 = ImageDraw.Draw(temp1)
        r_land_1.text((1070, 660), str(dict_image_data[0]['rover_landing_date']), fill=(255, 255, 255), font=fieldFont)

        r_land_2 = ImageDraw.Draw(temp1)
        r_land_2.text((1370, 660), str(dict_image_data[1]['rover_landing_date']), fill=(255, 255, 255), font=fieldFont)

        r_land_3 = ImageDraw.Draw(temp1)
        r_land_3.text((1670, 660), str(dict_image_data[2]['rover_landing_date']), fill=(255, 255, 255), font=fieldFont)

        # Row 5 - Rover Launching Date
        r_launch_1 = ImageDraw.Draw(temp1)
        r_launch_1.text((1070, 730), str(dict_image_data[0]['rover_launch_date']), fill=(255, 255, 255), font=fieldFont)

        r_launch_2 = ImageDraw.Draw(temp1)
        r_launch_2.text((1370, 730), str(dict_image_data[1]['rover_launch_date']), fill=(255, 255, 255), font=fieldFont)

        r_launch_3 = ImageDraw.Draw(temp1)
        r_launch_3.text((1670, 730), str(dict_image_data[2]['rover_launch_date']), fill=(255, 255, 255), font=fieldFont)

        # Row 5 - Status
        status1 = ImageDraw.Draw(temp1)
        status1.text((1070, 800), str(dict_image_data[0]['status']), fill=(255, 255, 255), font=fieldFont)

        status2 = ImageDraw.Draw(temp1)
        status2.text((1370, 800), str(dict_image_data[1]['status']), fill=(255, 255, 255), font=fieldFont)

        status3 = ImageDraw.Draw(temp1)
        status3.text((1670, 800), str(dict_image_data[2]['status']), fill=(255, 255, 255), font=fieldFont)


    # add description
    ques = ImageDraw.Draw(temp1)
    descTitleFont = ImageFont.truetype("arial.ttf", 33)
    ques.text((60, 180), "What is " + title[1 : -1] + "?", fill = (255, 255, 255), font=descTitleFont)

    desc = ImageDraw.Draw(temp1)
    descFont = ImageFont.truetype("arial.ttf", 23)
    descText = textwrap.fill(text=description, width=45)
    desc.text((60, 260), descText, fill = (255, 255, 255), font=descFont, spacing=15)

    # Add sources
    source = ImageDraw.Draw(temp1)
    source2 = "https://api.nasa.gov/"
    if(len(src) > 0):
        source.text((60, 1000), "Sources: " + src[0][1:-1] + "\t|\t" + source2, fill = (255, 255, 255), font=descFont)

    # Save Poster
    temp1.save("static/images/posters/T1 - " + title.upper()[1:-1] + ".png")


def getDataForPosterTemp1(inputSearch):
    cursor = db.cursor()

    if (inputSearch != "" or inputSearch != None):
        cursor.execute("SELECT image1, image2, image3 FROM search_image WHERE search_text=" + inputSearch.upper())
        get_img_ids = cursor.fetchall()
        chosen_img_ids = []
        if(len(get_img_ids)>0):
            chosen_img_ids = get_img_ids[random.randint(0, len(get_img_ids)-1)]

        image_paths = []
        for id in chosen_img_ids:
            cursor.execute("SELECT path from image_info where image_id = " + "\"" + str(id) + "\"")
            image_paths.append(str(cursor.fetchone())[2 : -3])

        comp_img_data = {}
        i = 0
        for id in chosen_img_ids:
            cursor.execute("SELECT sol, earth_date, rover_name, rover_landing_date, rover_launch_date, status from image_info where image_id = " + "\"" + str(id) + "\"")
            data = cursor.fetchone()
            image_data = {}
            image_data["sol"] = data[0]
            image_data["earth_date"] = data[1]
            image_data["rover_name"] = data[2]
            image_data["rover_landing_date"] = data[3]
            image_data["rover_launch_date"] = data[4]
            image_data["status"] = data[5]
            comp_img_data[i] = image_data
            i += 1

        description = ""
        sources = []
        if(filterInput(inputSearch[1 : -1]) == "camera"):
            if(inputSearch[1 : -1] == "FHAZ" or inputSearch[1 : -1] == "RHAZ"):
                cursor.execute("SELECT description from camera_info where camera_name = " + "\"" + inputSearch[2:-1].upper() + "\"")
                description = cursor.fetchone()
                cursor.execute("SELECT source from camera_info where camera_name = " + "\"" + inputSearch[2:-1].upper() + "\"")
                sources.append(str(cursor.fetchone())[1 : -1])

            else:
                cursor.execute("SELECT description from camera_info where camera_name = " + inputSearch.upper())
                description = cursor.fetchone()
                cursor.execute("SELECT source from camera_info where camera_name = " + inputSearch.upper())
                sources.append(str(cursor.fetchone())[1 : -2])
        
        description = str(description)[1 : -2]
        
        db.commit()
        
        createPosterTemp1(inputSearch.upper(), image_paths, comp_img_data, description, sources)