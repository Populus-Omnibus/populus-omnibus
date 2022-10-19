using System.Text.RegularExpressions;
using DSharpPlus;
using DSharpPlus.Entities;
using DSharpPlus.EventArgs;

namespace Populus.Discord
{
    public static class Events
    {
        public static async Task ComponentInteractionCreatedAsync(ComponentInteractionCreateEventArgs eventArgs)
        {
            var config = DiscordBot.discordConfig;
            if (eventArgs.Message.Id == config.yearMessage)
                await AddSingleRole(config.roles.yearRoles, eventArgs);
            else if (eventArgs.Message.Id == config.courseMessage)
                await AddSingleRole(config.roles.courseRoles, eventArgs);
            else if (eventArgs.Message.Id == config.colorMessage)
                await AddSingleRole(config.roles.courseRoles, eventArgs);
            else if (eventArgs.Message.Id == config.resetMessage)
            {
                int.TryParse(Regex.Match(eventArgs.Id, @"\d+").Value, out int resetButtonNumber);
                switch (resetButtonNumber)
                {
                    case 1:
                        await DeleteRoles(config.roles.yearRoles, eventArgs);
                        break;
                    case 2:
                        await DeleteRoles(config.roles.courseRoles, eventArgs);
                        break;
                    case 3:
                        await DeleteRoles(config.roles.colorRoles, eventArgs);
                        break;

                }
            }
        }

        private static async Task AddSingleRole(Dictionary<string, ulong> roles, ComponentInteractionCreateEventArgs eventArgs)
        {
            string? rolename = eventArgs.Values.FirstOrDefault();
            DiscordRole? toAdd = null;
            if (rolename != null)
            {
                ulong roleId = roles.FirstOrDefault(p => p.Key.Contains(rolename)).Value;
                toAdd = eventArgs.Guild.GetRole(roleId);
            }
            if (toAdd != null)
            {
                await ((DiscordMember)eventArgs.User).GrantRoleAsync(toAdd);
                await eventArgs.Interaction.CreateResponseAsync(InteractionResponseType.ChannelMessageWithSource, new DiscordInteractionResponseBuilder()
                {
                    Content = $"{toAdd.Name} hozzáadva!",
                    IsEphemeral = true
                });
            }
            else
            {
                await eventArgs.Interaction.CreateResponseAsync(InteractionResponseType.ChannelMessageWithSource, new DiscordInteractionResponseBuilder()
                {
                    Content = "Sikertelen hozzáadás, kérlek próbáld újra! Többszöri sikertelen próbálkozás esetén értesítsd az adminokat!",
                    IsEphemeral = true
                });
            }
        }

        private static async Task DeleteRoles(Dictionary<string, ulong> roles, ComponentInteractionCreateEventArgs eventArgs)
        {
            foreach (var role in roles)
            {
                if(((DiscordMember)eventArgs.User).Roles.Any(p => p.Id == role.Value))
                {
                    await ((DiscordMember)eventArgs.User).RevokeRoleAsync(eventArgs.Guild.GetRole(role.Value));
                }
            }
            await eventArgs.Interaction.CreateResponseAsync(InteractionResponseType.ChannelMessageWithSource, new DiscordInteractionResponseBuilder()
            {
                Content = "Rangok eltávolítva!",
                IsEphemeral = true
            });
        }
    }
}
