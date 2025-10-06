# from fastapi import APIRouter, UploadFile, HTTPException, File, Form, Query, Request
# from fastapi.responses import JSONResponse
# from typing import Optional, List
# import os
# from datetime import datetime

# from .models import Category, SubCategory, Banner, Product, ProductImage

# router = APIRouter()
# UPLOAD_DIR = "uploads"


# # ---------------- Helper ----------------
# async def save_file(file: UploadFile, folder: str) -> str:
#     """Save uploaded file and return file path."""
#     os.makedirs(os.path.join(UPLOAD_DIR, folder), exist_ok=True)
#     filename = f"{datetime.now(timezone.utc).timestamp()}_{file.filename}"
#     filepath = os.path.join(UPLOAD_DIR, folder, filename)
#     with open(filepath, "wb") as f:
#         f.write(await file.read())
#     return filepath


# # ---------------- CATEGORY ----------------
# @router.post("/category/")
# async def create_category(name: str = Form(...), description: Optional[str] = Form(None), image: Optional[UploadFile] = File(None)):
#     category = Category(name=name, description=description)
#     if image:
#         category.image = await save_file(image, "categories")
#     await category.save()
#     return {"message": "Category created", "id": category.id}


# @router.put("/category/{id}/")
# async def update_category(id: int, name: str = Form(...), description: Optional[str] = Form(None), image: Optional[UploadFile] = File(None)):
#     category = await Category.get_or_none(id=id)
#     if not category:
#         raise HTTPException(status_code=404, detail="Category not found")
#     category.name = name
#     category.description = description
#     if image:
#         category.image = await save_file(image, "categories")
#     await category.save()
#     return {"message": "Category updated", "id": category.id}


# @router.get("/category/")
# async def list_categories():
#     return await Category.all()


# @router.get("/category/{id}/")
# async def get_category(id: int):
#     category = await Category.get_or_none(id=id)
#     if not category:
#         raise HTTPException(status_code=404, detail="Category not found")
#     return category


# @router.delete("/category/{id}/")
# async def delete_category(id: int):
#     category = await Category.get_or_none(id=id)
#     if not category:
#         raise HTTPException(status_code=404, detail="Category not found")
#     await category.delete()
#     return {"message": "Category deleted"}


# # ---------------- SUBCATEGORY ----------------
# @router.post("/subcategory/")
# async def create_subcategory(
#     category_id: int = Form(...),
#     name: str = Form(...),
#     description: Optional[str] = Form(None),
#     banner: Optional[UploadFile] = File(None),
#     image: Optional[UploadFile] = File(None),
#     popular: bool = Form(False),
# ):
#     sub = SubCategory(category_id=category_id, name=name, description=description, popular=popular)
#     if banner:
#         sub.banner = await save_file(banner, "subcategories")
#     if image:
#         sub.image = await save_file(image, "subcategories")
#     await sub.save()
#     return {"message": "SubCategory created", "id": sub.id}


# @router.put("/subcategory/{id}/")
# async def update_subcategory(
#     id: int,
#     category_id: int = Form(...),
#     name: str = Form(...),
#     description: Optional[str] = Form(None),
#     banner: Optional[UploadFile] = File(None),
#     image: Optional[UploadFile] = File(None),
#     popular: bool = Form(False),
# ):
#     sub = await SubCategory.get_or_none(id=id)
#     if not sub:
#         raise HTTPException(status_code=404, detail="SubCategory not found")
#     sub.category_id = category_id
#     sub.name = name
#     sub.description = description
#     sub.popular = popular
#     if banner:
#         sub.banner = await save_file(banner, "subcategories")
#     if image:
#         sub.image = await save_file(image, "subcategories")
#     await sub.save()
#     return {"message": "SubCategory updated", "id": sub.id}


# @router.get("/subcategory/")
# async def list_subcategories(category_id: Optional[int] = Query(None)):
#     qs = SubCategory.all()
#     if category_id:
#         qs = qs.filter(category_id=category_id)
#     return await qs


