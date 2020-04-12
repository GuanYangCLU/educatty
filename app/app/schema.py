import graphene
import graphql_jwt
import courses.schema
import users.schema

class Query(users.schema.Query, courses.schema.Query, graphene.ObjectType):
    pass

class Mutation(users.schema.Mutation, courses.schema.Mutation, graphene.ObjectType):
    # graphql jwt fields
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
