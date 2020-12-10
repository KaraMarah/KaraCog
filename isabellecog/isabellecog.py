import discord
import random
import string
import asyncio
from redbot.core import commands
from redbot.core import checks
from redbot.core.utils import chat_formatting as chat
from redbot.core.utils.chat_formatting import pagify


class isabellecog(commands.Cog):
    """A set of custom commands for Isabelle Bot"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        ctx = await self.bot.get_context(message)
        is_self = ctx.author == ctx.bot.user
        if not is_self:
            if "vent" not in message.channel.name:
                if "RIP AND TEAR" == message.content:
                    await ctx.send("UNTIL IT IS DONE")
                if "rip and tear" == message.content:
                    await ctx.send("...until it is done.")
                if "blood for the blood god" in message.content.lower():
                    await ctx.send("SKULLS FOR THE SKULL THRONE")
                if "skulls for the skull throne" in message.content.lower():
                    await ctx.send("BLOOD FOR THE BLOOD GOD")


    @commands.command()
    async def i(self, ctx, action: str, *, thing: str = ""):
        """bond with isabelle"""
        bad_words = ["fuck", "kill", "beat"]
        if action in bad_words and thing == "":
            await ctx.send(f"I don't {action} at all.")
        elif action in bad_words and thing != "":
            await ctx.send(f"I don't {action} {thing} at all.")
        elif thing == "":
            await ctx.send(f"I {action} too, {ctx.author.mention}!")
        else:
            await ctx.send(f"I {action} {thing} too, {ctx.author.mention}!")

    @commands.command()
    async def goodnight(self, ctx):
        await ctx.send(f"Have a good night's sleep, {ctx.author.mention}!")

    @commands.command()
    async def ondrugs(self, ctx, *, input: str):
        await ctx.send(input.swapcase)

    @commands.command()
    async def hellpit(self, ctx, p2: discord.Member,
                      length: int = 9, mode: str = "normal"):
        """
        Welcome to the hellpit. Only one may leave.

        length (default: 9) - How many letters you want in the set.
        mode (default: normal) - Which mode you want to play in.

        Modes: normal, hardcore
        """

        # Players
        p1 = ctx.author
        # p2 from function signature
        p1_letters = []
        p2_letters = []

        # XXX This implementation is dumb, but...
        # It makes the most sense to the end user. probably.

        # Initial checks
        # Ban Ability on hardcore mode
        cant_ban = not ctx.author.guild_permissions.ban_members
        if mode == "hardcore" and cant_ban:
            return await ctx.send(
                "**You can't ban!** No hardcore mode for you."
            )

        # Check For self
        elif p1 == p2:
            return await ctx.send("**Can't throw yourself in the hellpit!**")

        # Get consent from participant
        else:
            consent_msg = await ctx.send(
                f"{p2.mention}, "
                f"**{p1.name}** is attempting to throw you in the hellpit.\n"
                f"The mode is `{mode}`. Do you wish to proceed?\n\n"
                "_Type `i accept` to accept, or anything else to cancel. "
                "This message will time out in one minute._"
            )

            # Waits for response
            try:
                consent_resp = await self.bot.wait_for(
                    'message',
                    check=lambda m: m.author == p2,
                    timeout=60.0
                )
            # On Timeout
            except asyncio.TimeoutError:
                return await consent_msg.edit(
                    content="**Request timed out.**"
                )
            # If response received
            else:
                # Deletes and continues if consenting
                if consent_resp.content.lower() == "i accept":
                    await consent_msg.delete()
                # Stops if not
                else:
                    return await consent_msg.edit(
                        content="**Request cancelled.**"
                    )

        # Secret
        letters = string.ascii_lowercase
        orig_secret = random.sample(letters, length)
        secret = orig_secret.copy()

        # Names
        weird_names = [
            "dummy", "silly head", "pig carcass",
            "bad at hellpit", "i lost the game", "has no feet",
            "god left me unfinished", "piss", "i hit villagers",
            "i cant eat", "bread", "hell piggy", "30 feral hogs",
            "aaaaassssssssss", "i write bad poetry", "never",
            "destroy my limeaid wow!", "i own sonic forces",
            "i like sonic 06", "date me infinite from sonic",
            "peetah died i cried", "stick bread in my ear",
            "eat my chair", "i deleted my system32",
            "i'm scared.", "stank hole", "overengineered toenails",
            "the gecs beat me up", "wow", "tf2 homework mod",
            "pinkie pie stan", "i play overwatch",
            "ellen as live action monokuma",
            "bubububububububububububub", "i'm elton john!",
            "stan nothing the void lingers", "im not poggers :<",
            "shave my head", "i got hacked at furcon",
            "i simped the pink panther", "im drunk birds",
            "i was bullied by my mother", "eggs in my nostrils",
            "wetbeans andy", "ant hoarder", "the one who pees the bed",
            "scared by pots and pans", "bajinga!", "SSN 712-45-7834", "Marvine"
        ]

        # Check for game logic
        def is_correct(msg):
            """Checks whether the message is gucci or not."""
            return (
                (msg.author == p1 or msg.author == p2)
                and len(msg.content) == 1
            )

        # Sends Prompt
        if mode == "normal":
            consequence = "given a weird nickname"
        elif mode == "hardcore":
            consequence = "banned (HARDCORE MODE)"
        prompt = (
            "**You have fallen into the hellpit, "
            f"{p1.name} and {p2.name}.**\n"
            "_I am the devil, and you will play my game._\n\n"
            "I will now generate a random set of characters.\n\n"
            "Your task is to send random letters to the chat. "
            "If your letter is in the set of characters, you will "
            "receive that letter, "
            "and it will be removed from the set.\n\n"
            "Play will continue until all letters are gone.\n\n"
            "Letters may repeat, so you may have a letter "
            "Whoever has the most letters at the end wins. "
            f"The loser will be **{consequence}**."
        )
        await ctx.send(prompt)

        # Handling
        finished = False
        while not finished:

            # Waits for correct message
            working_msg = await self.bot.wait_for(
                'message', check=is_correct
            )
            letter = working_msg.content.lower()

            # Adds the letter to the correct player list.
            # Removes it from the secret.
            if letter in secret:
                if working_msg.author == p1:
                    p1_letters.append(letter)
                elif working_msg.author == p2:
                    p2_letters.append(letter)
                secret.remove(letter)

                if len(secret) > 1:
                    amt_left = f"There are {len(secret)} letters left in the set."
                elif len(secret) == 1:
                    amt_left = f"There is {len(secret)} letter left in the set."
                else:
                    amt_left = "The set is empty."

                await ctx.send(
                    f"`{letter}` was in the secret. You now own it, "
                    f"{working_msg.author.mention}.\n"
                    f"{amt_left}"
                )
            else:
                await ctx.send(
                    f"`{letter}` was not in the secret, "
                    f"{working_msg.author.mention}."
                )

            # Finish on empty list
            if not secret:
                finished = True

        # Detect winner
        if len(p1_letters) > len(p2_letters):
            winner = p1
            winner_letters = p1_letters
            loser = p2
            loser_letters = p2_letters
        elif len(p2_letters) > len(p1_letters):
            winner = p2
            winner_letters = p2_letters
            loser = p1
            loser_letters = p1_letters

        # Do final stuff
        new_nick = random.choice(weird_names)

        if mode == "normal":
            punishment = f"Their loss has earned them the nickname `{new_nick}`."
        elif mode == "hardcore":
            punishment = "They will now be banned."

        final = (
            "**The game is over, and the pit is filled.**\n"
            f"_`{''.join(orig_secret)}` was the set of letters._\n\n"
            f"**{winner.name}** won and gets to go back to the surface.\n"
            f"_They had {len(winner_letters)} letters._\n\n"
            f"**{loser.name}** lost. {punishment}\n"
            f"_They had {len(loser_letters)} letters._\n\n"
            f"_Welcome to hell, {loser.mention}. You're here forever._"
        )

        if mode == "normal":
            await loser.edit(nick=new_nick)
            await ctx.send(final)
        elif mode == "hardcore":
            await ctx.send(final)
            await asyncio.sleep(15.0)
            await ctx.guild.ban(loser, reason=new_nick)
