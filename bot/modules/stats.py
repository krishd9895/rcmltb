from psutil import (
    disk_usage,
    cpu_percent,
    swap_memory,
    cpu_count,
    virtual_memory,
    net_io_counters,
    boot_time,
    disk_io_counters,
    cpu_freq,
    getloadavg
)
from pyrogram.handlers import MessageHandler
from pyrogram.filters import command
from time import time
from os import path as ospath
from bot.helper.telegram_helper.message_utils import sendMessage
from bot import bot, botUptime
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.ext_utils.bot_utils import cmd_exec, get_readable_time
from bot.helper.ext_utils.human_format import get_readable_file_size
from bot.helper.telegram_helper.filters import CustomFilters

async def stats(client, message):
    if ospath.exists(".git"):
        last_commit = await cmd_exec(
            "git log -1 --date=short --pretty=format:'%cd <b>From</b> %cr'", True
        )
        last_commit = last_commit[0]
    else:
        last_commit = "No UPSTREAM_REPO"
    total, used, free, disk = disk_usage("/")
    swap = swap_memory()
    memory = virtual_memory()
    disk_io = disk_io_counters()

    stats = (
        "┎ <b>BOT STATISTICS :</b>\n"
        f"┖ <b>Bot Uptime :</b> {get_readable_time(time() - botUptime)}\n\n"
        "┎ <b>RAM ( MEMORY ) :</b>\n"
        f"┃ \n"
        f"┖ <b>U :</b> {get_readable_file_size(memory.used)} | <b>F :</b> {get_readable_file_size(memory.available)} | <b>T :</b> {get_readable_file_size(memory.total)}\n\n"
        "┎ <b>SWAP MEMORY :</b>\n"
        f"┃ \n"
        f"┖ <b>U :</b> {get_readable_file_size(swap.used)} | <b>F :</b> {get_readable_file_size(swap.free)} | <b>T :</b> {get_readable_file_size(swap.total)}\n\n"
        "┎ <b>DISK :</b>\n"
        f"┃\n"
        f"┃ <b>Total Disk Read :</b> {get_readable_file_size(disk_io.read_bytes)} ({get_readable_time(disk_io.read_time / 1000)})\n"
        f"┃ <b>Total Disk Write :</b> {get_readable_file_size(disk_io.write_bytes)} ({get_readable_time(disk_io.write_time / 1000)})\n"
        f"┖ <b>U :</b> {get_readable_file_size(used)} | <b>F :</b> {get_readable_file_size(free)} | <b>T :</b> {get_readable_file_size(total)}\n\n"
        f"┎ <b>CPU :</b> {cpu_percent(interval=0.5)}%\n"
        f"┖ <b>CPU Frequency:</b> {cpu_freq().current / 1000:.2f} GHz\n"
        f"┎ <b>Load Average:</b> {', '.join(str(round((x / cpu_count() * 100), 2)) for x in getloadavg())} (1m, 5m, 15m)\n\n"
        f"┎ <b>Physical Cores:</b> {cpu_count(logical=False)}\n"
        f"┖ <b>Total Cores:</b> {cpu_count(logical=True)}\n\n"
        f"┎ <b>Network Packets Sent:</b> {net_io_counters().packets_sent}\n"
        f"┖ <b>Network Packets Received:</b> {net_io_counters().packets_recv}\n\n"
        f"<b>Commit Date:</b> {last_commit}\n"
    )
    await sendMessage(stats, message)

bot.add_handler(
    MessageHandler(
        stats,
        filters=command(BotCommands.StatsCommand)
        & (CustomFilters.user_filter | CustomFilters.chat_filter),
    )
)
