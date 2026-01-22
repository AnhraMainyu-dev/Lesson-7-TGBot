import ptbot
from pytimeparse import parse
from decouple import config

TG_TOKEN = config('TELEGRAM_API')


def render_progressbar(
        total,
        iteration,
        prefix='',
        suffix='',
        length=30,
        fill='█',
        zfill='░'
):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(secs_left, chat_id, message_id, progress, bot):
    bot.update_message(
        chat_id,
        message_id,
        "У вас осталось {} cекунд.\n{}".format(
            secs_left,
            render_progressbar(progress, progress-secs_left)))
    if secs_left == 0:
        bot.send_message(chat_id, "Время вышло!")


def answer(chat_id, secs, bot):
    progress = parse(secs)
    progressbar = render_progressbar(progress, 0)
    message_id = bot.send_message(
        chat_id,
        "Запускаю таймер:\n {}.".format(progressbar)
    )
    bot.create_countdown(
        parse(secs),
        notify_progress,
        chat_id=chat_id,
        message_id=message_id,
        progress=progress,
        bot = bot
    )


def main():
    bot = ptbot.Bot(TG_TOKEN)
    bot.reply_on_message(answer, bot=bot)
    bot.run_bot()


if __name__ == '__main__':
    main()
