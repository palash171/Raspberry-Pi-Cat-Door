# Telegram Setup

This guide covers the Telegram part of the cat door project.
Use it before hardware testing so the notification channel is already working.

## 1. Create the bot

In Telegram:

1. Open `@BotFather`
2. Send `/newbot`
3. Choose a bot name
4. Choose a username ending in `bot`
5. Copy the token BotFather gives you

## 2. Start the chat properly

Open your bot and send:

```text
/start
hi
```

Sending both messages helps make sure the bot has a real update waiting.

## 3. Prepare the local software folder

From inside `software/`:

```bash
./setup_pi.sh
```

If you prefer the manual version:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## 4. Save the bot token

Open the config file:

```bash
nano .env
```

Set:

```env
CAT_DOOR_TELEGRAM_BOT_TOKEN=your-token-here
```

Leave `CAT_DOOR_TELEGRAM_CHAT_ID` blank for now.

## 5. Find your chat ID

Run:

```bash
./run_cat_door.sh show-chat-id
```

If it says no chat ID was found, send another message to the bot and run this:

```bash
./run_cat_door.sh debug-updates
```

That prints the recent updates and usually shows the chat ID directly.

Then store the value in `.env`:

```env
CAT_DOOR_TELEGRAM_CHAT_ID=123456789
```

## 6. Save and exit `nano`

When editing `.env` in `nano`:

1. Press `Ctrl + O` to write the file
2. Press `Enter` to confirm the filename
3. Press `Ctrl + X` to exit

## 7. Test Telegram delivery

```bash
./run_cat_door.sh text-test
./run_cat_door.sh approval-test
```

Expected result:

- `text-test` sends a message to the chat
- `approval-test` sends `Open Door` and `Keep Closed` buttons
- pressing a button sends the result back to the terminal

## 8. Test photo delivery on the Pi

Once the camera is connected on the Raspberry Pi:

```bash
./run_cat_door.sh photo-test
```

That captures one image and sends it to Telegram with the approval buttons.
