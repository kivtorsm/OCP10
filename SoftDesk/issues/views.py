from rest_framework.fields import CurrentUserDefault
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from issues.models import Project, Issue, Comment, Contributor
from issues.serializers import ProjectSerializer, IssueSerializer, CommentSerializer, ContributorSerializer


class ProjectViewset(ModelViewSet):

    serializer_class = ProjectSerializer
    # detail_serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_is_contributor_in = Contributor.objects.filter(user_id=self.request.user.id)
        project_id_list = []
        [
            project_id_list.append(contributor_item.project_id.id)
            for contributor_item
            in user_is_contributor_in
            if contributor_item.project_id.id not in project_id_list
        ]
        queryset = Project.objects.filter(id__in=project_id_list)
        return queryset


class IssueViewset(ModelViewSet):

    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Issue.objects.all()


class CommentViewset(ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.all()


class ContributorViewset(ModelViewSet):

    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contributor.objects.all()
