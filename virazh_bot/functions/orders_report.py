import csv
import db
from openpyxl import Workbook

async def report_orders():
    fieldnames = ["id", "Номер заказа", "Телефон", "Дата заказа", "Доставить к", "Адрес", "Тип оплаты", "Сумма"]
    orders_data = await db.orders.get_orders_data_successful()
    data = []
    price = 0
    for order, i in enumerate(orders_data):
        price += i["price"]
        data.append({
            "id": order+1,
            "Номер заказа": i["id"],
            "Телефон": i["text"][-10:],
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

    wb = Workbook()
    ws = wb.active
    with open('orders_report.csv', 'r', encoding='utf-8') as f:
        for row in csv.reader(f):
            ws.append(row)
    wb.save('orders_report.xlsx')

    return price, price//len(orders_data), len(orders_data)
