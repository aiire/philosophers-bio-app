from dataclasses import dataclass
from typing import List, Optional, Dict

@dataclass
class ImageLinks:
    """
    Data class to hold different image links for a philosopher.
    """
    face500x500: Optional[str] = None
    face250x250: Optional[str] = None
    face750x750: Optional[str] = None
    full1200x1600: Optional[str] = None
    full840x1120: Optional[str] = None
    full600x800: Optional[str] = None
    full1260x1680: Optional[str] = None
    full420x560: Optional[str] = None
    ill250x250: Optional[str] = None
    ill750x750: Optional[str] = None
    ill500x500: Optional[str] = None
    thumbnailIll50x50: Optional[str] = None
    thumbnailIll100x100: Optional[str] = None
    thumbnailIll150x150: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Dict[str, str]]):
        """
        Constructs an ImageLinks object from a dictionary.
        """
        face_images = data.get('faceImages', {})
        full_images = data.get('fullImages', {})
        illustrations = data.get('illustrations', {})
        thumbnail_illustrations = data.get('thumbnailIllustrations', {})

        return cls(
            face500x500=face_images.get('face500x500'),
            face250x250=face_images.get('face250x250'),
            face750x750=face_images.get('face750x750'),
            full1200x1600=full_images.get('full1200x1600'),
            full840x1120=full_images.get('full840x1120'),
            full600x800=full_images.get('full600x800'),
            full1260x1680=full_images.get('full1260x1680'),
            full420x560=full_images.get('full420x560'),
            ill250x250=illustrations.get('ill250x250'),
            ill750x750=illustrations.get('ill750x750'),
            ill500x500=illustrations.get('ill500x500'),
            thumbnailIll50x50=thumbnail_illustrations.get('thumbnailIll50x50'),
            thumbnailIll100x100=thumbnail_illustrations.get('thumbnailIll100x100'),
            thumbnailIll150x150=thumbnail_illustrations.get('thumbnailIll150x150'),
        )

@dataclass
class Philosopher:
    images: ImageLinks
    life: str
    name: str
    interests: str
    birth_date: Optional[str] = None
    topical_description: Optional[str] = None
    birth_year: Optional[str] = None
    death_year: Optional[str] = None
    death_date: Optional[str] = None
    school: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, str]) :
        images = ImageLinks.from_dict(data.get('images', {}))
        return cls(
            images=images,
            life=data.get('life'),
            name=data.get('name'),
            interests=data.get('interests'),
            birth_date=data.get('birthDate'),
            topical_description=data.get('topicalDescription'),
            birth_year=data.get('birthYear'),
            death_year=data.get('deathYear'),
            death_date=data.get('deathDate'),
            school=data.get('school')
        )