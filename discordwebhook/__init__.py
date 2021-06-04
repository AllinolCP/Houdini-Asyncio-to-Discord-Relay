from houdini.plugins import IPlugin
from houdini import handlers
from dhooks import Webhook, Embed
from houdini.handlers import XTPacket
from houdini.handlers.play.message import handle_send_message
from houdini.handlers.play.navigation import handle_join_server

# Fill these in.
chatlogwebhook = ''
coinslogwebhook = ''
connectionlogwebhook = ''
cppsname = ''
playlink = ''
website = ''

class DiscordWebhookLogger(IPlugin):
    author = "Allinol & atlogical"
    description = "Discord Webhook Plugin"
    version = "1.1.0"

    def __init__(self, server):
        super().__init__(server)

    async def ready(self):
        self.server.logger.info("DiscordWebhookLogger.ready()")

    @handlers.handler(XTPacket('j', 'js'), after=handle_join_server)
    async def connected_logger(self, p):
        async with Webhook.Async(connectionlogwebhook) as webhook:
            embed = Embed(title='Log', description='Connected', color=242424, timestamp='now')

            embed.set_author(name=f'{p.username}', url=f'https://{website}', icon_url=f'https://{playlink}/avatar/{p.id}/cp?size=120')
            embed.set_thumbnail(url=f'https://{playlink}/avatar/{p.id}/cp?size=120')
            embed.set_footer(text=f'© {cppsname}')
            embed.add_field(name='Server', value=f'{self.server.config.name}')
            embed.add_field(name='Location', value=f'{p.room.name}')
            embed.add_field(name='Name', value=f'{p.username}')
            embed.add_field(name=f'Players In {self.server.config.name}', value=f"{await p.server.redis.hget('houdini.population',f'{self.server.config.id}', encoding='utf-8')}")

            await webhook.send(embed=embed)

    @handlers.disconnected
    @handlers.player_attribute(joined_world=True)
    async def disconnected(self, p):
        async with Webhook.Async(connectionlogwebhook) as webhook:
            embed = Embed(title='Log', description='Disconnected', color=242424, timestamp='now')

            embed.set_author(name=f'{p.username}', url=f'https://{website}', icon_url=f'https://{playlink}/avatar/{p.id}/cp?size=120')
            embed.set_thumbnail(url=f'https://{playlink}/avatar/{p.id}/cp?size=120')
            embed.set_footer(text=f'© {cppsname}')
            embed.add_field(name='Server', value=f'{self.server.config.name}')
            embed.add_field(name='Name', value=f'{p.username}')
            embed.add_field(name=f'Players In {self.server.config.name}', value=f"{await p.server.redis.hget('houdini.population',f'{self.server.config.id}', encoding='utf-8')}")

            await webhook.send(embed=embed)

    @handlers.handler(XTPacket('m', 'sm'), after=handle_send_message)
    @handlers.cooldown(1)
    async def chat_logger(self, p, penguin_id: int, message: str):
        async with Webhook.Async(chatlogwebhook) as webhook:
            embed = Embed(title='Chat-Log', description='Chat logger', color=242424, timestamp='now')

            embed.set_author(name=f'{p.username}', url=f'https://{website}', icon_url=f'https://{playlink}/avatar/{penguin_id}/cp?size=120')
            embed.set_thumbnail(url=f'https://{playlink}/avatar/{penguin_id}/cp?size=120')
            embed.set_footer(text=f'© {cppsname}')
            embed.add_field(name='Server', value=f'{self.server.config.name}')
            embed.add_field(name='Location', value=f'{p.room.name}')
            embed.add_field(name='Name', value=f'{p.username}')
            embed.add_field(name='Message', value=f'{message}')

            await webhook.send(embed=embed)
