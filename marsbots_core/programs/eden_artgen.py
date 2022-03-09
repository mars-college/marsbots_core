import time

import discord

from marsbots_core.resources.discord_utils import update_message


async def generation_loop(client, token, message, ctx, refresh_interval: int):
    finished = False
    while not finished:
        result = client.fetch(token=token)
        status = result["status"]["status"]
        if status == "complete":
            filepath = "testimage.png"
            output_img = result["output"]["creation"]
            output_img.save(filepath)
            finished = True
            async with ctx.channel.typing():
                local_file = discord.File(filepath, filename=filepath)
                await message.reply("result", file=local_file)

        elif status == "failed":
            finished = True
            async with ctx.channel.typing():
                await message.reply("Something went wrong :(")
        else:
            progress = result["status"].get("progress")
            if progress:
                update_progress(message, progress)
            time.sleep(refresh_interval)


async def update_progress(message, progress):
    message_content = f"Generation is {progress*100}% complete"
    await update_message(message, content=message_content)
