from datetime import datetime

class Days_before_Death:

    def __init__(self, date_str: str, gender:str, country):
     self.country = country
     self.life_expectancy = {
    'Russia': {'male': 68, 'female': 78},
    'USA': {'male': 76, 'female': 81},
    'Japan': {'male': 81, 'female': 87},
    'Germany': {'male': 79, 'female': 83},
    'World': {'male': 70, 'female': 75}}
     self.current_date = datetime.now()
     self.birth_date = datetime.strptime(date_str, "%d/%m/%Y")
     self.gender = gender.lower()

     try:
        self.avg_male_live = self.life_expectancy[country]['male'] * 365
        self.avg_female_live = self.life_expectancy[country]['female'] * 365
     except Exception as e:
         print(f"Ошибка! {e}, Нет такой страны")
         
     self.lived_days = (self.current_date - self.birth_date).days

    
    def calc_days_before_death(self):
        if self.gender in ['m', 'м']:
            days_left = self.avg_male_live - self.lived_days
            gender_text = "Мужчина"
            avg_years = self.life_expectancy[self.country]['male'] 
        else:
            days_left = self.avg_female_live - self.lived_days
            gender_text = "Женщина"
            avg_years = self.life_expectancy[self.country]['female'] 

        years_left = days_left // 365
        months_left = (days_left%365)//30
        remaining_days = days_left % 30

        current_age = self.lived_days // 365
        life_percentage = (current_age/avg_years) * 100
        your_country = self.country

        if days_left < 0:
            return f"""
 **ПОЗДРАВЛЯЕМ!** 

Вы превысили среднюю продолжительность жизни!

**Статистика:**
- Пол: {gender_text}
- Текущий возраст: {current_age} лет
- Прожито дней: {self.lived_days:,}
- Средняя продолжительность: {avg_years} лет
- Вы уже прожили на {abs(days_left)} дней больше!

**Так держать! Желаем вам долгих лет жизни!**
            """
        



        return f"""
📊 **РЕЗУЛЬТАТ РАСЧЕТА**

👤 **Ваши данные:**
- Пол: {gender_text}
- Возраст: {current_age} лет
- Прожито дней: {self.lived_days:,}

⏳ **ОСТАЛОСЬ ЖИТЬ:**
- Всего дней: {days_left:,}
- Лет: {years_left}
- Месяцев: {months_left}
- Дней: {remaining_days}

📈 **Прогресс жизни:** {life_percentage:.1f}%

💡 *На основе статистики в {your_country} {gender_text.replace('а', 'ы')} живут в среднем: {avg_years} лет*

🔄 Новый расчет: /start
        """