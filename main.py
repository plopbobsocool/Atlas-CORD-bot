import discord
from discord.ext import commands
import pandas as pd
import re
from datetime import datetime

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
    ("8/26/24", "https://rustmaps.com/map/27c85775ca6648ce81e2872e8cf16542?embed=img_i_l"),
    ("8/30/24", "https://rustmaps.com/map/b4b7244ccf364871b259e5fa9e888f15?embed=img_i_l"),
    ("9/02/24", "https://rustmaps.com/map/8aa75e3fbefa48208e8bd3eac86bc0bb?embed=img_i_l"),
    ("9/06/24", "https://rustmaps.com/map/d46d4e55d3644ce0a663699d150e1ea8?embed=img_i_l"),
    ("9/09/24", "https://rustmaps.com/map/27efb3991980414196114d0aad4634a8?embed=img_i_l"),
    ("9/13/24", "https://rustmaps.com/map/e152db8ccf894e9dbdca26be595edbdf?embed=img_i_l"),
    ("9/16/24", "https://rustmaps.com/map/78464f8487f6409887f99cfea79b3cbf?embed=img_i_l"),
    ("9/20/24", "https://rustmaps.com/map/fcbe5e17a2a442b9a63de27f57a66256?embed=img_i_l"),
    ("9/23/24", "https://rustmaps.com/map/34ed5cdb49494616b6faba724c5e7420?embed=img_i_l"),
    ("9/27/24", "https://rustmaps.com/map/3127ac32251a49918ca96603871993ea?embed=img_i_l"),
    ("9/30/24", "https://rustmaps.com/map/98b96e1a953d44e7b52148537d330c37?embed=img_i_l"),
    ("10/04/24", "https://rustmaps.com/map/7dfa90907cce4c1a8f23353699f026a4?embed=img_i_l"),
    ("10/07/24", "https://rustmaps.com/map/af8a958668474d77b5aa6ba60dd4faca?embed=img_i_l"),
    ("10/11/24", "https://rustmaps.com/map/55da0f29031847ff882baf7b0d810017?embed=img_i_l"),
    ("10/14/24", "https://rustmaps.com/map/dcb283e410584773bca0a0ce1ace0f14?embed=img_i_l"),
    ("10/18/24", "https://rustmaps.com/map/fb6239edc9e74ea5b146d368b2f8e36c?embed=img_i_l"),
    ("10/21/24", "https://rustmaps.com/map/cb63342e95584c90a37aadf41e7c5b04?embed=img_i_l"),
    ("10/25/24", "https://rustmaps.com/map/0156e7562df74d95b31bb9a47abb9690?embed=img_i_l"),
    ("10/28/24", "https://rustmaps.com/map/80e50ea90b334bb785264a5c89e5b9f2?embed=img_i_l"),
    ("11/01/24", "https://rustmaps.com/map/31bc826569d94800a785bd028efdd6ef?embed=img_i_l"),
    ("11/04/24", "https://rustmaps.com/map/0cf45f66f9314c1caf1ad7f8485b01b3?embed=img_i_l"),
    ("11/08/24", "https://rustmaps.com/map/2236bede0f4346f18d3846e31fd15502?embed=img_i_l"),
    ("11/11/24", "https://rustmaps.com/map/250ffa0933b0493384834483e71c53b9?embed=img_i_l"),
    ("11/15/24", "https://rustmaps.com/map/dad98728e65b498a88bb17db76499d47?embed=img_i_l"),
    ("11/19/24", "https://rustmaps.com/map/f05f70a87e584093b12b9c1d56b3b12c?embed=img_i_l"),
]

# Global variable to hold the log channel
log_channel = None
TARGET_GUILD_ID =   # Replace with your target guild ID

