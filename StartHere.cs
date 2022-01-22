using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace Populus
{
    
    public class StartHere
    {
        public static Configuration config = new Configuration();
        public static string configFile = "config.json";
        public static void Main(string[] args)
        {
            try
            {
                config = LoadConfig();
                if (config.discordConfig != null)
                    Discord.DiscordBot.MainAsync(config.discordConfig).GetAwaiter().GetResult();
            }
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
                return;
            }
        }


        public static string GetTime()
        {
            return DateTime.Now.ToString("HH:mm:ss");
        }
        private static Configuration LoadConfig()
        {
            if (File.Exists(configFile))
            {
                var result = JsonConvert.DeserializeObject<Configuration>(File.ReadAllText(configFile));
                if (result != null)
                    return result;
            }

            return new Configuration();
        }
    }


    public class Configuration
    {
        public DiscordConfig? discordConfig = default;
    }

    public class DiscordConfig
    {
        //basic setup
        public string prefix { get; set; } = default!;
        public string discordToken { get; set; } = default!;
        //channels
        public ulong newsChannel { get; set; }
        //roles
        public DiscordRoles roles { get; set; } = default!;
        public ulong yearMessage { get; set; }
        public ulong courseMessage { get; set; }        
        public ulong colorMessage { get; set; }
        public ulong resetMessage { get; set; }
    }
    public class DiscordRoles
    {
        public Dictionary<string, ulong> gamingRoles { get; set; } = default!;
        public Dictionary<string, ulong> yearRoles { get; set; } = default!;
        public Dictionary<string, ulong> courseRoles { get; set; } = default!;
        public Dictionary<string, ulong> colorRoles { get; set; } = default!;
        public Dictionary<string, ulong> adminRoles { get; set; } = default!;
    }
}