# @router.get("/subcategory/{id}/")
# async def get_subcategory(id: int):
#     sub = await SubCategory.get_or_none(id=id)
#     if not sub:
#         raise HTTPException(status_code=404, detail="SubCategory not found")
#     return sub


# @router.delete("/subcategory/{id}/")
# async def delete_subcategory(id: int):
#     sub = await SubCategory.get_or_none(id=id)
#     if not sub:
#         raise HTTPException(status_code=404, detail="SubCategory not found")
#     await sub.delete()
#     return {"message": "SubCategory deleted"}


# # ---------------- BANNER ----------------
# BANNER_OPTIONS = ["top_banner", "bottom_banner", "new_arrival", "hot_deals", "popular_products"]


# @router.post("/banner/")
# async def create_banner(position: str = Form(...), link: Optional[str] = Form(None), banner: UploadFile = File(...)):
#     if position not in BANNER_OPTIONS:
#         raise HTTPException(status_code=400, detail=f"Position must be one of {BANNER_OPTIONS}")
#     b = Banner(position=position, link=link, banner=await save_file(banner, "banners"))
#     await b.save()
#     return {"message": "Banner created", "id": b.id}


# @router.put("/banner/{id}/")
# async def update_banner(id: int, position: str = Form(...), link: Optional[str] = Form(None), banner: Optional[UploadFile] = File(None)):
#     b = await Banner.get_or_none(id=id)
#     if not b:
#         raise HTTPException(status_code=404, detail="Banner not found")
#     if position not in BANNER_OPTIONS:
#         raise HTTPException(status_code=400, detail=f"Position must be one of {BANNER_OPTIONS}")
#     b.position = position
#     b.link = link
#     if banner:
#         b.banner = await save_file(banner, "banners")
#     await b.save()
#     return {"message": "Banner updated", "id": b.id}


# @router.get("/banner/")
# async def list_banners(position: Optional[str] = Query(None)):
#     qs = Banner.all()
#     if position:
#         qs = qs.filter(position=position)
#     return await qs


# @router.get("/banner/{id}/")
# async def get_banner(id: int):
#     b = await Banner.get_or_none(id=id)
#     if not b:
#         raise HTTPException(status_code=404, detail="Banner not found")
#     return b


# @router.delete("/banner/{id}/")
# async def delete_banner(id: int):
#     b = await Banner.get_or_none(id=id)
#     if not b:
#         raise HTTPException(status_code=404, detail="Banner not found")
#     await b.delete()
#     return {"message": "Banner deleted"}


# # ---------------- PRODUCT ----------------
# @router.post("/product/")
# async def create_product(
#     subcategory_id: int = Form(...),
#     name: str = Form(...),
#     review: Optional[str] = Form(None),
#     details: Optional[str] = Form(None),
#     description: Optional[str] = Form(None),
#     stock: int = Form(0),
#     price: int = Form(...),
#     discount: float = Form(...),
#     box_price: int = Form(0),
#     weight: float = Form(...),
#     quantity: int = Form(1),
#     point: int = Form(0),
#     popular: bool = Form(False),
#     free_delivery: bool = Form(False),
#     hot_deals: bool = Form(False),
#     flash_sale: bool = Form(False),
#     tag: Optional[str] = Form("academic_books"),
# ):
#     p = Product(
#         subcategory_id=subcategory_id,
#         name=name,
#         review=review,
#         details=details,
#         description=description,
#         stock=stock,
#         price=price,
#         discount=discount,
#         box_price=box_price,
#         weight=weight,
#         quantity=quantity,
#         point=point,
#         popular=popular,
#         free_delivery=free_delivery,
#         hot_deals=hot_deals,
#         flash_sale=flash_sale,
#         tag=tag,
#     )
#     await p.save()
#     return {"message": "Product created", "id": p.id}


