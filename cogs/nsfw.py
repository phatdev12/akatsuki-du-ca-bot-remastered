from discord import Embed, Interaction, app_commands
from discord.ext.commands import GroupCog
from modules.database_utils import get_user_lang
from modules.embed_process import rich_embeds
from modules.log_utils import command_log

from modules.nsfw import get_nsfw
from modules.checks_and_utils import user_cooldown_check

class NSFWCog(GroupCog, name = "nsfw"):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot
    
    @app_commands.checks.cooldown(1, 1, key = user_cooldown_check)
    @app_commands.command(name = "art")
    async def nsfw(self, interaction : Interaction):
        """
        Good nsfw art huh?
        """
        
        author = interaction.user
        command_log(author.id, author.guild.id, interaction.channel.id, interaction.command.name)
        
        lang = await get_user_lang(self.bot.redis_ins, author.id)
        if not interaction.channel.is_nsfw():
            await interaction.response.send_message(lang["nsfw"]["PlsGoToNSFW"], ephemeral = True)
        
        url, source = await get_nsfw()
        
        await interaction.response.send_message(
            rich_embeds(
                Embed(title = "0.0",
                      description = f"{lang['fun']['PoweredByWaifuim']}\nSource: [{source}]({source})"),
                author,
                lang["main"]
            ).set_image(url = url)
        )