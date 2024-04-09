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
            first: 100
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
      first: 100
      orderBy: {field: CREATED_AT, direction: DESC}
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
          reviews(first: 1) {
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
    }
  }
}
"""