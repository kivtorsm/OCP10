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

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    type = models.CharField(max_length=30, choices=TYPE_CHOICES)


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

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    tag = models.CharField(max_length=30, choices=TAG_CHOICES)
    priority = models.CharField(max_length=30, choices=PRIORITY_CHOICES)
    project_id = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    author_user_id = models.ForeignKey(
        null=True,
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='%(class)s_author_related'
    )
    assignee_user_id = models.ForeignKey(
        null=True,
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='%(class)s_assignees_related')
    created_time = models.DateTimeField()


class Comment(models.Model):
    description = models.CharField(max_length=2048)
    author_user_id = models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL)
    issue_id = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField()


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
    permission = models.CharField(max_length=30, choices=PERMISSION_CHOICES)
    role = models.CharField(max_length=30)


