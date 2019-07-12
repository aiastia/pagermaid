""" Module to automate message deletion. """

from asyncio import sleep
from telethon.errors import rpcbaseerrors
from jarvis import log, log_chatid, command_help
from jarvis.events import register


@register(outgoing=True, pattern="^-prune$")
async def prune(context):
    """ Purge every single message after the message you replied to. """
    if not context.text[0].isalpha() and context.text[0] not in ("/", "#", "@", "!"):
        chat = await context.get_input_chat()
        msgs = []
        count = 0

        async for msg in context.client.iter_messages(chat, min_id=context.reply_to_msg_id):
            msgs.append(msg)
            count = count + 1
            msgs.append(context.reply_to_msg_id)
            if len(msgs) == 100:
                await context.client.delete_messages(chat, msgs)
                msgs = []

        if msgs:
            await context.client.delete_messages(chat, msgs)
        notify = await context.client.send_message(
            context.chat_id,
            "Deleted "
            + str(count)
            + " messages.",
        )

        if log:
            await context.client.send_message(
                log_chatid, "Deleted " +
                            str(count) + " messages."
            )
        await sleep(3)
        await notify.delete()


@register(outgoing=True, pattern="^-selfprune")
async def selfprune(context):
    """ Prune self message. """
    if not context.text[0].isalpha() and context.text[0] not in ("/", "#", "@", "!"):
        message = context.text
        count = int(message[11:])
        i = 1

        async for message in context.client.iter_messages(context.chat_id, from_user='me'):
            if i > count + 1:
                break
            i = i + 1
            await message.delete()

        notification = await context.client.send_message(
            context.chat_id,
            "Deleted "
            + str(count)
            + " messages.",
        )
        if log:
            await context.client.send_message(
                log_chatid, "Deleted " +
                            str(count) + " messages."
            )
        await sleep(3)
        await notification.delete()


@register(outgoing=True, pattern="^-delete$")
async def delete(context):
    """ Deletes the replied message. """
    if not context.text[0].isalpha() and context.text[0] not in ("/", "#", "@", "!"):
        msg_src = await context.get_reply_message()
        if context.reply_to_msg_id:
            try:
                await msg_src.delete()
                await context.delete()
                if log:
                    await context.client.send_message(
                        log_chatid,
                        "Deleted a message."
                    )
            except rpcbaseerrors.BadRequestError:
                if log:
                    await context.client.send_message(
                        log_chatid,
                        "Lacks message deletion permission."
                    )


@register(outgoing=True, pattern="^-edit")
async def edit(context):
    """ Edits your last message. """
    if not context.text[0].isalpha() and context.text[0] not in ("/", "#", "@", "!"):
        message = context.text
        chat = await context.get_input_chat()
        self_id = await context.client.get_peer_id('me')
        string = str(message[6:])
        i = 1
        async for message in context.client.iter_messages(chat, self_id):
            if i == 2:
                await message.edit(string)
                await context.delete()
                break
            i = i + 1
        if log:
            await context.client.send_message(log_chatid, "Message edited.")


@register(outgoing=True, pattern="^-timed")
async def timed(context):
    """ A timed message that deletes itself. """
    if not context.text[0].isalpha() and context.text[0] not in ("/", "#", "@", "!"):
        try:
            message = context.text
            counter = int(message[7:9])
            text = str(context.text[9:])
            await context.delete()
            source_msg = await context.client.send_message(context.chat_id, text)
            await sleep(counter)
            await source_msg.delete()
            if log:
                await context.client.send_message(log_chatid, "Created timed message.")
        except ValueError:
            await context.edit("`Invalid time parameter specified.`")
