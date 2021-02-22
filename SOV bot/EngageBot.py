# bot.py
import os
import platform
from discord.ext import commands
import discord
import datetime
from dotenv import load_dotenv
import threading
import time
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
EngagementOn = False
EngagementList = []
EngagementStartMsgId = 0
swearListArray = []
SwearBroadcast = False

#time = datetime.datetime.now

unixStartTime = time.time()
startDay = datetime.date.today().strftime("%B %d, %Y")
startTime = datetime.datetime.now().strftime("%H:%M:%S")

bot = commands.Bot(command_prefix='!')

print("Bot initialized at ", startDay, "at", startTime)
#TIMER FUNCTION VARIABLES

#HELPER FUNCTIONS:

#class multiThread(object):

#    def __init__(self, interval = 60):
#        self.interval = interval

#        thread = threading.Thread(target=self.run, args=())
#        thread.daemon = True
#        thread.start()

#    def run(self):
#        global EngagementOn
#        global client
#        while True:
#            current_date = datetime.datetime.now()
#            #print(datetime.datetime.now().__str__())
#            #Monday, Wednesday, Friday
#            #if current_date.strftime("%w") in ('1','3','5'):
#            #    if current_date.strftime("%H") == '11' and current_date.strftime("%M") == '00' and EngagementOn == False:
#            n = client.get_channel(762922000888627211)
#            await n.send('test')

#            time.sleep(self.interval)

#PRINT LIST OF MEMBERS AND THE MEMBER COUNT
def memberListPrint(guild):
    members = '\n - '.join([member.name for member in guild.members])
    counter = 0
    for member in guild.members:
        nickName = member.nick;
        if member.roles != 'Bot':
            if type(nickName) is str:
                print(' - ' + str(nickName))
            else:
                print(' - ' + member.name)
            counter = counter + 1
    #print(f'Guild Members:\n - {members}')
    print(f'Count: {counter}')

##PRINT INSIGHTS FOR MEMBER
#def memberInsightsPrint(message,authorRoles,argument,channel):
#    for r in authorRoles[1:]:
#        if 'Moderator' == r.name or 'Admin' == r.name:
#            permission = True
#    if permission == False:
#        return
#    member = discord.utils.get(message.guild.members, name=argument)
#    if type(member) == None.__class__:
#        member = discord.utils.get(message.guild.members, nick=argument)
#        if type(member) == None.__class__:
#            await channel.send('Username not found in Community. Try again.')
#            return
#        nickN = str(member.nick)
#    else:
#        nickN = str(member.name)

#    #header
#    await channel.send('--------------------------------')
#    await channel.send('**INSIGHTS FOR ' + nickN + '**')
#    await channel.send('--------------------------------')

#    #user enter date
#    response = '**' + 'Joined on: ' + '**' + str(member.joined_at)
#    await channel.send(response)

#    #users roles
#    response = '**' + 'Roles: ' + '**'
#    for r in member.roles[1:]:
#        response = response + '\n-' + r.name
#        if r.name == 'Beta-Tester' or r.name == 'Moderator' or r.name == 'Admin':
#            EngagementRound = True
#    await channel.send(response)

#    #users Engagement Rounds
#    if EngagementRound:
#        response = '**'+'Engagement Rounds: ' + '**' + 'True'
#    else:
#        response = '**'+'Engagement Rounds: ' + '**' + 'False'
#    await channel.send(response)

def duplicateChecker(entry, list):
    if entry.lower() in (x.lower() for x in list):
        return False
    else:
        return True

def modAdminPermissions(authorRoles):
    for r in authorRoles[1:]:
        if 'Moderator' == r.name or 'Admin' == r.name:
            return True
    return False

def swearListOpen(textFileName):
    file = open(textFileName, "r")
    for line in file:
        if line[-1:] == '\n':
            #print(line[:-1])
            swearListArray.append(line[:-1])
        else:
            swearListArray.append(line)
    file.close()
    #print(swearListArray)

