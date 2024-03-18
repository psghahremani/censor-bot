import discord

censor_bot_token = '<TOKEN>'
client = discord.Client()


@client.event
async def on_message(message):
    # Ignore messages sent by CensorBot.
    if message.author == client.user:
        return

    # Check if user has mentioned CensorBot.
    censor_bot_mention_tag = f'<@{client.user.id}>'
    if censor_bot_mention_tag not in message.content:
        return

    # Check if user has mentioned CensorBot without replying to another message.
    if message.reference is None:
        await message.reply(
            '*Are you tired of getting in trouble because your friends send naughty messages '
            'in your Discord server but forget to flag them as **spoilers**?*\n\n*Oh worry no longer my child, '
            '**CensorBot** is at your disposal!*\n*Just __mention me in reply__ to '
            'naughty messages and I\'ll take care of those gosh darn obscenities!*\n\n'
            '*Stay safe, eat your vegetables and always listen to your mom. She knows best!*\n'
            '*#family_friendly #god_is_watching #jesus_saves*\n'
        )
        return

    # Fetch user's target message.
    target_message = await message.channel.fetch_message(message.reference.message_id)

    # Check if target message is not sent by CensorBot.
    if target_message.author == client.user:
        await message.delete()
        return

    # Delete target message and user's request message.
    await target_message.delete()
    await message.delete()

    # Censor all attachments by tagging them as "Spoilers".
    censored_attachments = []
    for attachment in target_message.attachments:
        attachment.filename = f"SPOILER_{attachment.filename}"
        spoiler = await attachment.to_file()
        censored_attachments.append(spoiler)

    # Censor message content.
    censored_message_content = f'*Sent by <@{target_message.author.id}>, censored by <@{message.author.id}>:*\n'
    if len(target_message.content) > 0:
        if not (target_message.content.startswith('||') and target_message.content.endswith('||')):
            censored_message_content += f'||{target_message.content}||'
        else:
            censored_message_content += target_message.content

    if target_message.reference is not None:
        # Reply censored message to its original referenced message.
        reply_to = await message.channel.fetch_message(target_message.reference.message_id)
        await reply_to.reply(censored_message_content, files=censored_attachments, mention_author=True)
    else:
        # Send censored message normally.
        await message.channel.send(censored_message_content, files=censored_attachments)


client.run(censor_bot_token)