# @router.put("/product/{id}/")
# async def update_product(
#     id: int,
#     subcategory_id: int = Form(...),
#     name: str = Form(...),
#     review: Optional[str] = Form(None),
#     details: Optional[str] = Form(None),
#     description: Optional[str] = Form(None),
#     stock: int = Form(0),
#     price: int = Form(...),
#     discount: float = Form(...),
#     box_price: int = Form(0),
#     weight: float = Form(...),
#     quantity: int = Form(1),
#     point: int = Form(0),
#     popular: bool = Form(False),
#     free_delivery: bool = Form(False),
#     hot_deals: bool = Form(False),
#     flash_sale: bool = Form(False),
#     tag: Optional[str] = Form("academic_books"),
# ):
#     p = await Product.get_or_none(id=id)
#     if not p:
#         raise HTTPException(status_code=404, detail="Product not found")
#     p.subcategory_id = subcategory_id
#     p.name = name
#     p.review = review
#     p.details = details
#     p.description = description
#     p.stock = stock
#     p.price = price
#     p.discount = discount
#     p.box_price = box_price
#     p.weight = weight
#     p.quantity = quantity
#     p.point = point
#     p.popular = popular
#     p.free_delivery = free_delivery
#     p.hot_deals = hot_deals
#     p.flash_sale = flash_sale
#     p.tag = tag
#     await p.save()
#     return {"message": "Product updated", "id": p.id}


# @router.get("/product/")
# async def list_products(subcategory_id: Optional[int] = Query(None)):
#     qs = Product.all()
#     if subcategory_id:
#         qs = qs.filter(subcategory_id=subcategory_id)
#     return await qs


# @router.get("/product/{id}/")
# async def get_product(id: int):
#     p = await Product.get_or_none(id=id)
#     if not p:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return p


# @router.delete("/product/{id}/")
# async def delete_product(id: int):
#     p = await Product.get_or_none(id=id)
#     if not p:
#         raise HTTPException(status_code=404, detail="Product not found")
#     await p.delete()
#     return {"message": "Product deleted"}


# # ---------------- PRODUCT IMAGE ----------------
# @router.post("/product/image/")
# async def create_product_image(
#     product_id: int = Form(...),
#     color: Optional[str] = Form(None),
#     size: Optional[str] = Form(None),
#     image: UploadFile = File(...),
# ):
#     product = await Product.get_or_none(id=product_id)
#     if not product:
#         raise HTTPException(status_code=404, detail="Product not found")
#     img_path = await save_file(image, "products")
#     img = ProductImage(product=product, color=color, size=size, image=img_path)
#     await img.save()
#     return {"message": "Product image created", "id": img.id}


# @router.put("/product/image/{id}/")
# async def update_product_image(
#     id: int,
#     color: Optional[str] = Form(None),
#     size: Optional[str] = Form(None),
#     image: Optional[UploadFile] = File(None),
# ):
#     img = await ProductImage.get_or_none(id=id)
#     if not img:
#         raise HTTPException(status_code=404, detail="Image not found")
#     if color:
#         img.color = color
#     if size:
#         img.size = size
#     if image:
#         img.image = await save_file(image, "products")
#     await img.save()
#     return {"message": "Product image updated", "id": img.id}


# @router.get("/product/image/")
# async def list_product_images(product_id: Optional[int] = Query(None)):
#     qs = ProductImage.all()
#     if product_id:
#         qs = qs.filter(product_id=product_id)
#     return await qs


# @router.get("/product/image/{id}/")
# async def get_product_image(id: int):
#     img = await ProductImage.get_or_none(id=id)
#     if not img:
#         raise HTTPException(status_code=404, detail="Image not found")
#     return img


# @router.delete("/product/image/{id}/")
# async def delete_product_image(id: int):
#     img = await ProductImage.get_or_none(id=id)
#     if not img:
#         raise HTTPException(status_code=404, detail="Image not found")
#     await img.delete()
#     return {"message": "Product image deleted"}




from fastapi import APIRouter, HTTPException, Form, UploadFile, File, Request
from typing import List, Optional
from tortoise.contrib.pydantic import pydantic_model_creator
from datetime import datetime, timezone
import os

from .models import Category, SubCategory, Banner, Product, ProductImage

router = APIRouter()

# ==============================
# File Upload Helper
# ==============================
UPLOAD_DIR = "uploads"

