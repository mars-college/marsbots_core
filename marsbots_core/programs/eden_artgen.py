import asyncio
import uuid

import discord

from marsbots_core.resources.discord_utils import update_message


async def generation_loop(
    client,
    token,
    og_message,
    bot_message,
    ctx,
    output_dir,
    refresh_interval: int,
):
    task_id = str(uuid.uuid4())
    finished = False
    last_image = None
    filepath = str(output_dir / f"{task_id}-testimage.png")
    while not finished:
        result = client.fetch(token=token)
        print(result)
        status = result["status"]["status"]
        if status == "complete":
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
            output = result.get("output")
            queue_position = result["status"].get("queue_position")
            if output:
                latest_image = output.get("intermediate_creation")
            else:
                latest_image = None

            if queue_position:
                await update_queue_position(bot_message, queue_position)

            if progress:
                await update_progress(bot_message, progress)

            if latest_image and latest_image != last_image:
                latest_image.save(filepath)
                local_file = discord.File(filepath, filename=filepath)
                await update_image(bot_message, local_file)
                last_image = latest_image

            await asyncio.sleep(refresh_interval)


def appender(message, suffix):
    return message.split('\n')[0] + '\n\n' + suffix


async def update_progress(message, progress):
    if progress == "__none__":
        progress = 0
    progress_num = min(int(progress * 100), 100)
    message_suffix = f"_Generation is **{progress_num}%** complete_"
    message_content = appender(message.content, message_suffix)
    await update_message(message, content=message_content)


async def update_queue_position(message, position):
    message_suffix = f"_Queue position: **{position}**_"
    message_content = appender(message.content, message_suffix)
    await update_message(message, content=message_content)


async def update_image(message, image):
    await update_message(message, files=[image])
