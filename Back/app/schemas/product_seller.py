from typing import Optional
from pydantic import BaseModel, Field
from Back.app.schemas.product_line import ProductLine


class ProductSeller(BaseModel):
  id_product_seller: Optional[int] = None
  id_product:int 
  id_seller:int 
  quantity:int =Field(gt=0)
  price:float =Field(ge=0)
  shipping_costs:float=Field(ge=0)
  #shopping_cart_products: list[InShoppingCart]=[]
  #wish_list_products: list[InWishList]=[]
  product_lines: list[ProductLine]=[]

  class Config:
    orm_mode=True


 