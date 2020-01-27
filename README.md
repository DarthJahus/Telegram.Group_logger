:warning: This project has been discontinued long ago. If you need a logger for your Telegram group, don't use this. You can hire me to make one for you, but not to adapt this project. Thank you for your understanding.

# Telegram.Group_logger
Logger for Telegram groups.

## How to log Telegram group messages?

Just invite this bot into the groups you want to log and it will automatically save all messages in readable files.

If you do not want to create your own bot and log your (public) channel, message me (`@Jahus`) on Telegram; and if my bot or another is available, we will put it there and send you the logs when needed.

## Configure the bot

### 1. Create a Telegram bot

Talk to `@BotFather` and create a new bot. Open `logger_config.json` file and put your API key in `token` parameter:

        "token": "YOUR_TOKEN_HERE"

Set your bot name in `bot_name` parameter.

**Warning:** _As it is, your bot sees only commands. Use `/setprivacy` with `@BotFather` in order to allow it to see all messages in a group._

### 2. Invite your bot to groups you want to watch

Launch the script and invite your bot into your groups. The bot will automatically send a greetings message to the groups, giving at the same time their ID.

Save these ID in `groups` parameter, and give each group a (custom) name – it is important because group names on Telegram might change or collide. This should seem like this:

        "groups": {
            "-00001": "MyGroup"
        }

You can add as many groups as you want (put a comma at the end of each line, except for the last one):

        "groups": {
            "-00001": "MyGroup",
            "-00002": "AnotherGroup"
        }

You can close the script for now.

### 3. Set admins for the bot

Talk on a monitored group and launch the bot. Look at its logs (on the console window) and wait for a line that reports what you have said:

        [#123]    <Jahus(67026917)@Codex> b'Hello, World!'

The user ID is written between brackets.

Add that user ID to the `admins` array.

        "admins": [67026917]

You can add as many as you want, seperated with commas:

        "admins": [67026917, 90930757]

Admins can pause the logging process on a group and resume it using the `/log_pause` command.

To stop the bot and close the script, use `/bot_halt`.

Now terminate the script (close the window or use CTRL+C) and run it again, it's ready to serve.

### Other settings

`timeout` setting designates in seconds the time between new messages check.

## Features and limitations

### Message types

As it is now, at version 1.0, the bot handles only text messages (and forwards of text messages).

In the next version, there will be support for:

* Images: by uploading them to Imgur and linking into the log file;
* Stickers; by replacing them by their respective emoji and indicating that it was a sticker (and maybe link to the sticker pack).

Other types may or may not be handled.

### Emojis

Emojis are fully supported and saved into the log file using the UNICODE standard. For best readings, use `Segoe UI Emoji` font as it has been made specially to support UNICODE emojis.

## Log dump file

An admin may ask the bot for a log by using `/get_log` command on a monitored group. The log-file is sent in private.

## Contribution

~~Other feature to come may be uploading the logs to an FTP folder using a command like `/upload_ftp`.~~

Don't hesitate to push your contribution, like with the Imgur API ;-)

----

_Find me on:_

> Twitter: [@JahusVagabond](https://twitter.com/JahusVagabond)
> Telegram: [@Jahus](https://t.me/Jahus)
