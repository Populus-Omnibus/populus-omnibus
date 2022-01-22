using DSharpPlus;
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
        [SlashCommand("roleselector", "Elküldi a rangválasztást lehetővé tévő üzenetet.")]
        public async Task SlashRoleSelector(InteractionContext ctx,
        [Choice("Évfolyam", 0)]
        [Choice("Szak", 1)]
        [Choice("Gárda", 2)]
        [Choice("Reset", 3)]
        [Option("tipus", "3 választó menü, illetve 1 reset üzenet")] long select)
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
                    DiscordBot.discordConfig.yearMessage = RoleSelectorDropdownSend(DiscordBot.discordConfig.roles.yearRoles, "Az év amikor felvettek ide", ctx).Id;
                    break;
                case 1:
                    DiscordBot.discordConfig.courseMessage = RoleSelectorDropdownSend(DiscordBot.discordConfig.roles.courseRoles, "Ebben a képzésben veszel részt", ctx).Id;
                    break;
                case 2:
                    DiscordBot.discordConfig.colorMessage = RoleSelectorDropdownSend(DiscordBot.discordConfig.roles.colorRoles, "A szín aminek tagja vagy", ctx).Id;
                    break;
                case 3:
                    DiscordBot.discordConfig.resetMessage = RoleResetButtonsSend(ctx).Id;
                    break;
            }
            File.WriteAllText(StartHere.configFile, JsonConvert.SerializeObject(StartHere.config, Formatting.Indented));
        }
        public DiscordMessage RoleSelectorDropdownSend(Dictionary<string, ulong> selectedRoles, string content, InteractionContext ctx)
        {
            var options = new List<DiscordSelectComponentOption>();
            foreach (var role in selectedRoles)
            {
                var rolename = Regex.Replace(role.Key, @"\p{Cs}|\p{So}", "");
                options.Add(new DiscordSelectComponentOption(rolename, rolename, emoji: new DiscordComponentEmoji(role.Key.Replace(rolename, "")))); //wtf why does this work
            }
            var dropdown = new DiscordSelectComponent("dropdown", null, options, false, 0, 1);
            var builder = new DiscordMessageBuilder().WithContent(content).AddComponents(dropdown);
            var result = builder.SendAsync(ctx.Channel).Result;
            ctx.CreateResponseAsync(new DiscordInteractionResponseBuilder()
            {
                Content = "Kész!",
                IsEphemeral = true
            });
            return result;
        }
        public DiscordMessage RoleResetButtonsSend(InteractionContext ctx)
        {
            var builder = new DiscordMessageBuilder()
            .WithContent("Visszaállítás, azaz reset gombok:")
            .AddComponents(new DiscordComponent[]
            {
                new DiscordButtonComponent(ButtonStyle.Danger, "rolereset1", "Évfolyam reset", false),
                new DiscordButtonComponent(ButtonStyle.Secondary, "x1", " ", true),
                new DiscordButtonComponent(ButtonStyle.Danger, "rolereset2", "Szak reset", false),
                new DiscordButtonComponent(ButtonStyle.Secondary, "x2", " ", true),     
                new DiscordButtonComponent(ButtonStyle.Danger, "rolereset3", "Gárda reset", false)
        });
            var result = builder.SendAsync(ctx.Channel).Result;
            ctx.CreateResponseAsync(new DiscordInteractionResponseBuilder()
            {
                Content = "Kész!",
                IsEphemeral = true
            });
            return result;
        }
    }
}