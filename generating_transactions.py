import pandas as pd
import re


def process_bank_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    exact_headers = {
        "дата и время", "операции", "дата", "списания",
        "сумма в валюте", "сумма операции", "в валюте карты",
        "описание", "номер", "карты"
    }

    data = []
    current_desc = []
    current_date = None
    current_amount = None

    for line in lines:
        line_clean = re.sub(r'\\s*', '', line).strip()

        if not line_clean:
            continue

        line_lower = line_clean.lower()

        if line_lower in exact_headers:
            continue

        if "тбанк" in line_lower or "бик" in line_lower or "инн" in line_lower:
            continue
        if line_clean.isdigit() and len(line_clean) < 3:
            continue

        if re.match(r"^\d{2}:\d{2}$", line_clean):
            continue

        if re.match(r"^\d{2}\.\d{2}\.\d{4}$", line_clean):
            if current_amount is not None:
                if current_desc and current_desc[-1].isdigit() and len(current_desc[-1]) == 4:
                    current_desc.pop()

                data.append({
                    'Дата': current_date,
                    'Сумма': current_amount,
                    'Описание': " ".join(current_desc)
                })

                current_amount = None
                current_desc = []
                current_date = line_clean

            elif current_date is None:
                current_date = line_clean
            continue

        amount_match = re.search(r'-([\d\s]+[\.,]\d+)\s*₽', line_clean)

        if amount_match and current_amount is None:
            raw_amount = amount_match.group(1).replace(' ', '').replace(',', '.')
            current_amount = float(raw_amount)

            text_part = line_clean.split('₽')[-1].strip()
            if text_part:
                current_desc.append(text_part)
            continue

        if current_amount is not None:
            current_desc.append(line_clean)

    if current_date and current_amount is not None:
        if current_desc and current_desc[-1].isdigit() and len(current_desc[-1]) == 4:
            current_desc.pop()
        data.append({'Дата': current_date, 'Сумма': current_amount, 'Описание': " ".join(current_desc)})

    return pd.DataFrame(data)


df = process_bank_file(r"C:\Users\HUAWEI\Downloads\транзакции.txt")


def clean_for_ml(text):
    text = re.sub(r'[^а-яёa-z\s]', ' ', text, flags=re.IGNORECASE)

    garbage = ['tomsk', 'rus', 'оплата', 'в', 'moskva', 'г', 'ул']
    for g in garbage:
        text = re.sub(rf'\b{g}\b', '', text, flags=re.IGNORECASE)

    return " ".join(text.split())

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', None)

df['Очищенное_описание'] = df['Описание'].apply(clean_for_ml)
print(df.head())