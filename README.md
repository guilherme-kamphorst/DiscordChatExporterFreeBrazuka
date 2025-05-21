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

Installation: Clone the repo, install dependencies (pip install discord.py aiohttp), add your bot token, and run with python3 discord_bot.py.
