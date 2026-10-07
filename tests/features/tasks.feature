@spec
Feature: Task domain invariants
  The canonical Task model enforces the invariants the API layer
  relies on, at construction time.

  Scenario: Tags are stripped and deduplicated
    Given a task titled "Ship the spec workflow" with tags "  api  ", "api", " docs"
    Then the task tags are "api", "docs"

  Scenario: A blank title is rejected
    When I create a task titled "   "
    Then task creation fails with "title must not be blank"
