import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from django.db.models import Q
from .models import Course, Like
from users.schema import UserType

class CourseType(DjangoObjectType):
    class Meta:
        model = Course

class LikeType(DjangoObjectType):
    class Meta:
        model = Like
        
class Query(graphene.ObjectType):
    courses = graphene.List(CourseType, search=graphene.String())
    likes = graphene.List(LikeType)

    def resolve_courses(self, info, search):
        if search:
            filter = (
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(url__icontains=search) |
                Q(posted_by__username__icontains=search)
            )
            # ref the django match string functions: __exact, __iexact(case insensitive), __gt, __startswith
            return Course.objects.filter(filter)
        return Course.objects.all()

    def resolve_likes(self, info):
        return Like.objects.all()

class CreateCourse(graphene.Mutation):
    course = graphene.Field(CourseType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    # more args can use **kwargs like ...rest
    def mutate(self, info, title, description, url):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Please Log in and Post')
        course = Course(title=title, description=description, url=url, posted_by=user)
        course.save()
        return CreateCourse(course=course)

class UpdateCourse(graphene.Mutation):
    course = graphene.Field(CourseType)

    class Arguments:
        course_id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, course_id, title, description, url):
        user = info.context.user
        course = Course.objects.get(id=course_id)

        if course.posted_by != user:
            raise GraphQLError('You have no permission to update.')

        course.title = title
        course.description = description
        course.url = url

        course.save()
        return UpdateCourse(course=course)

class DeleteCourse(graphene.Mutation):
    course_id = graphene.Int()

    class Arguments:
        course_id = graphene.Int(required=True)

    def mutate(self, info, course_id):
        user = info.context.user
        course = Course.objects.get(id=course_id)

        if course.posted_by != user:
            raise GraphQLError('You have no permission to delete.')

        course.delete()
        return DeleteCourse(course_id=course_id)

# Like CRUD
class CreateLike(graphene.Mutation):
    user = graphene.Field(UserType)
    course = graphene.Field(CourseType)

    class Arguments:
        course_id = graphene.Int(required=True)

    def mutate(self, info, course_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Please Log in and Like')

        course = Course.objects.get(id=course_id)
        if not course:
            raise GraphQLError('Course Not Found')

        Like.objects.create(
            user=user,
            course=course
        )

        return CreateLike(user=user, course=course)

class Mutation(graphene.ObjectType):
    create_course = CreateCourse.Field()
    update_course = UpdateCourse.Field()
    delete_course = DeleteCourse.Field()
    create_like = CreateLike.Field()
