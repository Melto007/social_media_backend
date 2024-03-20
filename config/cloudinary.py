""" image upload """
import cloudinary
import datetime

def upload_image(file):
    url = cloudinary.uploader.upload(
        file,
        public_id=f"image/{datetime.datetime.utcnow()}",
        use_filename=True,
        unique_filename=True
    )
    return url

def delete_image(public_key):
    url = cloudinary.uploader.destroy(public_key)
    return url