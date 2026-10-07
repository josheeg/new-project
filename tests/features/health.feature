@spec
Feature: Service health endpoint
  The health operation defined in openapi/openapi.yaml is served by
  connexion with strict request validation.

  Scenario: Health check reports ok and the app version
    When I request "/health"
    Then the response status is 200
    And the response body field "status" is "ok"
    And the response body has field "version"

  Scenario: Unknown query parameters are rejected
    When I request "/health?bogus=1"
    Then the response status is 400

  Scenario: Unknown paths fall through to 404
    When I request "/nope"
    Then the response status is 404
