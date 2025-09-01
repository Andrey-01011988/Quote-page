from django.core.management.base import BaseCommand
from django.db import transaction
from quotes.models import Quote, Source
import random

class Command(BaseCommand):
    help = 'Добавляет 30 тестовых цитат в базу данных'

    def handle(self, *args, **options):
        # Создаем источники
        sources_data = [
            {'name': 'Война и мир', 'type': 'book'},
            {'name': 'Преступление и наказание', 'type': 'book'},
            {'name': 'Мастер и Маргарита', 'type': 'book'},
            {'name': 'Гарри Поттер', 'type': 'book'},
            {'name': 'Властелин колец', 'type': 'book'},
            {'name': 'Крестный отец', 'type': 'movie'},
            {'name': 'Зеленая миля', 'type': 'movie'},
            {'name': 'Форрест Гамп', 'type': 'movie'},
            {'name': 'Назад в будущее', 'type': 'movie'},
            {'name': 'Титаник', 'type': 'movie'},
            {'name': 'Аристотель', 'type': 'other'},
            {'name': 'Цицерон', 'type': 'other'},
            {'name': 'Конфуций', 'type': 'other'},
            {'name': 'Сократ', 'type': 'other'},
        ]

        sources = []
        for source_data in sources_data:
            source, created = Source.objects.get_or_create(
                name=source_data['name'],
                defaults={'type': source_data['type']}
            )
            sources.append(source)
            self.stdout.write(self.style.SUCCESS(f'Создан источник: {source.name}'))

        # Цитаты для заполнения
        quotes_data = [
            {'text': 'Чем меньше человеку нужно, тем ближе он к богам.', 'source': 'Сократ'},
            {'text': 'Познай самого себя.', 'source': 'Сократ'},
            {'text': 'Я знаю, что ничего не знаю.', 'source': 'Сократ'},
            {'text': 'Век живи — век учись.', 'source': 'Цицерон'},
            {'text': 'Бумага все стерпит.', 'source': 'Цицерон'},
            {'text': 'Краткость — сестра таланта.', 'source': 'Цицерон'},
            {'text': 'Не откладывай на завтра то, что можно сделать сегодня.', 'source': 'Аристотель'},
            {'text': 'Привычка — вторая натура.', 'source': 'Аристотель'},
            {'text': 'Платон мне друг, но истина дороже.', 'source': 'Аристотель'},
            {'text': 'Ученье — свет, а неученье — тьма.', 'source': 'Конфуций'},
            {'text': 'Не дай вам Бог жить в эпоху перемен.', 'source': 'Конфуций'},
            {'text': 'Выбери себе работу по душе, и тебе не придется работать ни одного дня в своей жизни.', 'source': 'Конфуций'},
            {'text': 'Все счастливые семьи похожи друг на друга, каждая несчастливая семья несчастлива по-своему.', 'source': 'Война и мир'},
            {'text': 'Сила могущества не в силе, а в неустанном стремлении.', 'source': 'Война и мир'},
            {'text': 'Человек предназначен для жизни в обществе; он не вполне человек и противоречит своей сущности, если живет отшельником.', 'source': 'Война и мир'},
            {'text': 'Человек — это всего лишь тростинка, слабейшее из творений природы, но это тростинка мыслящая.', 'source': 'Преступление и наказание'},
            {'text': 'Страдание и боль всегда обязательны для широкого сознания и глубокого сердца.', 'source': 'Преступление и наказание'},
            {'text': 'Во всем есть черта, за которую перейти опасно; ибо, раз переступив, воротиться назад невозможно.', 'source': 'Преступление и наказание'},
            {'text': 'Рукописи не горят.', 'source': 'Мастер и Маргарита'},
            {'text': 'Никогда ничего не просите! Никогда и ничего, и в особенности у тех, кто сильнее вас.', 'source': 'Мастер и Маргарита'},
            {'text': 'Трусость — самый страшный порок.', 'source': 'Мастер и Маргарита'},
            {'text': 'Счастье можно найти даже в темные времена, если не забывать обращаться к свету.', 'source': 'Гарри Поттер'},
            {'text': 'Мы все должны столкнуться с выбором между тем, что правильно, и тем, что легко.', 'source': 'Гарри Поттер'},
            {'text': 'Не мечтай, а действуй.', 'source': 'Гарри Поттер'},
            {'text': 'Даже самая маленькая личность может изменить ход будущего.', 'source': 'Властелин колец'},
            {'text': 'Не все те странники, кто сбился с пути.', 'source': 'Властелин колец'},
            {'text': 'Я предлагаю вам тост. За то, чтобы у вас был друг.', 'source': 'Крестный отец'},
            {'text': 'Дружба — это всё. Дружба превыше таланта. Сильнее любого правительства.', 'source': 'Крестный отец'},
            {'text': 'Жизнь как коробка конфет: никогда не знаешь, какая начинка тебе попадется.', 'source': 'Форрест Гамп'},
            {'text': 'Беги, Форрест, беги!', 'source': 'Форрест Гамп'},
        ]

        created_count = 0
        with transaction.atomic():
            for quote_data in quotes_data:
                # Находим источник по имени
                source = next((s for s in sources if s.name == quote_data['source']), None)
                if not source:
                    self.stdout.write(self.style.WARNING(f'Источник не найден: {quote_data["source"]}'))
                    continue

                # Проверяем, не превышен ли лимит цитат для источника
                existing_quotes_count = Quote.objects.filter(source=source).count()
                if existing_quotes_count >= 3:
                    self.stdout.write(self.style.WARNING(
                        f'Пропускаем цитату для "{source.name}" - достигнут лимит в 3 цитаты'
                    ))
                    continue

                # Создаем цитату
                quote, created = Quote.objects.get_or_create(
                    text=quote_data['text'],
                    defaults={
                        'source': source,
                        'weight': random.randint(1, 10),  # Случайный вес от 1 до 10
                        'views': random.randint(0, 100),  # Случайное количество просмотров
                        'likes': random.randint(0, 50),   # Случайное количество лайков
                        'dislikes': random.randint(0, 10) # Случайное количество дизлайков
                    }
                )

                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'Добавлена цитата: {quote.text[:50]}...'))

        self.stdout.write(self.style.SUCCESS(
            f'Успешно добавлено {created_count} цитат из {len(quotes_data)}'
        ))
