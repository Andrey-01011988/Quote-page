from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum, F
from django.contrib import messages
from django.core.exceptions import ValidationError
import random
from .models import Quote
from .forms import QuoteForm

def random_quote(request):
    """
    Возвращает случайную цитату

    Args:
        request (HttpRequest): Запрос

    Returns:
        HttpResponse: Страница с случайной цитатой
    """
    total_weight = Quote.objects.aggregate(total=Sum('weight'))['total']
    if total_weight:
        random_index = random.randint(1, total_weight)
        current = 0
        for quote in Quote.objects.all():
            current += quote.weight
            if current >= random_index:
                break
    else:
        quote = None
    
    if quote:
        quote.views += 1
        quote.save()
    
    return render(request, 'quotes/random_quote.html', {'quote': quote})


def like_quote(request, quote_id):
    """
    Увеличивает количество лайков для указанной цитаты

    Args:
        request (HttpRequest): Запрос
        quote_id (int): Идентификатор цитаты

    Returns:
        JsonResponse: JSON-ответ с обновленными количествами лайков и дизлайков
    """
    quote = get_object_or_404(Quote, id=quote_id)
    quote.likes += 1
    quote.save()
    return JsonResponse({'likes': quote.likes, 'dislikes': quote.dislikes})

def dislike_quote(request, quote_id):
    """
    Увеличивает количество дизлайков для указанной цитаты

    Args:
        request (HttpRequest): Запрос
        quote_id (int): Идентификатор цитаты

    Returns:
        JsonResponse: JSON-ответ с обновленными количествами лайков и дизлайков    
    """
    quote = get_object_or_404(Quote, id=quote_id)
    quote.dislikes += 1
    quote.save()
    return JsonResponse({'likes': quote.likes, 'dislikes': quote.dislikes})

def top_quotes(request):
    """
    Возвращает список самых популярных цитат

    Args:
        request (HttpRequest): Запрос

    Returns:
        HttpResponse: Страница с самыми популярными цитатами
    """
    top_quotes = Quote.objects.annotate(
        like_ratio=F('likes') * 1.0 / (F('likes') + F('dislikes'))
    ).order_by('-likes')[:10]
    
    # Добавляем вычисленный like_ratio к каждому объекту для использования в шаблоне
    for quote in top_quotes:
        total = quote.likes + quote.dislikes
        quote.like_ratio = quote.likes / total if total > 0 else 0
    
    return render(request, 'quotes/top_quotes.html', {'quotes': top_quotes})


def add_quote(request):
    """
    Добавляет новую цитату с обработкой ошибок

    Args:       
        request (HttpRequest): Запрос    

    Returns:
        HttpResponse: Страница с формой для добавления цитаты
    """
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Цитата успешно добавлена!')
                return redirect('random_quote')
            except ValidationError as e:
                # Добавляем ошибки валидации в форму
                for field, errors in e.error_dict.items():
                    for error in errors:
                        if field == '__all__':
                            form.add_error(None, error)
                        else:
                            form.add_error(field, error)
                messages.error(request, 'Ошибка при добавлении цитаты. Проверьте введенные данные.')
            except Exception as e:
                form.add_error(None, f'Произошла непредвиденная ошибка: {str(e)}')
                messages.error(request, 'Произошла ошибка при сохранении цитаты.')
    else:
        form = QuoteForm()
    
    return render(request, 'quotes/add_quote.html', {
        'form': form,
        'error_messages': messages.get_messages(request)
    })
