## Readability

***
### ENG infomation.

A script for creating a convenient form for reading news sites, in which there are no ads,
unnecessary markers and most of the unnecessary information for the user.

Before starting work, you need to make sure that the libraries specified in
the "requirements.txt" file are installed.\
And also Python version 3.6+.

The script is run from the command line with the specified python package,
as well as the -u prefix and the required site for parsing.
>python3 readability.py -u URL_SITES

The readability.py module, taking the -u key as an argument and the URL, 
calls the function from the url_request.py module.

The url_request.py module contains the get_text_form function and 
ParserNews with the main functionality:

* run - Start function as well as start all functions.
* url_parser - Function to parse a site using BeautifulSoup on HTML tags.
* text_convector - Function of preparing the text taken from the <p> tags, 
as well as preparing it for writing to the final file.
* name_file - Function of preparing the name of a new file, 
as well as collecting the necessary directories
* directory_create - Creating directories along the formed chain, checking for its presence.
* with_file - Recording of the prepared text formed according to the necessary criteria 
(the length of the lines is no more than 80 characters, the urls were not cut but inserted
additionally, and the site tabulation was also observed).

***
### RUS infomation.

Скрипт для создания удобной формы чтения новостных сайтов, на которых нет рекламы,
ненужные маркеры и большая часть ненужной информации для пользователя.

Перед началом работы необходимо убедиться, что библиотеки, указанные в "requirements.txt"
установлены. А также Python версии 3.6+.

Скрипт запускается из командной строки с указанным пакетом python,
а также префикс -u и необходимый сайт для разбора.
> python3 readability.py -u URL_SITES

Модуль readability.py, принимая ключ -u в качестве аргумента и URL-адрес,
вызывает функцию из модуля url_request.py.

Модуль url_request.py содержит функцию get_text_form и
ParserNews с основным функционалом:
* run - Запуск функции, а также запуск всех функций.
* url_parser - Функция для анализа сайта с помощью BeautifulSoup по тегам HTML.
* text_convector - Функция подготовки текста, взятого из тегов <'p'>, 
а также подготовка к записи в окончательный файл.
* name_file - Функция подготовки имени нового файла,
а также сбор необходимых справочников
* directory_create - Создание директорий по сформированной цепочке, проверка на ее наличие.
* with_file - Запись подготовленного текста, сформированного по необходимым критериям
(длина строк не более 80 символов, адреса не вырезаны, а вставлены
кроме того, и табуляция сайта также соблюдалась).
