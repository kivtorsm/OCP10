from django.db import models
from django.conf import settings


class Project(models.Model):
    BACK_END = 'BACK-END'
    FRONT_END = 'FRONT_END'
    IOS = 'IOS'
    ANDROID = 'ANDROID'

    TYPE_CHOICES = (
        (BACK_END, 'Back-end'),
        (FRONT_END, 'Front-end'),
        (IOS, 'iOS'),
        (ANDROID, 'Android'),
    )

    title = models.CharField()
    description = models.CharField()
    type = models.CharField()


class Issue(models.Model):

    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'

    PRIORITY_CHOICES = (
        (LOW, 'Basse'),
        (MEDIUM, 'Moyenne'),
        (HIGH, 'Haute')
    )

    BUG = 'BUG'
    CHANGE = 'CHANGE'
    TASK = 'TASK'

    TAG_CHOICES = (
        (BUG, 'Anomalie'),
        (CHANGE, 'Amélioration'),
        (TASK, 'Tâche')
    )

    TO_DO = 'TO_DO'
    ONGOING = 'ONGOING'
    DONE = 'DONE'

    STATUS_CHOICES = (
        (TO_DO, 'A faire'),
        (ONGOING, 'En cours'),
        (DONE, 'Fait')
    )

    title = models.CharField()
    description = models.CharField()
    tag = models.CharField(choices=TAG_CHOICES)
    priority = models.CharField(choices=PRIORITY_CHOICES)
    project_id = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL)
    assignee_user_id = models.ForeignKey(to=settings.AUTH_UER_MODEL)
    created_time = models.DateTimeField()


class Comment(models.Model):
    description = models.CharField()
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL)
    issue_id = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField


class Contributor(models.Model):
    AUTHOR = 'AUTHOR'
    MANAGER = 'MANAGER'
    CREATOR = 'CREATOR'

    PERMISSION_CHOICES = (
        (AUTHOR, 'Auteur'),
        (MANAGER, 'Responsable'),
        (CREATOR, 'Créateur'),
    )

    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_id = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    permission = models.TextChoices()
    role = models.charField()


