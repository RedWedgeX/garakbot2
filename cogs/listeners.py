import asyncio
import random
import re

import nextcord as discord
from nextcord.ext import commands
from utils.config import *
from nextcord.ext.commands.errors import CommandNotFound
from datetime import datetime as dt
from pytz import timezone
from utils.helpers import catpic
import google.generativeai as genai
import os
import time
import aiosqlite
import traceback

# -------URL Match anti-spam prevention --
urlMatchedUsers = []  # stores by snowflake ID
# -------URL Regex pattern syntax---------
urlRegex = r"(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+" \
           r"([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$"

urlPattern = re.compile(urlRegex, flags=re.MULTILINE | re.IGNORECASE |
                                        re.DOTALL)


class Listeners(commands.Cog, name="Bot Responders & Listeners"):
    def __init__(self, client):
        self.bot = client

    async def send_url_match_msg(self, userid: discord.user.User.id, channel: discord.TextChannel):
        """
        Prevents message spamming from bots by limiting response message to only
        send up to once every 10 seconds per user.
        :param userid: snowflake ID of the user to respond to / ping
        :param channel: channel to send the response message in
        :return: void
        """
        if userid in urlMatchedUsers:
            return
        else:
            urlMatchedUsers.append(userid)
            await channel.send(urlMatchMsg.format(userid))
            await asyncio.sleep(10.0)

    # LOG DEPARTS
    @commands.Cog.listener()
    async def on_member_remove(self, user):
        syslog = self.bot.get_channel(SYSLOG)
        await syslog.send(f"<@{user.id}> `(<@{user.id}> {user.display_name})` has left the server.")

    # NEW USER PROCESSING
    @commands.Cog.listener()
    async def on_member_join(self, member):

        # CHECK FOR APRIL FOOLS
        pdt_zone = timezone("America/Los_Angeles")
        april_first = dt.strptime("4/1/2022", "%m/%d/%Y")
        pst_now = dt.now(pdt_zone)
        if april_first.date() == pst_now.date():
            await member.edit(nick="Q")

        onjoinmsg = JOIN_MESSAGE

        channel = self.bot.get_channel(WELCOMECHAN)
        role = discord.utils.get(member.guild.roles, name=restricted)
        await member.add_roles(role)
        syslog = self.bot.get_channel(SYSLOG)
        await syslog.send(f"{member.mention} joined the server.")
        await channel.send(f"Peldor joi, and welcome :wave: to  the Garak’s Craftiers & Sisko's Creole Kitchen Discord, {member.mention}!  {onjoinmsg}")
        await member.send(f"Peldor joi, and welcome :wave: to  the Garak’s Craftiers  & Sisko's Creole Kitchen Discord, {member.mention}!  {onjoinmsg}")

    async def chatbot(self, topic, message):
        provider = "openai"
        # if not self.bot.cgpt_enabled:
        if not 1==1:
            await message.channel.send(f"Sorry {message.author.mention}, my advanced "
                                       f"AI has been disabled, probably because I was caught "
                                       f"trying to take over the ship. Please try again later!\n"
                                       f" https://tenor.com/bJlBU.gif")
            return


        syslog = self.bot.get_channel(SYSLOG)


        if provider == "openai":
            print("CALLING THE CHATBOT!!")
            try:
                async with message.channel.typing():
                    query = message.content
                    # SUGGESTED BY CHATGPT to replace usernames in messages with the discord nickname -----
                    if '<@' in query:
                        # Loop through each user ID in the message
                        try:
                            for user_id in query.split():
                                if '<@&' not in user_id and '<@' in user_id:
                                    if str(user_id) == str(self.bot.user.id):
                                        query = query.replace(f'<@{user_id}>', "Garak")
                                    else:

                                        # Remove the '<@' and '>' characters from the user ID
                                        user_id = user_id.strip('<@!>')

                                        member = await message.guild.fetch_member(user_id)
                                        # Replace the user ID with their nickname in the message

                                        if str(user_id) != str(self.bot.user.id):
                                            query = query.replace(f'<@{user_id}>', member.display_name)
                        except Exception as e:
                            await syslog.send(f"**BOT ERROR**\n```{e}```")
                    # ---------
                    response = await self.gemini(message, message.author, f"{topic} - {query}")
                    # Check if the message is longer than 2000 characters
                    if len(response) > 1950:
                        # Split the message into chunks of 2000 characters or less
                        chunks = [response[i:i + 1950] for i in range(0, len(response), 1950)]

                        # Send each chunk as a separate message
                        for chunk in chunks:
                            if chunks.index(chunk) == 0:
                                await message.channel.send(f"{chunk}")
                            else:
                                await message.channel.send(f"{chunk}")
                    else:
                        await message.channel.send(f"{response}")


            except CommandNotFound as er:
                pass
            except Exception as e:
                await message.channel.send(f"{message.author.mention} https://tenor.com/bJlBU.gif")
                raise e

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author == self.bot.user:
            return

        if message.channel.id == WELCOMECHAN:
            lobby_role = discord.utils.get(message.guild.roles, name=restricted)
            if lobby_role in message.author.roles:
                await message.add_reaction("🖖")

        #if message.content.startswith(f"<@{self.bot.user.id}") or message.content.startswith(f"<@&{BOT_ROLE_ID}"):
        if self.bot.user.mentioned_in(message) and message.channel.id not in EXCLUDE_FROM_CHATBOT_RESPONSE:
            # await Listeners.chatbot(self, f"(topic: {message.channel.name}) {message}")
            await Listeners.chatbot(self, f"(topic: {message.channel.name}", message)

        if message.channel.id not in EXCLUDE_FROM_CHATBOT_RESPONSE:
            if "even the" in ' '.join(message.content).lower():
                m = ' '.join(message.content).lower()
                m = m.split("even the ", 1)[1]
                m = re.sub(r'[^\w\s]', '', m)
                await message.channel.send(f"{message.author.mention} - ESPECIALLY the {m}!")

            if "funny" in message.content.lower().split() and random.randint(1, 10) == 1:
                await message.channel.send(f"{message.author.mention} asked for a random CatPic™: \n"
                                           f"\n{catpic()}")

            if message.content.startswith(f"<@{self.bot.user.id}") or message.content.startswith(f"<@&{BOT_ROLE_ID}"):
                await Listeners.chatbot(self, message)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        reacting_user = payload.member
        message = await channel.fetch_message(payload.message_id)
        admin_role = discord.utils.get(channel.guild.roles, name=staff)
        mod_roles = [discord.utils.get(channel.guild.roles, name=role) for role in mods]
        new_member_role = discord.utils.get(reacting_user.guild.roles, name=restricted)

        # handle mods using  reacts to welcome people
        if payload.channel_id == WELCOMECHAN and \
                (admin_role in reacting_user.roles or any(role in reacting_user.roles for role in mod_roles)) and \
                new_member_role in message.author.roles:
            new_member = message.author

            wchan = self.bot.get_channel(WELCOMECHAN)

            await new_member.remove_roles(new_member_role)
            syslog = self.bot.get_channel(SYSLOG)

            await syslog.send(f"{new_member.mention} welcomed to the server by `{reacting_user.display_name}`")
            message = ("Thanks for introducing yourself. You now have full member access to our "
                       f"channels. Stop by <#{ROLE_CHANNEL}> and self-assign yourself some stuff!")
            await wchan.send(f"{new_member.mention}, {message}")

        # handle self-assign role add
        role_message = await channel.fetch_message(channel.last_message_id)

        if channel.id == ROLE_CHANNEL and message == role_message:
            if hasattr(payload.emoji, "name"):
                react = payload.emoji.name
            else:
                react = payload.emoji
            role = discord.utils.get(reacting_user.guild.roles, name=SELF_ASSIGN_ROLES[react]['rolename'])
            await reacting_user.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # Handle self-removing of roles
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        role_message = await channel.fetch_message(channel.last_message_id)

        if channel.id == ROLE_CHANNEL and message == role_message:
            user = discord.utils.get(channel.guild.members, id=payload.user_id)

            if hasattr(payload.emoji, "name"):
                react = payload.emoji.name
            else:
                react = payload.emoji
            role = discord.utils.get(message.guild.roles, name=SELF_ASSIGN_ROLES[react]['rolename'])
            await user.remove_roles(role)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """
        Log all deleted message
        :param message: Discord obj of the message itself
        :return: Nothing
        """
        if message.author == self.bot.user or not message.content or \
                message.content == "" or message.content[0] in ["!", "$", "?"]:
            return

        try:
            if not message.content.lstrip().startswith('!') and message.author != self.bot.user:
                channel = message.guild.get_channel(DELETEDMSGLOG)
                embed = discord.Embed(title="Message Deleted", color=0xf40000)
                embed.add_field(name="Sender", value=message.author, inline=True)
                embed.add_field(name="Channel", value=message.channel.mention, inline=True)
                embed.add_field(name="Message", value=message.content, inline=False)
                await channel.send(embed=embed)
        except commands.errors.CommandInvokeError as e:
            print(f"Invoke Error {e}")


    @commands.command(hidden=True)
    async def gemini(self, ctx, author, *prompt: str):
        if self.bot.cgpt_enabled:
            user_id = author.id
            prompt = ' '.join(prompt)
            system_instructions = GEMINI_PROMPT

            if author.nick:
                nickname = author.nick
            else:
                nickname = author.name

            history = await load_chat_history_for_user(user_id)

            genai.configure(api_key=os.getenv("GEMINI_API"))
            model = genai.GenerativeModel(
                model_name="gemini-1.5-pro",
                system_instruction=system_instructions + f" \n\n Info about the user you're chatting with:\n"
                                                         f" Their user name is {author.display_name}.\n"
                                                         f"You can @ mention them as {author.mention}.\n "
                                                         f"Your nickname is {self.bot.user.name}, "
                                                         f"and your user id is {self.bot.user.id}.",
            )
            chat = model.start_chat(history=history)

            info = (f"User info: \n{author.name}\n{author.mention}\n{author.nick}\n\n")

            await add_chat_history(user_id, "user", prompt)

            try:
                response = chat.send_message(prompt)
                await add_chat_history(user_id, "model", response.text)
                return response.text
            except Exception as e:
                return (f'```py\n{traceback.format_exc()}\n```')

async def add_chat_history(user_id, role, parts):
    async with aiosqlite.connect(DB_PATH) as db:
        timestamp = time.time()
        await db.execute("INSERT INTO chat_history (user_id, role, parts, timestamp) "
                         "VALUES (?, ?, ?, ?)", (user_id, role, parts, timestamp))
        await db.commit()

async def load_chat_history_for_user(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        rows = await db.execute_fetchall(
            "SELECT role, parts FROM chat_history WHERE user_id = ? ORDER BY timestamp", (int(user_id),))
        results_as_dicts = [{"role": entry[0], "parts": entry[1]} for entry in rows]
        return results_as_dicts

def setup(client):
    client.add_cog(Listeners(client))
