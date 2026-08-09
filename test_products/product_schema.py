from datetime import datetime
from pydantic import BaseModel, Field

"""
Schema used to validate retrieved objects. 
"""

class DimensionsSchema(BaseModel):
    width: float = Field(gt=0)
    height: float = Field(gt=0)
    depth: float = Field(gt=0)

class ReviewSchema(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str
    date: datetime
    reviewerName: str
    reviewerEmail: str

class MetaSchema(BaseModel):
    createdAt: datetime
    updatedAt: datetime
    barcode: str
    qrCode: str

class ProductSchema(BaseModel):
    id: int
    title: str
    description: str
    category: str
    price: float = Field(gt=0)
    discountPercentage: float = Field(ge=0, le=100)
    rating: float = Field(ge=0, le=5)
    stock: int = Field(ge=0)
    tags: list[str]
    dimensions: DimensionsSchema
    warrantyInformation: str
    shippingInformation: str
    availabilityStatus: str
    reviews: list[ReviewSchema]
    returnPolicy: str
    minimumOrderQuantity: int = Field(ge=1)
    meta: MetaSchema
    thumbnail: str
    images: list[str]