# Initialize a DataFrame to hold message logs
atlas_cords = pd.DataFrame(columns=["Timestamp", "Username", "User  ID", "User  Mention", "Message", "Matched Date", "Map URL"])

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

    # Initialize variables at the start of the method
    found_cords = False
    logged_dates = []  # List to store found dates for cross-referencing

    if lines:
        # Define a more flexible regex pattern for dates
        date_pattern = r'\b(\d{1,2}/\d{1,2}/\d{2,4})\b'

        # Try to find a date in the message
        message_date = None
        map_url = None

        # Check first line for date
        if lines:
            first_line = lines[0]
            print(f"First line: {first_line}")  # Detailed logging
            
            first_line_date_match = re.search(date_pattern, first_line)
            if first_line_date_match:
                # Normalize the date format
                original_date = first_line_date_match.group(0)
                try:
                    # Parse the full date and convert to short format
                    # Use custom parsing to handle different date formats
                    month, day, year = map(int, original_date.split('/'))
                    
                    # Ensure 2-digit year is interpreted correctly
                    if year > 100:
                        year = year % 100
                    
                    # Format the date consistently
                    message_date = f"{month:02d}/{day:02d}/{year:02d}"
                    print(f"Normalized date: {message_date}")  # Debugging
                except Exception as e:
                    print(f"Date parsing error: {e}")
                    message_date = original_date

                # Find the corresponding map URL
                for date, url in maps_data:
                    # Normalize both dates for comparison
                    try:
                        comp_month, comp_day, comp_year = map(int, date.split('/'))
                        comp_date = f"{comp_month:02d}/{comp_day:02d}/{comp_year:02d}"
                        
                        if comp_date.strip() == message_date.strip():
                            map_url = url
                            print(f"Matched map URL: {map_url}")  # Detailed logging
                            break
                    except Exception as e:
                        print(f"Comparison error: {e}")

        # If no date found in first line, try searching through all lines
        if not message_date:
            for line in lines:
                date_match = re.search(date_pattern, line)
                if date_match:
                    original_date = date_match.group(0)
                    try:
                        # Parse the full date and convert to short format
                        month, day, year = map(int, original_date.split('/'))
                        
                        # Ensure 2-digit year is interpreted correctly
                        if year > 100:
                            year = year % 100
                        
                        # Format the date consistently
                        message_date = f"{month:02d}/{day:02d}/{year:02d}"
                    except Exception as e:
                        print(f"Date parsing error: {e}")
                        message_date = original_date

                    # Find the corresponding map URL
                    for date, url in maps_data:
                        try:
                            comp_month, comp_day, comp_year = map(int, date.split('/'))
                            comp_date = f"{comp_month:02d}/{comp_day:02d}/{comp_year:02d}"
                            
                            if comp_date.strip() == message_date.strip():
                                map_url = url
                                break
                        except Exception as e:
                            print(f"Comparison error: {e}")
                    
                    if map_url:
                        break

        # Fallback to current date if no date found
        if not message_date:
            # Use current date in the desired format
            current_date = datetime.now()
            message_date = current_date.strftime('%m/%d/%y')
            print(f"No date found, using current date: {message_date}")

        # Process each line for coordinates
        for line in lines:
            # Check for double slashes (indicating coordinates)
            if "//" in line:
                found_cords = True
                timestamp_str = message.created_at.strftime("%Y-%m-%d %H:%M:%S")
                
                # Log detailed information
                print(f"Coordinates found: {line}")
                print(f"Associated Date: {message_date}")
                print(f"Associated Map URL: {map_url}")

                new_entry = pd.DataFrame({
                    "Timestamp": [timestamp_str],
                    "Username": [str(message.author)],
                    "User   ID": [message.author.id],
                    "User   Mention": [f"<@{message.author.id}>"],
                    "Message": [line],
                    "Matched Date": [message_date],
                    "Map URL": [map_url]
                })

                # Append the new entry to the DataFrame
                atlas_cords = pd.concat([atlas_cords, new_entry], ignore_index=True)

        # Save the DataFrame to an Excel file only if we found coordinates
        try:
            if found_cords:
                export_atlas_cords_to_excel()
        except Exception as e:
            print(f"Error during export: {e}")

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

@bot.command()
async def search_clan(ctx, clan_name: str):
    """Search for coordinates and map URLs associated with a specific clan."""
    # Ensure the results channel exists
    results_channel = discord.utils.get(ctx.guild.text_channels, name="results")
    if results_channel is None:
        await ctx.send("The 'results' channel does not exist.")
        return

    # Read the Excel file
    try:
        atlas_cords = pd.read_excel("atlas_cords.xlsx")
    except FileNotFoundError:
        await ctx.send("The Excel file does not exist.")
        return
    except Exception as e:
        await ctx.send(f"An error occurred while reading the Excel file: {e}")
        return

    # Filter the DataFrame for the specified clan and remove duplicates
    clan_results = atlas_cords[atlas_cords['Message'].str.contains(clan_name, case=False, na=False)]
    clan_results = clan_results.drop_duplicates(subset='Message')  # Remove duplicates based on the 'Message' column

    # Debugging output to check how many results were found
    print(f"Found {len(clan_results)} unique results for clan '{clan_name}'.")

    if clan_results.empty:
        await results_channel.send(f"No coordinates found for clan '{clan_name}'.")
    else:
        # Prepare the results to send
        results_message = f"Coordinates for clan '{clan_name}':\n"
        for index, row in clan_results.iterrows():
            # Remove crown and money bag emojis
            formatted_message = row['Message'].replace('', '').replace('', '').strip()
            
            # Include the map URL and matched date if they exist
            map_info = f"\nMap: {row['Map URL']}" if pd.notna(row['Map URL']) else ""
            date_info = f"\nDate: {row['Matched Date']}" if pd.notna(row['Matched Date']) else ""
            
            results_message += f"{formatted_message}{map_info}{date_info}\n"

        # Check if the message is too long
        if len(results_message) > 2000:  # Discord's message limit is 2000 characters
            # Split the message into chunks
            for chunk in [results_message[i:i + 2000] for i in range(0, len(results_message), 2000)]:
                await results_channel.send(chunk)
        else:
            await results_channel.send(results_message)
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
def export_atlas_cords_to_excel():
    global atlas_cords
    try:
        # Fill NaN values with a placeholder
        atlas_cords_export = atlas_cords.fillna({
            'Matched Date': 'No Date Found',
            'Map URL': 'No Map URL Found'
        })

        # Export to Excel with additional formatting
        with pd.ExcelWriter('atlas_cords.xlsx', engine='openpyxl') as writer:
            atlas_cords_export.to_excel(writer, index=False, sheet_name='Coordinates')
            
            # Get the workbook and worksheet
            workbook = writer.book
            worksheet = writer.sheets['Coordinates']
            
            # Auto-adjust columns' width
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
                adjusted_width = (max_length + 2)
                worksheet.column_dimensions[column_letter].width = adjusted_width
            
            # Add hyperlink formatting to the Map URL column
            for row in range(2, len(atlas_cords_export) + 2):
                cell = worksheet.cell(row=row, column=list(atlas_cords_export.columns).index('Map URL') + 1)
                if cell.value and 'https://' in str(cell.value):
                    cell.hyperlink = cell.value
                    cell.style = 'Hyperlink'
        
        print("Atlas coordinates exported to Excel successfully.")
    except Exception as e:
        print(f"Error exporting to Excel: {e}")    

# Running the bot
TOKEN = ("")

bot.run(TOKEN)
