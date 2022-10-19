namespace Populus;

public class Configuration
{
    public readonly DiscordConfig discordConfig = default!;
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
public abstract class DiscordRoles
{
    public Dictionary<string, ulong> gamingRoles { get; set; } = default!;
    public Dictionary<string, ulong> yearRoles { get; set; } = default!;
    public Dictionary<string, ulong> courseRoles { get; set; } = default!;
    public Dictionary<string, ulong> colorRoles { get; set; } = default!;
    public Dictionary<string, ulong> adminRoles { get; set; } = default!;
}