import pandas as pd
import matplotlib.pyplot as plt
import wordcloud

#Create dataframe
df = pd.read_csv("data/rocksamples.csv", index_col=0)

#calculating frequencies and create wordcloud
rock_types = {}
rock_subtypes = {}

def calculate_frequencies(dict):
   
    #Get types of rocks
    for type in df["Type"]:
        if type not in rock_types:
            rock_types[type] = 0

    #Get sub types of rocks
    for sub in df["Subtype"]:
        if sub not in rock_subtypes:
            rock_subtypes[str(sub)] = 0
    
    for type in df["Type"]:
        if type in rock_types:
            rock_types[type] += 1
        else:
            rock_types[type] = 1

    for sub in df["Subtype"]:
        if sub in rock_subtypes:
            rock_subtypes[str(sub)] += 1
        else:
            rock_subtypes[str(sub)] = 1

    cloud = wordcloud.WordCloud()
    cloud.generate_from_frequencies(dict)
    return cloud.to_array()

#display wordcloud image
print("1 - Rock types\n2 - Rock subtypes")
print("Enter a number to begin: ", end = "")
n = int(input())
if (n == 1):
    image = calculate_frequencies(rock_types)
elif(n == 2):
    image = calculate_frequencies(rock_subtypes)

try:
    plt.imshow(image, interpolation='nearest')
    plt.axis('off')
    plt.show()

except:
    print("INVALID INPUT")