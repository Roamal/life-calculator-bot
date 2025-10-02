import Death_bot
from TOKEN  import BOT_TOKEN



def main():
    try:
        bot = Death_bot(BOT_TOKEN)
        bot.run()
    except Exception as e:
        print(f"Error: {e}")

        
if __name__ == "__main__":
    main()