def swearCheck(messageString):
    swearFlag = False
    length = len(messageString)
    for i in messageString.split()[:length]:
        if i.lower() in swearListArray:
            swearFlag = True
    return swearFlag

def swearUpdate(action,array,textFileName):
    file = open(textFileName, "w")
    file.write('')
    for i in range(0,len(array)-1):
        file.write(array[i] + '\n')
        #print(f'loop{array[i]}')
    file.write(array[len(array)-1])
    #print(f'outloop{array[len(array)-1]}')
    file.close()
    return True
    #if type == 'add':
    #    file = open(textFileName,'a+')
    #    print('d')
    #    file.write('\n' + string)
    #    file.close()
    #    return True

    #if type == 'remove':
    #    for line in file:
    #        if line[:-1] == string:
    #            file.write(line.replace(string +'\n', ''))
    #            return True




#-----------------------------------------------------------------------------------------------------------------------------------------------------------

async def timer():
    global EngagementList
    global EngagementOn
    global EngagementStartMsgId

    await client.wait_until_ready()
    engageChannel = client.get_channel(int(os.getenv('ENGAGEMENT_ROUNDS'))) #Replace with EngagementID
    #engageChannel = client.get_channel(762922000888627211) #Test Channel - #bot-spam
    msg_sent = False

    while True:
        current_date = datetime.datetime.now()

        # Reminder for EngagementRounds
        # beta 770508504163024928
        #if (current_date.strftime("%w") in ('2','4','5') and current_date.strftime("%H") == '23' and current_date.strftime("%M") == '55'):
        #    await engageChannel.send("Hey <@&770508504163024928>! This is a reminder that the next engagement round sign up is tomorrow from 11-11:59am! Please react to this comment if you're interested")

        if (current_date.strftime("%w") in ('0','2','4') and current_date.strftime("%H") == '19' and current_date.strftime("%M") == '00'):
            await engageChannel.send("Hey <@&770508504163024928>! This is a reminder that the next engagement round sign up is tomorrow from 11-11:59am! Please react to this message if you can make it!")

        if (current_date.strftime("%w") in ('2','4') and current_date.strftime("%H") == '12' and current_date.strftime("%M") == '00'):
            await engageChannel.send("Hey <@&770508504163024928>! This is a reminder that the engagement round sign up is today at 5-5:59pm! Please react to this message if you can make it!")


        if ((current_date.strftime("%w") in ('1','3','5') and current_date.strftime("%H") == '11' and current_date.strftime("%M") == '00') or (current_date.strftime("%w") in ('2','4') and current_date.strftime("%H") == '17' and current_date.strftime("%M") == '00')) and (EngagementOn == False):
        #if current_date.strftime("%M") == '04':
            EngagementList = ['@streetsofvancity']
            if EngagementOn == True:
                await engageChannel.send('Engagement Rounds have already been started!')
                continue
            startString = '-------------------------------------------------------------------------------------\nTHIS IS THE START OF SIGNUPS FOR TODAYS ENGAGEMENT ROUNDS'
            await engageChannel.send(startString)
            EngagementOn = True
            EngagementStartMsgId = engageChannel.last_message_id


        if ((current_date.strftime("%w") in ('1','3','5') and current_date.strftime("%H") == '12' and current_date.strftime("%M") == '05') or (current_date.strftime("%w") in ('2','4') and current_date.strftime("%H") == '18' and current_date.strftime("%M") == '01')) and (EngagementOn == True):
            if EngagementOn == False:
                await engageChannel.send('$EngagementRoundStart hasnt been started yet!')
                continue
            endString = 'THIS IS THE END OF SIGNUPS FOR TODAYS ENGAGEMENT ROUNDS\n-------------------------------------------------------------------------------------'
            likeString = 'Remember to save, share, comment and like!'
            await engageChannel.send(endString)
            await engageChannel.send(likeString)

            async for messages in engageChannel.history(limit=200):
                #print('hello there', messages.content)
                #print(messages.content[0])
                #print(len(messages.mentions))
                if messages.id == EngagementStartMsgId:
                    break
                else:
                    if EngagementOn == True and (messages.content[0] == '@' or len(messages.mentions) >=1):
                        if len(messages.mentions) >= 1:
                            #print('hi')
                            print(messages.mentions[0].nick)
                            tagged = messages.mentions[0].nick
                            if type(tagged) == None.__class__:
                                tagged = messages.mentions[0].name
                            if duplicateChecker('@'+tagged,EngagementList):
                                EngagementList.append('@'+tagged)
                        else:
                            if duplicateChecker(messages.content.split(' ')[0],EngagementList):
                                EngagementList.append(messages.content.split(' ')[0])

            EngagementString = '```'
            for x in EngagementList:
                EngagementString = EngagementString + x + '\n'
            EngagementString = EngagementString + '```'
            await engageChannel.send(EngagementString)
            EngagementOn = False

        await asyncio.sleep(60)
        current_date = datetime.datetime.now()
        #print(f'{current_date}')
        #print((current_date.strftime("%w") in ('1','3','5') and current_date.strftime("%H") == '12' and current_date.strftime("%M") == '50') or (current_date.strftime("%w") in ('2','4') and current_date.strftime("%H") == '17' and current_date.strftime("%M") == '55') and (EngagementOn == True))

