"""
File storage utility for handling image uploads
"""
import os
import base64
from pathlib import Path
from uuid import uuid4
from typing import List, Optional


UPLOAD_DIR = Path("uploads/service_requests")


def ensure_upload_dir():
    """Ensure upload directory exists"""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_base64_image(base64_string: str, user_id: int) -> str:
    """
    Save base64 encoded image to disk
    
    Args:
        base64_string: Base64 encoded image (with or without data URI prefix)
        user_id: User ID for organizing uploads
        
    Returns:
        Relative file path to saved image
    """
    ensure_upload_dir()
    
    if ',' in base64_string:
        base64_string = base64_string.split(',')[1]
    
    try:
        image_data = base64.b64decode(base64_string)
    except Exception as e:
        raise ValueError(f"Invalid base64 image data: {e}")
    
    user_dir = UPLOAD_DIR / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)
    
    filename = f"{uuid4()}.jpg"
    file_path = user_dir / filename
    
    with open(file_path, 'wb') as f:
        f.write(image_data)
    
    return str(file_path)


def save_base64_images(base64_images: List[str], user_id: int) -> List[str]:
    """
    Save multiple base64 encoded images
    
    Args:
        base64_images: List of base64 encoded images
        user_id: User ID for organizing uploads
        
    Returns:
        List of relative file paths
    """
    if not base64_images:
        return []
    
    file_paths = []
    for base64_img in base64_images:
        if base64_img:  # Skip empty strings
            try:
                file_path = save_base64_image(base64_img, user_id)
                file_paths.append(file_path)
            except Exception as e:
                print(f"Error saving image: {e}")
                continue
    
    return file_paths


def delete_image(file_path: str) -> bool:
    """
    Delete image file
    
    Args:
        file_path: Path to image file
        
    Returns:
        True if deleted successfully, False otherwise
    """
    try:
        path = Path(file_path)
        if path.exists():
            path.unlink()
            return True
        return False
    except Exception as e:
        print(f"Error deleting image {file_path}: {e}")
        return False


def delete_images(file_paths: List[str]) -> int:
    """
    Delete multiple image files
    
    Args:
        file_paths: List of file paths
        
    Returns:
        Number of files deleted successfully
    """
    if not file_paths:
        return 0
    
    deleted_count = 0
    for file_path in file_paths:
        if delete_image(file_path):
            deleted_count += 1
    
    return deleted_count
