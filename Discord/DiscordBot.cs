using DSharpPlus;
using DSharpPlus.CommandsNext;
using DSharpPlus.SlashCommands;
using Microsoft.Extensions.Logging;


using Populus.Discord.Commands;

namespace Populus.Discord
{


    public static class DiscordBot
    {
        public static DiscordClient discordClient { get; private set; } = default!;

        public static async Task MainAsync(DiscordConfig config)
        {

            try
            {
                discordClient = new DiscordClient(new DiscordConfiguration()
                {
                    Token = config.discordToken,
                    TokenType = TokenType.Bot,
                    Intents = DiscordIntents.AllUnprivileged,
                    MinimumLogLevel = LogLevel.Warning
                });
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
                return;
            }
            var commands = discordClient.UseCommandsNext(new CommandsNextConfiguration()
            {
                StringPrefixes = new[] { config.prefix }
            });
            var slashCommands = discordClient.UseSlashCommands();
            discordClient.Ready += async (s, e) =>
            {
                await s.UpdateStatusAsync(new DSharpPlus.Entities.DiscordActivity("vibing"));
                Console.WriteLine($"{discordClient.CurrentUser.Username}#{discordClient.CurrentUser.Discriminator} has connected to Discord!");
            };
            //Discord.MessageCreated += async (s, e) => await discord_Events.MessageReceivedAsync(e.Message);
            slashCommands.RegisterCommands<MiscSlash>(724740489517203550);
            await discordClient.ConnectAsync();
            await Task.Delay(-1);
        }

    }
}