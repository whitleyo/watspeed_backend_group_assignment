from typing import List, Optional
from app.daos.menu_dao import MenuDAO
from app.domain.menu_item import MenuItem
from app.messages.responses.menu_item_response_dto import MenuItemResponseDTO
from app.mappers.menu_mapper import menu_item_to_response, menu_list_to_response
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

class MenuService:
    """
    Service layer for managing menu operations.
    """

    def __init__(self, menu_dao: MenuDAO):
        """Initialize service with DAO."""
        self.menu_dao = menu_dao

    def get_menu_item(self, item_id: int) -> Optional[MenuItemResponseDTO]:
        """Retrieve menu item by ID and convert to response DTO."""
        menu_item = self.menu_dao.find(item_id)
        return menu_item_to_response(menu_item) if menu_item else None

    def get_all_menu_items(self) -> List[MenuItemResponseDTO]:
        """Retrieve all menu items and convert them to DTOs."""
        menu_items = self.menu_dao.findAll()
        return menu_list_to_response(menu_items)
    
    def add_menu_item(self, menu_item: MenuItem) -> MenuItemResponseDTO:
        """Add a new menu item and return response DTO."""
        saved_item = self.menu_dao.save(menu_item)
        return menu_item_to_response(saved_item)

    def update_menu_item(self, item_id: int, menu_item: MenuItem) -> MenuItemResponseDTO:
        """update a menu item and return response DTO."""
        saved_item = self.menu_dao.update(item_id, menu_item)
        return menu_item_to_response(saved_item) if saved_item else None

    def remove_menu_item(self, item_id: int) -> None:
        """Delete a menu item."""
        self.menu_dao.delete(item_id)

    def generate_menu_pdf(self) -> bytes:
        """
        Generate a PDF menu from all menu items and return the PDF as bytes.
        """
        menu_items = self.get_all_menu_items()  # List[MenuItemResponseDTO]
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(width / 2, height - 60, "Cafe Watspeed Menu")

        c.setFont("Helvetica", 14)
        y = height - 120
        for item in menu_items:
            c.drawString(72, y, f"{item.name} - ${item.price:.2f}")
            c.setFont("Helvetica-Oblique", 12)
            c.drawString(90, y - 16, item.description)
            c.setFont("Helvetica", 14)
            y -= 40
            if y < 80:
                c.showPage()
                y = height - 60

        c.save()
        buffer.seek(0)
        return buffer.getvalue()
