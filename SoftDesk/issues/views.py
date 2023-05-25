from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from issues.models import Project, Issue, Comment, Contributor
from issues.serializers import ProjectSerializer, IssueSerializer, CommentSerializer, ContributorSerializer

from authentication.models import User


class ProjectViewset(ModelViewSet):

    serializer_class = ProjectSerializer
    # detail_serializer_class = ProjectDetailSerializer
    # lookup_field = 'pk'
    # permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Project.objects.filter()
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Project.objects.filter()
        project = get_object_or_404(queryset, pk=pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

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
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Issue.objects.all()


class ProjectIssueViewset(ModelViewSet):
    queryset = Issue.objects.all().select_related(
        'project_id'
    )
    # lookup_field = 'pk'
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, project_pk=None):
        project = get_object_or_404(Project, id=project_pk)
        user = get_object_or_404(User, id=request.user.id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(project_id=project, author_user_id=user)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def list(self, request, project_pk=None):
    #     queryset = Issue.objects.filter(project_id=project_pk)
    #     serializer = IssueSerializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, pk=None, project_pk=None):
    #     queryset = Issue.objects.filter(id=pk, project_id=project_pk)
    #     issue = get_object_or_404(queryset, id=pk)
    #     serializer = IssueSerializer(issue)
    #     return Response(serializer.data)

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get("project_pk")
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise NotFound('A project with this id does not exist')
        return self.queryset.filter(project_id=project)


class CommentViewset(ModelViewSet):

    serializer_class = CommentSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.all()


class ProjectIssueCommentViewset(ModelViewSet):
    queryset = Comment.objects.all().select_related(
        'issue_id'
    )
    # lookup_field = 'pk'
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthenticated]

    def list(self, request, project_pk=None, issue_pk=None):
        queryset = Comment.objects.filter(issue_id__project_id=project_pk, issue_id=issue_pk)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, project_pk=None, issue_pk=None):
        queryset = Comment.objects.filter(id=pk, issue_id=issue_pk, issue_id__project_id=project_pk)
        comment = get_object_or_404(queryset, id=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def get_queryset(self, *args, **kwargs):
        issue_id = self.kwargs.get("issue_pk")
        try:
            issue = Issue.objects.get(id=issue_id)
        except Issue.DoesNotExist:
            raise NotFound(f'An issue with id {issue_id} does not exist')
        return self.queryset.filter(issue_id=issue)


class ProjectContributorViewset(ModelViewSet):

    serializer_class = ContributorSerializer
    queryset = Contributor.objects.all().select_related(
        'project_id'
    )
    lookup_field = 'id'
    # permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get("project_pk")
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise NotFound('A project with this id does not exist')
        return self.queryset.filter(project_id=project)

    def create(self, request, project_pk=None):
        project = get_object_or_404(Project, id=project_pk)
        user = get_object_or_404(User, id=request.data['user_id'])

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(project_id=project, user_id=user)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def list(self, request, project_pk=None):
    #     queryset = Contributor.objects.filter(project_id=project_pk)
    #     serializer = ContributorSerializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, pk=None, project_pk=None):
    #     queryset = Comment.objects.filter(id=pk, project_id=project_pk)
    #     contributor = get_object_or_404(queryset, id=pk)
    #     serializer = CommentSerializer(contributor)
    #     return Response(serializer.data)
