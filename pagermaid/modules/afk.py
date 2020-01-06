""" PagerMaid auto-response for when you are AFK. """

from telethon.events import StopPropagation
from pagermaid import log, log_chatid, command_help, redis_check, count_msg, users
from pagermaid.events import register, diagnostics
from pagermaid.utils import afk_reason, is_afk, not_afk, db_afk


@register(outgoing=True, pattern="^-afk")
@diagnostics
async def afk(context):
    """ To set yourself as afk. """
    if not redis_check():
        await context.edit("`The database is malfunctioning.`")
        return
    message = context.text
    try:
        reason = str(message[5:])
    except:
        reason = ''
    if not reason:
        reason = 'rest'
    await context.edit("Entering afk status.")
    if log:
        await context.client.send_message(
            log_chatid,
            "User is afk, begin message logging."
        )
    await db_afk(reason)
    raise StopPropagation


command_help.update({
    "afk": "Parameter: -afk <text>\
    \nUsage: Sets yourself to afk and enables message logging and auto response, a message cancels the status."
})


@register(outgoing=True)
@diagnostics
async def back(context):
    global count_msg
    if not redis_check():
        return
    afk_query = await is_afk()
    if afk_query is True:
        await not_afk()
        if log:
            await context.client.send_message(
                log_chatid,
                "You received " +
                str(count_msg) +
                " messages from " +
                str(len(users)) +
                " chats while afk.",
            )
            for i in users:
                name = await context.client.get_entity(i)
                name0 = str(name.first_name)
                await context.client.send_message(
                    log_chatid,
                    "[" +
                    name0 +
                    "](tg://user?id=" +
                    str(i) +
                    ")" +
                    " messaged/mentioned you " +
                    "`" +
                    str(users[i]) +
                    " times.`",
                )
        cleanup()


@register(incoming=True, disable_edited=True)
@diagnostics
async def mention_respond(context):
    """ Auto-respond to mentions. """
    global count_msg
    if not redis_check():
        return
    query_afk = await is_afk()
    if context.message.mentioned and not (await context.get_sender()).bot:
        if query_afk is True:
            if context.sender_id not in users:
                await context.reply(
                    "I am away for "
                    + await afk_reason()
                    + ", your message is logged."
                )
                users.update({context.sender_id: 1})
                count_msg = count_msg + 1
            elif context.sender_id in users:
                if users[context.sender_id] % 5 == 0:
                    await context.reply(
                        "I am still away for "
                        + await afk_reason()
                        + ", your message priority is upgraded."
                    )
                    users[context.sender_id] = users[context.sender_id] + 1
                    count_msg = count_msg + 1
                else:
                    users[context.sender_id] = users[context.sender_id] + 1
                    count_msg = count_msg + 1


@register(incoming=True)
@diagnostics
async def afk_on_pm(context):
    global count_msg
    if not redis_check():
        return
    query_afk = await is_afk()
    if context.is_private and not (await context.get_sender()).bot:
        if query_afk is True:
            if context.sender_id not in users:
                await context.reply(
                    "I am away for "
                    + await afk_reason()
                    + ", your message is logged."
                )
                users.update({context.sender_id: 1})
                count_msg = count_msg + 1
            elif context.sender_id in users:
                if users[context.sender_id] % 5 == 0:
                    await context.reply(
                        "I am still away for "
                        + await afk_reason()
                        + ", your message priority is upgraded."
                    )
                    users[context.sender_id] = users[context.sender_id] + 1
                    count_msg = count_msg + 1
                else:
                    users[context.sender_id] = users[context.sender_id] + 1
                    count_msg = count_msg + 1


def cleanup():
    global count_msg
    global users
    count_msg = 0
    users = {}