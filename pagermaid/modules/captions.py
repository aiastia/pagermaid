""" PagerMaid module for adding captions to image. """

from os import remove
from magic import Magic
from pygments import highlight as syntax_highlight
from pygments.formatters import img
from pygments.lexers import guess_lexer
from pagermaid import log, module_dir
from pagermaid.listener import listener
from pagermaid.utils import execute, upload_attachment


@listener(outgoing=True, command="convert",
          description="Converts attachment of replied message to png.")
async def convert(context):
    """ Converts image to png. """
    reply = await context.get_reply_message()
    await context.edit("Converting . . .")
    target_file_path = await context.download_media()
    reply_id = context.reply_to_msg_id
    if reply:
        target_file_path = await context.client.download_media(
            await context.get_reply_message()
        )
    if target_file_path is None:
        await context.edit("There are no attachments in target message.")
    result = await execute(f"{module_dir}/assets/caption.sh \"" + target_file_path +
                           "\" result.png" + " \"" + str("") +
                           "\" " + "\"" + str("") + "\"")
    if not result:
        await handle_failure(context, target_file_path)
        return
    if not await upload_attachment("result.png", context.chat_id, reply_id):
        await context.edit("An error occurred during the conversion.")
        remove(target_file_path)
        return
    await context.delete()
    remove(target_file_path)
    remove("result.png")


@listener(outgoing=True, command="caption",
          description="Adds two lines of captions to attached image of replied message, separated by a comma.",
          parameters="<string>,<string> <image>")
async def caption(context):
    """ Generates images with captions. """
    await context.edit("Rendering image . . .")
    if context.arguments:
        if ',' in context.arguments:
            string_1, string_2 = context.arguments.split(',', 1)
        else:
            string_1 = context.arguments
            string_2 = " "
    else:
        await context.edit("Invalid syntax.")
        return
    reply = await context.get_reply_message()
    target_file_path = await context.download_media()
    reply_id = context.reply_to_msg_id
    if reply:
        target_file_path = await context.client.download_media(
            await context.get_reply_message()
        )
    if target_file_path is None:
        await context.edit("There are no attachments in target message.")
    if not target_file_path.endswith(".mp4"):
        result = await execute(f"{module_dir}/assets/caption.sh \"{target_file_path}\" "
                               f"{module_dir}/assets/Impact-Regular.ttf "
                               f"\"{str(string_1)}\" \"{str(string_2)}\"")
        result_file = "result.png"
    else:
        result = await execute(f"{module_dir}/assets/caption-gif.sh \"{target_file_path}\" "
                               f"{module_dir}/assets/Impact-Regular.ttf "
                               f"\"{str(string_1)}\" \"{str(string_2)}\"")
        result_file = "result.gif"
    if not result:
        await handle_failure(context, target_file_path)
        return
    if not await upload_attachment(result_file, context.chat_id, reply_id):
        await context.edit("An error occurred during the conversion.")
        remove(target_file_path)
        return
    await context.delete()
    if string_2 != " ":
        message = string_1 + "` and `" + string_2
    else:
        message = string_1
    remove(target_file_path)
    remove(result_file)
    await log(f"Caption `{message}` added to an image.")


@listener(outgoing=True, command="ocr",
          description="Extract text from attached image of replied message.")
async def ocr(context):
    """ Extracts texts from images. """
    reply = await context.get_reply_message()
    await context.edit("`Processing image, please wait . . .`")
    if reply:
        target_file_path = await context.client.download_media(
            await context.get_reply_message()
        )
    else:
        target_file_path = await context.download_media()
    if target_file_path is None:
        await context.edit("`There are no attachment in target.`")
        return
    result = await execute(f"tesseract {target_file_path} stdout")
    if not result:
        await context.edit("`Something wrong happened, please report this problem.`")
        try:
            remove(target_file_path)
        except FileNotFoundError:
            pass
        return
    success = False
    if result == "/bin/sh: fbdump: command not found":
        await context.edit("A utility is missing.")
    else:
        result = await execute(f"tesseract {target_file_path} stdout", False)
        await context.edit(f"**Extracted text: **\n{result}")
        success = True
    remove(target_file_path)
    if not success:
        return


@listener(outgoing=True, command="highlight",
          description="Generates syntax highlighted images.",
          parameters="<string>")
async def highlight(context):
    """ Generates syntax highlighted images. """
    if context.fwd_from:
        return
    reply = await context.get_reply_message()
    reply_id = None
    await context.edit("Rendering image, please wait . . .")
    if reply:
        reply_id = reply.id
        target_file_path = await context.client.download_media(
            await context.get_reply_message()
        )
        if target_file_path is None:
            message = reply.text
        else:
            if Magic(mime=True).from_file(target_file_path) != 'text/plain':
                message = reply.text
            else:
                with open(target_file_path, 'r') as file:
                    message = file.read()
            remove(target_file_path)
    else:
        if context.arguments:
            message = context.arguments
        else:
            await context.edit("`Unable to retrieve target message.`")
            return
    lexer = guess_lexer(message)
    formatter = img.JpgImageFormatter(style="colorful")
    result = syntax_highlight(message, lexer, formatter, outfile=None)
    await context.edit("Uploading image . . .")
    await context.client.send_file(
        context.chat_id,
        result,
        reply_to=reply_id
    )
    await context.delete()


async def handle_failure(context, target_file_path):
    await context.edit("Something wrong happened, please report this problem.")
    try:
        remove("result.png")
        remove(target_file_path)
    except FileNotFoundError:
        pass
