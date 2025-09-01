from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Source(models.Model):
    """
    Модель источника

    Attributes:
        name (str): Название источника
        type (str): Тип источника

    Methods:
        __str__(): Вывод названия источника
    """
    name = models.CharField(max_length=200, unique=True)
    type_choices = [
        ('movie', 'Фильм'),
        ('book', 'Книга'),
        ('other', 'Другое'),
    ]
    type = models.CharField(max_length=10, choices=type_choices)

    def __str__(self):
        return self.name

class Quote(models.Model):
    """
    Модель цитаты

    Attributes:
        text (str): Текст цитаты
        source (Source): Источник цитаты
        weight (int): Вес цитаты
        views (int): Количество просмотров цитаты
        likes (int): Количество лайков цитаты
        dislikes (int): Количество дизлайков цитаты
        created_at (datetime): Дата создания цитаты

    Methods:
        __str__(): Вывод информации о цитате
        like_ratio(): Рассчет коэффициента лайков
        save(): Полная валидация при сохранении
    """
    text = models.TextField(unique=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    weight = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1, message='Вес не может быть меньше 1'),
            MaxValueValidator(10, message='Вес не может быть больше 10')
        ]
    )
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        # Вывод информации о цитате
        return f'"{self.text[:50]}..." - {self.source}'

    def like_ratio(self):
        # Рассчет коэффициента лайков        
        total = self.likes + self.dislikes
        return self.likes / total if total > 0 else 0
    
    def save(self, *args, **kwargs):
        """
        Выполняем полную валидацию при сохранении
        """
        self.full_clean()
        super().save(*args, **kwargs)
    