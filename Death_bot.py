from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from datetime import datetime
import re
from Days_bf_death import Days_before_Death


ENTER_BIRTHDATE, CHOOSE_GENDER, CHOOSE_COUNTRY= range(3)
class death_bot:
     def __init__(self,token:str):
         print(f"🔍 DEBUG: Bot __init__ called with token: {token[:10]}...")
         self.token = token
         self.app = Application.builder().token(token).build()
         self.setup_handlers()
         self.user_data = {}

     def setup_handlers(self):
        print("🔍 DEBUG: Setting up handlers...")
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states={
                ENTER_BIRTHDATE: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.receive_birthdate)

                ],
                CHOOSE_GENDER: [
                    MessageHandler(filters.Regex('^(Male|Female)$'), self.receive_gender)

                ],
                CHOOSE_COUNTRY: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.receive_country)
                ]
},
                
                fallbacks=[CommandHandler('cancel', self.cancel)],
        )
        self.app.add_handler(conv_handler)
        self.app.add_handler(CommandHandler("help", self.help))
        self.app.add_handler(CommandHandler("cancel", self.cancel))
        print("🔍 DEBUG: Handlers setup completed")  

        
     async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print("🔍 DEBUG: /start command received")
        """Вывожу приветствие"""
        welcome_text = """
    **Бот расчитывает продолжительность жизни**

    я помогу вам, понять сколько дней вам примерно осталось жить.

    **Введите вашу дату рождения в формате ДД/ММ/ГГГГ**

    Пример 11/09/2011

"""
        context.user_data.clear()
        await update.message.reply_text(welcome_text, 
                                        reply_markup=ReplyKeyboardRemove())
        return ENTER_BIRTHDATE
    
     async def receive_birthdate(self, update:Update, context:ContextTypes.DEFAULT_TYPE):
         
         user_input = update.message.text.strip()
         try:
             if not re.match(r'\d{2}/\d{2}/\d{4}', user_input):
                 await update.message.reply_text("Неверный формат даты!")
                 return ENTER_BIRTHDATE
             
             birth_date = datetime.strptime(user_input, "%d/%m/%Y")
             cur_date = datetime.now()

             if birth_date > cur_date:
                 await update.message.reply_text("Указана дата рождения еще не наступившегро дня")
                 return ENTER_BIRTHDATE
             
             lived_days = (cur_date - birth_date).days
             if lived_days > 365 * 120:
                 await update.message.reply_text("Да вы прям динозавр! А если честно?")
                 return ENTER_BIRTHDATE
             
             context.user_data['birthdate'] = user_input
             context.user_data['birth_date_obj'] = birth_date

             keyboard = [
                 ["Male", "Female"]
             ]
             reply_markup = ReplyKeyboardMarkup(
                 keyboard,
                 resize_keyboard=True,
                 one_time_keyboard=True,
                 input_field_placeholder="Выберите ваш пол"
                                                )
             
             await update.message.reply_text(
                            "✅ Дата рождения принята!\n\n👥 **Теперь выберите ваш пол:**",
                            reply_markup=reply_markup
                        )

             return CHOOSE_GENDER
         

         except ValueError as e:
             await update.message.reply_text("Ошибка в дате!")
             return ENTER_BIRTHDATE
         

     async def receive_gender(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
         
         gender_choice = update.message.text
         gender = 'm' if gender_choice == "Male" else 'f'
            
         context.user_data['gender'] = gender

         
   

         try:
            await update.message.reply_text("✅ гендер принят!\n\n👥 **Теперь выберите вашу страну:**")
            return CHOOSE_COUNTRY
         
         except Exception as e:
             await update.message.reply_text("Ошибка расчета, попробуйте снова: /start")
             return ConversationHandler.END
         

     async def receive_country(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
         self.country = update.message.text
         context.user_data['country'] = self.country

         await self.show_results(update, context)
         return ConversationHandler.END
     





     
     async def show_results(self, update: Update, context: ContextTypes.DEFAULT_TYPE):  
    # Получаем все данные
        birthdate = context.user_data.get('birthdate')
        gender = context.user_data.get('gender')
        country = context.user_data.get('country')

    
    # Рассчитываем результат
        calculator = Days_before_Death(birthdate, gender, country)
        
        result = calculator.calc_days_before_death()
        
        # Показываем результат
        await update.message.reply_text(
            result,
            reply_markup=ReplyKeyboardMarkup([["/start - Новый расчет"]], resize_keyboard=True),
            parse_mode='Markdown'
        )      



     async def help(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
         await update.message.reply_text("Для пользование ботом напиши дату своего рождение и пол в формате 'ДД/ММ/ГГГГ gender(M/F)', бот выведет сколько вам осталось примерно жить")


     async def cancel(self, update: Update, context:ContextTypes.DEFAULT_TYPE):
         await update.message.reply_text(
             "Операция отменена.",
             reply_markup=ReplyKeyboardRemove()
         )
         return ConversationHandler.END
     
     

     def run(self):
        print("bot is start polling")
        try:
        # Правильный запуск для версии 20.x
            self.app.run_polling(
            poll_interval=1.0,
            timeout=10,
            drop_pending_updates=True,
            allowed_updates=None
        )
        except Exception as e:
            print(f"Polling error: {e}")

                


