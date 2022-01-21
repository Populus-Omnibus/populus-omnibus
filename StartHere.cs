using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace Populus
{
    
    internal class StartHere
    {
        public static Configuration config;
        private static string configFile = "config.json";
        public static void Main(string[] args)
        {
            config = LoadConfig();

            if (config.discordConfig != null)
            {
                Discord.DiscordBot.MainAsync((DiscordConfig) config.discordConfig).GetAwaiter().GetResult();
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
                return JsonConvert.DeserializeObject<Configuration>(File.ReadAllText(configFile));
            }

            return new Configuration();
        }
    }


    public struct Configuration
    {
        public DiscordConfig? discordConfig { get; set; }  
    }

    public struct DiscordConfig
    {
        //basic setup
        public string prefix { get; set; }
        public string discordToken { get; set; }
        //channels
        public ulong newsChannel { get; set; }
        public ulong roleReset { get; set; }
        public ulong yearSelect { get; set; }
        public ulong colorSelect { get; set; }
        public ulong courseSelect { get; set; }
        //roles
        public DiscordRoles roles { get; set; }
    }
    public struct DiscordRoles
    {
        public Dictionary<string, ulong> gamingRoles { get; set; }
        public Dictionary<string, ulong> yearRoles { get; set; }
        public Dictionary<string, ulong> courseRoles { get; set; }
        public Dictionary<string, ulong> colorRoles { get; set; }
    }
}
