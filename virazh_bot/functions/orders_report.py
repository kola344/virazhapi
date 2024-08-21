import csv
import db

async def report_orders():
    fieldnames = ["Номер заказа", "Текст заказа", "Дата заказа", "Доставить к", "Адрес", "Тип оплаты", "Сумма"]
    orders_data = await db.orders.get_orders_data_successful()
    data = []

    for order, i in enumerate(orders_data):
        data.append({
            "id": order+1,
            "Номер заказа": i["id"],
            "Текст заказа": i["text"],
            "Дата заказа": i["date"],
            "Доставить к": i["delivery_at"],
            "Адрес": i["address"],
            "Тип оплаты": i["payment"],
            "Сумма": i["price"]
        })

    with open("orders_report.csv", "w", newline="") as orders_file:
        writer = csv.DictWriter(orders_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    return