async def save_file(file: UploadFile, folder: str) -> str:
    """Save uploaded file to folder inside UPLOAD_DIR and return path."""
    folder_path = os.path.join(UPLOAD_DIR, folder)
    os.makedirs(folder_path, exist_ok=True)  # Ensure folder exists

    # Unique filename
    filename = f"{datetime.now(timezone.utc).timestamp()}_{file.filename}"
    file_path = os.path.join(folder_path, filename)

    # Write file
    with open(file_path, "wb") as f:
        f.write(await file.read())

    return file_path

# ==============================
# CATEGORY
# ==============================
Category_Pydantic = pydantic_model_creator(Category, name="Category")

@router.post("/categories", response_model=Category_Pydantic, tags=["Categories"])
async def create_category(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    image: UploadFile = File(...),
):
    image_path = await save_file(image, "categories")
    obj = await Category.create(name=name, description=description, image=image_path)
    return await Category_Pydantic.from_tortoise_orm(obj)

@router.put("/categories/{id}", response_model=Category_Pydantic, tags=["Categories"])
async def update_category(
    id: int,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
):
    update_data = {k: v for k, v in {"name": name, "description": description}.items() if v is not None}
    if image:
        update_data["image"] = await save_file(image, "categories")
    await Category.filter(id=id).update(**update_data)
    return await Category_Pydantic.from_queryset_single(Category.get(id=id))

@router.get("/categories", response_model=List[Category_Pydantic], tags=["Categories"])
async def list_categories():
    return await Category_Pydantic.from_queryset(Category.all())

@router.get("/categories/{id}", response_model=Category_Pydantic, tags=["Categories"])
async def get_category(id: int):
    return await Category_Pydantic.from_queryset_single(Category.get(id=id))

@router.delete("/categories/{id}", tags=["Categories"])
async def delete_category(id: int):
    deleted = await Category.filter(id=id).delete()
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}

# ==============================
# SUBCATEGORY
# ==============================
SubCategory_Pydantic = pydantic_model_creator(SubCategory, name="SubCategory")

@router.post("/subcategories", response_model=SubCategory_Pydantic, tags=["SubCategories"])
async def create_subcategory(
    name: str = Form(...),
    category_id: int = Form(...),
    description: Optional[str] = Form(None),
    banner: Optional[UploadFile] = File(None),
    image: Optional[UploadFile] = File(None),
    popular: Optional[bool] = Form(False),
):
    obj_data = {
        "name": name,
        "category_id": category_id,
        "description": description,
        "popular": popular
    }

    if banner:
        obj_data["banner"] = await save_file(banner, "subcategories")
    if image:
        obj_data["image"] = await save_file(image, "subcategories")

    obj = await SubCategory.create(**obj_data)
    return await SubCategory_Pydantic.from_tortoise_orm(obj)



@router.put("/subcategories/{id}", response_model=SubCategory_Pydantic, tags=["SubCategories"])
async def update_subcategory(
    id: int,
    name: Optional[str] = Form(None),
    category_id: Optional[int] = Form(None),
    description: Optional[str] = Form(None),
    banner: Optional[UploadFile] = File(None),
    image: Optional[UploadFile] = File(None),
    popular: Optional[bool] = Form(None),
):
    update_data = {k: v for k, v in {
        "name": name,
        "category_id": category_id,
        "description": description,
        "popular": popular
    }.items() if v is not None}

    if banner:
        update_data["banner"] = await save_file(banner, "subcategories")
    if image:
        update_data["image"] = await save_file(image, "subcategories")

    await SubCategory.filter(id=id).update(**update_data)
    return await SubCategory_Pydantic.from_queryset_single(SubCategory.get(id=id))

@router.get("/subcategories", response_model=List[SubCategory_Pydantic], tags=["SubCategories"])
async def list_subcategories():
    return await SubCategory_Pydantic.from_queryset(SubCategory.all())

