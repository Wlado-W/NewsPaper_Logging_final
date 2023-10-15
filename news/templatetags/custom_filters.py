from django import template

censor_words = ["Свинья", "Далбон", "Ушлепок"]

register = template.Library()  # если мы не зарегестрируем наши фильтры,


# то django никогда не узнает где именно их искать и фильтры потеряются :(

@register.filter(name='censor')  # регистрируем наш фильтр под именем censor,
# чтоб django понимал, что это именно фильтр, а не простая функция

def censor(censor_text):  # первый аргумент здесь — это то значение, к которому надо применить фильтр,
    # второй аргумент — это аргумент фильтра, т.е. примерно следующее будет в шаблоне value|multiply:arg
    for word in censor_words:
        censor_text = censor_text.lower().replace(word.lower(),
                                                  '*censor*')  # переводим в строчные буквы, заменяем на *censor*
    return censor_text  # возвращаемое функцией значение — это то значение, которое подставится к нам в шаблон