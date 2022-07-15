import asyncio
import io
import json

import aiohttp
import discord
import requests

from marsbots.resources.discord_utils import update_message


async def generation_loop(
    gateway_url,
    minio_url,
    interaction_message,
    config,
    refresh_interval: int,
):
    result = requests.post(gateway_url + "/request_creation", json=config)

    if not await check_server_result_ok(result, interaction_message):
        return

    result = json.loads(result.content)
    task_id = result["task_id"]
    current_sha = None
    await update_progress(interaction_message, 0)

    while True:
        result = requests.post(
            gateway_url + "/get_creations",
            json={"task_id": task_id},
        )

        if not await check_server_result_ok(result, interaction_message):
            return

        result = json.loads(result.content)

        if not result:
            message_suffix = "_Server error: task ID not found_"
            message_content = appender(interaction_message.content, message_suffix)
            return await update_message(interaction_message, content=message_content)

        result = result[0]
        status = result["status"]
        progress = -1 if status == "pending" else result["status_code"]
        await update_progress(interaction_message, progress)

        if "intermediate_sha" in result:
            last_sha = result["intermediate_sha"][-1]
            if last_sha != current_sha:
                current_sha = last_sha
                sha_url = f"{minio_url}/{current_sha}"
                filename = f"{current_sha}.png"
                discord_file = await get_discord_file_from_url(sha_url, filename)
                await update_image(interaction_message, discord_file)

        if status == "failed":
            message_suffix = "_Server error: Eden task failed_"
            message_content = appender(interaction_message.content, message_suffix)
            return await update_message(interaction_message, content=message_content)

        if status not in ["pending", "running"]:
            break

        await asyncio.sleep(refresh_interval)


def appender(message, suffix):
    return message.split("\n")[0] + "\n\n" + suffix


async def update_progress(message, progress):
    if progress == "__none__":
        progress = 0
    progress_str = "pending" if progress == -1 else f"**{progress}%** complete"
    message_suffix = "" if progress == 100 else f"_Creation is {progress_str}_"
    message_content = appender(message.content, message_suffix)
    await update_message(message, content=message_content)


async def update_queue_position(message, position):
    message_suffix = f"_Queue position: **{position}**_"
    message_content = appender(message.content, message_suffix)
    await update_message(message, content=message_content)


async def update_image(message, image):
    await update_message(message, files=[image])


async def get_discord_file_from_url(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return None
            data = io.BytesIO(await resp.read())
            discord_file = discord.File(data, filename)
            return discord_file


async def check_server_result_ok(result, interaction_message):
    if result.status_code != 200:
        error_message = result.content.decode("utf-8")
        message_suffix = f"_Server error: {error_message}_"
        message_content = appender(interaction_message.content, message_suffix)
        await update_message(interaction_message, content=message_content)
    return result.status_code == 200
