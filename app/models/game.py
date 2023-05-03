from pydantic import BaseModel, AnyUrl, Field


class Game(BaseModel):

    name: str
    description: str
    publisher: str

    discount_price: int = Field(alias='discountPrice')
    original_price: int = Field(alias='originalPrice')
    currency_code: str = Field(alias='currencyCode')

    offer_image_wide: AnyUrl = Field(alias='offerImageWide')
    offer_image_tall: AnyUrl = Field(alias='offerImageTall')

    app_url: AnyUrl = Field(alias="appUrl")