@router.get("/subcategories/{id}", response_model=SubCategory_Pydantic, tags=["SubCategories"])
async def get_subcategory(id: int):
    return await SubCategory_Pydantic.from_queryset_single(SubCategory.get(id=id))

@router.delete("/subcategories/{id}", tags=["SubCategories"])
async def delete_subcategory(id: int):
    deleted = await SubCategory.filter(id=id).delete()
    if not deleted:
        raise HTTPException(status_code=404, detail="SubCategory not found")
    return {"message": "SubCategory deleted successfully"}

# ==============================
# BANNER
# ==============================
Banner_Pydantic = pydantic_model_creator(Banner, name="Banner")

@router.post("/banners", response_model=Banner_Pydantic, tags=["Banners"])
async def create_banner(
    banner: UploadFile = File(...),
    position: str = Form("top_banner"),
    link: Optional[str] = Form(None),
):
    banner_path = await save_file(banner, "banners")
    obj = await Banner.create(banner=banner_path, position=position, link=link)
    return await Banner_Pydantic.from_tortoise_orm(obj)

@router.put("/banners/{id}", response_model=Banner_Pydantic, tags=["Banners"])
async def update_banner(
    id: int,
    banner: Optional[UploadFile] = File(None),
    position: Optional[str] = Form(None),
    link: Optional[str] = Form(None),
):
    update_data = {k: v for k, v in {"position": position, "link": link}.items() if v is not None}
    if banner:
        update_data["banner"] = await save_file(banner, "banners")
    await Banner.filter(id=id).update(**update_data)
    return await Banner_Pydantic.from_queryset_single(Banner.get(id=id))

@router.get("/banners", response_model=List[Banner_Pydantic], tags=["Banners"])
async def list_banners():
    return await Banner_Pydantic.from_queryset(Banner.all())

@router.get("/banners/{id}", response_model=Banner_Pydantic, tags=["Banners"])
async def get_banner(id: int):
    return await Banner_Pydantic.from_queryset_single(Banner.get(id=id))

@router.delete("/banners/{id}", tags=["Banners"])
async def delete_banner(id: int):
    deleted = await Banner.filter(id=id).delete()
    if not deleted:
        raise HTTPException(status_code=404, detail="Banner not found")
    return {"message": "Banner deleted successfully"}

# ==============================
# PRODUCT
# ==============================
Product_Pydantic = pydantic_model_creator(Product, name="Product")
class ProductOut(Product_Pydantic):
    new_arrival: bool
    todays_deals: bool
    discount_price: int
    sell_price: int

@router.post("/products", response_model=Product_Pydantic, tags=["Products"])
async def create_product(
    name: str = Form(...),
    subcategory_id: int = Form(...),
    price: int = Form(...),
    discount: int = Form(...),
    weight: float = Form(...),
    stock: int = Form(0),
    box_price: int = Form(0),
    ratings: float = Form(0),
    video_id: Optional[str] = Form(None),
    details: Optional[str] = Form(None),
    description: Optional[str] = Form(None),

    popular: Optional[bool] = Form(False),
    free_delivery: Optional[bool] = Form(False),
    hot_deals: Optional[bool] = Form(False),
    flash_sale: Optional[bool] = Form(False),
    tag: Optional[str] = Form("ladz"),
):
    obj = await Product.create(
        name=name,
        subcategory_id=subcategory_id,
        price=price,
        discount=discount,
        weight=weight,
        stock=stock,
        box_price=box_price,
        ratings=ratings,
        video_id=video_id,
        details=details,
        description=description,
        popular=popular,
        free_delivery=free_delivery,
        hot_deals=hot_deals,
        flash_sale=flash_sale,
        tag=tag,
    )
    return await Product_Pydantic.from_tortoise_orm(obj)

