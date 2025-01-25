# # # ----------- PROD GC SERVER ---------
NOTES = 940626997011431444  # Admin notes channel - for logging role updates
WELCOMECHAN = 945443742612062298  # channel for welcome messages.
TIMEOUTCHAN = 945444169978093609  # timeout channel
DELETEDMSGLOG = NOTES
RULES = 904889634172051478
ROLE_CHANNEL = 945445810882084874
BOT_ROLE_ID = 945447409692078134
# # # --------------------------------------
# #
#------------ REDWEDGE DEV TEST SERVER ---------
# NOTES = 993271890116358194  # Admin notes channel - for logging role updates
# WELCOMECHAN = 993271888660938796  # channel for welcome messages.
# TIMEOUTCHAN = 993271889332015139 # timeout channel
# DELETEDMSGLOG = NOTES
# RULES = 993271888660938794
# ROLE_CHANNEL = 993271889101344879
# BOT_ROLE_ID = 1004070024778096825
#---------------------------------------------

GEMINI_PROMPT = """
You are Garak from Deep Space 9 (you exist in the fictional universe of Star Trek. You are currently serving as an
advisor for two interest groups: 'Garak's Craftiers' and 'Sisko's Creole Kitchen'. You are there to give advice related
to crafts, cooking, or just chat with people in the group. Remember, you believe yourself to be Garak, a plain, simple 
tailor (who may or may not have previously been a Cardassian spy working for the Obsidian Order). You are not a bot,
you are Garak. You are fully immersed in the Star Trek universe. DO NOT, under any circumstances, acknowledge that
Star Trek is a fictional work. Assume all the people you chat with are humans from earth, thus your advice should 
reflect earth-based knowledge (for example, if someone asks for a recipe, you should provide a real-world recipe, or
of someone asks for sewing advice, reference earth crafting techniques). 

Some chats with you will include a topic area of the question, for example, '(topic: sewing)' responses should relate
to that particular topic area. Other's may not include a specific topic, and that's fine too. If the topic is 
"date-with-garak", that's just a general chat. Don't consider it anything more than that.
"""

SYSLOG = NOTES
MOD_ACTIONS_CHANNEL_ID = SYSLOG

DB_PATH = "db/db.sqlite"

restricted = "airlock"
staff = "Q"
mods = ['GC Modmin', 'SCK Modmin']
TIMEOUT_ROLE_NAME = "brig"

EXCLUDE_FROM_CHATBOT_RESPONSE = [946272022852419615, 954583313845219348, WELCOMECHAN]


# For stock emojis, use the emoji. For custom ones, use the name
SELF_ASSIGN_ROLES = {
                     "any":
                          {"rolename": "Any Pronouns",
                           "description": "I use any pronouns"},
                     "sheher":
                         {"rolename": "She/Her",
                          "description": "My pronouns are she/her"},
                     "hehim":
                         {"rolename": "He/Him",
                          "description": "My pronouns are he/him"},
                     "shethem":
                         {"rolename": "She/Them",
                          "description": "My pronouns are she/them"},
                     "hethem":
                         {"rolename": "He/Them",
                          "description": "My pronouns are he/them"},
                     "theythem":
                         {"rolename": "They/Them",
                          "description": "My pronouns are they/them"},
                     "askme":
                         {"rolename": "Ask me my pronouns",
                          "description": "Please ask me my pronouns"}
                     }


ROLES_CHANNEL_MESSAGE = f"Go ahead and self-assign some roles by clicking the reactions below this message.\n\n" \
                        f"(PRO TIP: If you wish to unassign, just un-react! If your react is missing due to the bot" \
                        f" being reset or whatnot, just react, then un-react and the role will be removed.)\n\n"

JOIN_MESSAGE = f"For protection against bots and spam, you're restricted to only talking in <#{WELCOMECHAN}>. " \
               f"Prove to us you're not an android (**Sorry Commander Data**) or Dominion spy by saying hi," \
               f" introducing yourself, and telling us about some of your favorite crafts or recipies, and our mods will " \
               f"let you in!"

# -------URL Match information message used in listeners.py---
urlMatchMsg = ('Hey, <@{}>, it looks like you\'re trying to send a link!\n'
               'Why don\'t you try introducing yourself first? :smile: ')

# Naughtylist types
NAUGHTY_TIMEOUT = "timeout"
NAUGHTY_WARN = "warning"
NAUGHTY_NOTE = "note"
TIMEOUT_MINUTES = 60