from pyrogram import filters
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
import os
from datetime import datetime

import config
from Flexyy import app  # inner folder

@app.on_message(filters.command("update") & filters.user(config.OWNER_ID))
async def update_bot(client, message):
    msg = await message.reply_text("🔄 Checking for updates... Please wait.")

    try:
        repo = Repo()
    except InvalidGitRepositoryError:
        return await msg.edit("❌ This folder is not a Git repository.")
    except GitCommandError as e:
        return await msg.edit(f"❌ Git error:\n`{e}`")

    os.system(f"git fetch origin {config.UPSTREAM_BRANCH}")

    commits = list(repo.iter_commits(f"HEAD..origin/{config.UPSTREAM_BRANCH}"))

    if not commits:
        return await msg.edit("✅ Bot is already up-to-date! No new commits.")

    text = "🆕 **New Updates Found:**\n\n"
    for c in commits:
        date = datetime.fromtimestamp(c.committed_date).strftime("%d %b %Y")
        text += (
            f"• `{c.hexsha[:7]}` {c.summary}\n"
            f"   👤 {c.author}\n"
            f"   📅 {date}\n\n"
        )

    await msg.edit(text + "⬇️ Pulling updates now...")

    os.system("git stash &> /dev/null")
    os.system("git pull")

    await msg.edit("♻️ Updates applied! Restarting bot now...")

    os.system(f"kill -9 {os.getpid()} && bash start")
