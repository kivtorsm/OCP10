from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from issues.models import Project, Issue, Comment, Contributor
from issues.serializers import ProjectSerializer, IssueSerializer, CommentSerializer, ContributorSerializer

from authentication.models import User

from issues.permissions import IsOwnerOrReadOnly


class ProjectViewset(ModelViewSet):

    serializer_class = ProjectSerializer
    permission_classes = [
        IsAuthenticated,
        IsOwnerOrReadOnly
    ]

    def retrieve(self, request, pk=None, **kwargs):
        queryset = self.get_queryset()
        project = get_object_or_404(Project.objects.all(), pk=pk)

        if project in queryset:
            serializer = ProjectSerializer(project)
            status_response = status.HTTP_200_OK
            headers = self.get_success_headers(serializer.data)

        else:
            project = None
            serializer = ProjectSerializer(project)
            status_response = status.HTTP_401_UNAUTHORIZED
            headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status_response, headers=headers)

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

    def create(self, request, pk=None, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(pk=pk)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProjectIssueViewset(ModelViewSet):
    queryset = Issue.objects.all().select_related(
        'project_id'
    )
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def create(self, request, project_pk=None, **kwargs):
        project = get_object_or_404(Project, id=project_pk)
        user = get_object_or_404(User, id=request.user.id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(project_id=project, author_user_id=user)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get("project_pk")
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise NotFound(f'A project with id {project_id} does not exist')
        return self.queryset.filter(project_id=project)

    def dispatch(self, request, *args, **kwargs):
        parent_view = ProjectViewset.as_view({"get": "retrieve"})
        original_method = request.method
        request.method = "GET"
        parent_kwargs = {"pk": kwargs["project_pk"]}

        parent_response = parent_view(request, *args, **parent_kwargs)
        if parent_response.exception:
            return parent_response

        request.method = original_method
        return super().dispatch(request, *args, **kwargs)


class ProjectIssueCommentViewset(ModelViewSet):
    queryset = Comment.objects.all().select_related(
        'issue_id'
    )
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def create(self, request, issue_pk=None, project_pk=None, **kwargs):
        issue = get_object_or_404(Issue, id=issue_pk)
        user = get_object_or_404(User, id=request.user.id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(issue_id=issue, author_user_id=user)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self, *args, **kwargs):
        issue_id = self.kwargs.get("issue_pk")
        try:
            issue = Issue.objects.get(id=issue_id)
        except Issue.DoesNotExist:
            raise NotFound(f'An issue with id {issue_id} does not exist')
        return self.queryset.filter(issue_id=issue)

    def dispatch(self, request, *args, **kwargs):
        parent_view = ProjectIssueViewset.as_view({"get": "retrieve"})
        original_method = request.method
        request.method = "GET"
        parent_kwargs = {
            "pk": kwargs["issue_pk"],
            "project_pk": kwargs["project_pk"]
        }

        parent_response = parent_view(request, *args, **parent_kwargs)
        if parent_response.exception:
            return parent_response

        request.method = original_method
        return super().dispatch(request, *args, **kwargs)


class ProjectContributorViewset(ModelViewSet):

    serializer_class = ContributorSerializer
    queryset = Contributor.objects.all().select_related(
        'project_id'
    )
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get("project_pk")
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise NotFound('A project with this id does not exist')
        return self.queryset.filter(project_id=project)

    def create(self, request, project_pk=None, **kwargs):
        project = get_object_or_404(Project, id=project_pk)
        user = get_object_or_404(User, id=request.data['user_id'])

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(project_id=project, user_id=user)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def dispatch(self, request, *args, **kwargs):
        parent_view = ProjectViewset.as_view({"get": "retrieve"})
        original_method = request.method
        request.method = "GET"
        parent_kwargs = {"pk": kwargs["project_pk"]}

        parent_response = parent_view(request, *args, **parent_kwargs)
        if parent_response.exception:
            return parent_response

        request.method = original_method
        return super().dispatch(request, *args, **kwargs)
