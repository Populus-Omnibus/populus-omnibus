using DSharpPlus.Entities;
using DSharpPlus.SlashCommands;

namespace Populus.Discord.Commands
{
    public abstract class MiscSlash : ApplicationCommandModule
    {
        [SlashCommand("ping", "Returns the current latency of the Discord bot.")]
        public async Task SlashPing(InteractionContext ctx)
        {
            await ctx.CreateResponseAsync(new DiscordInteractionResponseBuilder()
                .WithContent($"{DiscordBot.discordClient.Ping} ms").AsEphemeral());
        }
    }
}