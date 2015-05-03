# ----------------------------------------------------------------------------------
# PURPOSE: EVENT PLOTTING
# ----------------------------------------------------------------------------------
# This script is designed to read in a series of earthquake locations in
# Indonesia for January 2015 from a text file and plot them into a basemap 
# based on weekly basis. 

# ----------------------------------------------------------------------------------
# STEP 1: IMPORT FUNCTION
# ----------------------------------------------------------------------------------

# Importing matplotlib.pyplot and define it as plt
import matplotlib.pyplot as plt
#Importing Basemap from mpl_toolkits.basemap
from mpl_toolkits.basemap import Basemap
#Importing date and time function
import datetime

# ----------------------------------------------------------------------------------
# STEP 2: MAP DISPLAY
# ----------------------------------------------------------------------------------

# Create a map with mercator projection highlighting Indonesia
map = Basemap(projection='merc', lat_0 =-0.659, lon_0 =113.379,
    resolution = 'h', area_thresh = 0.1,
    llcrnrlon=93.1304, llcrnrlat=-20.9248,
    urcrnrlon=142.3492, urcrnrlat=14.3024)
 
# Draw NASA bluemarble map
map.bluemarble()

# Draw lat/lon grid lines every 15 degrees.
map.drawmeridians(range(0, 360, 15), linewidth=0.5, color='grey', dashes=[2,2])
map.drawparallels(range(-90, 90, 15), linewidth=0.5, color='grey', dashes=[2,2])

# ----------------------------------------------------------------------------------
# STEP 3: SPATIO TEMPORAL DATA
# ----------------------------------------------------------------------------------

# Empty list of earthquake location data
locationData = []

# Open up a connection to read in data from the earthquake locations text file
inFile = open("earthquake_id_jan15.txt", 'r')

# Read in the first line from the text file, which is the header line
inLine = inFile.readline()
# Read in the next line from the text file, which is the first line of data
inLine = inFile.readline()
# Begin a while loop using the not equal to assessment (!=) that will continue until
# a blank line of text is read in
while inLine != "":
    # Split the text line up based on tabs "\t"
    dataLine = inLine.split("\t")
    # Create a label called "lon" that is a float equal to longitude of the
    # location
    lon = float(dataLine[0])
    # Create a label called "lon" that is a float equal to latitude of the
    # location
    lat = float(dataLine[1])
    # Create a label called "date" that is a date of occurence
    date = dataLine[2]
    # Append to the locationData list another list the first index of which will be 
    # the coordinate of the location and the second index will be a tuple of 
    # date
    locationData.append([(lon, lat), date])
    # Read in the next line from the text file
    inLine = inFile.readline()
    
# Close the connection to the earthquake locations text file
inFile.close()

# ----------------------------------------------------------------------------------
# STEP 3: CALCULATE TIME DIFFERENCE
# ----------------------------------------------------------------------------------

# Set the a base time to the first day of the month February to categorise date 
# on weekly basis
baseTime = datetime.datetime(2015, 2, 1)

# For each data point
for time in locationData:
    # Extract the data
    lon = time[0][0]
    lat = time[0][1]
    x,y = map(lon, lat)
    date = time[1]
    year, month, day = date.split("-")
    time = datetime.datetime(int(year), int(month), int(day))
    # Calculate the time difference
    deltaTime = time - baseTime
    deltaSeconds = deltaTime.total_seconds()
    deltaDays = float(deltaSeconds) / 86400

# ----------------------------------------------------------------------------------
# STEP 4: PLOTTING THE DATA
# ----------------------------------------------------------------------------------

    # Set the base size for point symbols
    size = 5 + (deltaDays * 5)
    # Plot the data differently based on time since base time
    # For earthquake events occured on week 4 of January 2015
    if deltaDays < -21:
        map.plot(x, y, "yo", markersize=6, alpha=.5)
     # For earthquake events occured on week 3 of January 2015
    elif deltaDays < -14:
        map.plot(x, y, "bo", markersize=5, alpha=.5)
    # For earthquake events occured on week 2 of January 2015
    elif deltaDays < -7:
        map.plot(x, y, "ro", markersize=4, alpha=.5)
    # For earthquake events occured on week 1 of January 2015
    else:
        map.plot(x, y, "go", markersize=3, alpha=.5)
        
# ----------------------------------------------------------------------------------
# STEP 5: SET UP EXTRAS
# ----------------------------------------------------------------------------------        
# Add a map scale
atLon = 135 # Longitude position for scale
atLat = -18 # Latitude position for scale
forLength =1000 # length in km
map.drawmapscale(atLon, atLat, atLon, atLat, length=forLength)

# Add a north arrow
atLon = 96  # Longitude position for north arrow
atLat = 10 # Latitude position for north arrow
forLength = 2 # length in degrees
x, y = map(atLon, atLat)
x2, y2 = map(atLon, atLat + forLength)
plt.arrow(x, y, 0, y2 - y, fc="k", ec="k", 
          head_width=75000, head_length=75000) 
# head width and length control size of arrow head
plt.text(x, y, "N", verticalalignment="top", horizontalalignment="center")

# Add a legend
yellow = plt.scatter([], [], s=12, c="yellow", edgecolors="none")
blue = plt.scatter([], [], s=10, c="blue", edgecolors="none")
red = plt.scatter([], [], s=8, c="red", edgecolors="none")
green = plt.scatter([], [], s=6, c="green", edgecolors="none")
labels = ["Week 1", "Week 2", "Week 3", "Week 4"]

leg = plt.legend([green, red, blue, yellow], labels, frameon=True, fontsize=8,
                 handlelength=0.5, loc=3, borderpad=0.5, handletextpad=1, 
                 scatterpoints=1)
# Add a title
plt.title("Earthquake Event in Indonesia - January 2015")

# Display and export the map
plt.show()
plt.savefig("earthquake_map.png", dpi=300, bbox_inches="tight", 
            transparent=False)

# End of script