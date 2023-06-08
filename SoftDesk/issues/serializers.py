from rest_framework.serializers import ModelSerializer

from .models import Project, Issue, Comment, Contributor


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'type', 'description']


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'project_id', 'user_id', 'permission', 'role']
        read_only_fields = ['project_id', 'user_id']


class IssueSerializer(ModelSerializer):
    parent_lookup_kwargs = {
        'project_pk': 'project__pk',
    }

    class Meta:
        model = Issue
        fields = [
            'id',
            'title',
            'description',
            'tag',
            'priority',
            'project_id',
            'status',
            'author_user_id',
            'assignee_user_id',
            'created_time',
        ]
        read_only_fields = ['project_id', 'author_user_id']


class CommentSerializer(ModelSerializer):
    parent_lookup_kwargs = {
        'issue_pk': 'issue__pk',
        'project_pk': 'issue__project__pk'
    }

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author_user_id', 'issue_id', 'created_time']
        read_only_fields = ['issue_id']


