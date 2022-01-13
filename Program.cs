using DSharpPlus;
using DSharpPlus.CommandsNext;
using DSharpPlus.SlashCommands;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using System.Reflection;

namespace Populus
{
    public struct Configuration
    {
        public string Prefix { get; set; }
        public string DiscordToken { get; set; }
    }

    public static class Global
    {
        public static string ConfigFile = "Config.txt";
        public static string execDir = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
        public static Configuration Config = new Configuration();
        static void Main(string[] args)
        {
            MainAsync().GetAwaiter().GetResult();
        }
        public static async Task MainAsync()
        {
            if(!LoadConfig()) return;
            var Discord = new DiscordClient(new DiscordConfiguration()
            {
                Token = Config.DiscordToken,
                TokenType = TokenType.Bot,
                Intents = DiscordIntents.AllUnprivileged,
                MinimumLogLevel = LogLevel.Debug
            });
            var commands = Discord.UseCommandsNext(new CommandsNextConfiguration()
            {
                StringPrefixes = new[] { Config.Prefix }
            });
            var slashcommands = Discord.UseSlashCommands();
            Discord.Ready += async (s, e) =>
            {
                await s.UpdateStatusAsync(new DSharpPlus.Entities.DiscordActivity("vibing"));
                Console.WriteLine($"{Discord.CurrentUser.Username}#{Discord.CurrentUser.Discriminator} has connected to Discord!");
            };
            //Discord.MessageCreated += async (s, e) => await discord_Events.MessageReceivedAsync(e.Message);
            //commands.RegisterCommands<Misc>();
            await Discord.ConnectAsync();
            await Task.Delay(-1);
        }
        public static string GetTime()
        {
            return DateTime.Now.ToString("HH:mm:ss");
        }
        private static bool LoadConfig()
        {
            if (File.Exists(ConfigFile))
            {
                Config = JsonConvert.DeserializeObject<Configuration>(File.ReadAllText(ConfigFile));
                return true;
            }
            return false;
        }
    }
}