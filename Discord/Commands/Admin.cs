using DSharpPlus.CommandsNext;
using DSharpPlus.Entities;
using DSharpPlus.SlashCommands;
using Populus;
using Newtonsoft.Json;

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;


namespace Populus.Discord.Commands
{
    public class AdminSlash : ApplicationCommandModule
    {
        [SlashCommand("roleselector", "Sends the message allowing role selection in this channel.")]
        public async Task SlashRoleSelector(InteractionContext ctx,
        [Choice("Évfolyam", 0)]
        [Choice("Szak", 1)]
        [Choice("Gárda", 2)]
        [Option("select", "Number of days of message history to delete")] long select = 0)
        {
            if(!ctx.Member.Roles.Where(p => DiscordBot.discordConfig.roles.adminRoles.ContainsValue(p.Id)).Any())
            {
                var responseBuilder = new DiscordInteractionResponseBuilder()
                {
                    Content = "Nem vagy jogosult ennek a használatára!",
                    IsEphemeral = true
                };
                await ctx.CreateResponseAsync(responseBuilder);
                return;
            }
            switch (select)
            {
                case 0:
                    StartHere.config.discordConfig.yearMessage = RoleSelectorDropdownSend(DiscordBot.discordConfig.roles.yearRoles, "Az év amikor felvettek ide", ctx).Id;
                    break;
                case 1:
                    StartHere.config.discordConfig.courseMessage = RoleSelectorDropdownSend(DiscordBot.discordConfig.roles.courseRoles, "Ebben a képzésben veszel részt", ctx).Id;
                    break;
                default:
                    StartHere.config.discordConfig.colorMessage = RoleSelectorDropdownSend(DiscordBot.discordConfig.roles.colorRoles, "A szín aminek tagja vagy", ctx).Id;
                    break;
            }
            File.WriteAllText(StartHere.configFile, JsonConvert.SerializeObject(StartHere.config, Formatting.Indented));
        }
        public DiscordMessage RoleSelectorDropdownSend(Dictionary<string, ulong> selectedRoles, string content, InteractionContext ctx)
        {
            var options = new List<DiscordSelectComponentOption>();
            foreach (var role in selectedRoles)
            {
                var rolename = Regex.Replace(role.Key, @"\p{Cs}", "");
                options.Add(new DiscordSelectComponentOption(rolename, rolename, emoji: new DiscordComponentEmoji(role.Key.Replace(rolename, "")))); //wtf why does this work
            }
            var dropdown = new DiscordSelectComponent("dropdown", null, options, false, 0, 1);
            var builder = new DiscordMessageBuilder().WithContent(content).AddComponents(dropdown);
            var result = builder.SendAsync(ctx.Channel);
            return result.Result;
        }
    }
}