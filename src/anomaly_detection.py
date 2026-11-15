
import pandas as pd


def find_profit_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect potential profit outliers using the IQR method.
    """

    #Sprawdzenie, czy kolumna Profit istnieje w DataFrame
    if "Profit" not in df.columns:
        raise ValueError("Missing required column: Profit")

    #Sprawdzenie, czy DataFrame nie jest pusty
    if df.empty:
        raise ValueError("Input DataFrame is empty")

    #Sprawdzenie poprawności danych w kolumnie Profit, czy zawiera wartości numeryczne
    if not pd.api.types.is_numeric_dtype(df["Profit"]):
        raise TypeError("Profit column must contain numeric values")

    #Sprawdzenie poprawności danych w kolumnie Profit, czy nie zawiera brakujących wartości
    if df["Profit"].isna().any():
        raise ValueError("Profit column contains missing values")

    #Liczenie kwartylów i IQR dla detekcji anomalii
    q1 = df["Profit"].quantile(0.25)
    q3 = df["Profit"].quantile(0.75)
    iqr = q3 - q1

    #Liczenie granic IQR dla detekcji anomalii
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    #Identyfikacja potencjalnych anomalii w zysku
    result = df.loc[
        (df["Profit"] < lower) | (df["Profit"] > upper)
    ].copy()

    #Dodanie kolumny z powodem detekcji anomalii oraz granicami IQR
    result["anomaly_reason"] = "Profit outside IQR boundaries"
    result["iqr_lower_bound"] = lower
    result["iqr_upper_bound"] = upper

    return result

#Wyniki detekcji anmolaii, zapis do pliku csv, oraz wyświetlenie w konsoli pierwszych 20 rekordów potencjalnych anomalii
if __name__ == "__main__":

    from src.data_loader import load_data
    from src.data_cleaning import clean_data

    df = clean_data(load_data())

    anomalies = find_profit_outliers(df)

    print("Total records:", len(df))
    print("Potential profit outliers:", len(anomalies))

    print("\nFirst 20 potential outliers:")
    print(anomalies.head(20).to_string(index=False))

    anomalies.to_csv(
        "data/processed/profit_outliers.csv",
        index=False
    )


#Dzielenie potencjalnych anomalii na dolne i górne, oraz wyświetlenie liczby anomalii w każdej kategorii produktów
lower_outliers = anomalies[
    anomalies["Profit"] < anomalies["iqr_lower_bound"]
]

upper_outliers = anomalies[
    anomalies["Profit"] > anomalies["iqr_upper_bound"]
]

print("\nLower outliers:", len(lower_outliers))
print("Upper outliers:", len(upper_outliers))

print("\nOutliers by category:")
print(
    anomalies.groupby("Category").size()
    .sort_values(ascending=False)
)

#Kalkulacja wskaźnika anomalii w każdej kategorii produktów, oraz wyświetlenie wyników w konsoli
category_anomalies = anomalies.groupby("Category").size()

category_total = df.groupby("Category").size()

anomaly_rate = (
    category_anomalies / category_total * 100
).round(2)

print("\nAnomaly rate by category:")

print(
    anomaly_rate.sort_values(ascending=False)
    .to_string()
)

print("\nLower outliers by category:")
print(
    lower_outliers.groupby("Category").size()
)

print("\nUpper outliers by category:")
print(
    upper_outliers.groupby("Category").size()
)

#Analiza średniej zniżki wśród wszystkich rekordów, dolnych anomalii
print("\nAverage discount - lower outliers:")

print(
    lower_outliers.groupby("Category")["Discount"]
    .mean()
    .mul(100)
    .round(2)
)

#Porównanie średniej zniżki wśród wszystkich rekordów z średnią zniżką wśród górnych anomalii
print("\nAverage discount - all records:")

print(
    df.groupby("Category")["Discount"]
    .mean()
    .mul(100)
    .round(2)
)

#Średnia zniżka wśród górnych anomalii, oraz porównanie z wszystkimi rekordami
print("\nAverage discount - upper outliers:")

print(
    upper_outliers.groupby("Category")["Discount"]
    .mean()
    .mul(100)
    .round(2)
)

#Porównanie mediany zniżek w każdej kategorii produktów dla wszystkich rekordów, dolnych anomalii i górnych anomalii
print("\nMedian discount - all records:")
print(df.groupby("Category")["Discount"].median() * 100)

print("\nMedian discount - lower outliers:")
print(lower_outliers.groupby("Category")["Discount"].median() * 100)

print("\nMedian discount - upper outliers:")
print(upper_outliers.groupby("Category")["Discount"].median() * 100)