from hashlib import md5

from django.db import models


class AuthorVeracity(models.Model):
    author_id = models.TextField(primary_key=True)
    veracity = models.IntegerField(default=0)

    @classmethod
    def GetByAuthorDisplayName(cls, channel, author_display_name):
        author_id = md5('%s %s' % (channel, author_display_name)).hexdigest()
        try:
            return AuthorVeracity.objects.get(author_id=author_id)
        except AuthorVeracity.DoesNotExist:
            author_veracity = AuthorVeracity(author_id=author_id)
            author_veracity.save()
            return author_veracity

    @classmethod
    def GetManyByAuthorDisplayName(cls, channel, author_display_names):
        author_ids = {}
        for author_display_name in author_display_names:
            author_ids[author_display_name] = md5('%s %s' % (channel, author_display_name)).hexdigest()
        author_veracities = AuthorVeracity.objects.filter(author_id__in=author_ids.values())
        for key in author_ids.keys():
            try:
                author_veracity = [a for a in author_veracities if a.author_id == key]
            except:
                author_veracity = AuthorVeracity(author_id=key)
                author_veracity.save()
            author_ids[key] = author_veracity
        return author_ids

    def increment_veracity(self):
        self.veracity += 1
        self.save()

    def decrement_veracity(self):
        self.veracity -= 1
        self.save()

    def veracity_as_string(self):
        if self.veracity < 0:
            return 'low'
        if self.veracity > 0:
            return 'high'
        return 'none'
