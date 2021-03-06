import config
from db import session, Photo, Tag, PhotoTag
from sqlalchemy import and_, or_
from flask.ext.restful.fields import DateTime
import math

""" utility functions """

class NoSuchObjectException(Exception):
    pass
    
def get_photo_fname(photo_id, photo_ext):
    return config.IMG_DIR + str(photo_id) + "." + photo_ext
    
def static_photo_fname(photo_id, photo_ext):
    return '/img/' + str(photo_id) + "." + photo_ext
    
def get_photo(photo_id):
    assert_photo_exists(photo_id)
    return session.query(Photo).filter(Photo.id==photo_id).first()
    
def get_photo_tags(photo_id):
    query = session.query(Tag).filter(and_(PhotoTag.p_id==photo_id, PhotoTag.t_id==Tag.id))
    tags = [tag.text for tag in query]
    return tags

def in_radius(photo, lat, lon, radius):
    factor = 10.0
    rad = radius / factor
    d_lat = photo.lat - lat
    d_lon = photo.lon - lon
    dist = math.sqrt(pow(d_lat,2) + pow(d_lon,2))
    return dist <= rad
    
# asserts that the photo exists
def assert_photo_exists(id):
    if not photo_exists(id):
        raise NoSuchObjectException()

# returns true if id matches Photo object in database
def photo_exists(id):
    if session.query(Photo).filter(Photo.id==id).count() == 0:
        return False
    return True
