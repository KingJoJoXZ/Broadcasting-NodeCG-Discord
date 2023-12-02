import discord
import motor.motor_asyncio
from discord.ext import commands
from keys import token
import valo_api as VAPI
import requests 
import json
from valo_api.exceptions.valo_api_exception import ValoAPIException
from datetime import datetime
import pytz


# Initialize the bot

intents = discord.Intents.all()
intents.typing = False
intents.presences = False
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

#Initialize the API

api_key = "#######################"


#Initialize MongoDB

url = "mongodb+srv://group:group@groupproject.nt55qnv.mongodb.net/?retryWrites=true&w=majority"
port = 27017
database_name = "test_data"
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(url)
db = mongo_client["test_data"]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

#Commands

@bot.command()
async def hello(ctx):
    await ctx.send("Hello, I am your Discord bot!")

#Add to db



#Get Stats from the database

@bot.command()
async def getOldStats(ctx, username):
    # Retrieve data from the MongoDB collection
    collection = db["tests"]
    query = {"username" : username}
    stats_cursor = collection.find(query)

    # Convert the cursor to a list
    stats_list = await stats_cursor.to_list(length=100)
    stats = stats_list[0]
    print(stats)
    # Send each document as a separate message
    await ctx.send(f"__{username}'s Stats from {stats['date']} and older__ \n**Most recent game** \n   When: {stats['date']} at {stats['time']}EST \n**Total** \n  Kills: {stats['total_kills']}, Deaths: {stats['total_deaths']} \n**Average** \n   Kills: {stats['average_kills']}, Deaths: {stats['average_deaths']}") 
#Put Stats into DB
async def setOldStats(username,kills,deaths,assists,total_kills,average_kills,total_deaths,average_deaths,date,time):
    # Insert data into the MongoDB collection
    new_vals = {
    "$set": {
        "kills" : kills,
        "deaths" : deaths,
        "assists" : assists,
        "username": username,
        "total_kills": total_kills,
        "average_kills": average_kills,
        "total_deaths": total_deaths,
        "average_deaths": average_deaths,
        "date": date,
        "time": time
        }
    }
    collection = db["tests"]
    try:
        query = {"username" : username}
        await collection.update_one(query,new_vals)
    except:
        await collection.insert_one(new_vals)
@bot.command()
async def getStats(ctx,*,username):
    #Splitting name and tag
    tag = ""
    name, tag = username.split("#", 1)
    # Replace spaces with '%'
    name = name.replace(' ', '%')

    mode = "competitive"
    headers = {
    "Authorization": api_key,
}   
    #Endpoint URL
    try:
        url = f"https://api.henrikdev.xyz/valorant/v1/lifetime/matches/na/{name}/{tag}?mode={mode}"
        #Get json response from API
        response = requests.get(url=url, headers=headers)
        json_data = response.json()
        # Extract the list of matches
        matches = json_data['data']
    except:
        await ctx.send("User does not exist or has not played any matches")

    # Sort the matches by the 'started_at' field in descending order
    sorted_matches = sorted(matches, key=lambda x: x['meta']['started_at'], reverse=True)

    #loop over the sorted matches to extract information
    count = 0
    total_kills = 0
    average_kills = 0
    total_deaths = 0
    average_deaths = 0
    
    for match in sorted_matches:
        # Extract specific data
        count += 1
        match_id = match['meta']['id']
        if(count ==1):
            #Get Start time of most recent match
            start_time = match['meta']['started_at']
            #Split date and time 
            date,time = start_time.split("T",1)
            #Date is returned Y/M/D we want M/D/Y
            year = date[0:4]
            month = date[5:7]
            day = date[8:10]
            #Set to M/D/Y
            date = month+"/"+day+"/"+year
            utc_timestamp_str = start_time
            utc_timestamp = datetime.strptime(utc_timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            # Define the UTC timezone
            utc_timezone = pytz.timezone("UTC")
            # Localize the UTC timestamp
            utc_timestamp = utc_timezone.localize(utc_timestamp)

            # Define the Eastern Standard Time (EST) timezone
            est_timezone = pytz.timezone("America/New_York")

            # Convert the timestamp to EST
            est_timestamp = utc_timestamp.astimezone(est_timezone)
            est_timestamp_str = est_timestamp.strftime("%Y-%m-%d %H:%M:%S.%f %Z")
            #Extract time from date string
            time = est_timestamp_str[11:16]
        kills = match['stats']['kills']
        deaths = match['stats']['deaths']
        assists = match['stats']['assists']
        #Get total and average kills/deaths
        total_kills += kills
        average_kills = round(total_kills/count,2)
        total_deaths += deaths
        average_deaths = round(total_deaths/count,2)
        # Send the latest match data to the Discord channel
    name = name.replace('%',' ')
    await ctx.send(f"__{name}'s Stats__ \n**Most recent game** \n   When: {date} at {time}EST, Kills: {kills}, Deaths: {deaths}, Assists: {assists} \n**Total** \n  Kills: {total_kills}, Deaths: {total_deaths} \n**Average** \n   Kills: {average_kills}, Deaths: {average_deaths}") 
    await setOldStats(username,kills,deaths,assists,total_kills,average_kills,total_deaths,average_deaths,date,time)


# Run the bot
bot.run('YOUR_DISCORD_BOT_KEY_HERE')