from fastapi import APIRouter

from app.api.deps import CardServiceDep, CurrentUserDep
from app.schemas.users.card import Card, CardCreate, CardUpdate

# router = APIRouter(prefix="/buyers/{buyer_id}/cards", tags=["Cards"])


# @router.get("/", response_model=list[Card])
# async def read_cards(*, buyer_id: int, card_service: CardServiceDep):
#     """
#     Retrieve cards from buyer.
#     """
#     return card_service.get_by_id_buyer(id_buyer=buyer_id)


# @router.post("/", response_model=Card)
# async def create_card(*, buyer_id: int, card: CardCreate, card_service: CardServiceDep):
#     """
#     Create a new card for the buyer.
#     """
#     return card_service.add(id_buyer=buyer_id, card=card)


# @router.delete("/")
# async def delete_cards(buyer_id: int, card_service: CardServiceDep):
#     """
#     Delete all cards from a buyer.
#     """
#     return card_service.delete_all_by_id_buyer(id_buyer=buyer_id)


# @router.get("/{card_id}", response_model=Card)
# async def read_card(*, buyer_id: int, card_id: int, card_service: CardServiceDep):
#     """
#     Retrieve a specific buyer card.
#     """

#     card = card_service.get_by_id(card_id)

#     if card is None or card.id_buyer != buyer_id:
#         raise HTTPException(status_code=404, detail="Card not found")

#     return card


# @router.put("/{card_id}", response_model=Card)
# async def update_card(
#     *,
#     buyer_id=int,
#     card_id: int,
#     card: CardUpdate,
#     card_service: CardServiceDep,
# ):
#     """
#     Update a card.
#     """
#     existing_card = card_service.get_by_id(card_id)

#     if existing_card is None or existing_card.id_buyer != int(buyer_id):
#         raise HTTPException(status_code=404, detail="Card not found")

#     return card_service.update(card_id=card_id, new_data=card)


# @router.delete("/{card_id}")
# async def delete_card(*, buyer_id=int, card_id: int, card_service: CardServiceDep):
#     """
#     Delete a card.
#     """
#     existing_card = card_service.get_by_id(card_id)

#     if existing_card is None or existing_card.id_buyer != int(buyer_id):
#         raise HTTPException(status_code=404, detail="Card not found")

#     return card_service.delete_by_id(card_id)


cards_router = APIRouter(prefix="/cards/me", tags=["Cards"])


@cards_router.get("/", response_model=list[Card])
async def read_my_cards(current_user: CurrentUserDep, card_service: CardServiceDep):
    """
    Retrieve cards from the current user.
    """
    return card_service.get_by_user(current_user)


@cards_router.get("/{card_id}", response_model=Card)
async def read_my_card(
    card_id: int, current_user: CurrentUserDep, card_service: CardServiceDep
):
    """
    Retrieve a specific card from the current user.
    """
    return card_service.get_one_by_user(current_user, card_id)


@cards_router.delete("/")
async def delete_my_cards(current_user: CurrentUserDep, card_service: CardServiceDep):
    """
    Delete all cards from the current user.
    """
    card_service.delete_all_by_user(current_user)


@cards_router.post("/", response_model=Card)
async def create_my_card(
    card: CardCreate, current_user: CurrentUserDep, card_service: CardServiceDep
):
    """
    Create a new card for the current user.
    """
    return card_service.add_by_user(user=current_user, card=card)


@cards_router.put("/{card_id}", response_model=Card)
async def update_my_card(
    card_id: int,
    card: CardUpdate,
    current_user: CurrentUserDep,
    card_service: CardServiceDep,
):
    """
    Update a card from the current user.
    """
    return card_service.update_by_user(
        user=current_user, card_id=card_id, new_data=card
    )


@cards_router.delete("/{card_id}")
async def delete_my_card(
    card_id: int, current_user: CurrentUserDep, card_service: CardServiceDep
):
    """
    Delete a card from the current user.
    """
    return card_service.delete_one_by_user(card_id, current_user)
