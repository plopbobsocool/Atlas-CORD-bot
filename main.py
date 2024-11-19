import discord
from discord.ext import commands
import pandas as pd
import re

# Set up intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Ensure this is enabled

# Create bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# Keeps a list of authorized users
authorized_users = []

# Maps log (your data here)
maps_data = [
    ("6/14/24", "https://rustmaps.com/map/f12b5f7fa61e496f80ebf0fe18d60465?embed=img_i_l"),
    ("6/17/24", "https://rustmaps.com/map/b1f1f8de928f4b0ab5c7b0130c27de72?embed=img_i_l"),
    ("6/21/24", "https://rustmaps.com/map/bb2bbb82370d4e9da9a62159a02804c1?embed=img_i_l"),
    ("6/21/24", "https://rustmaps.com/map/6f114b8d0a6e495d82978947f6b9be9e?embed=img_i_l"),
    ("6/28/24", "https://rustmaps.com/map/a0c50ae026fb432099f962d496365840?embed=img_i_l"),
    ("7/1/24", "https://rustmaps.com/map/c35bd99f64284d7bb00395baf8424b65?embed=img_i_l"),
    ("7/5/24", "https://rustmaps.com/map/ed53046021cf445389e5c586df35769d?embed=img_i_l"),
    ("7/8/24", "https://rustmaps.com/map/ed32703b143545c88254ea4d0dafcec4?embed=img_i_l"),
    ("7/12/24", "https://rustmaps.com/map/e1767235a7db4d789abba343e3529dee?embed=img_i_l"),
    ("7/15/24", "https://rustmaps.com/map/af3cd61067b94a3aaf54cc44211b5476?embed=img_i_l"),
    ("7/18/24", "https://rustmaps.com/map/0b0a74ed1f104b96819c55433896814c?embed=img_i_l"),
    ("7/22/24", "https://rustmaps.com/map/392cf0365d5f4208a4f5415971996ee0?embed=img_i_l"),
    ("7/26/24", "https://rustmaps.com/map/41417037a6c849a19dc0d7d8f49ff36e?embed=img_i_l"),
    ("7/29/24", "https://rustmaps.com/map/0a89a461d0c94b6bb892f780e7540c7c?embed=img_i_l"),
    ("8/2/24", "https://rustmaps.com/map/51668b2aaf474494b919fa145d56dfe4?embed=img_i_l"),
    ("8/5/24", "https://rustmaps.com/map/57714d6c1766498885ce7a1f9a278b1e?embed=img_i_l"),
    ("8/9/24", "https://rustmaps.com/map/822a62969f1945e3b49be0ce7c322106?embed=img_i_l"),
    ("8/12/24", "https://rustmaps.com/map/6ff036f67d934ece9b9cd97e45bb514a?embed=img_i_l"),
    ("8/16/24", "https://rustmaps.com/map/d0919155b16d4a50996b32ca8c73c602?embed=img_i_l"),
    ("8/19/24", "https://rustmaps.com/map/239c147cbbc844bdacbbdb21a542b3de?embed=img_i_l"),
    ("8/23/24", "https://rustmaps.com/map/dc02f4c848634b9fb6145e9ce3d529ec?embed=img_i_l"),
    ("8/26/24", "https://rustmaps.com/map/27c85775ca6648ce81e2872e8cf16542?embed=img_i_l"),
    ("8/26/24", "https://rustmaps.com/map/b4b7244ccf364871b259e5fa9e888f15?embed=img_i_l"),
    ("9/2/24", "https://rustmaps.com/map/8aa75e3fbefa48208e8bd3eac86bc0bb?embed=img_i_l"),
    ("9/6/24", "https://rustmaps.com/map/d46d4e55d3644ce0a663699d150e1ea8?embed=img_i_l"),
    ("9/9/24", "https://rustmaps.com/map/27efb3991980414196114d0aad4634a8?embed=img_i_l"),
    ("9/13/24", "https://rustmaps.com/map/e152db8ccf894e9dbdca26be595edbdf?embed=img_i_l"),
    ("9/16/24", "https://rustmaps.com/map/78464f8487f6409887f99cfea79b3cbf?embed=img_i_l"),
    ("9/20/24", "https://rustmaps.com/map/fcbe5e17a2a442b9a63de27f57a66256?embed=img_i_l"),
    ("9/23/24", "https://rustmaps.com/map/34ed5cdb49494616b6faba724c5e7420?embed=img_i_l"),
    ("9/27/24", "https://rustmaps.com/map/3127ac32251a49918ca96603871993ea?embed=img_i_l"),
    ("9/30/24", "https://rustmaps.com/map/98b96e1a953d44e7b52148537d330c37?embed=img_i_l"),
    ("10/4/24", "https://rustmaps.com/map/7dfa90907cce4c1a8f23353699f026a4?embed=img_i_l"),
    ("10/7/24", "https://rustmaps.com/map/af8a958668474d77b5aa6ba60dd4faca?embed=img_i_l"),
    ("10/11/24", "https://rustmaps.com/map/55da0f29031847ff882baf7b0d810017?embed=img_i_l"),
    ("10/14/24", "https://rustmaps.com/map/dcb283e410584773bca0a0ce1ace0f14?embed=img_i_l"),
    ("10/18/24", "https://rustmaps.com/map/fb6239edc9e74ea5b146d368b2f8e36c?embed=img_i_l"),
    ("10/21/24", "https://rustmaps.com/map/cb63342e95584c90a37aadf41e7c5b04?embed=img_i_l"),
    ("10/25/24", "https://rustmaps.com/map/0156e7562df74d95b31bb9a47abb9690?embed=img_i_l"),
    ("10/28/24", "https://rustmaps.com/map/80e50ea90b334bb785264a5c89e5b9f2?embed=img_i_l"),
    ("11/1/24", "https://rustmaps.com/map/31bc826569d94800a785bd028efdd6ef?embed=img_i_l"),
    ("11/4/24", "https://rustmaps.com/map/0cf45f66f9314c1caf1ad7f8485b01b3?embed=img_i_l"),
    ("11/8/24", "https://rustmaps.com/map/2236bede0f4346f18d3846e31fd15502?embed=img_i_l"),
    ("11/11/24", "https://rustmaps.com/map/250ffa0933b0493384834483e71c53b9?embed=img_i_l"),
    ("11/15/24", "https://rustmaps.com/map/dad98728e65b498a88bb17db76499d47?embed=img_i_l"),
    ("11/19/24", "https://rustmaps.com/map/f05f70a87e584093b12b9c1d56b3b12c?embed=img_i_l")
]


