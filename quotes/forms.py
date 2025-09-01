# from django import forms
# from django.core.exceptions import ValidationError
# from .models import Quote, Source

# class QuoteForm(forms.ModelForm):
#     """
#     Форма для создания цитаты

#     Attributes:
#         source_name (str): Название источника
#         source_type (str): Тип источника

#     Methods:
#         save(): Сохранение цитаты
#     """
#     source_name = forms.CharField(max_length=200, label='Название источника')
#     source_type = forms.ChoiceField(
#         choices=Source.type_choices,
#         label='Тип источника'
#     )

#     class Meta:
#         model = Quote
#         fields = ['text', 'weight']
#         widgets = {
#             'text': forms.Textarea(attrs={'rows': 4}),
#             'weight': forms.NumberInput(attrs={'min': 1}),
#         }

#     def clean_text(self):
#         """
#         Проверяет, что цитата с таким текстом еще не существует
#         """
#         text = self.cleaned_data.get('text')
#         if text:
#             # Проверяем, существует ли уже цитата с таким текстом
#             if Quote.objects.filter(text__iexact=text).exists():
#                 raise forms.ValidationError('Цитата с таким текстом уже существует!')
#         return text

#     def clean(self):
#         cleaned_data = super().clean()
#         source_name = cleaned_data.get('source_name')
#         source_type = cleaned_data.get('source_type')
#         text = cleaned_data.get('text')

#         # Если есть ошибки в отдельных полях, не продолжаем валидацию
#         if self.errors:
#             return cleaned_data
        
#         if source_name and source_type:
#             source, created = Source.objects.get_or_create(
#                 name=source_name,
#                 defaults={'type': source_type}
#             )
            
#             quote_id = self.instance.id if self.instance else None
#             existing_count = Quote.objects.filter(source=source).exclude(id=quote_id).count()

#             if existing_count >= 3:
#                 raise ValidationError(f'У источника "{source_name}" уже есть 3 цитаты. Максимальное количество достигнуто.')
        
#         return cleaned_data

#     def save(self, commit=True):
#         source_name = self.cleaned_data['source_name']
#         source_type = self.cleaned_data['source_type']
        
#         source, created = Source.objects.get_or_create(
#             name=source_name,
#             defaults={'type': source_type}
#         )
        
#         quote = super().save(commit=False)
#         quote.source = source
        
#         if commit:
#             quote.save()
#         return quote
    
from django import forms
from django.core.exceptions import ValidationError
from .models import Quote, Source

class QuoteForm(forms.ModelForm):
    """
    Форма для создания цитаты

    Attributes:
        source_name (str): Название источника
        source_type (str): Тип источника

    Methods:
        clean_text(): Проверка на уникальность текста цитаты
        clean(): Общая валидация формы
        save(): Сохранение цитаты
    """
    source_name = forms.CharField(max_length=200, label='Название источника')
    source_type = forms.ChoiceField(
        choices=Source.type_choices,
        label='Тип источника'
    )

    class Meta:
        model = Quote
        fields = ['text', 'weight']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
            'weight': forms.NumberInput(attrs={'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем HTML5 атрибуты для клиентской валидации
        self.fields['weight'].widget.attrs.update({
            'min': 1,
            'max': 10
        })

    def clean_weight(self):
        """
        Проверяет, что вес цитаты находится в диапазоне 1-10
        """
        weight = self.cleaned_data.get('weight')
        if weight is not None:
            if weight < 1:
                raise ValidationError('Вес не может быть меньше 1')
            if weight > 10:
                raise ValidationError('Вес не может быть больше 10')
        return weight

    def clean_text(self):
        """
        Проверяет, что цитата с таким текстом еще не существует
        """
        text = self.cleaned_data.get('text')
        if text:
            # Проверяем, существует ли уже цитата с таким текстом
            if Quote.objects.filter(text__iexact=text).exists():
                raise ValidationError('Цитата с таким текстом уже существует!')
        return text

    def clean(self):
        """
        Общая валидация формы, проверка ограничения на количество цитат у источника
        """
        cleaned_data = super().clean()
        source_name = cleaned_data.get('source_name')
        source_type = cleaned_data.get('source_type')
        
        # Если есть ошибки в отдельных полях, не продолжаем валидацию
        if self.errors:
            return cleaned_data
            
        if source_name and source_type:
            source, created = Source.objects.get_or_create(
                name=source_name,
                defaults={'type': source_type}
            )
            
            # Проверяем ограничение на количество цитат у источника
            quote_id = self.instance.id if self.instance else None
            existing_count = Quote.objects.filter(source=source).exclude(id=quote_id).count()

            if existing_count >= 3:
                raise ValidationError({
                    'source_name': [
                        f'У источника "{source_name}" уже есть 3 цитаты. '
                        f'Максимальное количество достигнуто. '
                        f'Выберите другой источник или удалите существующие цитаты.'
                    ]
                })
        
        return cleaned_data

    def save(self, commit=True):
        """
        Сохранение цитаты с обработкой возможных ошибок
        """
        try:
            source_name = self.cleaned_data['source_name']
            source_type = self.cleaned_data['source_type']
            
            source, created = Source.objects.get_or_create(
                name=source_name,
                defaults={'type': source_type}
            )
            
            # Дополнительная проверка перед сохранением
            quote_id = self.instance.id if self.instance else None
            existing_count = Quote.objects.filter(source=source).exclude(id=quote_id).count()
            
            if existing_count >= 3:
                raise ValidationError(
                    f'У источника "{source_name}" уже есть 3 цитаты. '
                    f'Максимальное количество достигнуто.'
                )
            
            quote = super().save(commit=False)
            quote.source = source
            
            if commit:
                quote.save()
            return quote
            
        except ValidationError as e:
            # Пробрасываем ошибку дальше для обработки в view
            raise e
        except Exception as e:
            # Ловим любые другие ошибки
            raise ValidationError(f'Произошла ошибка при сохранении: {str(e)}')