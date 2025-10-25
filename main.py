from Death_bot import death_bot
from TOKEN  import BOT_TOKEN



def main():
    try:
        print("🔍 DEBUG: Main function started")
        bot = death_bot(BOT_TOKEN)
        print("🔍 DEBUG: Bot created, starting...")
        bot.run()
    except Exception as e:
        print(f"Error: {e}")

        
if __name__ == "__main__":
    main()