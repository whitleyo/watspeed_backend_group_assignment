import os
import openpyxl
from openpyxl.styles import Font
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from app.mappers.order_mapper import order_to_response
from app.daos.order_dao import OrderDAO

class OrderXLSXService:
    """Service for managing orders with XLSX export capabilities."""
    
    def __init__(self, order_dao: OrderDAO):
        self.dao = order_dao
        self.export_folder = os.path.join(os.getcwd(), "exports")  # Define a sensible folder
        os.makedirs(self.export_folder, exist_ok=True)  # Ensure the folder exists

    def export_orders_to_xlsx(
        self, 
        file_name: Optional[str] = "orders.xlsx", 
        begin_datetime: Optional[str] = None, 
        end_datetime: Optional[str] = None
    ) -> str:
        """Exports filtered orders to an XLSX spreadsheet."""
        
        # Convert datetime strings to actual datetime objects
        begin_dt = datetime.fromisoformat(begin_datetime) if begin_datetime else None
        end_dt = datetime.fromisoformat(end_datetime) if end_datetime else None
        
        # Apply filtering logic
        query = self.dao.session.query(self.dao.findAll())
        if begin_dt:
            query = query.filter(Order.order_time >= begin_dt)
        if end_dt:
            query = query.filter(Order.order_time <= end_dt)

        orders = query.all()
        order_data = [order_to_response(order).dict() for order in orders]

        file_path = os.path.join(self.export_folder, file_name)
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Orders"

        # Add headers
        headers = ["Order ID", "Customer Name", "Status", "Order Time", "Items"]
        sheet.append(headers)
        for cell in sheet[1]:
            cell.font = Font(bold=True)

        # Add order data
        for order in order_data:
            sheet.append([
                order["id"], 
                order["customer_name"], 
                order["status"], 
                order["order_time"], 
                ", ".join([f"{item['menu_item_id']} (x{item['quantity']})" for item in order["order_items"]])
            ])

        workbook.save(file_path)
        return file_path