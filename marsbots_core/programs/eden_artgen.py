import time
import uuid

import discord

from marsbots_core.resources.discord_utils import update_message


async def generation_loop(
    client,
    token,
    og_message,
    bot_message,
    ctx,
    refresh_interval: int,
):
    task_id = str(uuid.uuid4())
    finished = False
    last_image = None
    while not finished:
        result = client.fetch(token=token)
        print(result)
        status = result["status"]["status"]
        if status == "complete":
            filepath = f"{task_id}-testimage.png"
            output_img = result["output"]["creation"]
            output_img.save(filepath)
            await update_progress(bot_message, 1)
            finished = True
            async with ctx.channel.typing():
                local_file = discord.File(filepath, filename=filepath)
                await og_message.reply("result", file=local_file)

        elif status == "failed":
            finished = True
            async with ctx.channel.typing():
                await og_message.reply("Something went wrong :(")
        else:
            progress = result["status"].get("progress")
            data = result["config"].get("data")
            latest_image = data.get("progress_image") if data else None

            if progress:
                await update_progress(bot_message, progress)

            if latest_image and latest_image != last_image:
                await update_image(bot_message, latest_image)
                last_image = latest_image

            time.sleep(refresh_interval)


async def update_progress(message, progress):
    if progress == "__none__":
        return
    progress_num = min(int(progress * 100), 100)
    message_content = f"Generation is {progress_num}% complete"
    await update_message(message, content=message_content)


async def update_image(message, image):
    await update_message(message, [image])
