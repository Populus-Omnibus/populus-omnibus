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
        public string prefix { get; set; }
        public string discordToken { get; set; }
    }
}
