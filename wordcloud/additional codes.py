#Print 1st five lines
#print(df.head())

#Print total rows and columns
#print("There are {} observations and {} features in this dataset.\n".format(df.shape[0], df.shape[1]))

#selected columns
#print(df[["Mission", "Type", "Subtype"]].head())

#group by mission
#mission = df.groupby("Mission")

#select highest average weight per mission
#print(mission.mean().sort_values(by="Weight(g)", ascending=False).head())

#Weight VS Mission Graph
# plt.figure(figsize=(15, 10))
# mission.size().sort_values(ascending=False).plot.bar()
# plt.xticks(rotation=50)
# plt.xlabel("Mission Name")
# plt.ylabel("Weight")
# plt.show()