import pandas as pd

#Zdefiniowanie KPI
def calculate_kpis(df: pd.DataFrame) -> dict:

    required_columns = ["Sales", "Profit", "Quantity", "Order ID"]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    total_sales = float(df["Sales"].sum())
    total_profit = float(df["Profit"].sum())
    total_quantity = int(df["Quantity"].sum())

    #Wiersz odpowiada jednaj pozycji zamówienia, a nie całemu zamówieniu, więc liczymy unikalne ID zamówień
    order_count = int(df["Order ID"].nunique())

    return {
        "total_sales": round(total_sales, 2),
        "total_profit": round(total_profit, 2),
        "total_quantity": total_quantity,
        "order_count": order_count,
        "profit_margin_pct": (
            round(total_profit / total_sales * 100, 2)
            if total_sales != 0 else None
        ),
    }

#Agregacja spzedaży i zysków według kategorii produktów
def sales_by_category(df: pd.DataFrame) -> pd.DataFrame:

    return (
        df.groupby("Category", as_index=False)
        .agg(
            sales=("Sales", "sum"),
            profit=("Profit", "sum"),
            quantity=("Quantity", "sum")
        )
        .sort_values("sales", ascending=False)
    )

#Agregacja spzedaży i zysków według miesięcy
def monthly_sales(df: pd.DataFrame) -> pd.DataFrame:

    if not pd.api.types.is_datetime64_any_dtype(df["Order Date"]):
        raise TypeError("Data zamówienia musi być w formacie daty!")

    data = df.copy()

    data["Month"] = data["Order Date"].dt.to_period("M").astype(str)

    return (
        data.groupby("Month", as_index=False)
        .agg(
            sales=("Sales", "sum"),
            profit=("Profit", "sum")
        )
        .sort_values("Month")
    )


#Przegląd wyników analizy danych
if __name__ == "__main__":

    from src.data_loader import load_data
    from src.data_cleaning import clean_data

    df = clean_data(load_data())

    print("KPI:")
    print(calculate_kpis(df))

    print("\nSales by category:")
    print(sales_by_category(df).round(2).to_string(index=False))

    print("\nMonthly sales:")
    print(monthly_sales(df).round(2).to_string(index=False))
