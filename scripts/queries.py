repo_query = """
query search($perPage: Int!, $cursor: String) {
  search(query: "stars:>0 sort:stars-desc", type: REPOSITORY, first: $perPage, after: $cursor) {
    edges {
      node {
        ... on Repository {
          nameWithOwner
          stargazers {
            totalCount
          }
          pullRequests(
            states: [MERGED, CLOSED]
            orderBy: { field: CREATED_AT, direction: DESC }
          ) {
            totalCount
          }
        }
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
"""

pr_query = """
query repository($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    pullRequests(
      states: [MERGED, CLOSED]
      orderBy: {field: CREATED_AT, direction: DESC}
      first: 100
    ) {
      edges {
        node {
          title
          number
          state
          createdAt
          closedAt
          mergedAt
          bodyText
          reviewDecision
          reviews {
            totalCount
          }
          files {
            totalCount
          }
          additions
          deletions
          participants {
            totalCount
          }
          comments {
            totalCount
          }
        }
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
}
"""