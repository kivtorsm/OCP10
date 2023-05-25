from rest_framework.serializers import ModelSerializer, SerializerMethodField, HyperlinkedModelSerializer
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from issues.models import Project, Issue, Comment, Contributor


class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['id', 'project_id', 'user_id', 'permission', 'role']


class ProjectSerializer(ModelSerializer):
    contributors = SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'type', 'description', 'contributors']

    def get_contributors(self, instance):
        queryset = instance.contributors.all()
        serializer = ContributorSerializer(queryset, many=True)
        return serializer.data


class IssueSerializer(ModelSerializer):
    parent_lookup_kwargs = {
        'project_id': 'project_id',
    }

    class Meta:
        model = Issue
        fields = [
            'id',
            'title',
            'tag',
            'priority',
            'project_id',
            'status',
            'author_user_id',
            'assignee_user_id',
            'created_time',
        ]


class CommentSerializer(ModelSerializer):
    parent_lookup_kwargs = {
        'issue_id': 'issue_id',
        'project_id': 'project_id'
    }

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author_user_id', 'issue_id', 'created_time']