# Global variable to hold the log channel
log_channel = None
TARGET_GUILD_ID = 1299054694697533481  # Replace with your target guild ID

# Initialize a DataFrame to hold message logs
atlas_cords = pd.DataFrame(columns=["Timestamp", "Username", "User  ID", "User  Mention", "Message", "Matched Date", "Map URL"])

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Predicting Atlas Build Spots"))
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')

    global log_channel  # Declare it as global to modify it

    # Get the target guild by ID
    guild = bot.get_guild(TARGET_GUILD_ID)

    if guild is None:
        print("Bot is not connected to the specified guild.")
        return

    # Print out all text channels in the guild for debugging
    print("Current channels in the guild:")
    for channel in guild.text_channels:
        print(f"- {channel.name}")

    # Check if the "atlas-cord-logs" channel exists
    log_channel = discord.utils.get(guild.text_channels, name="atlas-cord-logs")

    # If the channel doesn't exist, create it
    if log_channel is None:
        try:
            log_channel = await guild.create_text_channel("atlas-cord-logs")
            await log_channel.send("Channel created for logging messages.")
            print("Channel 'atlas-cord-logs' created.")
        except discord.Forbidden:
            print("Failed to create channel: Insufficient permissions.")
        except discord.HTTPException as e:
            print(f"Failed to create channel: {e}")
    else:
        print("Channel 'atlas-cord-logs' already exists.")

