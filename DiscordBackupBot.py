import discord
from discord.ext import commands
import asyncio
import os
import shutil
from datetime import datetime
import requests
import zipfile
import aiohttp

# Configure intents
intents = discord.Intents.default()
intents.message_content = True

# Initialize the bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Event handler for bot readiness
@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')

# Function to download attachments
async def download_attachment(attachment, backup_dir, channel_name, message_author, timestamp, is_thread=False):
    # Determine the directory based on whether it's a thread or channel
    if is_thread:
        attachment_dir = os.path.join(backup_dir, channel_name, "threads", "attachments")
    else:
        attachment_dir = os.path.join(backup_dir, channel_name, "attachments")
    os.makedirs(attachment_dir, exist_ok=True)
    # Sanitize username for filename (replace spaces and remove special characters)
    sanitized_username = message_author.name.replace(" ", "_").replace("#", "").replace(".", "").replace("!", "")
    # Create a filename with sanitized username, original base name, and timestamp
    base_name = os.path.splitext(attachment.filename)[0]
    ext = os.path.splitext(attachment.filename)[1]
    timestamp_str = timestamp.strftime('%Y%m%d_%H%M%S')
    new_filename = f"{sanitized_username}_{base_name}_{timestamp_str}{ext}"
    attachment_path = os.path.join(attachment_dir, new_filename)
    # Handle potential filename collisions with a counter
    counter = 1
    while os.path.exists(attachment_path):
        new_filename = f"{sanitized_username}_{base_name}_{timestamp_str}_{counter}{ext}"
        attachment_path = os.path.join(attachment_dir, new_filename)
        counter += 1
    async with aiohttp.ClientSession() as session:
        async with session.get(attachment.url) as response:
            if response.status == 200:
                with open(attachment_path, 'wb') as f:
                    f.write(await response.read())
                return attachment_path
    return None

# Function to back up a channel or thread
async def backup_channel_or_thread(ctx, channel_or_thread, backup_dir, limit=None, include_attachments=True):
    try:
        # Determine the type (channel or thread) and file name
        if isinstance(channel_or_thread, discord.Thread):
            file_name = f"thread_{channel_or_thread.name}_{channel_or_thread.id}"
            entity_type = "thread"
            # Use the parent channel name for the directory structure
            parent_channel_name = channel_or_thread.parent.name
            thread_dir = os.path.join(backup_dir, parent_channel_name, "threads")
            os.makedirs(thread_dir, exist_ok=True)
            file_path = os.path.join(thread_dir, f"{file_name}.txt")
        else:
            file_name = channel_or_thread.name
            entity_type = "channel"
            file_path = os.path.join(backup_dir, f"{file_name}.txt")

        await ctx.send(f"Processing {entity_type} #{channel_or_thread.name}...")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"Backup of {entity_type} #{channel_or_thread.name} ({channel_or_thread.id})\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            async for message in channel_or_thread.history(limit=limit):
                timestamp = message.created_at
                timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                author = message.author
                content = message.content or "[Message with no text]"
                f.write(f"[{timestamp_str}] {author.name}: {content}\n")

                # Download attachments, if requested
                if include_attachments and message.attachments:
                    for attachment in message.attachments:
                        attachment_path = await download_attachment(
                            attachment, 
                            backup_dir, 
                            channel_or_thread.name if not isinstance(channel_or_thread, discord.Thread) else channel_or_thread.parent.name, 
                            author, 
                            timestamp, 
                            is_thread=isinstance(channel_or_thread, discord.Thread)
                        )
                        if attachment_path:
                            f.write(f"[Attachment] {os.path.basename(attachment_path)} saved at {attachment_path}\n")

        await ctx.send(f"Backup of {entity_type} #{channel_or_thread.name} completed.")
    except Exception as e:
        await ctx.send(f"Error backing up {entity_type} #{channel_or_thread.name}: {str(e)}")

