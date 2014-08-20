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

# Create your models here.
class EstateAd(models.Model):
    ad_id = models.CharField(unique=True, max_length=255, db_index=True)
    region = models.IntegerField(choices=REGIONS)
    title = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    picture = models.URLField(max_length=255, null=True)

    short_description = models.TextField(null=True)
    author_name = models.CharField(max_length=255, null=True)

    # Raw recordings for possible re-parse
    raw_data = models.TextField()
    raw_html = models.TextField()

    def __unicode__(self):
        return u"[%s] -> %s" % (self.ad_id, self.title, )