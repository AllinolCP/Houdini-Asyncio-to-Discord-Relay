# Houdini To Discord Relay v1.2
Relay chat from [Houdini](https://github.com/Solero/Houdini) to [Discord](https://discordapp.com).

# Previews
![](https://prnt.sc/t0gvpj)


# Installation
1. Run `git clone https://github.com/AllinolCP/Houdini-Asyncio-to-Discord-Relay.git` in `Houdini/Plugins`
2. Move into the `Houdini-asyncio-to-discord-relay` directory
3. Open `__init__.py` and set `chatlogwebhook, coinslogwebhook,connectionlogwebhook` to your [webhook URL](#how-to-get-a-webhook-url)
then set your cpps name, play link and the website 
4. Make sure the `discord-webhook` package is installed (`pip install discord-webhook`)
5. Enjoy!

# How to get a Webhook URL
1. Edit the Discord channel you want to have messages forwarded from Houdini to.  
2. Navigate to the Webhooks tab and press "Create Webhook".  
3. Give it a cool name and icon if you want.
4. Copy the webhook URL and set `chatlogwebhook, coinslogwebhook,connectionlogwebhook`'s value to it

