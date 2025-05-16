from app.domain.menu_item import MenuItem
from app.messages.responses.menu_item_response_dto import MenuItemResponseDTO


def menu_item_to_response(menu_item: MenuItem) -> MenuItemResponseDTO:
    return MenuItemResponseDTO(
        id=menu_item.id,
        name=menu_item.name,
        description=menu_item.description,
        size=menu_item.size,
        price=menu_item.price
    )


def menu_list_to_response(menu_items: list[MenuItem]) -> list[MenuItemResponseDTO]:
    return [menu_item_to_response(item) for item in menu_items]
