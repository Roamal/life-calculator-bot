from datetime import datetime
from who_statistic import getLiveByCountrySex


class Days_before_Death:

    def __init__(self, date_str: str, gender: str, country: str):
        self.country = country.lower()
        self.gender = gender.lower()
        self.current_date = datetime.now()
        self.birth_date = datetime.strptime(date_str, "%d/%m/%Y")
        self.lived_days = (self.current_date - self.birth_date).days
        

        self.avg_live_years = None
        self.avg_live_days = None
        self.life_data = None
        


    def calc_days_before_death(self):
        try:
            self.life_data = getLiveByCountrySex(self.country, self.gender)
            self.avg_live_years = self.life_data.HowMuchRemained()
            self.avg_live_days = self.avg_live_years * 365
            
        except Exception as e:
            return f"Ошибка! {e}, Нет такой страны"

        # Проверяем, что данные были успешно получены
        if self.avg_live_days is None or self.avg_live_years is None:
            return "❌ Ошибка: Не удалось получить данные о продолжительности жизни для указанной страны и пола."
        
        days_left = self.avg_live_days - self.lived_days
       
        if self.gender in ['m', 'м']:
            gender_text = "Мужчина" 
        else: 
            gender_text = "Женщина"
            
        years_left = days_left // 365 
        months_left = (days_left % 365) // 30
        remaining_days = (days_left % 365) % 30

        current_age = self.lived_days // 365
        life_percentage = (current_age / self.avg_live_years) * 100
        
        # Красивое форматирование страны
        your_country = self.country.capitalize()

        if days_left < 0:
            return f"""
🎉 **ПОЗДРАВЛЯЕМ!** 

Вы превысили среднюю продолжительность жизни!

**Статистика:**
- Пол: {gender_text}
- Текущий возраст: {current_age} лет
- Прожито дней: {self.lived_days:,}
- Средняя продолжительность: {self.avg_live_years} лет
- Вы уже прожили на {abs(int(days_left)):,} дней больше!

**Так держать! Желаем вам долгих лет жизни!**
            """

        return f"""
📊 **РЕЗУЛЬТАТ РАСЧЕТА**

👤 **Ваши данные:**
- Пол: {gender_text}
- Возраст: {current_age} лет
- Прожито дней: {self.lived_days:,}

⏳ **ОСТАЛОСЬ ЖИТЬ:**
- Всего дней: {int(days_left):,}
- Лет: {int(years_left)}
- Месяцев: {int(months_left)}
- Дней: {int(remaining_days)}

📈 **Прогресс жизни:** {life_percentage:.1f}%

💡 *На основе статистики в {your_country} {gender_text.replace('а', 'ы')} живут в среднем: {self.avg_live_years} лет*

🔄 Новый расчет: /start
        """

    def get_raw_data(self):
        """Возвращает сырые данные для отладки"""
        return {
            'country': self.country,
            'gender': self.gender,
            'lived_days': self.lived_days,
            'avg_live_years': self.avg_live_years,
            'avg_live_days': self.avg_live_days,
            'current_age': self.lived_days // 365
        }