#EVENT LISTENTER
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

####CONFIRMATION OF CONNECTION
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    swearListOpen("swearList.txt")

####BEGIN MULTITHREAD FOR TIMER
#ti = multiThread()

#####GUILD MEMBER LIST PRINT
    #memberListPrint(guild)


@client.event
async def on_message(message):
    global EngagementOn
    global EngagementList
    global EngagementStartMsgId
    global startDay
    global startTime
    global unixStartTime
    global SwearBroadcast

    nickN = ''
    N = 2
    authorMessage = message.author
    authorRoles = authorMessage.roles
    permission = False
    if authorMessage == client.user:
        return
    focus = message.content
    length = len(message.content)
    command = focus.split(' ')[0]
    argument = ''
    firstNameFlag = True
    EngagementRound = False
    #print(argument)

    for i in focus.split(' ')[1:length]:
        if firstNameFlag == False:
            argument = argument + ' '
        argument = argument + i
        firstNameFlag = False
    channel = message.channel

####UPDATING SWEAR LIST - "$swearAdd *swear*"
    if command in ('$swearAdd', '$swearadd'):
        confirmString = f'Operation failed!'
        if modAdminPermissions(authorRoles) == False:
            await channel.send('You do not have the right permissions for this command!')
            return
        swear = focus.split(' ')[1]
        if swear in swearListArray:
            await channel.send('Item already exists in the list')
            return
        swearListArray.append(swear)
        if swearUpdate('add',swearListArray,'swearList.txt'):
            confirmString = f'{swear} has been added to the list'
        await channel.send(confirmString)

####UPDATING SWEAR LIST - "$swearRemove *swear*"
    if command in ('$swearRemove', '$swearremove'):
        confirmString = f'Operation failed!'
        if modAdminPermissions(authorRoles) == False:
            await channel.send('You do not have the right permissions for this command!')
            return
        swear = focus.split(' ')[1]
        if swear not in swearListArray:
            await channel.send('Item cannot be found')
            return
        swearListArray.remove(swear)
        if swearUpdate('remove',swearListArray,'swearList.txt'):
            confirmString = f'{swear} has been removed from the list'
        else:
            confirmString = f'{swear} is not on the list'
        await channel.send(confirmString)

####SWEAR LIST PRINT - "$swearPrint
    if command in ('$swearPrint', '$swearprint'):
        if modAdminPermissions(authorRoles) == False:
            await channel.send('You do not have the right permissions for this command!')
            return
        #print(swearListArray)
        await channel.send(swearListArray)
        await channel.send("Total characters: " + str(len(str(swearListArray))))


