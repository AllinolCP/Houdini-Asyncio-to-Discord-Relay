from houdini.plugins import IPlugin
from houdini import handlers
from discord_webhook import DiscordWebhook, DiscordEmbed
from houdini.handlers import XTPacket
from houdini.handlers.games import determine_coins_earned, game_over_cooling
import difflib
import time
chatlogwebhook = ''
coinslogwebhook = ''
connectionlogwebhook = ''
cppsname =''
playlink = '' 
website = ''


class DiscordWebhookLogger(IPlugin):
    author = "Allinol"
    description = "Discord Webhook plugin"
    version = "1.0.0"

    def __init__(self, server):
        super().__init__(server)

        self.items_by_name = None

    async def ready(self):
        self.server.logger.info("Discord Webhook Logger Ready!")
        
        
    @handlers.handler(XTPacket('j', 'js'), pre_login=True)   
    async def connected_logger(self, p):
        webhook = DiscordWebhook(url=connectionlogwebhook, content=f'{p.username} connected to {p.server.config.name}')
        response = webhook.execute()
    
    @handlers.disconnected
    @handlers.player_attribute(joined_world=True)
    async def disconnected(self, p):
        webhook = DiscordWebhook(url=connectionlogwebhook, content=f'{p.username} disconnected')
        response = webhook.execute()
    
    @handlers.handler(XTPacket('zo', ext='z'))
    @handlers.cooldown(10, callback=game_over_cooling)
    async def coins_logger(self, p, score: int):
        coins_earned = determine_coins_earned(p, score)
        webhook = DiscordWebhook(url=coinslogwebhook, content=f'{p.username} earned {coins_earned}')
        response = webhook.execute()
        
    @handlers.handler(XTPacket('m', 'sm'))   
    async def chat_logger(self, p, penguin_id: int, message: str):
        webhook = DiscordWebhook(url=chatlogwebhook)

        # create embed object for webhook
        embed = DiscordEmbed(title='Chat-Log', description='Chat logger', color=242424)

        # set author
        embed.set_author(name=f'{p.username}', url=f'https://{website}', icon_url=f'https://{playlink}/avatar/{penguin_id}/cp?size=120')


        # set thumbnail
        embed.set_thumbnail(url=f'https://{playlink}/avatar/{penguin_id}/cp?size=120')

        # set footer
        embed.set_footer(text=f'© {cppsname}')

        # set timestamp (default is now)
        embed.set_timestamp()

        # add fields to embed
        embed.add_embed_field(name='Server', value=f'{self.server.config.name}')
        embed.add_embed_field(name='Location', value=f'{p.room.name}')
        embed.add_embed_field(name='Name', value=f'{p.username}')
        embed.add_embed_field(name='Message', value=f'{message}',)
        embed.add_embed_field(name=f'Players In {self.server.config.name}', value=f"{await p.server.redis.hget('houdini.population',f'{self.server.config.id}', encoding='utf-8')}")


        # add embed object to webhook
        webhook.add_embed(embed)
        time.sleep(1)
        response = webhook.execute()