@bot.event
async def on_message(message):
    global log_channel  # Declare log_channel as global
    global atlas_cords  # Declare atlas_cords as global to retain its state

    # Ignore messages from the bot itself
    if message.author.bot:
        return

    # Check if the message starts with the command prefix
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
        return

    # Store the original message content
    original_content = message.content
    cleaned_content = original_content.replace("<a:Arrow:1164337263568752660>", "")
    lines = cleaned_content.splitlines()

    if lines:
        found_cords = False  # Flag to check if coordinates or dates were found
        logged_dates = []  # List to store found dates for cross-referencing

        # Define a regex pattern for dates (MM/DD/YYYY or MM/DD/YY)
        date_pattern = r'\b(\d{1,2}/\d{1,2}/\d{2,4})\b'

        # Extract the date from the first line
        first_line = lines[0]
        print(f"First line content: '{first_line}'")  # Debugging statement

        first_line_date_match = re.search(date_pattern, first_line)
        if first_line_date_match:
            first_line_date = first_line_date_match.group(0)
            logged_dates.append(first_line_date)  # Store the first line date for cross-referencing

                        # Log the extracted date for debugging
            print(f"Extracted date from first line: '{first_line_date}'")  # Debugging statement

        # Process each line for coordinates and dates
        for line in lines:
            # Check for double slashes (indicating coordinates)
            if "//" in line:
                found_cords = True
                timestamp_str = message.created_at.strftime("%Y-%m-%d %H:%M:%S")
                log_message = f"[{timestamp_str}] Received line (coordinates): '{line}'"
                print(log_message)

                if log_channel:
                    await log_channel.send(log_message)

                new_entry = pd.DataFrame({
                    "Timestamp": [timestamp_str],
                    "Username": [str(message.author)],
                    "User   ID": [message.author.id],
                    "User   Mention": [f"<@{message.author.id}>"],  # Add a mention format
                    "Message": [line],
                    "Matched Date": [None],
                    "Map URL": [None]
                })

                # Append the new entry to the DataFrame
                atlas_cords = pd.concat([atlas_cords, new_entry], ignore_index=True)

            # Check for dates in the line
            date_found = None  # Reset date_found for each line
            if re.search(date_pattern, line):
                found_cords = True
                date_found = re.search(date_pattern, line).group(0)  # Get the matched date
                logged_dates.append(date_found)  # Store the date for cross-referencing
                timestamp_str = message.created_at.strftime("%Y-%m-%d %H:%M:%S")
                log_message = f"[{timestamp_str}] Date found in line: '{line}'"
                print(log_message)

                if log_channel:
                    await log_channel.send(log_message)

                # Check if the found date exists in maps_data
                for date, url in maps_data:
                    if date_found == date:
                        match_message = f"Matched date '{date_found}' with URL: {url}"
                        if log_channel:
                            await log_channel.send(match_message)
                        print(match_message)  # Print for debugging

                        new_entry = pd.DataFrame({
                            "Timestamp": [timestamp_str],
                            "Username": [str(message.author)],
                            "User   ID": [message.author.id],  # Keep this as the raw ID if you need it
                            "User   Mention": [f"<@{message.author.id}>"],  # Add a mention format
                            "Message": [line],
                            "Matched Date": [date_found],
                            "Map URL": [url]
                        })

                        # Append the new entry to the DataFrame
                        atlas_cords = pd.concat([atlas_cords, new_entry], ignore_index=True)

        # Save the DataFrame to an Excel file only if we found coordinates or dates
        if found_cords:
            atlas_cords.to_excel("atlas_cords.xlsx", index=False)

        # Cross-reference dates with maps_data
        if logged_dates:
            matched_dates = set(logged_dates)
            for date in matched_dates:
                for ref_date, url in maps_data:
                    if date == ref_date:
                        match_message = f"Cross-referenced date '{date}' with URL: {url}"
                        if log_channel:
                            await log_channel.send(match_message)
                        print(match_message)  # Print for debugging

    # Ensure that the bot continues to process other commands or messages
    await bot.process_commands(message)

# Example command: !ping
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# Example command: !echo
@bot.command()
async def echo(ctx, *, content: str):
    await ctx.send(content)

# Command to purge the logs
@bot.command()
@commands.has_permissions(manage_messages=True)  # Ensure the user has permission to manage messages
async def purge_logs(ctx):
    global log_channel

    if log_channel is None:
        await ctx.send("Log channel does not exist.")
        return

    # Fetch and delete messages in the log channel
    deleted = await log_channel.purge()
    await ctx.send(f"Purged {len(deleted)} messages from the log channel.")

@bot.command()
@commands.has_permissions(administrator=True)  # Only allow administrators to use this command
async def authorize(ctx, user_id: int):
    """Authorize a user to use the bot."""
    if user_id not in authorized_users:
        authorized_users.append(user_id)
        await ctx.send(f"User  with ID {user_id} is already authorized.")

# Error handling for commands
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use this command.")
    else:
        await ctx.send("An error occurred.")
        print(f"Error: {error}")  # Log the error for debugging

# Running the bot
TOKEN = ("MTMwODIwMDY4MTQ2Njc1NzEyMA.GB5X79.jKRSO6Zl_iYdPyTxAciAXM6JrnR6Cg5uWNLgVQ")
bot.run(TOKEN)
