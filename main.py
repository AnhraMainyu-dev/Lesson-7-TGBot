import ptbot
import os
from pytimeparse import parse
from dotenv import load_dotenv
load_dotenv()

TG_TOKEN = os.environ['TELEGRAM_API']
BOT = ptbot.Bot(TG_TOKEN)


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


def notify_progress(secs_left, chat_id, message_id, progress):
    BOT.update_message(
        chat_id,
        message_id,
        "У вас осталось {} cекунд.\n{}".format(
            secs_left,
            render_progressbar(progress, progress-secs_left)))
    if secs_left == 0:
        BOT.send_message(chat_id, "Время вышло!")


def answer(chat_id, secs):
    progress = parse(secs)
    progressbar = render_progressbar(progress, 0)
    message_id = BOT.send_message(
        chat_id,
        "Запускаю таймер:\n {}.".format(progressbar)
    )
    BOT.create_countdown(
        parse(secs),
        notify_progress,
        chat_id=chat_id,
        message_id=message_id,
        progress=progress
    )


def main():
    BOT.reply_on_message(answer)
    BOT.run_bot()


if __name__ == '__main__':
    main()
