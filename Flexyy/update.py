@app.on_message(filters.command("update") & filters.user(config.OWNER_ID))
async def update_bot(client, message):
    msg = await message.reply_text("🔄 Checking for updates...")

    try:
        repo = Repo()
    except InvalidGitRepositoryError:
        return await msg.edit("❌ This is not a git repository.")
    except GitCommandError as e:
        return await msg.edit(f"❌ Git error:\n`{e}`")

    os.system(f"git fetch origin {config.UPSTREAM_BRANCH}")

    commits = list(repo.iter_commits(f"HEAD..origin/{config.UPSTREAM_BRANCH}"))

    if not commits:
        return await msg.edit("✅ Bot already up-to-date.")

    text = "🆕 **New Updates Found:**\n\n"
    for c in commits:
        text += f"• `{c.hexsha[:7]}` {c.summary}\n"

    await msg.edit(text + "\n⬇️ Updating bot...")

    os.system("git pull")

    await msg.edit("♻️ Restarting bot...")

    os.system(f"kill -9 {os.getpid()} && bash start")