# Backup command with options
@bot.command()
@commands.has_permissions(administrator=True)
async def backup(ctx, *args):
    guild = ctx.guild
    backup_dir = f"backup_{guild.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)

    # Default options
    channels_to_backup = []
    excluded_channels = set()  # Use a set to avoid duplicates
    limit = None  # None means all messages
    include_attachments = True  # Attachments downloaded by default
    include_threads = False

    # Parse arguments
    i = 0
    while i < len(args):
        arg = args[i].lower()
        if arg == "--channels" and i + 1 < len(args):
            i += 1
            channel_names = args[i].split(",")
            for name in channel_names:
                channel = discord.utils.get(guild.text_channels, name=name.strip())
                if channel:
                    # Check if the command executor has permission to view the channel
                    if channel.permissions_for(ctx.author).view_channel:
                        channels_to_backup.append(channel)
                    else:
                        await ctx.send(f"You do not have permission to view the channel '{name}'.")
                else:
                    await ctx.send(f"Channel '{name}' not found and will be ignored.")
        elif arg == "--exclude-channels" and i + 1 < len(args):
            i += 1
            excluded_channel_names = args[i].split(",")
            for name in excluded_channel_names:
                channel = discord.utils.get(guild.text_channels, name=name.strip())
                if channel:
                    excluded_channels.add(channel.name)
                else:
                    await ctx.send(f"Channel '{name}' not found and will be ignored for exclusion.")
        elif arg == "--limit" and i + 1 < len(args):
            i += 1
            try:
                limit = int(args[i])
                if limit <= 0:
                    limit = None
            except ValueError:
                await ctx.send(f"Invalid limit: '{args[i]}'. Using all messages.")
                limit = None
        elif arg == "--attachments":
            include_attachments = True
        elif arg == "--no-attachments":
            include_attachments = False
        elif arg == "--threads":
            include_threads = True
        i += 1

    # If no channels are specified with --channels, back up all accessible channels except excluded ones
    if not channels_to_backup:
        channels_to_backup = [ch for ch in guild.text_channels if ch.permissions_for(ctx.author).view_channel and ch.name not in excluded_channels]

    # If specific channels are specified with --channels, filter out excluded ones
    else:
        channels_to_backup = [ch for ch in channels_to_backup if ch.name not in excluded_channels]

    if not channels_to_backup:
        await ctx.send("No accessible channels for backup after exclusions. Check your permissions or excluded channels.")
        return

    total_entities = len(channels_to_backup)
    if include_threads:
        total_entities += sum(len(ch.threads) for ch in channels_to_backup)
        for ch in channels_to_backup:
            # Include public archived threads
            async for thread in ch.archived_threads():
                if thread.permissions_for(ctx.author).view_channel and thread.parent.name not in excluded_channels:
                    total_entities += 1
            # Include private archived threads, if the user has permission
            if ch.permissions_for(ctx.author).manage_threads:
                async for thread in ch.archived_threads(private=True):
                    if thread.permissions_for(ctx.author).view_channel and thread.parent.name not in excluded_channels:
                        total_entities += 1

    await ctx.send(f"Starting backup of {total_entities} entity(ies) (channels and threads)...")

    # Back up each channel
    for channel in channels_to_backup:
        # Back up the main channel
        if not channel.permissions_for(guild.me).read_messages:
            await ctx.send(f"The bot does not have permission to read channel #{channel.name}. Add the 'Read Messages' permission to the bot.")
            continue
        await backup_channel_or_thread(ctx, channel, backup_dir, limit, include_attachments)

        # Back up threads, if requested
        if include_threads:
            # Active threads
            for thread in channel.threads:
                if thread.permissions_for(ctx.author).view_channel and thread.parent.name not in excluded_channels:
                    if not thread.permissions_for(guild.me).read_messages:
                        await ctx.send(f"The bot does not have permission to read thread #{thread.name}. Add the 'Read Messages' permission to the bot.")
                        continue
                    await backup_channel_or_thread(ctx, thread, backup_dir, limit, include_attachments)

            # Archived threads (public and private, if the user has permission)
            async for thread in channel.archived_threads():
                if thread.permissions_for(ctx.author).view_channel and thread.parent.name not in excluded_channels:
                    if not thread.permissions_for(guild.me).read_messages:
                        await ctx.send(f"The bot does not have permission to read archived thread #{thread.name}. Add the 'Read Messages' permission to the bot.")
                        continue
                    await backup_channel_or_thread(ctx, thread, backup_dir, limit, include_attachments)

            # Private archived threads (requires Manage Threads permission)
            if channel.permissions_for(ctx.author).manage_threads:
                async for thread in channel.archived_threads(private=True):
                    if thread.permissions_for(ctx.author).view_channel and thread.parent.name not in excluded_channels:
                        if not thread.permissions_for(guild.me).read_messages:
                            await ctx.send(f"The bot does not have permission to read private archived thread #{thread.name}. Add the 'Read Messages' permission to the bot.")
                            continue
                        await backup_channel_or_thread(ctx, thread, backup_dir, limit, include_attachments)

    # Compress the backup into a ZIP file
    zip_path = f"{backup_dir}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(backup_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, backup_dir)
                zipf.write(file_path, os.path.join(backup_dir, arcname))

    # Save locally only, do not send to Discord
    await ctx.send(f"Backup completed and saved locally at: {zip_path}")

    # Do not clean up the backup_dir and zip_path to ensure they remain for manual access
    # shutil.rmtree(backup_dir)
    # if os.path.exists(zip_path):
    #     os.remove(zip_path)

# Bot token (regenerate for security)
bot.run('INSERT TOKEN HERE')
