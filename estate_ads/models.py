from django.db import models

REGIONS = (
    (1, "LJ_OKOLICA"),
    (2, "J_PRIMORSKA"),
    (3, "GORENJSKA"),
    (4, "S_PRIMORSKA"),
    (5, "SAVINJSKA"),
    (6, "DOLENJSKA"),
    # 7 - Prazno?!
    (8, "NOTRANJSKA"),
    (9, "PODRAVSKA"),
    (10, "KOROSKA"),
    (11, "ZASAVSKA"),
    (12, "POSAVSKA"),
    # 13 - VSI KRAJI
    (14, "LJ_MESTO"),
    (15, "POMURSKA")
)

AD_TYPES = (
    (0, "PRODAJA"),
    (1, "NAKUP"),
    (2, "ODDAJA"),
    (3, "NAJEM")
)

BUILDING_TYPES = (
    (0, "STANOVANJE"),
    (1, "HISA"),
    (2, "POSEST"),
    (3, "POSLOVNI_PROSTOR"),
    (4, "GARAZA"),
    (5, "VIKEND")
)


# Create your models here.
class EstateAd(models.Model):
    """
    Represents a single Ad with all information related
    """
    ad_id = models.CharField(unique=True, max_length=255, db_index=True)
    region = models.IntegerField(choices=REGIONS, db_index=True)
    type = models.IntegerField(choices=AD_TYPES, null=True, db_index=True)
    building_type = models.IntegerField(choices=BUILDING_TYPES, null=True, db_index=True)

    # Minimum required details
    title = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    short_description = models.TextField(blank=True, null=False, default="")
    author_name = models.CharField(max_length=255, null=False, blank=True, default="")
    publish_date = models.DateTimeField()

    # These fields may not parse properly
    size_m2 = models.FloatField(null=True)
    price_m2 = models.FloatField(null=True)
    price = models.FloatField(null=True)
    year_built = models.IntegerField(null=True)
    floor = models.CharField(max_length=8, blank=True, null=False, default="")

    # Additional information
    description = models.TextField(blank=True, null=False, default="")
    administrative_unit = models.CharField(max_length=255, blank=True, null=False, default="")
    county = models.CharField(max_length=255, blank=True, null=False, default="")

    # Raw recordings for possible re-parse
    raw_data = models.TextField()
    raw_html = models.TextField()
    raw_detail_html = models.TextField(blank=True, null=False, default="")

    def __unicode__(self):
        return u"[%s] -> %s" % (self.ad_id, self.title, )


class AdPicture(models.Model):
    """
    Represents a picture for the Ad
    """
    picture_url = models.URLField(max_length=255)
    ad = models.ForeignKey(EstateAd, null=True)