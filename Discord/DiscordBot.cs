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
        public static DiscordConfig discordConfig = new DiscordConfig();

        public static async Task MainAsync(DiscordConfig config)
        {
            discordConfig = config;
            try
            {
                discordClient = new DiscordClient(new DiscordConfiguration()
                {
                    Token = discordConfig.discordToken,
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
                StringPrefixes = new[] { discordConfig.prefix }
            });
            var slashCommands = discordClient.UseSlashCommands();
            discordClient.Ready += async (s, e) =>
            {
                await s.UpdateStatusAsync(new DSharpPlus.Entities.DiscordActivity("vibing"));
                Console.WriteLine($"{discordClient.CurrentUser.Username}#{discordClient.CurrentUser.Discriminator} has connected to Discord!");
            };
            //discordClient.MessageCreated += async (s, e) => await Events.MessageReceivedAsync(e.Message);
            discordClient.ComponentInteractionCreated += async (s, e) => await Events.ComponentInteractionCreatedAsync(e);
            await slashCommands.RefreshCommands();
            slashCommands.RegisterCommands<MiscSlash>(724740489517203550);
            slashCommands.RegisterCommands<AdminSlash>(724740489517203550);
            await discordClient.ConnectAsync();
            await Task.Delay(-1);
        }

    }
}