####SWEAR BROADCAST TOGGLE
    if command in ('$swearbroadcasttoggle', '$swearBroadcastToggle'):
        #print('testdsf')
        if modAdminPermissions(authorRoles) == False:
            await channel.send('You do not have the right permissions for this command!')
            return
        if SwearBroadcast == True:
            await channel.send('Public Channel Swear Broadcasting has been turned off')
            SwearBroadcast = False
            return
        if SwearBroadcast == False:
            await channel.send('Public Channel Swear Broadcasting has been turned on')
            SwearBroadcast = True
            return


####SWEAR DETECTION
    if swearCheck(message.content) and command not in ('$swearRemove', '$swearremove') and command not in ('$swearAdd', '$swearadd'):
        alertChannel = client.get_channel(802814736630284329)
        alertString = f'**-SWEARING DETECTED-**\n Channel: {channel.mention}\n User: {authorMessage.mention}\n Content: {message.content}'
        await alertChannel.send(alertString)

        if SwearBroadcast == True:
            await channel.send(f'Hey {authorMessage.mention}, this is just a reminder of the rules regarding keeping the language clean in our community. Please remove or edit your message, otherwise it will need to be deleted. Thank you in advance! :)')

####INSIGHTS FOR A SPECIFIC USER - "$insights *username/nickname*"
    if command in ('$Insights','$insights'):
        if modAdminPermissions(authorRoles) == False:
            await channel.send('You do not have the right permissions for this command!')
            return
        member = discord.utils.get(message.guild.members, name=argument)
        if type(member) == None.__class__:
            member = discord.utils.get(message.guild.members, nick=argument)
            if type(member) == None.__class__:
                await channel.send('Username not found in Community. Try again.')
                return
            nickN = str(member.nick)
        else:
            nickN = str(member.name)

        #header
        await channel.send('--------------------------------')
        await channel.send('**INSIGHTS FOR ' + nickN + '**')
        await channel.send('--------------------------------')

        #user enter date
        response = '**' + 'Joined on: ' + '**' + str(member.joined_at)
        await channel.send(response)

        #users roles
        response = '**' + 'Roles: ' + '**'
        for r in member.roles[1:]:
            response = response + '\n-' + r.name
            if r.name == 'Beta-Tester' or r.name == 'Moderator' or r.name == 'Admin':
                EngagementRound = True
        await channel.send(response)

        #users Engagement Rounds
        if EngagementRound:
            response = '**'+'Engagement Rounds: ' + '**' + 'True'
        else:
            response = '**'+'Engagement Rounds: ' + '**' + 'False'
        await channel.send(response)

####ENGAGEMENT ROUNDS STARTING PERIOD
    if command in ('$EngagementRoundStart','$engagementroundstart'):
        EngagementList = ['@streetsofvancity']
        if modAdminPermissions(authorRoles) == False:
            await channel.send('You do not have the right permissions for this command!')
            return
        if EngagementOn == True:
            await channel.send('Engagement Rounds have already been started!')
            return
        startString = '-------------------------------------------------------------------------------------\nTHIS IS THE START OF SIGNUPS FOR TODAYS ENGAGEMENT ROUNDS'
        await channel.send(startString)
        EngagementOn = True
        EngagementStartMsgId = channel.last_message_id

