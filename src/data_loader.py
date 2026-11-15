from pathlib import Path
import pandas as pd

DATA_PATH = Path("data/raw/Sample - Superstore.csv")


#Załadowanie danych z pliku CSV
def load_data() -> pd.DataFrame:
    """
    Loads the Superstore dataset from a CSV file.
    """
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Data file not found at {DATA_PATH}"
        )
    
    
    #Zmiana kodowania na cp1252, oraz ustawienie typu danych dla kolumny "Postal Code" na string, aby uniknąć problemów z typami danych
    return pd.read_csv(
    DATA_PATH,
    encoding="cp1252",
    dtype={"Postal Code": "string"}
)


#Przegląd danych po wczytaniu, przed czyszczeniem
if __name__ == "__main__":
    data = load_data()

    print("Wymiary danych:", data.shape)
    print("\nKolumny danych:", data.columns.tolist())
    print("\nTypy i brakujące wartości w danych:")
    data.info()

    print("\nPierwsze rekordy danych:\n", data.head(10).to_string())

    print("\nStatystyki opisowe:")
    print(data.describe().to_string())

    print("\nLiczba duplikatów:")
    print(data.duplicated().sum())

    print("\nLiczba brakujących wartości:")
    print(data.isnull().sum())

    print("\nTypy danych w kolumnach:")
    print(data.dtypes)

    print("\nUnikalne wartości w kolumnach:")
    print(data.nunique())



    #test A
    print(
    data.groupby("Product ID")["Product Name"]
    .nunique()
    .sort_values(ascending=False)
    .head(10)
    )

    #test B
    print("Zakres dat zamówień:")

    print(data["Order Date"].min())
    print(data["Order Date"].max())

    print("\nPrzykładowe daty:")
    print(data["Order Date"].head(10).tolist())

