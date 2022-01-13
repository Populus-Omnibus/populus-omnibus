using DSharpPlus.CommandsNext;
using DSharpPlus.Entities;
using DSharpPlus.SlashCommands;

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Populus.Commands
{
    public class MiscSlash : ApplicationCommandModule
    {
        [SlashCommand("ping", "Returns the current latency of the Discord bot.")]
        public async Task SlashPing(InteractionContext ctx)
        {
            var responsebuilder = new DiscordInteractionResponseBuilder()
            {
                Content = $"{Global.Discord.Ping} ms"
            };
            await ctx.CreateResponseAsync(responsebuilder);
        }
    }
}