""" Fun related chat utilities. """

import asyncio

from random import seed
from random import choice
from random import random
from random import randint
from random import randrange
from jarvis import command_help
from jarvis.events import register


@register(pattern='-animate(?: |$)(.*)')
async def animate(context):
    """ Command for animated texts. """
    if not context.text[0].isalpha() and context.text[0] not in ("/", "#", "@", "!"):
        text = await context.get_reply_message()
        message = context.pattern_match.group(1)
        if message:
            pass
        elif text:
            message = text.text
        else:
            await context.edit("`Invalid argument.`")
            return
        sleep_time = 0.03
        typing_symbol = "█"
        old_text = ''
        await context.edit(typing_symbol)
        await asyncio.sleep(sleep_time)
        for character in message:
            old_text = old_text + "" + character
            typing_text = old_text + "" + typing_symbol
            await context.edit(typing_text)
            await asyncio.sleep(sleep_time)
            await context.edit(old_text)
            await asyncio.sleep(sleep_time)


@register(outgoing=True, pattern="^-mock(?: |$)(.*)")
async def mock(context):
    """ Mock people with weird caps. """
    if not context.text[0].isalpha() and context.text[0] not in ("/", "#", "@", "!"):
        text = await context.get_reply_message()
        message = context.pattern_match.group(1)
        if message:
            pass
        elif text:
            message = text.text
        else:
            await context.edit("`Invalid arguments.`")
            return

        result = mocker(message)
        await context.edit(result)


@register(outgoing=True, pattern="^-widen(?: |$)(.*)")
async def widen(context):
    """ Make texts weirdly wide. """
    if not context.text[0].isalpha() and context.text[0] not in ("/", "#", "@", "!"):
        text = await context.get_reply_message()
        message = context.pattern_match.group(1)
        if message:
            pass
        elif text:
            message = text.text
        else:
            await context.edit("`Invalid argument.`")
            return

        reply_text = str(message).translate(dict((i, i + 0xFEE0) for i in range(0x21, 0x7F)))
        await context.edit(reply_text)


@register(outgoing=True, pattern="^-fox(?: |$)(.*)")
async def fox(context):
    """ Make a fox scratch your message. """
    if not context.text[0].isalpha() and context.text[0] not in ("/", "#", "@", "!"):
        text = await context.get_reply_message()
        message = context.pattern_match.group(1)
        if message:
            pass
        elif text:
            message = text.text
        else:
            await context.edit(
                "`Invalid arguments.`"
            )
            return

        input_text = " ".join(message).lower()
        corrupted_text = corrupt(input_text)
        await context.edit(corrupted_text)


@register(outgoing=True, pattern=r"^-owo(?: |$)([\s\S]*)")
async def owo(context):
    """ Makes messages become owo. """
    if not context.text[0].isalpha() and context.text[0] not in ("/", "#", "@", "!"):
        if context.reply_to_msg_id:
            reply_msg = await context.get_reply_message()
            if reply_msg.sender.is_self:
                await reply_msg.edit(owoifier(reply_msg.text))
                await context.delete()
            else:
                await context.edit(owoifier(reply_msg.text))
            return
        elif context.pattern_match.group(1):
            text = context.pattern_match.group(1)
            await context.edit(owoifier(text))
        else:
            await context.edit("`Unable to get the target message.`")
            return


def last_replace(s, old, new):
    """ Helper util for owoifier. """
    li = s.rsplit(old, 1)
    return new.join(li)


def owoifier(text):
    """ Converts your text to OwO """
    smileys = [';;w;;', '^w^', '>w<', 'UwU', '(・`ω\´・)', '(´・ω・\`)']

    text = text.replace('L', 'W').replace('l', 'w')
    text = text.replace('R', 'W').replace('r', 'w')

    text = last_replace(text, '!', '! {}'.format(choice(smileys)))
    text = last_replace(text, '?', '? owo')
    text = last_replace(text, '.', '. {}'.format(choice(smileys)))

    for v in ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']:
        if 'n{}'.format(v) in text:
            text = text.replace('n{}'.format(v), 'ny{}'.format(v))
        if 'N{}'.format(v) in text:
            text = text.replace('N{}'.format(v), 'N{}{}'.format('Y' if v.isupper() else 'y', v))

    return text


