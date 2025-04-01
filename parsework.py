import requests
from bs4 import BeautifulSoup
import html


def get_text(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/58.0.3029.110 Safari/537.36",
        "Accept": "application/json",
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    main_content = soup.find('div', class_='item center menC')  # Измените на нужный тег и класс

    if not main_content:
        print("Основной контент не найден.")
        return []  # Возвращаем пустой список, если контент не найден

    # Список для хранения абзацев
    paragraphs = []

    # Переменная для отслеживания предыдущего типа элемента
    prev_element_type = None

    # Проходим по всем дочерним элементам контейнера
    for element in main_content.children:
        # Если элемент является текстовым блоком
        if element.name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            if element.get_text(strip=True) in ("НазадСодержаниеВперед",
                                                "СодержаниеВперед",
                                                "НазадСодержание"):
                break
            else:
                # Добавляем отступ, если предыдущий элемент был другого типа
                if prev_element_type not in ['text', None]:
                    paragraphs.append("\n")  # Пустая строка для отступа

                # Обрабатываем текст с учетом <span class="b">
                text = ""
                for content in element.contents:
                    if (content.name == 'span' and 'b' in content.get('class', [])) or (content.name == 'code'):
                        # Если это <span class="b">, оборачиваем текст в <b>
                        text += f"<b>{html.escape(content.get_text(strip=True))}</b>"
                    elif content.name == 'a':
                        if content.get('href'):
                            text += (f"<a href='https:{content.get('href')}'>"
                                     f"{html.escape(content.get_text(strip=True))}</a>")
                        else:
                            text += f"<a>{html.escape(content.get_text(strip=True))}</a>"
                    elif content.name == 'span' and 'ii' in content.get('class', []):
                        text += f"<i>{html.escape(content.get_text(strip=True))}</i>"
                    else:
                        # Иначе просто добавляем текст
                        text += html.escape(str(content))

                if prev_element_type not in ['code', None]:
                    paragraphs.append("\n")  # Пустая строка для отступа
                    # Добавляем текст
                if element.name == "h1":
                    paragraphs.append("\n")
                    paragraphs.append(f"<strong>{text}</strong>\n")
                elif element.name in ['h2', 'h3', 'h4', 'h5', 'h6']:
                    paragraphs.append("\n")
                    paragraphs.append(f"<strong>{text}</strong>\n")
                else:
                    paragraphs.append(f"{text}\n")
                prev_element_type = 'text'  # Обновляем тип предыдущего элемента

        # Если элемент содержит код
        elif element.name in ['pre', 'code']:
            # Обертываем код в теги <pre><code>
            code = html.escape(element.get_text(strip=True))
            paragraphs.append(f"<pre><code>{code}</code></pre>\n")
            prev_element_type = 'code'

        elif element.name == 'ul':
            text = ""
            # Обрабатываем каждый элемент списка
            for li in element.find_all('li'):
                for p in li.find_all('p'):
                    a = p.find('a')
                    if a:
                        if a.get('href'):
                            text += f"<a href='{a.get('href')}'>{html.escape(a.get_text(strip=True))}</a>"
                        else:
                            text += f"<a>{html.escape(a.get_text(strip=True))}</a>"
                    else:
                        text += f"{html.escape(p.get_text(strip=True))}"
                        # Добавляем маркер для элемента списка
                paragraphs.append(f"  • {text}\n")
                text = ""
            prev_element_type = 'text'

        elif element.name == 'img':
            src = (element.get('src', '')).replace("./", "https://metanit.com/python/tutorial/")
            if src:
                paragraphs.append(f"{src}\n")
            prev_element_type = 'text'

        # Если элемент содержит другие вложенные элементы (например, <div>)
        elif element.name is not None:
            # Рекурсивно обрабатываем вложенные элементы
            for sub_element in element.children:
                if sub_element.name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    if sub_element.get_text(strip=True) in ("НазадСодержаниеВперед",
                                                            "СодержаниеВперед",
                                                            "НазадСодержание"):
                        break
                    else:
                        # Добавляем отступ, если предыдущий элемент был другого типа
                        if prev_element_type not in ['text', None]:
                            paragraphs.append("\n")  # Пустая строка для отступа

                        # Обрабатываем текст с учетом <span class="b">
                        text = ""
                        for content in sub_element.contents:
                            if (content.name == 'span' and 'b' in content.get('class', [])) or (content.name == 'code'):
                                # Если это <span class="b">, оборачиваем текст в <b>
                                text += f"<b>{html.escape(content.get_text(strip=True))}</b>"
                            elif content.name == 'a':
                                if content.get('href'):
                                    text += (f"<a href='https:{content.get('href')}'>"
                                             f"{html.escape(content.get_text(strip=True))}</a>")
                            elif content.name == 'span' and 'ii' in content.get('class', []):
                                text += f"<i>{html.escape(content.get_text(strip=True))}</i>"
                            else:
                                # Иначе просто добавляем текст
                                text += html.escape(str(content))

                        if prev_element_type not in ['code', None]:
                            paragraphs.append("\n")  # Пустая строка для отступа
                        # Добавляем текст
                        if sub_element.name == "h1":
                            paragraphs.append("\n")
                            paragraphs.append(f"<strong>{text}</strong>\n")
                        elif sub_element.name in ['h2', 'h3', 'h4', 'h5', 'h6']:
                            paragraphs.append("\n")
                            paragraphs.append(f"<strong>{text}</strong>\n")
                        else:
                            paragraphs.append(f"{text}\n")
                        prev_element_type = 'text'

                elif sub_element.name in ['pre', 'code']:
                    # Обертываем код в теги <pre><code>
                    code = html.escape(sub_element.get_text(strip=True))
                    paragraphs.append(f"<pre><code>{code}</code></pre>\n")
                    prev_element_type = 'code'

                elif sub_element.name == 'ul':
                    text = ""
                    # Обрабатываем каждый элемент списка
                    for li in element.find_all('li'):
                        for p in li.find_all('p'):
                            a = p.find('a')
                            if a:
                                if a.get('href'):
                                    text += f"<a href='{a.get('href')}'>{html.escape(a.get_text(strip=True))}</a>"
                                else:
                                    text += f"<a>{html.escape(a.get_text(strip=True))}</a>"
                            else:
                                text += f"{html.escape(str(p.get_text(strip=True)))}"
                                # Добавляем маркер для элемента списка
                        paragraphs.append(f"  • {text}\n")
                        text = ""
                    prev_element_type = 'text'

                elif sub_element.name == 'img':
                    src = (sub_element.get('src', '')).replace("./", "https://metanit.com/python/tutorial/")
                    if src:
                        paragraphs.append(f"{src}\n")
                    prev_element_type = 'text'

    # Разделяем текст на части по абзацам, если он слишком длинный
    max_length = 4096  # Максимальная длина сообщения в Telegram
    parts = []
    current_part = ""

    for paragraph in paragraphs:
        if "/pics/" in paragraph:
            if current_part:
                parts.append(current_part)
                current_part = ""
            parts.append(paragraph)
        else:
            # Если добавление текущего абзаца превышает максимальную длину
            if len(current_part) + len(paragraph) > max_length:
                # Если текущая часть не пустая, добавляем её в список частей
                if current_part:
                    parts.append(current_part)
                # Начинаем новую часть с текущего абзаца
                current_part = paragraph
            else:
                current_part += paragraph

    # Добавляем последнюю часть, если она не пустая
    if current_part:
        parts.append(current_part)

    return parts
