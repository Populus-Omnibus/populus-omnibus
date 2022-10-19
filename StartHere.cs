using Newtonsoft.Json;
namespace Populus;

public static class StartHere
{
    //TODO: list services using ServiceProvider
    public const string configFile = "config.json";
    public static Configuration config { get; private set; } = null!;

    public static void Main(string[] args)
    {
        try
        {
            config = LoadConfig(); //config is initialised here, failure means some or all of it is null
            Discord.DiscordBot.MainAsync(config.discordConfig!).GetAwaiter().GetResult();
        }
        catch (FileNotFoundException e) //failure jumps here
        {
            Console.WriteLine(e.Message);
        }
    }


    public static string GetTime()
    {
        return DateTime.Now.ToString("HH:mm:ss");
    }
    private static Configuration LoadConfig()
    {
        return JsonConvert.DeserializeObject<Configuration>(File.ReadAllText(configFile))
               ?? throw new FileNotFoundException(); //if this fails, we can't run the app anyway
    }
}