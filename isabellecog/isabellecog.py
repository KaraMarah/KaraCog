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
    async def hellpit(self, ctx, p2: discord.Member, seed: str):
        """Welcome to the hellpit. Only one may leave."""

        # Players
        p1 = ctx.author
        # p2 from function signature
        p1.letters = []
        p2.letters = []

        # Secret
        letters = string.ascii_lowercase
        orig_secret = [random.sample(letters) for _ in range(9)]
        secret = orig_secret  

        # Names
        weird_names = [
            "dummy", "silly head", "pig carcass", 
            "bad at hellpit", "lost the game", "has no feet",
            "god left me unfinished", "piss", "i hit villagers",
            "i cant eat", "bread", "hell piggy", "30 feral hogs",
            "aaaaassssssssss", "i write bad poetry", "never"
        ]

        # Check
        def is_correct(msg):
            """Checks whether the message is gucci or not."""
            return (
                (msg.author == p1 or msg.author == p2)
                and len(msg.content) == 1
                and msg.content in secret
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
            working_msg = self.bot.wait_for(
                'message', check=is_correct
            )
            letter = working_msg.content

            # Adds the letter to the correct player list.
            # Removes it from the secret.
            if working_msg.author == p1:
                p1.letters.append(letter)
            elif working_msg.author == p2:
                p2.letters.append(letter)
            secret.remove(letter)

            # Finish on empty list
            if not secret:
                finished = True

    # Detect winner
    if len(p1.letters) > len(p2.letters):
        winner = p1
        loser = p2
    elif len(p2.letters) > len(p1.letters):
        winner = p2
        loser = p1

    # Do final stuff
    new_nick = random.choice(weird_names)

    final_str = (
        f"**The game is over, and the pit is filled.**\n"
        f"_`{''.join(orig_secret)}` was the set of letters._\n\n"
        f"**{winner.name}** won and gets to go back to the surface.\n\n"
        f"**{loser.name}** lost and gets the nickname {new_nick}.\n\n"
        f"_Welcome to hell, {loser.mention}. You're here forever._"
    )

    await loser.edit(name=new_nick)
    await ctx.send(final_str)