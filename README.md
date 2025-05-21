# DiscordBackupBot
A Python-based Discord bot for server admins to back up channels, threads, and attachments. Features: select channels, exclude others, include threads, limit messages, and save locally as ZIP. Thread attachments are organized in threads/attachments/. 

Welcome to DiscordBackupBot, a powerful and customizable Discord bot built to help server administrators securely back up their channels, threads, and attachments. Written in Python using the discord.py library, this bot allows you to:

    Back up all accessible channels or specify individual ones with the --channels option.
    Exclude specific channels using --exclude-channels for granular control.
    Include active and archived threads (public and private) with --threads.
    Download attachments (e.g., images, files) and organize them by channel and thread.
    Limit message counts per channel with --limit to manage backup size.
    Save backups locally as ZIP files for easy access and storage.

Key features include:

    Thread attachments are neatly stored in threads/attachments/ within the channel folder.
    Backups are always saved locally (no Discord uploads), avoiding nested ZIP issues.
    Fully configurable with administrator permissions required for security.

Perfect for server owners who need reliable data preservation without cluttering Discord with large files. Contribute, report issues, or suggest features on our GitHub page!

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# STEP BY STEP


This guide provides a detailed process for implementing the Discord backup bot, designed to back up channels and threads (public and private) accessible to the user executing the command. The bot uses the discord.py library and supports exporting text messages and attachments (e.g., images). Follow the steps below to set up and run the bot from scratch.

Step-by-Step Implementation

1. Create an Application and Bot in the Developer Portal

Visit the https://discord.com/developers/applications
Click New Application, provide a name (e.g., "BackupBot"), and create the application.
Click in the Bot tab.
In Token, click Copy (do not share the token publicly). Replace INSERT TOKEN HERE in the bot code with this token at the end of the process.
Enable the required Intents:

Enable Server Members Intent and Message Content Intent under Bot > Privileged Gateway Intents.
In OAuth2 > URL Generator, select the bot scope and add Administrator permission.
Generate the invite link and use it to add the bot to your server.



2. Install Dependencies on Your Machine

Open a terminal and ensure Python is installed by running:

python3 --version

Install the required dependencies directly on your machine:

pip install discord.py aiohttp



3. Create and Configure the Bot Code

Create a file named DiscordBackupBot.py in a directory of your choice (e.g., your home directory or a project folder) and download the code of DiscordBackupbot.py or just download the file.

Replace the placeholder INSERT TOKEN HERE (located on the final line of the code) with the token you copied in Step 1, and insert it at the end of the bot code.

4. Configure Permissions on the Server

In the Discord server, go to Server Settings > Roles.
Edit the bot's role (e.g., "BackupBot") and enable the Administrator permissions
For private channels (e.g., #testebackup), adjust specific permissions:

Go to the channel settings > Permissions.
Add the bot's role and enable View Channel and Read Message History.

5. Run the Bot

In the terminal, navigate to the directory containing the discord_backup.py file.
Run the bot directly on your machine:

python3 DiscordBackupBot.py

The bot should display in the terminal: Bot connected as <bot_name>. This means the bot is active and ready to receive commands on Discord.

6. Backup with Bot

Here are two examples to test different scenarios:

Backup a specific channel with threads and attachments: Type in Discord:

!backup --attachments --threads --channels testebackup

This will back up the #testebackup channel, including all threads (active and archived) and attachments (e.g., photos).

The bot will respond with messages like "Starting backup..." and "Processing channel #testebackup...".

Backup all channels except specific ones, with threads: Type:

!backup --attachments --threads --exclude-channels geral

This will back up all channels you have access to, except #geral, including threads and attachments.

Check if the bot responds with messages like "Starting backup..." and "Backup completed!".
Open the ZIP file saved locally and confirm that the text files and attachments are present.



Command Options

Here’s a list of available options to customize your backup:

!backup: Backs up all channels you have permission to access. This includes messages, attachments, and threads (if specified).

Example: !backup (backs up all accessible channels).
--channels <name>: Selects one or more specific channels to back up (comma-separated, e.g., testebackup,general).

Example: !backup --channels testebackup (backs up only the #testebackup channel).
--exclude-channels <name>: Excludes specific channels from the backup (comma-separated, e.g., general,announcements). Works with or without --channels:

Alone: !backup --exclude-channels general backs up all accessible channels except #general, including their threads and attachments.
With --channels: !backup --channels testebackup,random --exclude-channels random backs up only #testebackup, skipping #random.
Note: If an excluded channel isn’t found, the bot will ignore it and continue the backup.
--limit <number>: Limits the number of messages per channel (e.g., --limit 100). Use this to reduce backup size or focus on recent messages.

Example: !backup --limit 100 (backs up only the last 100 messages per channel).
--threads: Includes active and archived threads (public and private, if permitted) within the backed-up channels. Threads in excluded channels are also skipped.

Example: !backup --threads (backs up channels and their threads).
--attachments: Enables attachment downloading. Use --no-attachments to skip downloading attachments.

Example: !backup --threads --no-attachments (backs up messages and threads without attachments).
