import json

# Paste ALL your verified question/answer pairs here, combined from every domain
golden_dataset = [
  {
    "question": "When consuming the issues assigned endpoint, which custom media types can a client request, and what body representation does the default return?",
    "gold_answer": "This endpoint supports the following custom media types: application/vnd.github.raw+json (returns raw markdown body including `body`, which is the default if no specific media type is passed), application/vnd.github.text+json (returns text-only representation including `body_text`), application/vnd.github.html+json (returns HTML rendered from markdown including `body_html`), and application/vnd.github.full+json (returns raw, text, and HTML representations including `body`, `body_text`, and `body_html`).",
    "source_url": "https://docs.github.com/rest/issues/issues#list-issues-assigned-to-the-authenticated-user",
    "category": "parameters"
  },
  {
    "question": "When querying issues assigned to the authenticated user, what results do `filter=assigned` and `filter=all` or `filter=repos` return?",
    "gold_answer": "`assigned` means issues assigned to you. `all` or `repos` means all issues you can see, regardless of participation or creation.",
    "source_url": "https://docs.github.com/rest/issues/issues#list-issues-assigned-to-the-authenticated-user",
    "category": "parameters"
  },
  {
    "question": "If a client receives a validation or spam-related failure from `GET /repos/{owner}/{repo}/issues`, which HTTP status should it handle?",
    "gold_answer": "422 Validation failed, or the endpoint has been spammed.",
    "source_url": "https://docs.github.com/rest/issues/issues#list-repository-issues",
    "category": "error_code"
  },
  {
    "question": "If a client tries to create an issue in a repository where issues are disabled, which HTTP status should it expect?",
    "gold_answer": "The API returns a `410 Gone` status.",
    "source_url": "https://docs.github.com/rest/issues/issues#create-an-issue",
    "category": "error_code"
  },
  {
    "question": "When fetching repository issue comments, what ordering should a client expect if no sort is specified?",
    "gold_answer": "By default, issue comments are ordered by ascending ID.",
    "source_url": "https://docs.github.com/rest/issues/comments#list-issue-comments-for-a-repository",
    "category": "lookup"
  },
  {
    "question": "If a client adds a reaction that the user has already added to an issue comment, which HTTP status does the API return?",
    "gold_answer": "An HTTP `200` status means that you already added the reaction type to this issue comment.",
    "source_url": "https://docs.github.com/rest/reactions/reactions#create-reaction-for-an-issue-comment",
    "category": "error_code"
  },
  {
    "question": "How do I configure OAuth2 scopes for my application to access private repositories?",
    "gold_answer": "NOT_COVERED",
    "source_url": "",
    "category": "negative"
  },
  {
    "question": "What are the webhook payload delivery retry policies and secret signature validation steps?",
    "gold_answer": "NOT_COVERED",
    "source_url": "",
    "category": "negative"
  },
  {
    "question": "How do I trigger a GitHub Actions workflow run via the REST API?",
    "gold_answer": "NOT_COVERED",
    "source_url": "",
    "category": "negative"
  },
  {
    "question": "When calling the organization issues endpoint, what does the `org` path parameter represent, and is it case sensitive?",
    "gold_answer": "The organization name. The name is not case sensitive.",
    "source_url": "https://docs.github.com/rest/issues/issues#list-organization-issues-assigned-to-the-authenticated-user",
    "category": "parameters"
  },
  {
    "question": "When filtering repository issues by milestone, what inputs can the `milestone` parameter accept and what does each one mean?",
    "gold_answer": "If an `integer` is passed, it should refer to a milestone by its `number` field. If the string `*` is passed, issues with any milestone are accepted. If the string `none` is passed, issues without milestones are returned.",
    "source_url": "https://docs.github.com/rest/issues/issues#list-repository-issues",
    "category": "parameters"
  },
  {
    "question": "To fetch a specific issue comment, which path parameters must the client provide?",
    "gold_answer": "The required path parameters are `owner`, `repo`, and `comment_id` (the unique identifier of the comment).",
    "source_url": "https://docs.github.com/rest/issues/comments#get-an-issue-comment",
    "category": "parameters"
  },
  {
    "question": "When listing reactions for an issue comment, which query parameters control the reaction type and pagination?",
    "gold_answer": "The accepted query parameters are `content` (returns a single reaction type, or omits to list all reactions) and pagination parameters `per_page` and `page`.",
    "source_url": "https://docs.github.com/rest/reactions/reactions#list-reactions-for-an-issue-comment",
    "category": "parameters"
  },
  {
    "question": "When calling the endpoint to list issues assigned to the authenticated user, how does the API handle pull requests, what key identifies them, and how do you find their actual pull request ID rather than the issue ID returned?",
    "gold_answer": "GitHub's REST API considers every pull request an issue, but not every issue is a pull request, so these endpoints return both issues and pull requests in the response. You can identify pull requests by the `pull_request` key. The `id` returned from \"Issues\" endpoints will be an issue ID; to find out the pull request ID, you must use the \"List pull requests\" endpoint.",
    "source_url": "https://docs.github.com/rest/issues/issues#list-issues-assigned-to-the-authenticated-user",
    "category": "lookup"
  },
  {
    "question": "How should a client format `issue_field_values` when filtering repository issues, and what repository limitations apply?",
    "gold_answer": "You use the `issue_field_values` query parameter, which takes a comma-separated list of issue field filters in `field_slug:value` format (only issues matching all specified field values are returned). This requires issue fields to be enabled for the repository. Issue fields are not available for user-owned repositories, and field availability for organization-owned public repositories depends on the organization's visibility settings.",
    "source_url": "https://docs.github.com/rest/issues/issues#list-repository-issues",
    "category": "parameters"
  },
  {
    "question": "When filtering repository issues, what values can `assignee` and `milestone` accept?",
    "gold_answer": "For `assignee`, it can be the name of a user, `none` for issues with no assigned user, or `*` for issues assigned to any user. For `milestone`, if an integer is passed it refers to a milestone by its `number` field, `*` accepts issues with any milestone, and `none` returns issues without milestones.",
    "source_url": "https://docs.github.com/rest/issues/issues#list-repository-issues",
    "category": "parameters"
  },
  {
    "question": "When creating issues through the REST API, what conditions can cause `410 Gone` or secondary rate limiting?",
    "gold_answer": "The API returns a `410 Gone` status if issues are disabled in the repository. Creating content too quickly using this endpoint triggers notifications and may result in secondary rate limiting.",
    "source_url": "https://docs.github.com/rest/issues/issues#create-an-issue",
    "category": "error_code"
  },
  {
    "question": "When dealing with custom media types for issue comment endpoints like `GET /repos/{owner}/{repo}/issues/comments/{comment_id}`, what are the four available custom media types and how do their response payloads differ regarding body representations?",
    "gold_answer": "- `application/vnd.github.raw+json`: Returns raw markdown body including `body` (default if no specific media type is passed).\n- `application/vnd.github.text+json`: Returns a text-only representation including `body_text`.\n- `application/vnd.github.html+json`: Returns HTML rendered from markdown including `body_html`.\n- `application/vnd.github.full+json`: Returns raw, text, and HTML representations including `body`, `body_text`, and `body_html`.",
    "source_url": "https://docs.github.com/rest/issues/comments#get-an-issue-comment",
    "category": "parameters"
  },
  {
    "question": "When listing repository issue comments, how does `direction` interact with `sort`, and what ordering is used by default?",
    "gold_answer": "By default, issue comments are ordered by ascending ID. The `direction` query parameter takes either `asc` or `desc`, but it is ignored without the `sort` parameter.",
    "source_url": "https://docs.github.com/rest/issues/comments#list-issue-comments-for-a-repository",
    "category": "lookup"
  },
  {
    "question": "When querying the list issues endpoint, how does GitHub handle pull requests in the returned results, and what limitation exists regarding their IDs?",
    "gold_answer": "GitHub's REST API considers every pull request an issue, but not every issue is a pull request, so these endpoints return both issues and pull requests in the response. You can identify pull requests by the `pull_request` key. Be aware that the `id` of a pull request returned from \"Issues\" endpoints will be an issue ID; to find out the pull request ID, you must use the \"List pull requests\" endpoint.",
    "source_url": "https://docs.github.com/rest/issues/issues#list-issues-assigned-to-the-authenticated-user",
    "category": "lookup"
  },
  {
    "question": "Which custom media type should a client request to receive raw, text-only, and rendered HTML body representations in one response?",
    "gold_answer": "`application/vnd.github.full+json` returns raw, text, and HTML representations, including `body`, `body_text`, and `body_html`.",
    "source_url": "https://docs.github.com/rest/issues/issues#list-issues-assigned-to-the-authenticated-user",
    "category": "parameters"
  },
  {
    "question": "What values can the `filter` parameter use when querying issues assigned to the authenticated user, and what does each value return?",
    "gold_answer": "`assigned` means issues assigned to you. `created` means issues created by you. `mentioned` means issues mentioning you. `subscribed` means issues you're subscribed to updates for. `all` or `repos` means all issues you can see, regardless of participation or creation.",
    "source_url": "https://docs.github.com/rest/issues/issues#list-issues-assigned-to-the-authenticated-user",
    "category": "parameters"
  },
  {
    "question": "What query parameter syntax and repository conditions are required to filter repository issues using `issue_field_values`, and what restrictions apply to user-owned versus organization-owned repositories?",
    "gold_answer": "It uses a comma-separated list of issue field filters in `field_slug:value` format, returning only issues matching all specified field values. This requires issue fields to be enabled for the repository. Issue fields are not available for user-owned repositories, and field availability for organization-owned public repositories depends on the organization's visibility settings.",
    "source_url": "https://docs.github.com/rest/issues/issues#list-repository-issues",
    "category": "parameters"
  },
  {
    "question": "When filtering repository issues by milestone, how do a milestone number, `*`, and `none` differ?",
    "gold_answer": "If an `integer` is passed, it refers to a milestone by its `number` field. If the string `*` is passed, issues with any milestone are accepted. If the string `none` is passed, issues without milestones are returned.",
    "source_url": "https://docs.github.com/rest/issues/issues#list-repository-issues",
    "category": "parameters"
  },
  {
    "question": "What are the exact permission requirements and potential error statuses returned by `POST /repos/{owner}/{repo}/issues` if issues are disabled or content is created too quickly?",
    "gold_answer": "Any user with pull access to a repository can create an issue. If issues are disabled in the repository, the API returns a `410 Gone` status. Creating content too quickly may result in secondary rate limiting, and responses can include errors like 400 Bad Request, 403 Forbidden, 422 Validation failed, 503 Service unavailable, 404 Resource not found, and 410 Gone.",
    "source_url": "https://docs.github.com/rest/issues/issues#create-an-issue",
    "category": "error_code"
  },
  {
    "question": "For repository issue comments, what is the default sort order and when does the `direction` parameter take effect?",
    "gold_answer": "By default, issue comments are ordered by ascending ID. The `direction` parameter takes either `asc` or `desc`, but it is ignored without the `sort` parameter.",
    "source_url": "https://docs.github.com/rest/issues/comments#list-issue-comments-for-a-repository",
    "category": "lookup"
  },
  {
    "question": "If a user tries to create an issue-comment reaction they already have, which HTTP status does the API return, and what status represents a new reaction?",
    "gold_answer": "A response with an HTTP `200` status means that you already added the reaction type to this issue comment (whereas a new creation returns `201`).",
    "source_url": "https://docs.github.com/rest/reactions/reactions#create-reaction-for-an-issue-comment",
    "category": "error_code"
  },
  {
    "question": "Which HTTP statuses should a client handle when fetching an issue event for success, not found, gone, or forbidden access?",
    "gold_answer": "Responses include `200` Response, `404` Resource not found, `410` Gone, and `403` Forbidden.",
    "source_url": "https://docs.github.com/rest/issues/events#get-an-issue-event",
    "category": "error_code"
  },
  {
    "question": "What timestamp format should a client use for the `since` query parameter?",
    "gold_answer": "It is a timestamp in ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`.",
    "source_url": "https://docs.github.com/rest/issues/issues#list-issues-assigned-to-the-authenticated-user",
    "category": "parameters"
  },
  {
    "question": "When filtering repository issues, which `assignee` values select unassigned issues or issues assigned to any user?",
    "gold_answer": "Pass in `none` for issues with no assigned user, and `*` for issues assigned to any user (or a specific user's name).",
    "source_url": "https://docs.github.com/rest/issues/issues#list-repository-issues",
    "category": "parameters"
  },
  {
    "question": "Is the organization name supplied through the `org` path parameter case sensitive?",
    "gold_answer": "The organization name is not case sensitive.",
    "source_url": "https://docs.github.com/rest/issues/issues#list-organization-issues-assigned-to-the-authenticated-user",
    "category": "parameters"
  },
  {
    "question": "Which custom media type should a client request for a text-only issue-comment body representation?",
    "gold_answer": "`application/vnd.github.text+json` returns a text-only representation of the markdown body and includes `body_text` in the response.",
    "source_url": "https://docs.github.com/rest/issues/comments#get-an-issue-comment",
    "category": "parameters"
  },
  {
    "question": "Which HTTP error statuses should a client handle when pinning an issue comment?",
    "gold_answer": "Responses include `401` Requires authentication, `403` Forbidden, `404` Resource not found, `410` Gone, and `422` Validation failed, or the endpoint has been spammed.",
    "source_url": "https://docs.github.com/rest/issues/comments#pin-an-issue-comment",
    "category": "error_code"
  },
  {
    "question": "How does the `content` parameter control reaction filtering when listing reactions for an issue comment?",
    "gold_answer": "Passing the `content` parameter returns a single reaction type. Omitting this parameter lists all reactions to an issue comment.",
    "source_url": "https://docs.github.com/rest/reactions/reactions#list-reactions-for-an-issue-comment",
    "category": "parameters"
  },
  {
    "question": "What is the maximum `per_page` value a client can request for the repository issues endpoint?",
    "gold_answer": "The maximum allowed value for results per page is 100.",
    "source_url": "https://docs.github.com/rest/issues/issues#list-repository-issues",
    "category": "parameters"
  },
  {
    "question": "How do I configure OAuth token rotation policies and refresh token grants for secure background worker access?",
    "gold_answer": "NOT_COVERED",
    "source_url": "",
    "category": "negative"
  },
  {
    "question": "What are the exact steps and API parameters required to transfer a repository ownership to a new organization?",
    "gold_answer": "NOT_COVERED",
    "source_url": "",
    "category": "negative"
  },
  {
    "question": "How do I set up continuous deployment billing alerts and credit card payment methods via the REST API?",
    "gold_answer": "NOT_COVERED",
    "source_url": "",
    "category": "negative"
  },
  {
    "question": "Which users are authorized to view an organization's pull request creation cap configuration?",
    "gold_answer": "Only users with admin access to the organization can view the cap configuration.",
    "source_url": "https://docs.github.com/rest/interactions/orgs#get-pull-request-creation-cap-for-an-org",
    "category": "parameters"
  },
  {
    "question": "If updating an organization's pull request creation cap fails validation or is considered spam, which HTTP status is returned?",
    "gold_answer": "422 Validation failed, or the endpoint has been spammed.",
    "source_url": "https://docs.github.com/rest/interactions/orgs#update-pull-request-creation-cap-for-an-org",
    "category": "error_code"
  },
  {
    "question": "Can the `commit_sha` parameter accept a branch name when listing pull requests associated with a commit?",
    "gold_answer": "You can set the `commit_sha` parameter to the branch name.",
    "source_url": "https://docs.github.com/rest/commits/commits#list-pull-requests-associated-with-a-commit",
    "category": "parameters"
  },
  {
    "question": "Which repository permission level is required to view the pull request creation cap bypass list?",
    "gold_answer": "Only users with maintainer permissions can view the bypass list.",
    "source_url": "https://docs.github.com/rest/interactions/repos#get-pull-request-creation-cap-bypass-list-for-a-repository",
    "category": "parameters"
  },
  {
    "question": "What are the per-request and total user limits for a repository's pull request creation cap bypass list?",
    "gold_answer": "You can add a maximum of 100 users per request, and the bypass list can only hold a maximum of 100 users.",
    "source_url": "https://docs.github.com/rest/interactions/repos#add-users-to-the-pull-request-creation-cap-bypass-list-for-a-repository",
    "category": "parameters"
  },
  {
    "question": "After a user is removed from the pull request creation cap bypass list, what cap applies to them?",
    "gold_answer": "Removed users will be subject to any configured pull request creation cap.",
    "source_url": "https://docs.github.com/rest/interactions/repos#remove-users-from-the-pull-request-creation-cap-bypass-list-for-a-repository",
    "category": "lookup"
  },
  {
    "question": "When listing repository pull requests, what does sorting by `popularity` do, and what does `long-running` select?",
    "gold_answer": "`popularity` will sort by the number of comments. `long-running` will sort by date created and will limit the results to pull requests that have been open for more than a month and have had activity within the past month.",
    "source_url": "https://docs.github.com/rest/pulls/pulls#list-pull-requests",
    "category": "parameters"
  },
  {
    "question": "What access is required to create a pull request, and what rate-limiting behavior should the client account for?",
    "gold_answer": "You must have write access to the head or the source branch (and be a member of the organization for organization-owned repositories). Creating content too quickly using this endpoint may result in secondary rate limiting.",
    "source_url": "https://docs.github.com/rest/pulls/pulls#create-a-pull-request",
    "category": "error_code"
  },
  {
    "question": "When listing repository pull-request review comments, what order is used by default?",
    "gold_answer": "By default, review comments are in ascending order by ID.",
    "source_url": "https://docs.github.com/rest/pulls/comments#list-review-comments-in-a-repository",
    "category": "lookup"
  },
  {
    "question": "How can a client request only one reaction type when listing reactions on a pull-request review comment?",
    "gold_answer": "Use the `content` query parameter (omitting this parameter lists all reactions).",
    "source_url": "https://docs.github.com/rest/reactions/reactions#list-reactions-for-a-pull-request-review-comment",
    "category": "parameters"
  },
  {
    "question": "If creating a reaction on a pull-request review comment returns HTTP `200`, what does that indicate?",
    "gold_answer": "It means that you already added the reaction type to this pull request review comment.",
    "source_url": "https://docs.github.com/rest/reactions/reactions#create-reaction-for-a-pull-request-review-comment",
    "category": "error_code"
  },
  {
    "question": "When `mergeable` is `null` in a pull-request response, what should the client do before deciding whether the pull request is mergeable?",
    "gold_answer": "If the value is `null`, then GitHub has started a background job to compute the mergeability. After giving the job time to complete, resubmit the request.",
    "source_url": "https://docs.github.com/rest/pulls/pulls#get-a-pull-request",
    "category": "lookup"
  },
  {
    "question": "How do I configure webhook secret signatures and payload delivery retry policies for pull request events?",
    "gold_answer": "NOT_COVERED",
    "source_url": "",
    "category": "negative"
  },
  {
    "question": "What are the exact steps and API parameters required to transfer repository ownership to a new organization?",
    "gold_answer": "NOT_COVERED",
    "source_url": "",
    "category": "negative"
  },
  {
    "question": "How do I configure OAuth2 token rotation policies and refresh token grants for secure background worker access?",
    "gold_answer": "NOT_COVERED",
    "source_url": "",
    "category": "negative"
  },
  {
    "question": "Which token scope is required to read an enterprise's GitHub Actions cache retention limit?",
    "gold_answer": "OAuth tokens and personal access tokens (classic) need the `admin:enterprise` scope to use this endpoint.",
    "source_url": "https://docs.github.com/rest/actions/cache#get-github-actions-cache-retention-limit-for-an-enterprise",
    "category": "parameters"
  },
  {
    "question": "Which HTTP status indicates that setting an enterprise's GitHub Actions cache retention limit succeeded?",
    "gold_answer": "The API returns `204` (No Content).",
    "source_url": "https://docs.github.com/rest/actions/cache#set-github-actions-cache-retention-limit-for-an-enterprise",
    "category": "error_code"
  },
  {
    "question": "What value should a client provide for the `enterprise` path parameter when accessing the enterprise cache storage limit endpoint?",
    "gold_answer": "The slug version of the enterprise name.",
    "source_url": "https://docs.github.com/rest/actions/cache#get-github-actions-cache-storage-limit-for-an-enterprise",
    "category": "parameters"
  },
  {
    "question": "Which HTTP method should a client use to set an enterprise's GitHub Actions cache storage limit?",
    "gold_answer": "Use the `PUT` method.",
    "source_url": "https://docs.github.com/rest/actions/cache#set-github-actions-cache-storage-limit-for-an-enterprise",
    "category": "lookup"
  },
  {
    "question": "Which token scope is required to list OIDC custom property inclusions for an enterprise?",
    "gold_answer": "The `admin:enterprise` scope is needed to use this endpoint.",
    "source_url": "https://docs.github.com/rest/actions/oidc#list-oidc-custom-property-inclusions-for-an-enterprise",
    "category": "parameters"
  },
  {
    "question": "Which HTTP status indicates that an OIDC custom property inclusion already exists for an enterprise?",
    "gold_answer": "422",
    "source_url": "https://docs.github.com/rest/actions/oidc#create-an-oidc-custom-property-inclusion-for-an-enterprise",
    "category": "error_code"
  },
  {
    "question": "What does the `custom_property_name` path parameter identify when deleting an enterprise OIDC custom property inclusion?",
    "gold_answer": "The name of the custom property to remove from OIDC token inclusion",
    "source_url": "https://docs.github.com/rest/actions/oidc#delete-an-oidc-custom-property-inclusion-for-an-enterprise",
    "category": "parameters"
  },
  {
    "question": "Which token scope is required to read an organization's GitHub Actions cache retention limit?",
    "gold_answer": "The `admin:organization` scope is needed to use this endpoint.",
    "source_url": "https://docs.github.com/rest/actions/cache#get-github-actions-cache-retention-limit-for-an-organization",
    "category": "parameters"
  },
  {
    "question": "Which HTTP error statuses are documented when setting an organization's GitHub Actions cache storage limit?",
    "gold_answer": "400 Bad Request, 403 Forbidden, and 404 Resource not found",
    "source_url": "https://docs.github.com/rest/actions/cache#set-github-actions-cache-storage-limit-for-an-organization",
    "category": "error_code"
  },
  {
    "question": "How frequently should a client expect an organization's GitHub Actions cache usage data to refresh?",
    "gold_answer": "Every 5 minutes, so values returned from this endpoint may take at least 5 minutes to get updated.",
    "source_url": "https://docs.github.com/rest/actions/cache#get-github-actions-cache-usage-for-an-organization",
    "category": "lookup"
  },
  {
    "question": "What is the maximum `per_page` value when listing repositories with GitHub Actions cache usage for an organization?",
    "gold_answer": "The maximum is 100 results per page.",
    "source_url": "https://docs.github.com/rest/actions/cache#list-repositories-with-github-actions-cache-usage-for-an-organization",
    "category": "parameters"
  },
  {
    "question": "Which token scope is required to list GitHub-hosted runners for an organization?",
    "gold_answer": "The `manage_runner:org` scope is needed to use this endpoint.",
    "source_url": "https://docs.github.com/rest/actions/hosted-runners#list-github-hosted-runners-for-an-organization",
    "category": "parameters"
  },
  {
    "question": "How do I configure billing limits and update credit card information for my GitHub Enterprise account?",
    "gold_answer": "NOT_COVERED",
    "source_url": "",
    "category": "negative"
  },
  {
    "question": "What endpoint should I use to retrieve user profile emails and SSH keys?",
    "gold_answer": "NOT_COVERED",
    "source_url": "",
    "category": "negative"
  },
  {
    "question": "How can I set up GitHub Copilot seat assignments and manage license seating charts?",
    "gold_answer": "NOT_COVERED",
    "source_url": "",
    "category": "negative"
  },
  {
    "question": "What does the `org` path parameter represent for the organization GitHub Actions cache retention endpoint, and is it case sensitive?",
    "gold_answer": "The organization name. The name is not case sensitive.",
    "source_url": "https://docs.github.com/rest/actions/cache#get-github-actions-cache-retention-limit-for-an-organization",
    "category": "parameters"
  },
  {
    "question": "Which token scope is required to create an OIDC custom property inclusion for an organization?",
    "gold_answer": "The `admin:org` scope is needed to use this endpoint.",
    "source_url": "https://docs.github.com/rest/actions/oidc#create-an-oidc-custom-property-inclusion-for-an-organization",
    "category": "parameters"
  },
  {
    "question": "Which HTTP status indicates successful deletion of a custom image version from an organization?",
    "gold_answer": "The API returns `204`.",
    "source_url": "https://docs.github.com/rest/actions/hosted-runners#delete-an-image-version-of-custom-image-from-the-organization",
    "category": "error_code"
  },
  {
    "question": "Which HTTP method should a client use to set an organization's OIDC subject-claim customization template?",
    "gold_answer": "Use the `PUT` method.",
    "source_url": "https://docs.github.com/rest/actions/oidc#set-the-customization-template-for-an-oidc-subject-claim-for-an-organization",
    "category": "lookup"
  },
  {
    "question": "Which token scope is required to read an organization's GitHub Actions permissions?",
    "gold_answer": "The `admin:org` scope is needed to use this endpoint.",
    "source_url": "https://docs.github.com/rest/actions/permissions#get-github-actions-permissions-for-an-organization",
    "category": "parameters"
  },
  {
    "question": "When listing organization members, what does `filter=2fa_disabled` return, and who can use this filter?",
    "gold_answer": "It means that only members without two-factor authentication enabled will be returned (an option only available for organization owners).",
    "source_url": "https://docs.github.com/rest/orgs/members#list-organization-members",
    "category": "parameters"
  },
  {
    "question": "If the requester is not an organization member, which HTTP status is returned when checking another user's membership?",
    "gold_answer": "302",
    "source_url": "https://docs.github.com/rest/orgs/members#check-organization-membership-for-a-user",
    "category": "error_code"
  },
  {
    "question": "When removing a user from an organization, what happens if they also have indirect membership through an enterprise team?",
    "gold_answer": "Their indirect membership via an enterprise team remains until the user is removed from the enterprise team.",
    "source_url": "https://docs.github.com/rest/orgs/members#remove-an-organization-member",
    "category": "lookup"
  },
  {
    "question": "Which token scope is required to list an organization's Codespaces for a specific user?",
    "gold_answer": "The `admin:org` scope is needed to use this endpoint.",
    "source_url": "https://docs.github.com/rest/codespaces/organizations#list-codespaces-for-a-user-in-organization",
    "category": "parameters"
  },
  {
    "question": "Which HTTP status indicates that an organization Codespace deletion request was accepted?",
    "gold_answer": "202",
    "source_url": "https://docs.github.com/rest/codespaces/organizations#delete-a-codespace-from-the-organization",
    "category": "error_code"
  },
  {
    "question": "Which token scope is required to stop a Codespace belonging to an organization user?",
    "gold_answer": "The `admin:org` scope is needed to use this endpoint.",
    "source_url": "https://docs.github.com/rest/codespaces/organizations#stop-a-codespace-for-an-organization-user",
    "category": "parameters"
  },
  {
    "question": "Which organization role is authorized to view Copilot seat assignment details for members?",
    "gold_answer": "Only organization owners can view Copilot seat assignment details for members of their organization.",
    "source_url": "https://docs.github.com/rest/copilot/copilot-user-management#get-copilot-seat-assignment-details-for-a-user",
    "category": "parameters"
  },
  {
    "question": "What membership requirement must the authenticated user satisfy to retrieve another user's organization membership?",
    "gold_answer": "The authenticated user must be an organization member.",
    "source_url": "https://docs.github.com/rest/orgs/members#get-organization-membership-for-a-user",
    "category": "lookup"
  },
  {
    "question": "What are the 24-hour limits on organization invitations, and when does the higher limit apply?",
    "gold_answer": "Organization owners are limited to creating 50 organization invitations within a 24-hour period. If the organization is more than one month old or on a paid plan, the limit is 500 invitations per 24 hour period.",
    "source_url": "https://docs.github.com/rest/orgs/members#set-organization-membership-for-a-user",
    "category": "parameters"
  },
  {
    "question": "Which organization role must the authenticated user have to remove a user's membership?",
    "gold_answer": "The authenticated user must be an organization owner.",
    "source_url": "https://docs.github.com/rest/orgs/members#remove-organization-membership-for-a-user",
    "category": "lookup"
  },
  {
    "question": "For an organization membership audit, how can a client filter members based on their 2FA status, and who is allowed to use those filters?",
    "gold_answer": "You can use the `filter` query parameter. Setting `filter=2fa_disabled` returns only members without two-factor authentication enabled, and setting `filter=2fa_insecure` returns members with insecure 2FA methods. Note that these filtering options are restricted and only available for organization owners.",
    "source_url": "https://docs.github.com/rest/orgs/members#list-organization-members",
    "category": "parameters"
  },
  {
    "question": "When checking organization membership, which HTTP status indicates that both the requester and target user are members?",
    "gold_answer": "Your code should expect an HTTP 204 status response, which indicates that both the requester is an organization member and the target user is a member.",
    "source_url": "https://docs.github.com/rest/orgs/members#check-organization-membership-for-a-user",
    "category": "error_code"
  },
  {
    "question": "If a user has both direct organization membership and indirect enterprise-team membership, what access remains after removing the direct membership?",
    "gold_answer": "Removing them from the direct organization membership list removes them from all teams and repository access. However, if they have indirect membership via an enterprise team, that indirect membership will remain active until they are explicitly removed from the enterprise team.",
    "source_url": "https://docs.github.com/rest/orgs/members#remove-an-organization-member",
    "category": "lookup"
  },
  {
    "question": "Which token scope does a provisioning script need to list Codespaces for a specific organization member?",
    "gold_answer": "OAuth app tokens and classic personal access tokens require the `admin:org` scope to successfully query and use this endpoint.",
    "source_url": "https://docs.github.com/rest/codespaces/organizations#list-codespaces-for-a-user-in-organization",
    "category": "parameters"
  },
  {
    "question": "When an organization Codespace deletion request is accepted, which HTTP success status should the client handle?",
    "gold_answer": "The API returns an HTTP 202 (Accepted) status response.",
    "source_url": "https://docs.github.com/rest/codespaces/organizations#delete-a-codespace-from-the-organization",
    "category": "error_code"
  },
  {
    "question": "Which token scope must a client have to stop an organization user's Codespace?",
    "gold_answer": "You must use an OAuth app token or personal access token (classic) configured with the `admin:org` scope.",
    "source_url": "https://docs.github.com/rest/codespaces/organizations#stop-a-codespace-for-an-organization-user",
    "category": "parameters"
  },
  {
    "question": "Who can view Copilot seat assignment details for organization members, and which classic-token scopes are supported?",
    "gold_answer": "Only organization owners are permitted to view Copilot seat assignment details for members. For authentication, OAuth app tokens and personal access tokens (classic) need either the `manage_billing:copilot` or `read:org` scopes.",
    "source_url": "https://docs.github.com/rest/copilot/copilot-user-management#get-copilot-seat-assignment-details-for-a-user",
    "category": "parameters"
  },
  {
    "question": "What organization-membership requirement must the authenticated account satisfy before retrieving another user's membership details?",
    "gold_answer": "The authenticated user making the API request must already be a member of the organization in order to retrieve another user's membership details.",
    "source_url": "https://docs.github.com/rest/orgs/members#get-organization-membership-for-a-user",
    "category": "lookup"
  },
  {
    "question": "What invitation rate limits apply to organization owners over a 24-hour period, and when is the higher limit available?",
    "gold_answer": "Yes. To prevent abuse, organization owners are limited to creating 50 organization invitations within a 24-hour period. If the organization is older than one month or operating on a paid plan, that threshold increases to a maximum of 500 invitations per 24-hour period.",
    "source_url": "https://docs.github.com/rest/orgs/members#set-organization-membership-for-a-user",
    "category": "parameters"
  },
  {
    "question": "Which role must the authenticated account have to remove a user's organization membership through the API?",
    "gold_answer": "The authenticated user executing the removal request must be an organization owner; otherwise, the request will fail due to insufficient permissions.",
    "source_url": "https://docs.github.com/rest/orgs/members#remove-organization-membership-for-a-user",
    "category": "lookup"
  },
  {
    "question": "What happens if a directory contains more than 1,000 files when using the get repository content endpoint?",
    "gold_answer": "This API has an upper limit of 1,000 files for a directory. If you need to retrieve more files, you must use the Git Trees API instead.",
    "source_url": "https://docs.github.com/rest/repos/contents#get-repository-content",
    "category": "lookup"
  },
  {
    "question": "What custom media types are supported when a file's size is between 1 MB and 100 MB using the get repository content endpoint?",
    "gold_answer": "Only the `raw` or `object` custom media types are supported for files between 1-100 MB.",
    "source_url": "https://docs.github.com/rest/repos/contents#get-repository-content",
    "category": "parameters"
  },
  {
    "question": "Can I run the create or update file contents and delete a file endpoints in parallel?",
    "gold_answer": "No. Concurrent requests will conflict and result in errors, so you must use these endpoints serially instead.",
    "source_url": "https://docs.github.com/rest/repos/contents#create-or-update-file-contents",
    "category": "lookup"
  },
  {
    "question": "What is the maximum file size allowed to be searchable when using the search code endpoint?",
    "gold_answer": "Only files smaller than 384 KB are searchable.",
    "source_url": "https://docs.github.com/rest/search/search#search-code",
    "category": "lookup"
  },
  {
    "question": "Which branch is considered when performing a code search?",
    "gold_answer": "Only the default branch (in most cases, the `master` branch) is considered.",
    "source_url": "https://docs.github.com/rest/search/search#search-code",
    "category": "lookup"
  },
  {
    "question": "What field can you obtain text match metadata for when searching commits with the `text-match` media type?",
    "gold_answer": "You can get text match metadata for the `message` field.",
    "source_url": "https://docs.github.com/rest/search/search#search-commits",
    "category": "parameters"
  },
  {
    "question": "Does the search labels endpoint accept query qualifiers?",
    "gold_answer": "No, this endpoint does not accept qualifiers in the query.",
    "source_url": "https://docs.github.com/rest/search/search#search-labels",
    "category": "lookup"
  },
  {
    "question": "What query parameter is required to specify the repository identifier when searching for labels?",
    "gold_answer": "The `repository_id` parameter.",
    "source_url": "https://docs.github.com/rest/search/search#search-labels",
    "category": "parameters"
  },
  {
    "question": "What fields can be used to sort repository search results?",
    "gold_answer": "Results can be sorted by number of `stars`, `forks`, or `help-wanted-issues`, or how recently items were `updated`.",
    "source_url": "https://docs.github.com/rest/search/search#search-repositories",
    "category": "parameters"
  },
  {
    "question": "Which topic fields support text match metadata when passing the `text-match` media type?",
    "gold_answer": "The topic's `short_description`, `description`, `name`, or `display_name` field.",
    "source_url": "https://docs.github.com/rest/search/search#search-topics",
    "category": "parameters"
  },
  {
    "question": "Does the search users endpoint accept authentication?",
    "gold_answer": "This endpoint does not accept authentication and will only include publicly visible users.",
    "source_url": "https://docs.github.com/rest/search/search#search-users",
    "category": "lookup"
  },
  {
    "question": "What alternative API can be used to search for private users or Enterprise Managed Users (EMUs)?",
    "gold_answer": "You can use the GraphQL API, which requires authentication and returns private users.",
    "source_url": "https://docs.github.com/rest/search/search#search-users",
    "category": "lookup"
  },
  {
    "question": "What is the request rate limit for the search code endpoint?",
    "gold_answer": "It requires you to authenticate and limits you to 10 requests per minute.",
    "source_url": "https://docs.github.com/rest/search/search#search-code",
    "category": "lookup"
  },
  
  {
    "question": "How do I search for code using a specific query?",
    "gold_answer": "You can use the `/search/code` endpoint with the `q` query parameter containing your keywords and qualifiers.",
    "source_url": "https://docs.github.com/rest/search/search#search-code",
    "category": "parameters"
  },
  {
    "question": "What's the file size limit when searching code?",
    "gold_answer": "Only files smaller than 384 KB are searchable.",
    "source_url": "https://docs.github.com/rest/search/search#search-code",
    "category": "lookup"
  },
  {
    "question": "How do I find commits related to a certain topic in a repo?",
    "gold_answer": "Use the `/search/commits` endpoint and pass a query string like `q=repo:owner/name+keyword`.",
    "source_url": "https://docs.github.com/rest/search/search#search-commits",
    "category": "lookup"
  },
  {
    "question": "Can I use query qualifiers when searching for labels?",
    "gold_answer": "No, the search labels endpoint does not accept qualifiers in the query.",
    "source_url": "https://docs.github.com/rest/search/search#search-labels",
    "category": "lookup"
  },
  {
    "question": "How do I sort repository search results by stars?",
    "gold_answer": "Pass `sort=stars` and `order=desc` in your query parameters.",
    "source_url": "https://docs.github.com/rest/search/search#search-repositories",
    "category": "parameters"
  },
  {
    "question": "Does the user search endpoint require authentication?",
    "gold_answer": "This endpoint does not accept authentication and will only include publicly visible users.",
    "source_url": "https://docs.github.com/rest/search/search#search-users",
    "category": "lookup"
  },
  {
    "question": "How do I search for issues assigned to me using the API?",
    "gold_answer": "NOT_COVERED",
    "source_url": "",
    "category": "negative"
  },
  {
    "question": "Can I search for pull requests by author name?",
    "gold_answer": "NOT_COVERED",
    "source_url": "",
    "category": "negative"
  },
  {
    "question": "How do I list all the teams in my organization?",
    "gold_answer": "You can use the GET `/orgs/{org}/teams` endpoint to list all teams in an organization that are visible to you.",
    "source_url": "https://docs.github.com/rest/teams/teams#list-teams",
    "category": "lookup"
  },
  {
    "question": "What permissions do I need to create a team in an organization?",
    "gold_answer": "The authenticated user must be a member or owner of the organization.",
    "source_url": "https://docs.github.com/rest/teams/teams#create-a-team",
    "category": "parameters"
  },
  {
    "question": "How are team slugs generated from team names?",
    "gold_answer": "GitHub replaces special characters, changes all words to lowercase, and replaces spaces with a `-` separator.",
    "source_url": "https://docs.github.com/rest/teams/teams#get-a-team-by-name",
    "category": "lookup"
  },
  {
    "question": "What happens to child teams if an organization owner deletes a parent team?",
    "gold_answer": "Deleting a parent team will delete all of its child teams as well.",
    "source_url": "https://docs.github.com/rest/teams/teams#delete-a-team",
    "category": "lookup"
  },
  {
    "question": "What token scopes are needed to list team repositories using a personal access token?",
    "gold_answer": "OAuth app tokens and personal access tokens (classic) need either the `read:org` or `repo` scope.",
    "source_url": "https://docs.github.com/rest/teams/teams#list-team-repositories",
    "category": "parameters"
  },
  {
    "question": "How do I transfer a team to a different organization using the API?",
    "gold_answer": "NOT_COVERED",
    "source_url": "",
    "category": "negative"
  },
  {
    "question": "Can I automatically sync team members with an external LDAP directory?",
    "gold_answer": "NOT_COVERED",
    "source_url": "",
    "category": "negative"
  }


]



with open('data/eval/golden_dataset.json', 'w') as f:
    json.dump(golden_dataset, f, indent=2)

print(f"Total questions: {len(golden_dataset)}")