@router.put("/products/{slug}", response_model=Product_Pydantic, tags=["Products"])
async def update_product(
    slug: str,
    name: str = Form(...),
    subcategory_id: int = Form(...),
    price: int = Form(...),
    discount: int = Form(...),
    weight: float = Form(...),
    stock: int = Form(0),
    box_price: int = Form(0),
    point: int = Form(0),
    ratings: float = Form(0),
    video_id: Optional[str] = Form(None),
    details: Optional[str] = Form(None),
    description: Optional[str] = Form(None),

    popular: Optional[bool] = Form(False),
    free_delivery: Optional[bool] = Form(False),
    hot_deals: Optional[bool] = Form(False),
    flash_sale: Optional[bool] = Form(False),
    tag: Optional[str] = Form("ladz"),
):
    update_data = {k: v for k, v in locals().items() if k != "slug" and v is not None}
    await Product.filter(slug=slug).update(**update_data)
    return await Product_Pydantic.from_queryset_single(Product.get(slug=slug))



@router.get("/products", response_model=List[ProductOut], tags=["Products"])
async def list_products():
    products = await Product.all()
    return [
        ProductOut(
            **(await Product_Pydantic.from_tortoise_orm(p)).model_dump(),
            new_arrival=p.new_arrival,
            todays_deals=p.todays_deals,
            discount_price=p.discount_price,
            sell_price=p.sell_price,
        )
        for p in products
    ]
    


@router.get("/products/{slug}", response_model=ProductOut, tags=["Products"])
async def get_product(slug: str):
    product = await Product.get(slug=slug)
    base = await Product_Pydantic.from_tortoise_orm(product)
    return ProductOut(
        **base.model_dump(),
        new_arrival=product.new_arrival,
        todays_deals=product.todays_deals,
        discount_price=product.discount_price,
        sell_price=product.sell_price,
    )

@router.delete("/products/{slug}", tags=["Products"])
async def delete_product(slug: str):
    deleted = await Product.filter(slug=slug).delete()
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}



# ==============================
# PRODUCT IMAGE
# ==============================
ProductImage_Pydantic = pydantic_model_creator(ProductImage, name="ProductImage")



@router.post("/product-images", response_model=ProductImage_Pydantic, tags=["ProductImages"])
async def create_product_image(
    product_id: int = Form(...),
    color: Optional[str] = Form(None),
    size: Optional[str] = Form(None),
    image: UploadFile = File(...),
):
    image_path = await save_file(image, "product_images")
    obj = await ProductImage.create(
        product_id=product_id,
        color=color,
        size=size,
        image=image_path
    )
    return await ProductImage_Pydantic.from_tortoise_orm(obj)

@router.put("/product-images/{id}", response_model=ProductImage_Pydantic, tags=["ProductImages"])
async def update_product_image(
    id: int,
    product_id: Optional[int] = Form(None),
    color: Optional[str] = Form(None),
    size: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
):
    update_data = {k: v for k, v in locals().items() if k != "id" and v is not None}
    if image:
        update_data["image"] = await save_file(image, "product_images")

    await ProductImage.filter(id=id).update(**update_data)
    return await ProductImage_Pydantic.from_queryset_single(ProductImage.get(id=id))

@router.get("/product-images", response_model=List[ProductImage_Pydantic], tags=["ProductImages"])
async def list_product_images():
    return await ProductImage_Pydantic.from_queryset(ProductImage.all())

@router.get("/product-images/{id}", response_model=ProductImage_Pydantic, tags=["ProductImages"])
async def get_product_image(id: int):
    return await ProductImage_Pydantic.from_queryset_single(ProductImage.get(id=id))



@router.delete("/product-images/{id}", tags=["ProductImages"])
async def delete_product_image(id: int):
    deleted = await ProductImage.filter(id=id).delete()
    if not deleted:
        raise HTTPException(status_code=404, detail="ProductImage not found")
    return {"message": "ProductImage deleted successfully"}



@router.get("/product-images-list/{slug}", response_model=List[ProductImage_Pydantic], tags=["ProductImages"])
async def get_product_images(slug: str, request: Request):
    images = await ProductImage.filter(product__slug=slug).prefetch_related("product")
    
    return [
        ProductImage_Pydantic(
            id=img.id,
            color=img.color,
            size=img.size,
            image=str(request.base_url) + img.image.replace("\\", "/"),
            created_at=img.created_at
        )
        for img in images
    ]
