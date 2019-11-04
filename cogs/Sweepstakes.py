import asyncio
import os

import discord
from discord import File, Message
from discord.ext import commands
from discord.ext.commands import Context

from cogs.BaseCog import BaseCog
from utils import Utils, Lang, Questions
from datetime import datetime
from utils.Utils import save_to_disk


class Sweepstakes(BaseCog):

    def __init__(self, bot):
        super().__init__(bot)

    async def cog_check(self, ctx):
        if not hasattr(ctx.author, 'guild'):
            return False
        # TODO: should this be admin and/or custom role? PermissionViewSweepstakes, PermissionManageSweepstakes
        return ctx.author.guild_permissions.manage_channels

    async def get_reaction_message(self, ctx, jump_url):
        parts = jump_url.split('/')
        try:
            channel_id = parts[-2]
            message_id = parts[-1]
        except IndexError as e:
            await ctx.send(Lang.get_string('sweeps/jumpurl_prompt'))
            return

        try:
            channel = await self.bot.fetch_channel(channel_id)
            message = await channel.fetch_message(message_id)
            return message
        except Exception as e:
            await Utils.handle_exception(f"Failed to get message {channel_id}/{message_id}", self, e)
            await ctx.send(Lang.get_string('sweeps/fetch_message_failed', channel_id=channel_id, message_id=message_id))

    async def get_unique_react_users(self, message: Message):
        fields = ["id", "nick", "username", "discriminator", "mention", "left_guild"]
        data_list = ()
        user_list = {}
        for reaction in message.reactions:
            async for user in reaction.users():
                if user.id is not message.author.id and user.id is not self.bot.user.id:
                    user_list[user.id] = user
        for user_id, user in user_list.items():
            if hasattr(user, "nick"):
                nick = user.nick
                left_guild = ""
            else:
                nick = ""
                left_guild = "USER LEFT GUILD"
            data_list += ({"id": user.id,
                           "nick": nick,
                           "username": user.name,
                           "discriminator": user.discriminator,
                           "mention": user.mention,
                           "left_guild": left_guild},)
        return {'fields': fields, 'data': data_list}

    async def get_all_react_users(self, message: Message):
        fields = ["reaction", "id", "nick", "username", "discriminator", "mention", "left_guild"]
        data_list = ()
        reaction_list = {}
        for reaction in message.reactions:
            users = []
            async for user in reaction.users():
                if user.id is not message.author.id and user.id is not self.bot.user.id:
                    users.append(user)
            # store users, indexed by reaction emoji
            key = reaction.emoji.name if hasattr(reaction.emoji, "name") else reaction.emoji
            reaction_list[key] = users

        for emoji_name, users in reaction_list.items():
            for user in users:
                if hasattr(user, "nick"):
                    nick = user.nick
                    left_guild = ""
                else:
                    nick = ""
                    left_guild = "USER LEFT GUILD"
                data_list += ({"reaction": emoji_name,
                               "id": user.id,
                               "nick": nick,
                               "username": user.name,
                               "discriminator": user.discriminator,
                               "mention": user.mention,
                               "left_guild": left_guild},)
        return {'fields': fields, 'data': data_list}

    async def fetch_unique(self, ctx: Context, message: Message):
        channel_id = message.channel.id
        message_id = message.id
        try:
            unique_users = await self.get_unique_react_users(message)
            await ctx.send(Lang.get_string('sweeps/unique_result', count=len(unique_users['data'])))
            await self.send_csv(ctx, unique_users['fields'], unique_users['data'])
        except Exception as e:
            await Utils.handle_exception(f"Failed to get entries {channel_id}/{message_id}", self, e)
            await ctx.send(f"Failed to get entries {channel_id}/{message_id}")

    async def fetch_all(self, ctx: Context, message: Message):
        channel_id = message.channel.id
        message_id = message.id
        try:
            reactions = await self.get_all_react_users(message)
            await ctx.send(f"There are {len(reactions['data'])} entries to this drawing.")
            await self.send_csv(ctx, reactions['fields'], reactions['data'])
        except Exception as e:
            await Utils.handle_exception(f"Failed to get entries {channel_id}/{message_id}", self, e)
            await ctx.send(Lang.get_string('sweeps/fetch_entries_failed', channel_id=channel_id, message_id=message_id))

    async def send_csv(self, ctx, fields: list, data: tuple):
        now = datetime.today().timestamp()
        save_to_disk(f"entries_{now}", data, 'csv', fields)
        send_file = File(f"entries_{now}.csv")
        await ctx.send(file=send_file)
        os.remove(f"entries_{now}.csv")

    # TODO: command for taking an existing message (i.e. staged in private channel with reactions) and posting it
    #  publicly and adding reactions. paving the way for full reaction tracking and better automation, including
    #  message edits via bot for e.g. status updates.

    @commands.group(name="sweeps", aliases=['drawing'])
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True)
    async def sweepstakes(self, ctx: commands.Context):
        """sweeps help"""
        if ctx.invoked_subcommand is None:
            await ctx.send(Lang.get_string('sweeps/help'))

    @sweepstakes.group(name="entries")
    @commands.guild_only()
    async def entries(self, ctx: commands.Context):
        """reporting group"""
        if ctx.invoked_subcommand is None:
            await ctx.send(Lang.get_string('sweeps/entries_sub_command'))

    @sweepstakes.group(name="end", aliases=["cancel", "stop"])
    @commands.guild_only()
    async def end_sweeps(self, ctx: commands.Context):
        """reporting group"""
        # TODO: add sub-commands for ending, with reaction clear, restarting with reaction reset to only author
        if ctx.invoked_subcommand is None:
            await ctx.send(Lang.get_string('sweeps/end_sweeps_sub_command'))

    @end_sweeps.command(aliases=["clean", "clear"])
    @commands.guild_only()
    async def end_clean(self, ctx: commands.Context, jump_url: str):
        message: Message = await self.get_reaction_message(ctx, jump_url)
        try:
            await self.fetch_unique(ctx, message)
            await self.fetch_all(ctx, message)
            pending = await ctx.send(Lang.get_string('sweeps/removing_reactions'))
            await message.clear_reactions()
            await pending.delete()
        except Exception as e:
            await Utils.handle_exception(f"Failed to clear reactions {message.channel.id}/{message.id}", self, e)
            return
        await ctx.send(Lang.get_string('sweeps/drawing_closed'))

    @end_sweeps.command(aliases=["reset", "restart"])
    @commands.guild_only()
    async def end_reset(self, ctx: commands.Context, jump_url: str):
        message: Message = await self.get_reaction_message(ctx, jump_url)

        if not message.reactions:
            # no reactions to reset
            await ctx.send(Lang.get_string('sweeps/no_reactions'))
            return

        # gather all emojis from message reactions
        my_emoji = set()
        not_my_emoji = set()

        for reaction in message.reactions:
            if (isinstance(reaction.emoji, str) or
                    (hasattr(reaction.emoji, 'id') and self.bot.get_emoji(reaction.emoji.id))):
                my_emoji.add(reaction.emoji)
            else:
                # Can't use a custom emoji from a server I'm not in
                not_my_emoji.add(reaction.emoji)

        clear = True

        def no():
            nonlocal clear
            clear = False

        async def yes():
            await ctx.send(Lang.get_string('sweeps/invalid_emoji_confirm', count=len(not_my_emoji)))

        if not_my_emoji:
            # some emoji on the original message that I can't access
            if not my_emoji:
                # no emoji left that I can add back.
                prompt = Lang.get_string('sweeps/all_invalid_emoji')
            else:
                prompt = Lang.get_string('sweeps/some_invalid_emoji')

            try:
                await Questions.ask(self.bot,
                                    ctx.channel,
                                    ctx.author,
                                    prompt,
                                    [
                                        Questions.Option('YES', handler=yes),
                                        Questions.Option('NO', handler=no)
                                    ], delete_after=True)
            except asyncio.TimeoutError:
                return

        if clear:
            # show entries
            await self.fetch_unique(ctx, message)
            await self.fetch_all(ctx, message)

            pending = await ctx.send(Lang.get_string('sweeps/removing_reactions'))
            await message.clear_reactions()
            await pending.delete()

            if my_emoji:
                pending = await ctx.send(Lang.get_string('sweeps/adding_reactions'))
                emoji_success = True
                add_react_msg = await ctx.send(Lang.get_string('sweeps/adding_reactions_progress'))
                for emoji in my_emoji:
                    try:
                        # emoji = f"{emoji.id}" if hasattr(emoji, "id") else emoji
                        await message.add_reaction(emoji)
                        await add_react_msg.edit(content=f"{add_react_msg.content} {emoji}")
                    except discord.errors.HTTPException as e:
                        emoji_success = False
                        await ctx.send(Lang.get_string('sweeps/emoji_fail', emoji=emoji))
                        continue

                await pending.delete()
                if not emoji_success:
                    await ctx.send(Lang.get_string('sweeps/partial_emoji_fail'))

                await ctx.send(Lang.get_string('sweeps/drawing_restarted'))
            else:
                await ctx.send(Lang.get_string('sweeps/drawing_closed'))

    @entries.command(aliases=["unique"])
    @commands.guild_only()
    async def unique_entries(self, ctx: commands.Context, jump_url: str):
        """get a list of unique users who reacted to a given message"""
        message = await self.get_reaction_message(ctx, jump_url)
        await self.fetch_unique(ctx, message)

    @entries.command(aliases=["all"])
    @commands.guild_only()
    async def all_entries(self, ctx: commands.Context, jump_url: str):
        """get a list of all reactions to a given message"""
        message = await self.get_reaction_message(ctx, jump_url)
        await self.fetch_all(ctx, message)

    @sweepstakes.command(aliases=["h"])
    @commands.guild_only()
    async def help(self, ctx):
        await ctx.send(Lang.get_string('sweeps/help'))


def setup(bot):
    bot.add_cog(Sweepstakes(bot))