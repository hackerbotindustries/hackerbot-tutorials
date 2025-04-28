from hackerbot import Hackerbot
import time

# ====== ACTIONS ======

def shake_head(bot):
    bot.head.look(180, 180, 70)
    time.sleep(1)
    look_left(bot)
    look_right(bot)
    bot.head.look(180,180,70)
    time.sleep(1)

def nod_head(bot):
    bot.head.look(180, 180, 100)
    time.sleep(1)
    look_up(bot)
    look_down(bot)
    bot.head.look(180, 180, 100)
    time.sleep(1)

def look_left(bot):
    bot.head.look(130, 180, 100)
    time.sleep(1)

def look_right(bot):
    bot.head.look(230, 180, 100)
    time.sleep(1)

def look_up(bot):
    bot.head.look(180, 230, 100)
    time.sleep(1)

def look_down(bot):
    bot.head.look(180, 170, 100)
    time.sleep(1)

def spin_right(bot):
    bot.base.drive(0, 65)

def spin_left(bot):
    bot.base.drive(0, -65)

def spin_around(bot):
    bot.base.drive(0, 130)

def speak(bot, text):
    bot.head.speak(model_src="../models/en_GB-semaine-medium.onnx", text=text, speaker_id=2)


def main():
    bot = Hackerbot(verbose_mode=True)
    shake_head(bot)
    nod_head(bot)
    spin_right(bot)
    spin_left(bot)
    spin_around(bot)
    bot.base.destroy()

if __name__ == "__main__":
    main()