def mocker(text, diversity_bias=0.5, random_seed=None):
    if diversity_bias < 0 or diversity_bias > 1:
        raise ValueError('diversity_bias must be between the inclusive range [0,1]')
    seed(random_seed)
    out = ''
    last_was_upper = True
    swap_chance = 0.5
    for c in text:
        if c.isalpha():
            if random() < swap_chance:
                last_was_upper = not last_was_upper
                swap_chance = 0.5
            c = c.upper() if last_was_upper else c.lower()
            swap_chance += (1 - swap_chance) * diversity_bias
        out += c
    return out


def corrupt(text):
    """ Summons fox to scratch strings. """
    num_accents_up = (1, 3)
    num_accents_down = (1, 3)
    num_accents_middle = (1, 2)
    max_accents_per_letter = 3
    dd = ['̖', ' ̗', ' ̘', ' ̙', ' ̜', ' ̝', ' ̞', ' ̟', ' ̠', ' ̤', ' ̥', ' ̦', ' ̩', ' ̪', ' ̫', ' ̬', ' ̭', ' ̮',
          ' ̯', ' ̰', ' ̱', ' ̲', ' ̳', ' ̹', ' ̺', ' ̻', ' ̼', ' ͅ', ' ͇', ' ͈', ' ͉', ' ͍', ' ͎', ' ͓', ' ͔', ' ͕',
          ' ͖', ' ͙', ' ͚', ' ', ]
    du = [' ̍', ' ̎', ' ̄', ' ̅', ' ̿', ' ̑', ' ̆', ' ̐', ' ͒', ' ͗', ' ͑', ' ̇', ' ̈', ' ̊', ' ͂', ' ̓', ' ̈́', ' ͊',
          ' ͋', ' ͌', ' ̃', ' ̂', ' ̌', ' ͐', ' ́', ' ̋', ' ̏', ' ̽', ' ̉', ' ͣ', ' ͤ', ' ͥ', ' ͦ', ' ͧ', ' ͨ', ' ͩ',
          ' ͪ', ' ͫ', ' ͬ', ' ͭ', ' ͮ', ' ͯ', ' ̾', ' ͛', ' ͆', ' ̚', ]
    dm = [' ̕', ' ̛', ' ̀', ' ́', ' ͘', ' ̡', ' ̢', ' ̧', ' ̨', ' ̴', ' ̵', ' ̶', ' ͜', ' ͝', ' ͞', ' ͟', ' ͠', ' ͢',
          ' ̸', ' ̷', ' ͡', ]
    letters = list(text)
    new_letters = []

    for letter in letters:
        a = letter

        if not a.isalpha():
            new_letters.append(a)
            continue

        num_accents = 0
        num_u = randint(num_accents_up[0], num_accents_up[1])
        num_d = randint(num_accents_down[0], num_accents_down[1])
        num_m = randint(num_accents_middle[0], num_accents_middle[1])
        while num_accents < max_accents_per_letter and num_u + num_m + num_d != 0:
            rand_int = randint(0, 2)
            if rand_int == 0:
                if num_u > 0:
                    a = combine_with_diacritic(a, du)
                    num_accents += 1
                    num_u -= 1
            elif rand_int == 1:
                if num_d > 0:
                    a = combine_with_diacritic(a, dd)
                    num_d -= 1
                    num_accents += 1
            else:
                if num_m > 0:
                    a = combine_with_diacritic(a, dm)
                    num_m -= 1
                    num_accents += 1

        new_letters.append(a)

    new_word = ''.join(new_letters)
    return new_word


def combine_with_diacritic(letter, diacritic_list):
    """ The fox. """
    return letter.strip() + diacritic_list[randrange(0, len(diacritic_list))].strip()


command_help.update({
    "animate": "Parameter: -animate <text>\
    \nUsage: Animated text."
})

command_help.update({
    "mock": "Parameter: -mock <text>\
    \nUsage: Mock a string via weird caps."
})

command_help.update({
    "widen": "Parameter: -widen <text>\
    \nUsage: Widen every char in a string in a weird way."
})

command_help.update({
    "fox": "Parameter: -fox <text>\
    \nUsage: Make a fox corrupt your text."
})

command_help.update({
    "owo": "Parameter: -owo <text>\
    \nUsage: Converts messages to OwO."
})
