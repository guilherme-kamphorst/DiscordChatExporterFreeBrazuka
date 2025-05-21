# DiscordBackupBot

![Python](https://img.shields.io/badge/Python-3.6%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Last Updated](https://img.shields.io/badge/Last%20Updated-May%202025-orange)

A powerful and customizable Discord bot for server admins to back up channels, threads, and attachments. Built with Python and `discord.py`, this bot saves backups locally as ZIP files, organizing thread attachments in `threads/attachments/`.

## ✨ Features

- Back up all accessible channels or select specific ones with `--channels`.
- Exclude channels using `--exclude-channels` for precise control.
- Include active and archived threads (public/private) with `--threads`.
- Download attachments (e.g., images, files) and organize them by channel/thread.
- Limit messages per channel with `--limit` to manage backup size.
- Saves backups locally—no Discord uploads, avoiding nested ZIP issues.
- Requires administrator permissions for security.

Perfect for server owners who need reliable data preservation!

## 🚀 Getting Started

Follow these steps to set up and run the bot from scratch.

### 1. Create an Application and Bot in the Developer Portal

1. Visit [Discord Developer Portal](https://discord.com/developers/applications).
2. Click **New Application**, name it (e.g., "BackupBot"), and create it.
3. Go to the **Bot** tab and click **Copy** under **Token** (keep this private).
4. Enable the following under **Bot > Privileged Gateway Intents**:
   - Server Members Intent
   - Message Content Intent
5. In **OAuth2 > URL Generator**, select **bot** scope, add **Administrator** permission, generate the invite link, and add the bot to your server.

### 2. Install Dependencies

Ensure Python 3.6+ is installed:

```bash
python3 --version
```

Install the required dependencies directly on your machine:
```
pip install discord.py aiohttp
```



3. Configure the Bot Code

    Create a file named DiscordBackupBot.py in your chosen directory.
    Copy the code from DiscordBackupBot.py in this repository.
    Replace INSERT TOKEN HERE (last line of the code) with the token you copied in Step 1.

4. Configure Permissions on the Server

In the Discord server, go to Server Settings > Roles.
Edit the bot's role (e.g., "BackupBot") and enable the Administrator permissions.

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
