import discord
import requests
import json
import asyncio

intents = discord.Intents.default()
intents.messages = True  
client = discord.Client(intents=intents)

#writ your discord bot token here
TOKEN = ""


def get_score():
    leaderboard = ''
    id = 1
    response = requests.get("http://127.0.0.1:8000/api/score/leaderboard")
    json_data = json.loads(response.text)

    for item in json_data:
        leaderboard += str(id) + ' ' + item['name'] + ":  " + str(item['points']) + " points \n"
        id += 1 

    return(leaderboard)

def update_score(user,points):
    url = "http://127.0.0.1:8000/api/score/update"
    new_score = {'name': user, 'points': points}
    x = requests.post(url, data = new_score)

    return

def get_question():
    qs = ''
    id = 1
    answer = 0
    points = 0
    response = requests.get("http://127.0.0.1:8000/api/random")
    json_data = json.loads(response.text)
    qs+="Question: \n"
    qs+=json_data[0]['title'] + '\n'
    
    for item in json_data[0]['answer']:
        qs+=str(id) + '. ' + item['answer'] + '\n'
        
        if item['is_correct']:
            answer = id
        id+=1    
    
    points = json_data[0]['points']    
        
    return(qs, answer, points)    

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$score'):
       leaderboard = get_score()
       await message.channel.send(leaderboard)
       
    if message.content.startswith('$question'):
        
        qs , answer, points= get_question()
        await message.channel.send(qs)
    
        def check(m):
            return m.author == message.author and m.content.isdigit()
        
        try:
            guess = await client.wait_for('message', check=check)
        except asyncio.TimeoutError:
            return await message.channel.send('Sorry, you took too long')
        
        if int(guess.content) == answer:
            user = guess.author
            msg=''
            if points ==1:
               msg = str(guess.author.name)+" got it right +" + str(points) +" point"
            else :
               msg = str(guess.author.name)+" got it right +" + str(points) +" points"      
            await message.channel.send(msg)
            update_score(user , points)
        else:
            await message.channel.send('Oops. That is not right')
                
client.run(TOKEN)