####ENGAGEMENT ROUNDS ENDING PERIOD
    if command in ('$EngagementRoundEnd','$engagementroundend'):
        if modAdminPermissions(authorRoles) == False:
            await channel.send('You do not have the right permissions for this command!')
            return
        if EngagementOn == False:
            await channel.send('$EngagementRoundStart hasnt been started yet!')
            return
        endString = 'THIS IS THE END OF SIGNUPS FOR TODAYS ENGAGEMENT ROUNDS\n-------------------------------------------------------------------------------------'
        likeString = 'Remember to save, share, comment and like!'
        await channel.send(endString)
        await channel.send(likeString)

        async for messages in channel.history(limit=200):
            #print('hello there', messages.content)
            #print(messages.content[0])
            #print(len(messages.mentions))
            if messages.id == EngagementStartMsgId:
                break
            else:
                if EngagementOn == True and (messages.content[0] == '@' or len(messages.mentions) >=1):
                    if len(messages.mentions) >= 1:
                        #print('hi')
                        print(messages.mentions[0].nick)
                        tagged = messages.mentions[0].nick
                        if type(tagged) == None.__class__:
                            tagged = messages.mentions[0].name
                        if duplicateChecker('@'+tagged,EngagementList):
                            EngagementList.append('@'+tagged)
                    else:
                        if duplicateChecker(messages.content.split(' ')[0],EngagementList):
                            EngagementList.append(messages.content.split(' ')[0])

        EngagementString = '```'
        for x in EngagementList:
            EngagementString = EngagementString + x + '\n'
        EngagementString = EngagementString + '```'
        await channel.send(EngagementString)

        EngagementOn = False

####STRING DETECT - "$Respect"
    if command in ('$Respect','$respect'):
        await channel.send("<:CheemsHeart:773627934103175169> <:CheemsHeart:773627934103175169> Much Respect Very Wow! <:CheemsHeart:773627934103175169> <:CheemsHeart:773627934103175169>")

####STRING DETECT - "$Encourage *username/nickname*"
    if command in ('$Encourage','$encourage'):
        tagged = message.mentions[0].nick
        if type(tagged) == None.__class__:
            tagged = message.mentions[0].name
        await channel.send("<:CheemsHeart:773627934103175169> You got this " + tagged + "!!")

####STRING DETECT - "$Remy"
    if command in ('$Remy','$remy'):
        await channel.send("<:Remy:786815407444066324> Sq*oui*k Sq*oui*k <:Remy:786815407444066324>")

####STRING DETECT - "$Poggers"
    if command in ('$Poggers','$poggers'):
        await channel.send("<:pogcat:795256957874733087> ^ Now THIS is pogracing ^ <:pogcat:795256957874733087>")

####STRING DETECT - "$jwklee"
    if command in ('$jwklee','$Jwklee') and message.author.id == 233108654839037952:
        await channel.send("uwu <:CheemsHeart:773627934103175169> I'm jewwy bewwy <:pogcat:795256957874733087>")

####STRING DETECT - "ShutoffBot"
    #if command in ('$Uptime','$uptime'):
    #    if modAdminPermissions(authorRoles) == False:
    #        await channel.send('You do not have the right permissions for this command!')
    #        return
    #    else:
    #        unixCurrentTime = time.time()
    #        await channel.send("Bot initialized at " + startTime + " on " + startDay + ".")
    #        await channel.send(unixStartTime)
    #        await channel.send(unixCurrentTime)

####STRING DETECT - "ShutoffBot"
    if command in ('$ShutoffBot','$shutoffbot'):
        if modAdminPermissions(authorRoles) == False:
            await channel.send('You do not have the right permissions for this command!')
            return
        else:
            await channel.send('Shutting down... Have a good day :)')
            await client.logout()

####STRING DETECT - "RestartBot"
    if command in ('$RestartBot','$restartbot'):
        if modAdminPermissions(authorRoles) == False:
            await channel.send('You do not have the right permissions for this command!')
            return
        elif platform.system() == 'Linux':
            await channel.send('Restarting...')
            await os.system('sudo reboot')
        else:
            await channel.send('That command is not available. Please use $ShutoffBot instead.')

####PRINT FROM BOT - "$BotPrint"
    if command in ('$BotPrint','$botprint'):
        if modAdminPermissions(authorRoles) == False:
            await channel.send('You do not have the right permissions for this command!')
            return
        botMessage = ''
        channel_raw = focus.split(' ')[1]
        print(channel_raw[2:-1])
        channel_argument = client.get_channel(int(channel_raw[2:-1]))
        for i in focus.split(' ')[2:]:
            botMessage = botMessage + i + ' '
        await channel_argument.send(botMessage)

client.loop.create_task(timer())
client.run(TOKEN)
