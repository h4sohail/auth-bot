import json, argparse
import discord
from discord.ext import commands
from discord.utils import get
from utility import message_check, make_sequence, send_email, generate_hash

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--email_pass", help="The password of the email account", required=True)
parser.add_argument("-t", "--token", help="The discord application token", required=True)
args = vars(parser.parse_args())

email_password = args["email_pass"]
token = args["token"]

keys = set() # set of keys generated
log = {} # log file for keeping track of discord IDs and related emails
authorized = set() # set of authorized users

client = commands.Bot(command_prefix="!")

with open('students.json') as json_file:
    students = json.load(json_file) 
    print("Loaded Students") 

@client.event
async def on_member_join(member):
    print(f"Trying to authenticate {member.name}")
    await member.send("Please enter your Student ID to get authorized")
    response = await client.wait_for("message", check=message_check(channel=member.dm_channel))
    student_id = response.content.strip().replace(" ", "")
    
    if not student_id.isnumeric():
        await member.send("Incorrect Student ID")
        print(f"Failed to authenticate {member.name}")
        await member.kick()
        return

    if student_id not in students:
        await member.send("You are not enrolled in this class")
        print(f"Failed to authenticate {member.name}")
        await member.kick()
        return

    if member.id in authorized:
        await member.send("You are already authorized")
        print(f"{member.name} is already authenticated")
        return

    key = generate_hash()
    
    if key not in keys:
        keys.add(key)

    send_email("discord.auth.bot@gmail.com", email_password, students[student_id]["Email"], "Discord Auth Key", f"{key}")
    await member.send("Please check your Carleton email for a key, and enter it")
    response = await client.wait_for("message", check=message_check(channel=member.dm_channel))
    hashed_id = response.content.strip().replace(" ", "")

    if hashed_id in keys:
        role = get(member.guild.roles, name="Student")
        await member.add_roles(role)
        first_name = students[student_id]["First Name"]
        await member.edit(nick=first_name)
        print(f"Successfully to authenticated {member.name}")
        
        # Book keeping
        authorized.add(member.id)
        log[member.id] = students[student_id]["Email"]
        keys.discard(hashed_id)
        with open("log.json", "w") as outfile:
            json.dump(log, outfile)
    else:
        await member.send("The key is incorrect")
        await member.kick()
        print(f"Failed to authenticate {member.name}")
        return

@client.event
async def on_member_remove(member):
    print(f"{member.name} left, removed from authenticated users") 
    authorized.discard(member.id)

client.run(token)
