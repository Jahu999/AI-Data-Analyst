import pandas as pd

#Zdefiniowanie kolumn, które mają być konwertowane na typ daty
DATE_COLUMNS = ["Order Date", "Ship Date"]


def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()

    # Usunięcie spacji z nazw kolumn
    data.columns = [column.strip() for column in data.columns]

    # Konwersja dat.
    for column in DATE_COLUMNS:
        if column in data.columns:
            data[column] = pd.to_datetime(
                data[column],
                format="%m/%d/%Y",
                errors="coerce")

    # Kontrola brakujących wartości po konwersji
    if data.isnull().any().any():
        raise ValueError(
        "Wykryto brakujące wartości po czyszczeniu danych!"
    )

    # Zmiana typu danych w kolumnach liczbowych
    numeric_columns = ["Sales", "Quantity", "Discount", "Profit"]
    for column in numeric_columns:
        if column in data.columns:
            data[column] = pd.to_numeric(data[column], errors="coerce")

    # Usunięcie duplikatów
    data = data.drop_duplicates()

    # Kontrola minimalnych wymagań
    required = ["Order Date", "Sales", "Profit", "Category", "Region"]
    missing_columns = [col for col in required if col not in data.columns]
    if missing_columns:
        raise ValueError(f"Brakujące wymagane kolumny: {missing_columns}")

    return data


# Przegląd wyników czyszczenia danych, oraz zapisanie do pliku CSV
if __name__ == "__main__":
    from src.data_loader import load_data

    raw = load_data()
    cleaned_data = clean_data(raw)

    print("Przed czyszczeniem:", raw.shape)
    print("\nPo czyszczeniu:", cleaned_data.shape)
    print("\nBrakujące wartości po czyszczeniu:")
    print(cleaned_data.isnull().sum())
    cleaned_data.to_csv("data/processed/superstore_clean.csv", index=False)