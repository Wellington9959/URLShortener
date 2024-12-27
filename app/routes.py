import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Response, status
from pymongo import ReturnDocument

from app.schemas import LongURL, NotFoundException, ShortURL, ShortURLStats
from app.utilities.db import db

router = APIRouter(prefix="/shorten", tags=["Shorten"])


@router.post(
    "",
    response_model=ShortURL,
    status_code=status.HTTP_201_CREATED,
)
async def shorten_url(payload: LongURL) -> ShortURL:
    """
    Shorten a URL.\n
    A unique id will be created and provided in the response.
    """
    short_code = str(uuid.uuid4())[:8]
    now = datetime.now(timezone.utc)
    insert_result = await db.urls.insert_one(
        {
            "url": str(payload.url),
            "shortCode": short_code,
            "createdAt": now,
            "updatedAt": now,
            "accessCount": 0,
        }
    )
    inserted_id = insert_result.inserted_id
    inserted_document = await db.urls.find_one({"_id": inserted_id})

    return inserted_document


@router.get(
    "/{short_code}",
    response_model=ShortURL,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": NotFoundException,
            "description": "Not Found",
        }
    },
)
async def get_original_url(short_code: str) -> ShortURL:
    """
    Get original URL from short code
    """
    original_url = await db.urls.find_one_and_update(
        {"shortCode": short_code},
        {"$inc": {"accessCount": 1}},
        return_document=ReturnDocument.AFTER,
    )

    if not original_url:
        raise HTTPException(
            detail=f"No URL matches short code '{short_code}'.",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return original_url


@router.put(
    "/{short_code}",
    response_model=ShortURL,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": NotFoundException,
            "description": "Not Found",
        }
    },
)
async def update_shortened_url(
    short_code: str,
    payload: LongURL,
) -> ShortURL:
    """
    Update orginal URL of a shortened URL
    """
    now = datetime.now(timezone.utc)
    update_result = await db.urls.find_one_and_update(
        {"shortCode": short_code},
        {
            "$set": {
                "url": str(payload.url),
                "updatedAt": now,
            }
        },
        return_document=ReturnDocument.AFTER,
    )

    if not update_result:
        raise HTTPException(
            detail=f"No URL matches short code '{short_code}'.",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return update_result


@router.delete(
    "/{short_code}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": NotFoundException,
            "description": "Not Found",
        }
    },
)
async def remove_shortened_url(
    short_code: str,
) -> Response:
    """
    Remove a shortened URL
    """
    delete_result = await db.urls.delete_one({"shortCode": short_code})

    if delete_result.deleted_count == 0:
        raise HTTPException(
            detail=f"No URL matches short code '{short_code}'.",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{short_code}/stats",
    response_model=ShortURLStats,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": NotFoundException,
            "description": "Not Found",
        }
    },
)
async def get_shortened_url_stats(short_code: str) -> ShortURLStats:
    """
    Get shortened URL access statistics
    """
    shortened_url = await db.urls.find_one({"shortCode": short_code})

    if not shortened_url:
        raise HTTPException(
            detail=f"No URL matches short code '{short_code}'.",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return shortened_url
