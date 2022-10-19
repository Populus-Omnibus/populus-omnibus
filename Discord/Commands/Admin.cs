using DSharpPlus;
using DSharpPlus.Entities;
using DSharpPlus.SlashCommands;
using Newtonsoft.Json;
using System.Text.RegularExpressions;

namespace Populus.Discord.Commands
{
    public abstract class AdminSlash : ApplicationCommandModule
    {
        [SlashCommand("roleselector", "Elküldi a rangválasztást lehetővé tévő üzenetet.")]
        public async Task SlashRoleSelector(InteractionContext ctx,
        [Choice("Évfolyam", 0)]
        [Choice("Szak", 1)]
        [Choice("Gárda", 2)]
        [Choice("Reset", 3)]
        [Option("tipus", "3 választó menü, illetve 1 reset üzenet")] long select)
        {
            if(!ctx.Member.Roles.Any(p => DiscordBot.discordConfig.roles.adminRoles.ContainsValue(p.Id)))
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
            await File.WriteAllTextAsync(StartHere.configFile, JsonConvert.SerializeObject(StartHere.config, Formatting.Indented));
        }

        private static DiscordMessage RoleSelectorDropdownSend(Dictionary<string, ulong> selectedRoles, string content, BaseContext ctx)
        {
            var options = new List<DiscordSelectComponentOption>();
            foreach (var role in selectedRoles)
            {
                var rolename = Regex.Replace(role.Key, @"\p{Cs}|\p{So}", "");
                options.Add(new DiscordSelectComponentOption(rolename, rolename,
                    emoji: new DiscordComponentEmoji(role.Key.Replace(rolename, ""))));
            }

            var dropdown = new DiscordSelectComponent("dropdown", null, options, false, 0);
            var builder = new DiscordMessageBuilder().WithContent(content).AddComponents(dropdown);
            var result = builder.SendAsync(ctx.Channel).Result;
            
            ctx.CreateResponseAsync(new DiscordInteractionResponseBuilder
            {
                Content = "Kész!",
                IsEphemeral = true
            });
            return result;
        }

        private static DiscordMessage RoleResetButtonsSend(BaseContext ctx)
        {
            var builder = new DiscordMessageBuilder()
            .WithContent("Visszaállítás, azaz reset gombok:")
            .AddComponents(
                new DiscordButtonComponent(ButtonStyle.Danger, "rolereset1", "Évfolyam reset"),
                new DiscordButtonComponent(ButtonStyle.Secondary, "x1", " ", true),
                new DiscordButtonComponent(ButtonStyle.Danger, "rolereset2", "Szak reset"),
                new DiscordButtonComponent(ButtonStyle.Secondary, "x2", " ", true),
                new DiscordButtonComponent(ButtonStyle.Danger, "rolereset3", "Gárda reset"));
            var result = builder.SendAsync(ctx.Channel).Result;
            
            ctx.CreateResponseAsync(new DiscordInteractionResponseBuilder
            {
                Content = "Kész!",
                IsEphemeral = true
            });
            return result;
        }
    }
}