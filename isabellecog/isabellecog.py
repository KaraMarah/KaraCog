import discord
import random
import string
from redbot.core import commands
from redbot.core import checks
from redbot.core.utils import chat_formatting as chat
from redbot.core.utils.chat_formatting import pagify


class isabellecog(commands.Cog):
    """A set of custom commands for Isabelle Bot"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def i(self, ctx, action: str, *, thing: str):
        """bond with isabelle"""
        bad_words = ["fuck", "kill", "beat"]
        if action in bad_words:
            await ctx.send(f"I don't {action} {thing} at all.")
        else:
            await ctx.send(f"I {action} {thing} too, {ctx.author.mention}!")

    @commands.command()
    async def bajinga(self, ctx):
        """bajinga!"""
        await ctx.send("What?")

    @commands.command()
    async def hellpit(self, ctx, p2: discord.Member):
        """Welcome to the hellpit. Only one may leave."""

        # Players
        p1 = ctx.author
        # p2 from function signature
        p1_letters = []
        p2_letters = []

        # Secret
        letters = string.ascii_lowercase
        orig_secret = random.sample(letters, 9)
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
            "scared by pots and pans", "SSN 712-45-7834"
        ]

        # Check
        def is_correct(msg):
            """Checks whether the message is gucci or not."""
            return (
                (msg.author == p1 or msg.author == p2)
                and len(msg.content) == 1
            )

        # Sends Prompt
        prompt_str = (
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
            "The loser will be killed/given a weird nickname."
        )
        await ctx.send(prompt_str)

        # Handling
        finished = False
        while not finished:
    
            # Waits for correct message
            working_msg = await self.bot.wait_for(
                'message', check=is_correct
            )
            letter = working_msg.content

            # Adds the letter to the correct player list.
            # Removes it from the secret.
            if letter in secret:
                await ctx.send(
                    f"`{letter}` was in the secret. You now own it, "
                    f"{working_msg.author.mention}."
                )
                if working_msg.author == p1:
                    p1_letters.append(letter)
                elif working_msg.author == p2:
                    p2_letters.append(letter)
                secret.remove(letter)
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
            loser = p2
        elif len(p2_letters) > len(p1_letters):
            winner = p2
            loser = p1

        # Do final stuff
        new_nick = random.choice(weird_names)

        final_str = (
            f"**The game is over, and the pit is filled.**\n"
            f"_`{''.join(orig_secret)}` was the set of letters._\n\n"
            f"**{winner.name}** won and gets to go back to the surface.\n\n"
            f"**{loser.name}** lost and gets the nickname `{new_nick}`.\n\n"
            f"_Welcome to hell, {loser.mention}. You're here forever._"
        )

        await loser.edit(nick=new_nick)
        await ctx.send(final_str)