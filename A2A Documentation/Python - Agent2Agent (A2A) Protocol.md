---
title: "Python - Agent2Agent (A2A) Protocol"
description: "An open protocol enabling communication and interoperability between opaque agentic applications."
keywords: ""
source: "https://a2a-protocol.org/latest/sdk/python/"
---

Bases: `RootModel[Any]`

### `root` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.A2A.root "Permanent link")

## `A2AError` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.A2AError "Permanent link")

## `A2ARequest` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.A2ARequest "Permanent link")

## `APIKeySecurityScheme` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.APIKeySecurityScheme "Permanent link")

Bases: `A2ABaseModel`

API Key security scheme.

### `description = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.APIKeySecurityScheme.description "Permanent link")

Description of this security scheme.

### `in_ = Field(..., alias='in')` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.APIKeySecurityScheme.in_ "Permanent link")

The location of the API key. Valid values are "query", "header", or "cookie".

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.APIKeySecurityScheme.model_config "Permanent link")

### `name` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.APIKeySecurityScheme.name "Permanent link")

The name of the header, query or cookie parameter to be used.

### `type = 'apiKey'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.APIKeySecurityScheme.type "Permanent link")

## `AgentCapabilities` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentCapabilities "Permanent link")

Bases: `A2ABaseModel`

Defines optional capabilities supported by an agent.

### `extensions = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentCapabilities.extensions "Permanent link")

extensions supported by this agent.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentCapabilities.model_config "Permanent link")

### `pushNotifications = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentCapabilities.pushNotifications "Permanent link")

true if the agent can notify updates to client.

### `stateTransitionHistory = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentCapabilities.stateTransitionHistory "Permanent link")

true if the agent exposes status change history for tasks.

### `streaming = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentCapabilities.streaming "Permanent link")

true if the agent supports SSE.

## `AgentCard` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentCard "Permanent link")

Bases: `A2ABaseModel`

An AgentCard conveys key information: - Overall details (version, name, description, uses) - Skills: A set of capabilities the agent can perform - Default modalities/content types supported by the agent. - Authentication requirements

### `additionalInterfaces = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentCard.additionalInterfaces "Permanent link")

Announcement of additional supported transports. Client can use any of the supported transports.

### `capabilities` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentCard.capabilities "Permanent link")

Optional capabilities supported by the agent.

### `defaultInputModes` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentCard.defaultInputModes "Permanent link")

The set of interaction modes that the agent supports across all skills. This can be overridden per-skill. Supported media types for input.

### `defaultOutputModes` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentCard.defaultOutputModes "Permanent link")

Supported media types for output.

### `description = Field(..., examples=['Agent that helps users with recipes and cooking.'])` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentCard.description "Permanent link")

A human-readable description of the agent. Used to assist users and other agents in understanding what the agent can do.

### `documentationUrl = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentCard.documentationUrl "Permanent link")

A URL to documentation for the agent.

### `iconUrl = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentCard.iconUrl "Permanent link")

A URL to an icon for the agent.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentCard.model_config "Permanent link")

### `name = Field(..., examples=['Recipe Agent'])` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentCard.name "Permanent link")

Human readable name of the agent.

### `preferredTransport = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentCard.preferredTransport "Permanent link")

The transport of the preferred endpoint. If empty, defaults to JSONRPC.

### `protocolVersion = '0.2.5'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentCard.protocolVersion "Permanent link")

The version of the A2A protocol this agent supports.

### `provider = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentCard.provider "Permanent link")

The service provider of the agent

### `security = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentCard.security "Permanent link")

Security requirements for contacting the agent.

### `securitySchemes = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentCard.securitySchemes "Permanent link")

Security scheme details used for authenticating with this agent.

### `skills` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentCard.skills "Permanent link")

Skills are a unit of capability that an agent can perform.

### `supportsAuthenticatedExtendedCard = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentCard.supportsAuthenticatedExtendedCard "Permanent link")

true if the agent supports providing an extended agent card when the user is authenticated. Defaults to false if not specified.

### `url` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentCard.url "Permanent link")

A URL to the address the agent is hosted at. This represents the preferred endpoint as declared by the agent.

### `version = Field(..., examples=['1.0.0'])` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentCard.version "Permanent link")

The version of the agent - format is up to the provider.

## `AgentExtension` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentExtension "Permanent link")

Bases: `A2ABaseModel`

A declaration of an extension supported by an Agent.

### `description = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentExtension.description "Permanent link")

A description of how this agent uses this extension.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentExtension.model_config "Permanent link")

### `params = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentExtension.params "Permanent link")

Optional configuration for the extension.

### `required = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentExtension.required "Permanent link")

Whether the client must follow specific requirements of the extension.

### `uri` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentExtension.uri "Permanent link")

The URI of the extension.

## `AgentInterface` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentInterface "Permanent link")

Bases: `A2ABaseModel`

AgentInterface provides a declaration of a combination of the target url and the supported transport to interact with the agent.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentInterface.model_config "Permanent link")

### `transport` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentInterface.transport "Permanent link")

The transport supported this url. This is an open form string, to be easily extended for many transport protocols. The core ones officially supported are JSONRPC, GRPC and HTTP+JSON.

### `url` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentInterface.url "Permanent link")

## `AgentProvider` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentProvider "Permanent link")

Bases: `A2ABaseModel`

Represents the service provider of an agent.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentProvider.model_config "Permanent link")

### `organization` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentProvider.organization "Permanent link")

Agent provider's organization name.

### `url` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentProvider.url "Permanent link")

Agent provider's URL.

## `AgentSkill` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentSkill "Permanent link")

Bases: `A2ABaseModel`

Represents a unit of capability that an agent can perform.

### `description` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentSkill.description "Permanent link")

Description of the skill - will be used by the client or a human as a hint to understand what the skill does.

### `examples = Field(default=None, examples=[['I need a recipe for bread']])` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentSkill.examples "Permanent link")

The set of example scenarios that the skill can perform. Will be used by the client as a hint to understand how the skill can be used.

### `id` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentSkill.id "Permanent link")

Unique identifier for the agent's skill.

### `inputModes = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentSkill.inputModes "Permanent link")

The set of interaction modes that the skill supports (if different than the default). Supported media types for input.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentSkill.model_config "Permanent link")

### `name` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentSkill.name "Permanent link")

Human readable name of the skill.

### `outputModes = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentSkill.outputModes "Permanent link")

Supported media types for output.

### `tags = Field(..., examples=[['cooking', 'customer support', 'billing']])` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AgentSkill.tags "Permanent link")

Set of tagwords describing classes of capabilities for this specific skill.

## `Artifact` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Artifact "Permanent link")

Bases: `A2ABaseModel`

Represents an artifact generated for a task.

### `artifactId` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Artifact.artifactId "Permanent link")

Unique identifier for the artifact.

### `description = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Artifact.description "Permanent link")

Optional description for the artifact.

### `extensions = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Artifact.extensions "Permanent link")

The URIs of extensions that are present or contributed to this Artifact.

### `metadata = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Artifact.metadata "Permanent link")

Extension metadata.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Artifact.model_config "Permanent link")

### `name = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Artifact.name "Permanent link")

Optional name for the artifact.

### `parts` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Artifact.parts "Permanent link")

Artifact parts.

Bases: `A2ABaseModel`

Configuration details for a supported OAuth Flow

### `authorizationUrl` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AuthorizationCodeOAuthFlow.authorizationUrl "Permanent link")

The authorization URL to be used for this flow. This MUST be in the form of a URL. The OAuth2 standard requires the use of TLS

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AuthorizationCodeOAuthFlow.model_config "Permanent link")

### `refreshUrl = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AuthorizationCodeOAuthFlow.refreshUrl "Permanent link")

The URL to be used for obtaining refresh tokens. This MUST be in the form of a URL. The OAuth2 standard requires the use of TLS.

### `scopes` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AuthorizationCodeOAuthFlow.scopes "Permanent link")

The available scopes for the OAuth2 security scheme. A map between the scope name and a short description for it. The map MAY be empty.

### `tokenUrl` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.AuthorizationCodeOAuthFlow.tokenUrl "Permanent link")

The token URL to be used for this flow. This MUST be in the form of a URL. The OAuth2 standard requires the use of TLS.

## `CancelTaskRequest` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.CancelTaskRequest "Permanent link")

Bases: `A2ABaseModel`

JSON-RPC request model for the 'tasks/cancel' method.

### `id` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.CancelTaskRequest.id "Permanent link")

An identifier established by the Client that MUST contain a String, Number. Numbers SHOULD NOT contain fractional parts.

### `jsonrpc = '2.0'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.CancelTaskRequest.jsonrpc "Permanent link")

Specifies the version of the JSON-RPC protocol. MUST be exactly "2.0".

### `method = 'tasks/cancel'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.CancelTaskRequest.method "Permanent link")

A String containing the name of the method to be invoked.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.CancelTaskRequest.model_config "Permanent link")

### `params` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.CancelTaskRequest.params "Permanent link")

A Structured value that holds the parameter values to be used during the invocation of the method.

## `CancelTaskSuccessResponse` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.CancelTaskSuccessResponse "Permanent link")

Bases: `A2ABaseModel`

JSON-RPC success response model for the 'tasks/cancel' method.

### `id = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.CancelTaskSuccessResponse.id "Permanent link")

An identifier established by the Client that MUST contain a String, Number. Numbers SHOULD NOT contain fractional parts.

### `jsonrpc = '2.0'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.CancelTaskSuccessResponse.jsonrpc "Permanent link")

Specifies the version of the JSON-RPC protocol. MUST be exactly "2.0".

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.CancelTaskSuccessResponse.model_config "Permanent link")

### `result` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.CancelTaskSuccessResponse.result "Permanent link")

The result object on success.

## `ClientCredentialsOAuthFlow` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.ClientCredentialsOAuthFlow "Permanent link")

Bases: `A2ABaseModel`

Configuration details for a supported OAuth Flow

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.ClientCredentialsOAuthFlow.model_config "Permanent link")

### `refreshUrl = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.ClientCredentialsOAuthFlow.refreshUrl "Permanent link")

The URL to be used for obtaining refresh tokens. This MUST be in the form of a URL. The OAuth2 standard requires the use of TLS.

### `scopes` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.ClientCredentialsOAuthFlow.scopes "Permanent link")

The available scopes for the OAuth2 security scheme. A map between the scope name and a short description for it. The map MAY be empty.

### `tokenUrl` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.ClientCredentialsOAuthFlow.tokenUrl "Permanent link")

The token URL to be used for this flow. This MUST be in the form of a URL. The OAuth2 standard requires the use of TLS.

## `ContentTypeNotSupportedError` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.ContentTypeNotSupportedError "Permanent link")

Bases: `A2ABaseModel`

A2A specific error indicating incompatible content types between request and agent capabilities.

### `code = -32005` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.ContentTypeNotSupportedError.code "Permanent link")

A Number that indicates the error type that occurred.

### `data = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.ContentTypeNotSupportedError.data "Permanent link")

A Primitive or Structured value that contains additional information about the error. This may be omitted.

### `message = 'Incompatible content types'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.ContentTypeNotSupportedError.message "Permanent link")

A String providing a short description of the error.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.ContentTypeNotSupportedError.model_config "Permanent link")

## `DataPart` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.DataPart "Permanent link")

Bases: `A2ABaseModel`

Represents a structured data segment within a message part.

### `data` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.DataPart.data "Permanent link")

Structured data content

### `kind = 'data'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.DataPart.kind "Permanent link")

Part type - data for DataParts

### `metadata = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.DataPart.metadata "Permanent link")

Optional metadata associated with the part.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.DataPart.model_config "Permanent link")

## `DeleteTaskPushNotificationConfigParams` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.DeleteTaskPushNotificationConfigParams "Permanent link")

Bases: `A2ABaseModel`

Parameters for removing pushNotificationConfiguration associated with a Task

### `id` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.DeleteTaskPushNotificationConfigParams.id "Permanent link")

Task id.

### `metadata = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.DeleteTaskPushNotificationConfigParams.metadata "Permanent link")

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.DeleteTaskPushNotificationConfigParams.model_config "Permanent link")

### `pushNotificationConfigId` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.DeleteTaskPushNotificationConfigParams.pushNotificationConfigId "Permanent link")

## `DeleteTaskPushNotificationConfigRequest` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.DeleteTaskPushNotificationConfigRequest "Permanent link")

Bases: `A2ABaseModel`

JSON-RPC request model for the 'tasks/pushNotificationConfig/delete' method.

### `id` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.DeleteTaskPushNotificationConfigRequest.id "Permanent link")

An identifier established by the Client that MUST contain a String, Number. Numbers SHOULD NOT contain fractional parts.

### `jsonrpc = '2.0'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.DeleteTaskPushNotificationConfigRequest.jsonrpc "Permanent link")

Specifies the version of the JSON-RPC protocol. MUST be exactly "2.0".

### `method = 'tasks/pushNotificationConfig/delete'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.DeleteTaskPushNotificationConfigRequest.method "Permanent link")

A String containing the name of the method to be invoked.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.DeleteTaskPushNotificationConfigRequest.model_config "Permanent link")

### `params` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.DeleteTaskPushNotificationConfigRequest.params "Permanent link")

A Structured value that holds the parameter values to be used during the invocation of the method.

## `DeleteTaskPushNotificationConfigSuccessResponse` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.DeleteTaskPushNotificationConfigSuccessResponse "Permanent link")

Bases: `A2ABaseModel`

JSON-RPC success response model for the 'tasks/pushNotificationConfig/delete' method.

### `id = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.DeleteTaskPushNotificationConfigSuccessResponse.id "Permanent link")

An identifier established by the Client that MUST contain a String, Number. Numbers SHOULD NOT contain fractional parts.

### `jsonrpc = '2.0'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.DeleteTaskPushNotificationConfigSuccessResponse.jsonrpc "Permanent link")

Specifies the version of the JSON-RPC protocol. MUST be exactly "2.0".

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.DeleteTaskPushNotificationConfigSuccessResponse.model_config "Permanent link")

### `result` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.DeleteTaskPushNotificationConfigSuccessResponse.result "Permanent link")

The result object on success.

## `FileBase` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.FileBase "Permanent link")

Bases: `A2ABaseModel`

Represents the base entity for FileParts

### `mimeType = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.FileBase.mimeType "Permanent link")

Optional mimeType for the file

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.FileBase.model_config "Permanent link")

### `name = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.FileBase.name "Permanent link")

Optional name for the file

## `FilePart` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.FilePart "Permanent link")

Bases: `A2ABaseModel`

Represents a File segment within parts.

### `file` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.FilePart.file "Permanent link")

File content either as url or bytes

### `kind = 'file'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.FilePart.kind "Permanent link")

Part type - file for FileParts

### `metadata = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.FilePart.metadata "Permanent link")

Optional metadata associated with the part.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.FilePart.model_config "Permanent link")

## `FileWithBytes` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.FileWithBytes "Permanent link")

Bases: `A2ABaseModel`

Define the variant where 'bytes' is present and 'uri' is absent

### `bytes` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.FileWithBytes.bytes "Permanent link")

base64 encoded content of the file

### `mimeType = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.FileWithBytes.mimeType "Permanent link")

Optional mimeType for the file

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.FileWithBytes.model_config "Permanent link")

### `name = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.FileWithBytes.name "Permanent link")

Optional name for the file

## `FileWithUri` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.FileWithUri "Permanent link")

Bases: `A2ABaseModel`

Define the variant where 'uri' is present and 'bytes' is absent

### `mimeType = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.FileWithUri.mimeType "Permanent link")

Optional mimeType for the file

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.FileWithUri.model_config "Permanent link")

### `name = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.FileWithUri.name "Permanent link")

Optional name for the file

### `uri` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.FileWithUri.uri "Permanent link")

URL for the File content

## `GetTaskPushNotificationConfigParams` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.GetTaskPushNotificationConfigParams "Permanent link")

Bases: `A2ABaseModel`

Parameters for fetching a pushNotificationConfiguration associated with a Task

### `id` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.GetTaskPushNotificationConfigParams.id "Permanent link")

Task id.

### `metadata = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.GetTaskPushNotificationConfigParams.metadata "Permanent link")

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.GetTaskPushNotificationConfigParams.model_config "Permanent link")

### `pushNotificationConfigId = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.GetTaskPushNotificationConfigParams.pushNotificationConfigId "Permanent link")

## `GetTaskPushNotificationConfigRequest` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.GetTaskPushNotificationConfigRequest "Permanent link")

Bases: `A2ABaseModel`

JSON-RPC request model for the 'tasks/pushNotificationConfig/get' method.

### `id` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.GetTaskPushNotificationConfigRequest.id "Permanent link")

An identifier established by the Client that MUST contain a String, Number. Numbers SHOULD NOT contain fractional parts.

### `jsonrpc = '2.0'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.GetTaskPushNotificationConfigRequest.jsonrpc "Permanent link")

Specifies the version of the JSON-RPC protocol. MUST be exactly "2.0".

### `method = 'tasks/pushNotificationConfig/get'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.GetTaskPushNotificationConfigRequest.method "Permanent link")

A String containing the name of the method to be invoked.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.GetTaskPushNotificationConfigRequest.model_config "Permanent link")

### `params` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.GetTaskPushNotificationConfigRequest.params "Permanent link")

A Structured value that holds the parameter values to be used during the invocation of the method. TaskIdParams type is deprecated for this method use `GetTaskPushNotificationConfigParams` instead.

## `GetTaskPushNotificationConfigSuccessResponse` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.GetTaskPushNotificationConfigSuccessResponse "Permanent link")

Bases: `A2ABaseModel`

JSON-RPC success response model for the 'tasks/pushNotificationConfig/get' method.

### `id = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.GetTaskPushNotificationConfigSuccessResponse.id "Permanent link")

An identifier established by the Client that MUST contain a String, Number. Numbers SHOULD NOT contain fractional parts.

### `jsonrpc = '2.0'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.GetTaskPushNotificationConfigSuccessResponse.jsonrpc "Permanent link")

Specifies the version of the JSON-RPC protocol. MUST be exactly "2.0".

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.GetTaskPushNotificationConfigSuccessResponse.model_config "Permanent link")

### `result` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.GetTaskPushNotificationConfigSuccessResponse.result "Permanent link")

The result object on success.

## `GetTaskRequest` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.GetTaskRequest "Permanent link")

Bases: `A2ABaseModel`

JSON-RPC request model for the 'tasks/get' method.

### `id` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.GetTaskRequest.id "Permanent link")

An identifier established by the Client that MUST contain a String, Number. Numbers SHOULD NOT contain fractional parts.

### `jsonrpc = '2.0'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.GetTaskRequest.jsonrpc "Permanent link")

Specifies the version of the JSON-RPC protocol. MUST be exactly "2.0".

### `method = 'tasks/get'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.GetTaskRequest.method "Permanent link")

A String containing the name of the method to be invoked.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.GetTaskRequest.model_config "Permanent link")

### `params` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.GetTaskRequest.params "Permanent link")

A Structured value that holds the parameter values to be used during the invocation of the method.

## `GetTaskSuccessResponse` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.GetTaskSuccessResponse "Permanent link")

Bases: `A2ABaseModel`

JSON-RPC success response for the 'tasks/get' method.

### `id = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.GetTaskSuccessResponse.id "Permanent link")

An identifier established by the Client that MUST contain a String, Number. Numbers SHOULD NOT contain fractional parts.

### `jsonrpc = '2.0'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.GetTaskSuccessResponse.jsonrpc "Permanent link")

Specifies the version of the JSON-RPC protocol. MUST be exactly "2.0".

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.GetTaskSuccessResponse.model_config "Permanent link")

### `result` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.GetTaskSuccessResponse.result "Permanent link")

The result object on success.

## `HTTPAuthSecurityScheme` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.HTTPAuthSecurityScheme "Permanent link")

Bases: `A2ABaseModel`

HTTP Authentication security scheme.

### `bearerFormat = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.HTTPAuthSecurityScheme.bearerFormat "Permanent link")

A hint to the client to identify how the bearer token is formatted. Bearer tokens are usually generated by an authorization server, so this information is primarily for documentation purposes.

### `description = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.HTTPAuthSecurityScheme.description "Permanent link")

Description of this security scheme.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.HTTPAuthSecurityScheme.model_config "Permanent link")

### `scheme` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.HTTPAuthSecurityScheme.scheme "Permanent link")

The name of the HTTP Authentication scheme to be used in the Authorization header as defined in RFC7235. The values used SHOULD be registered in the IANA Authentication Scheme registry. The value is case-insensitive, as defined in RFC7235.

### `type = 'http'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.HTTPAuthSecurityScheme.type "Permanent link")

## `ImplicitOAuthFlow` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.ImplicitOAuthFlow "Permanent link")

Bases: `A2ABaseModel`

Configuration details for a supported OAuth Flow

### `authorizationUrl` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.ImplicitOAuthFlow.authorizationUrl "Permanent link")

The authorization URL to be used for this flow. This MUST be in the form of a URL. The OAuth2 standard requires the use of TLS

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.ImplicitOAuthFlow.model_config "Permanent link")

### `refreshUrl = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.ImplicitOAuthFlow.refreshUrl "Permanent link")

The URL to be used for obtaining refresh tokens. This MUST be in the form of a URL. The OAuth2 standard requires the use of TLS.

### `scopes` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.ImplicitOAuthFlow.scopes "Permanent link")

The available scopes for the OAuth2 security scheme. A map between the scope name and a short description for it. The map MAY be empty.

## `In` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.In "Permanent link")

Bases: `str`, `Enum`

The location of the API key. Valid values are "query", "header", or "cookie".

### `cookie = 'cookie'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.In.cookie "Permanent link")

### `query = 'query'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.In.query "Permanent link")

## `InternalError` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.InternalError "Permanent link")

Bases: `A2ABaseModel`

JSON-RPC error indicating an internal JSON-RPC error on the server.

### `code = -32603` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.InternalError.code "Permanent link")

A Number that indicates the error type that occurred.

### `data = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.InternalError.data "Permanent link")

A Primitive or Structured value that contains additional information about the error. This may be omitted.

### `message = 'Internal error'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.InternalError.message "Permanent link")

A String providing a short description of the error.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.InternalError.model_config "Permanent link")

## `InvalidAgentResponseError` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.InvalidAgentResponseError "Permanent link")

Bases: `A2ABaseModel`

A2A specific error indicating agent returned invalid response for the current method

### `code = -32006` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.InvalidAgentResponseError.code "Permanent link")

A Number that indicates the error type that occurred.

### `data = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.InvalidAgentResponseError.data "Permanent link")

A Primitive or Structured value that contains additional information about the error. This may be omitted.

### `message = 'Invalid agent response'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.InvalidAgentResponseError.message "Permanent link")

A String providing a short description of the error.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.InvalidAgentResponseError.model_config "Permanent link")

## `InvalidParamsError` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.InvalidParamsError "Permanent link")

Bases: `A2ABaseModel`

JSON-RPC error indicating invalid method parameter(s).

### `code = -32602` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.InvalidParamsError.code "Permanent link")

A Number that indicates the error type that occurred.

### `data = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.InvalidParamsError.data "Permanent link")

A Primitive or Structured value that contains additional information about the error. This may be omitted.

### `message = 'Invalid parameters'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.InvalidParamsError.message "Permanent link")

A String providing a short description of the error.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.InvalidParamsError.model_config "Permanent link")

## `InvalidRequestError` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.InvalidRequestError "Permanent link")

Bases: `A2ABaseModel`

JSON-RPC error indicating the JSON sent is not a valid Request object.

### `code = -32600` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.InvalidRequestError.code "Permanent link")

A Number that indicates the error type that occurred.

### `data = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.InvalidRequestError.data "Permanent link")

A Primitive or Structured value that contains additional information about the error. This may be omitted.

### `message = 'Request payload validation error'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.InvalidRequestError.message "Permanent link")

A String providing a short description of the error.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.InvalidRequestError.model_config "Permanent link")

## `JSONParseError` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.JSONParseError "Permanent link")

Bases: `A2ABaseModel`

JSON-RPC error indicating invalid JSON was received by the server.

### `code = -32700` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.JSONParseError.code "Permanent link")

A Number that indicates the error type that occurred.

### `data = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.JSONParseError.data "Permanent link")

A Primitive or Structured value that contains additional information about the error. This may be omitted.

### `message = 'Invalid JSON payload'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.JSONParseError.message "Permanent link")

A String providing a short description of the error.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.JSONParseError.model_config "Permanent link")

## `JSONRPCError` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.JSONRPCError "Permanent link")

Bases: `A2ABaseModel`

Represents a JSON-RPC 2.0 Error object. This is typically included in a JSONRPCErrorResponse when an error occurs.

### `code` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.JSONRPCError.code "Permanent link")

A Number that indicates the error type that occurred.

### `data = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.JSONRPCError.data "Permanent link")

A Primitive or Structured value that contains additional information about the error. This may be omitted.

### `message` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.JSONRPCError.message "Permanent link")

A String providing a short description of the error.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.JSONRPCError.model_config "Permanent link")

## `JSONRPCErrorResponse` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.JSONRPCErrorResponse "Permanent link")

Bases: `A2ABaseModel`

Represents a JSON-RPC 2.0 Error Response object.

### `error` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.JSONRPCErrorResponse.error "Permanent link")

### `id = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.JSONRPCErrorResponse.id "Permanent link")

An identifier established by the Client that MUST contain a String, Number. Numbers SHOULD NOT contain fractional parts.

### `jsonrpc = '2.0'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.JSONRPCErrorResponse.jsonrpc "Permanent link")

Specifies the version of the JSON-RPC protocol. MUST be exactly "2.0".

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.JSONRPCErrorResponse.model_config "Permanent link")

## `JSONRPCMessage` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.JSONRPCMessage "Permanent link")

Bases: `A2ABaseModel`

Base interface for any JSON-RPC 2.0 request or response.

### `id = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.JSONRPCMessage.id "Permanent link")

An identifier established by the Client that MUST contain a String, Number. Numbers SHOULD NOT contain fractional parts.

### `jsonrpc = '2.0'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.JSONRPCMessage.jsonrpc "Permanent link")

Specifies the version of the JSON-RPC protocol. MUST be exactly "2.0".

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.JSONRPCMessage.model_config "Permanent link")

## `JSONRPCRequest` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.JSONRPCRequest "Permanent link")

Bases: `A2ABaseModel`

Represents a JSON-RPC 2.0 Request object.

### `id = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.JSONRPCRequest.id "Permanent link")

An identifier established by the Client that MUST contain a String, Number. Numbers SHOULD NOT contain fractional parts.

### `jsonrpc = '2.0'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.JSONRPCRequest.jsonrpc "Permanent link")

Specifies the version of the JSON-RPC protocol. MUST be exactly "2.0".

### `method` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.JSONRPCRequest.method "Permanent link")

A String containing the name of the method to be invoked.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.JSONRPCRequest.model_config "Permanent link")

### `params = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.JSONRPCRequest.params "Permanent link")

A Structured value that holds the parameter values to be used during the invocation of the method.

## `JSONRPCResponse` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.JSONRPCResponse "Permanent link")

## `JSONRPCSuccessResponse` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.JSONRPCSuccessResponse "Permanent link")

Bases: `A2ABaseModel`

Represents a JSON-RPC 2.0 Success Response object.

### `id = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.JSONRPCSuccessResponse.id "Permanent link")

An identifier established by the Client that MUST contain a String, Number. Numbers SHOULD NOT contain fractional parts.

### `jsonrpc = '2.0'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.JSONRPCSuccessResponse.jsonrpc "Permanent link")

Specifies the version of the JSON-RPC protocol. MUST be exactly "2.0".

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.JSONRPCSuccessResponse.model_config "Permanent link")

### `result` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.JSONRPCSuccessResponse.result "Permanent link")

The result object on success

## `ListTaskPushNotificationConfigParams` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.ListTaskPushNotificationConfigParams "Permanent link")

Bases: `A2ABaseModel`

Parameters for getting list of pushNotificationConfigurations associated with a Task

### `id` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.ListTaskPushNotificationConfigParams.id "Permanent link")

Task id.

### `metadata = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.ListTaskPushNotificationConfigParams.metadata "Permanent link")

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.ListTaskPushNotificationConfigParams.model_config "Permanent link")

## `ListTaskPushNotificationConfigRequest` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.ListTaskPushNotificationConfigRequest "Permanent link")

Bases: `A2ABaseModel`

JSON-RPC request model for the 'tasks/pushNotificationConfig/list' method.

### `id` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.ListTaskPushNotificationConfigRequest.id "Permanent link")

An identifier established by the Client that MUST contain a String, Number. Numbers SHOULD NOT contain fractional parts.

### `jsonrpc = '2.0'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.ListTaskPushNotificationConfigRequest.jsonrpc "Permanent link")

Specifies the version of the JSON-RPC protocol. MUST be exactly "2.0".

### `method = 'tasks/pushNotificationConfig/list'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.ListTaskPushNotificationConfigRequest.method "Permanent link")

A String containing the name of the method to be invoked.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.ListTaskPushNotificationConfigRequest.model_config "Permanent link")

### `params` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.ListTaskPushNotificationConfigRequest.params "Permanent link")

A Structured value that holds the parameter values to be used during the invocation of the method.

## `ListTaskPushNotificationConfigSuccessResponse` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.ListTaskPushNotificationConfigSuccessResponse "Permanent link")

Bases: `A2ABaseModel`

JSON-RPC success response model for the 'tasks/pushNotificationConfig/list' method.

### `id = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.ListTaskPushNotificationConfigSuccessResponse.id "Permanent link")

An identifier established by the Client that MUST contain a String, Number. Numbers SHOULD NOT contain fractional parts.

### `jsonrpc = '2.0'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.ListTaskPushNotificationConfigSuccessResponse.jsonrpc "Permanent link")

Specifies the version of the JSON-RPC protocol. MUST be exactly "2.0".

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.ListTaskPushNotificationConfigSuccessResponse.model_config "Permanent link")

### `result` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.ListTaskPushNotificationConfigSuccessResponse.result "Permanent link")

The result object on success.

## `Message` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Message "Permanent link")

Bases: `A2ABaseModel`

Represents a single message exchanged between user and agent.

### `contextId = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Message.contextId "Permanent link")

The context the message is associated with

### `extensions = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Message.extensions "Permanent link")

The URIs of extensions that are present or contributed to this Message.

### `kind = 'message'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Message.kind "Permanent link")

Event type

### `messageId` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Message.messageId "Permanent link")

Identifier created by the message creator

### `metadata = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Message.metadata "Permanent link")

Extension metadata.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Message.model_config "Permanent link")

### `parts` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Message.parts "Permanent link")

Message content

### `referenceTaskIds = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Message.referenceTaskIds "Permanent link")

List of tasks referenced as context by this message.

### `role` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Message.role "Permanent link")

Message sender's role

### `taskId = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Message.taskId "Permanent link")

Identifier of task the message is related to

## `MessageSendConfiguration` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.MessageSendConfiguration "Permanent link")

Bases: `A2ABaseModel`

Configuration for the send message request.

### `acceptedOutputModes` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.MessageSendConfiguration.acceptedOutputModes "Permanent link")

Accepted output modalities by the client.

### `blocking = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.MessageSendConfiguration.blocking "Permanent link")

If the server should treat the client as a blocking request.

### `historyLength = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.MessageSendConfiguration.historyLength "Permanent link")

Number of recent messages to be retrieved.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.MessageSendConfiguration.model_config "Permanent link")

### `pushNotificationConfig = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.MessageSendConfiguration.pushNotificationConfig "Permanent link")

Where the server should send notifications when disconnected.

## `MessageSendParams` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.MessageSendParams "Permanent link")

Bases: `A2ABaseModel`

Sent by the client to the agent as a request. May create, continue or restart a task.

### `configuration = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.MessageSendParams.configuration "Permanent link")

Send message configuration.

### `message` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.MessageSendParams.message "Permanent link")

The message being sent to the server.

### `metadata = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.MessageSendParams.metadata "Permanent link")

Extension metadata.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.MessageSendParams.model_config "Permanent link")

## `MethodNotFoundError` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.MethodNotFoundError "Permanent link")

Bases: `A2ABaseModel`

JSON-RPC error indicating the method does not exist or is not available.

### `code = -32601` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.MethodNotFoundError.code "Permanent link")

A Number that indicates the error type that occurred.

### `data = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.MethodNotFoundError.data "Permanent link")

A Primitive or Structured value that contains additional information about the error. This may be omitted.

### `message = 'Method not found'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.MethodNotFoundError.message "Permanent link")

A String providing a short description of the error.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.MethodNotFoundError.model_config "Permanent link")

## `OAuth2SecurityScheme` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.OAuth2SecurityScheme "Permanent link")

Bases: `A2ABaseModel`

OAuth2.0 security scheme configuration.

### `description = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.OAuth2SecurityScheme.description "Permanent link")

Description of this security scheme.

### `flows` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.OAuth2SecurityScheme.flows "Permanent link")

An object containing configuration information for the flow types supported.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.OAuth2SecurityScheme.model_config "Permanent link")

### `type = 'oauth2'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.OAuth2SecurityScheme.type "Permanent link")

## `OAuthFlows` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.OAuthFlows "Permanent link")

Bases: `A2ABaseModel`

Allows configuration of the supported OAuth Flows

### `authorizationCode = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.OAuthFlows.authorizationCode "Permanent link")

Configuration for the OAuth Authorization Code flow. Previously called accessCode in OpenAPI 2.0.

### `clientCredentials = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.OAuthFlows.clientCredentials "Permanent link")

Configuration for the OAuth Client Credentials flow. Previously called application in OpenAPI 2.0

### `implicit = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.OAuthFlows.implicit "Permanent link")

Configuration for the OAuth Implicit flow

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.OAuthFlows.model_config "Permanent link")

### `password = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.OAuthFlows.password "Permanent link")

Configuration for the OAuth Resource Owner Password flow

## `OpenIdConnectSecurityScheme` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.OpenIdConnectSecurityScheme "Permanent link")

Bases: `A2ABaseModel`

OpenID Connect security scheme configuration.

### `description = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.OpenIdConnectSecurityScheme.description "Permanent link")

Description of this security scheme.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.OpenIdConnectSecurityScheme.model_config "Permanent link")

### `openIdConnectUrl` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.OpenIdConnectSecurityScheme.openIdConnectUrl "Permanent link")

Well-known URL to discover the [[OpenID-Connect-Discovery]] provider metadata.

### `type = 'openIdConnect'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.OpenIdConnectSecurityScheme.type "Permanent link")

## `Part` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Part "Permanent link")

Bases: `RootModel[[TextPart](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TextPart "TextPart (a2a.types.TextPart)") | [FilePart](https://a2a-protocol.org/latest/sdk/python/#a2a.types.FilePart "FilePart (a2a.types.FilePart)") | [DataPart](https://a2a-protocol.org/latest/sdk/python/#a2a.types.DataPart "DataPart (a2a.types.DataPart)")]`

### `root` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Part.root "Permanent link")

Represents a part of a message, which can be text, a file, or structured data.

## `PartBase` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.PartBase "Permanent link")

Bases: `A2ABaseModel`

Base properties common to all message parts.

### `metadata = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.PartBase.metadata "Permanent link")

Optional metadata associated with the part.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.PartBase.model_config "Permanent link")

## `PasswordOAuthFlow` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.PasswordOAuthFlow "Permanent link")

Bases: `A2ABaseModel`

Configuration details for a supported OAuth Flow

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.PasswordOAuthFlow.model_config "Permanent link")

### `refreshUrl = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.PasswordOAuthFlow.refreshUrl "Permanent link")

The URL to be used for obtaining refresh tokens. This MUST be in the form of a URL. The OAuth2 standard requires the use of TLS.

### `scopes` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.PasswordOAuthFlow.scopes "Permanent link")

The available scopes for the OAuth2 security scheme. A map between the scope name and a short description for it. The map MAY be empty.

### `tokenUrl` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.PasswordOAuthFlow.tokenUrl "Permanent link")

The token URL to be used for this flow. This MUST be in the form of a URL. The OAuth2 standard requires the use of TLS.

## `PushNotificationAuthenticationInfo` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.PushNotificationAuthenticationInfo "Permanent link")

Bases: `A2ABaseModel`

Defines authentication details for push notifications.

### `credentials = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.PushNotificationAuthenticationInfo.credentials "Permanent link")

Optional credentials

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.PushNotificationAuthenticationInfo.model_config "Permanent link")

### `schemes` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.PushNotificationAuthenticationInfo.schemes "Permanent link")

Supported authentication schemes - e.g. Basic, Bearer

## `PushNotificationConfig` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.PushNotificationConfig "Permanent link")

Bases: `A2ABaseModel`

Configuration for setting up push notifications for task updates.

### `authentication = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.PushNotificationConfig.authentication "Permanent link")

### `id = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.PushNotificationConfig.id "Permanent link")

Push Notification ID - created by server to support multiple callbacks

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.PushNotificationConfig.model_config "Permanent link")

### `token = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.PushNotificationConfig.token "Permanent link")

Token unique to this task/session.

### `url` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.PushNotificationConfig.url "Permanent link")

URL for sending the push notifications.

## `PushNotificationNotSupportedError` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.PushNotificationNotSupportedError "Permanent link")

Bases: `A2ABaseModel`

A2A specific error indicating the agent does not support push notifications.

### `code = -32003` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.PushNotificationNotSupportedError.code "Permanent link")

A Number that indicates the error type that occurred.

### `data = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.PushNotificationNotSupportedError.data "Permanent link")

A Primitive or Structured value that contains additional information about the error. This may be omitted.

### `message = 'Push Notification is not supported'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.PushNotificationNotSupportedError.message "Permanent link")

A String providing a short description of the error.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.PushNotificationNotSupportedError.model_config "Permanent link")

## `Role` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Role "Permanent link")

Bases: `str`, `Enum`

Message sender's role

### `agent = 'agent'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Role.agent "Permanent link")

### `user = 'user'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Role.user "Permanent link")

## `SecuritySchemeBase` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SecuritySchemeBase "Permanent link")

Bases: `A2ABaseModel`

Base properties shared by all security schemes.

### `description = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SecuritySchemeBase.description "Permanent link")

Description of this security scheme.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SecuritySchemeBase.model_config "Permanent link")

## `SendMessageRequest` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SendMessageRequest "Permanent link")

Bases: `A2ABaseModel`

JSON-RPC request model for the 'message/send' method.

### `id` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SendMessageRequest.id "Permanent link")

An identifier established by the Client that MUST contain a String, Number. Numbers SHOULD NOT contain fractional parts.

### `jsonrpc = '2.0'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SendMessageRequest.jsonrpc "Permanent link")

Specifies the version of the JSON-RPC protocol. MUST be exactly "2.0".

### `method = 'message/send'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SendMessageRequest.method "Permanent link")

A String containing the name of the method to be invoked.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SendMessageRequest.model_config "Permanent link")

### `params` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SendMessageRequest.params "Permanent link")

A Structured value that holds the parameter values to be used during the invocation of the method.

## `SendMessageSuccessResponse` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SendMessageSuccessResponse "Permanent link")

Bases: `A2ABaseModel`

JSON-RPC success response model for the 'message/send' method.

### `id = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SendMessageSuccessResponse.id "Permanent link")

An identifier established by the Client that MUST contain a String, Number. Numbers SHOULD NOT contain fractional parts.

### `jsonrpc = '2.0'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SendMessageSuccessResponse.jsonrpc "Permanent link")

Specifies the version of the JSON-RPC protocol. MUST be exactly "2.0".

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SendMessageSuccessResponse.model_config "Permanent link")

### `result` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SendMessageSuccessResponse.result "Permanent link")

The result object on success

## `SendStreamingMessageRequest` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SendStreamingMessageRequest "Permanent link")

Bases: `A2ABaseModel`

JSON-RPC request model for the 'message/stream' method.

### `id` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SendStreamingMessageRequest.id "Permanent link")

An identifier established by the Client that MUST contain a String, Number. Numbers SHOULD NOT contain fractional parts.

### `jsonrpc = '2.0'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SendStreamingMessageRequest.jsonrpc "Permanent link")

Specifies the version of the JSON-RPC protocol. MUST be exactly "2.0".

### `method = 'message/stream'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SendStreamingMessageRequest.method "Permanent link")

A String containing the name of the method to be invoked.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SendStreamingMessageRequest.model_config "Permanent link")

### `params` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SendStreamingMessageRequest.params "Permanent link")

A Structured value that holds the parameter values to be used during the invocation of the method.

## `SendStreamingMessageSuccessResponse` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SendStreamingMessageSuccessResponse "Permanent link")

Bases: `A2ABaseModel`

JSON-RPC success response model for the 'message/stream' method.

### `id = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SendStreamingMessageSuccessResponse.id "Permanent link")

An identifier established by the Client that MUST contain a String, Number. Numbers SHOULD NOT contain fractional parts.

### `jsonrpc = '2.0'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SendStreamingMessageSuccessResponse.jsonrpc "Permanent link")

Specifies the version of the JSON-RPC protocol. MUST be exactly "2.0".

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SendStreamingMessageSuccessResponse.model_config "Permanent link")

### `result` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SendStreamingMessageSuccessResponse.result "Permanent link")

The result object on success

## `SetTaskPushNotificationConfigRequest` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SetTaskPushNotificationConfigRequest "Permanent link")

Bases: `A2ABaseModel`

JSON-RPC request model for the 'tasks/pushNotificationConfig/set' method.

### `id` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SetTaskPushNotificationConfigRequest.id "Permanent link")

An identifier established by the Client that MUST contain a String, Number. Numbers SHOULD NOT contain fractional parts.

### `jsonrpc = '2.0'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SetTaskPushNotificationConfigRequest.jsonrpc "Permanent link")

Specifies the version of the JSON-RPC protocol. MUST be exactly "2.0".

### `method = 'tasks/pushNotificationConfig/set'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SetTaskPushNotificationConfigRequest.method "Permanent link")

A String containing the name of the method to be invoked.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SetTaskPushNotificationConfigRequest.model_config "Permanent link")

### `params` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SetTaskPushNotificationConfigRequest.params "Permanent link")

A Structured value that holds the parameter values to be used during the invocation of the method.

## `SetTaskPushNotificationConfigSuccessResponse` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SetTaskPushNotificationConfigSuccessResponse "Permanent link")

Bases: `A2ABaseModel`

JSON-RPC success response model for the 'tasks/pushNotificationConfig/set' method.

### `id = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SetTaskPushNotificationConfigSuccessResponse.id "Permanent link")

An identifier established by the Client that MUST contain a String, Number. Numbers SHOULD NOT contain fractional parts.

### `jsonrpc = '2.0'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SetTaskPushNotificationConfigSuccessResponse.jsonrpc "Permanent link")

Specifies the version of the JSON-RPC protocol. MUST be exactly "2.0".

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SetTaskPushNotificationConfigSuccessResponse.model_config "Permanent link")

### `result` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.SetTaskPushNotificationConfigSuccessResponse.result "Permanent link")

The result object on success.

## `Task` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Task "Permanent link")

Bases: `A2ABaseModel`

### `artifacts = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Task.artifacts "Permanent link")

Collection of artifacts created by the agent.

### `contextId` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Task.contextId "Permanent link")

Server-generated id for contextual alignment across interactions

### `history = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Task.history "Permanent link")

### `id` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Task.id "Permanent link")

Unique identifier for the task

### `kind = 'task'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Task.kind "Permanent link")

Event type

### `metadata = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Task.metadata "Permanent link")

Extension metadata.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Task.model_config "Permanent link")

### `status` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.Task.status "Permanent link")

Current status of the task

## `TaskArtifactUpdateEvent` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskArtifactUpdateEvent "Permanent link")

Bases: `A2ABaseModel`

Sent by server during sendStream or subscribe requests

### `append = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskArtifactUpdateEvent.append "Permanent link")

Indicates if this artifact appends to a previous one

### `artifact` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskArtifactUpdateEvent.artifact "Permanent link")

Generated artifact

### `contextId` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskArtifactUpdateEvent.contextId "Permanent link")

The context the task is associated with

### `kind = 'artifact-update'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskArtifactUpdateEvent.kind "Permanent link")

Event type

### `lastChunk = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskArtifactUpdateEvent.lastChunk "Permanent link")

Indicates if this is the last chunk of the artifact

### `metadata = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskArtifactUpdateEvent.metadata "Permanent link")

Extension metadata.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskArtifactUpdateEvent.model_config "Permanent link")

### `taskId` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskArtifactUpdateEvent.taskId "Permanent link")

Task id

## `TaskIdParams` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskIdParams "Permanent link")

Bases: `A2ABaseModel`

Parameters containing only a task ID, used for simple task operations.

### `id` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskIdParams.id "Permanent link")

Task id.

### `metadata = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskIdParams.metadata "Permanent link")

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskIdParams.model_config "Permanent link")

## `TaskNotCancelableError` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskNotCancelableError "Permanent link")

Bases: `A2ABaseModel`

A2A specific error indicating the task is in a state where it cannot be canceled.

### `code = -32002` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskNotCancelableError.code "Permanent link")

A Number that indicates the error type that occurred.

### `data = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskNotCancelableError.data "Permanent link")

A Primitive or Structured value that contains additional information about the error. This may be omitted.

### `message = 'Task cannot be canceled'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskNotCancelableError.message "Permanent link")

A String providing a short description of the error.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskNotCancelableError.model_config "Permanent link")

## `TaskNotFoundError` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskNotFoundError "Permanent link")

Bases: `A2ABaseModel`

A2A specific error indicating the requested task ID was not found.

### `code = -32001` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskNotFoundError.code "Permanent link")

A Number that indicates the error type that occurred.

### `data = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskNotFoundError.data "Permanent link")

A Primitive or Structured value that contains additional information about the error. This may be omitted.

### `message = 'Task not found'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskNotFoundError.message "Permanent link")

A String providing a short description of the error.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskNotFoundError.model_config "Permanent link")

## `TaskPushNotificationConfig` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskPushNotificationConfig "Permanent link")

Bases: `A2ABaseModel`

Parameters for setting or getting push notification configuration for a task

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskPushNotificationConfig.model_config "Permanent link")

### `pushNotificationConfig` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskPushNotificationConfig.pushNotificationConfig "Permanent link")

Push notification configuration.

### `taskId` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskPushNotificationConfig.taskId "Permanent link")

Task id.

## `TaskQueryParams` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskQueryParams "Permanent link")

Bases: `A2ABaseModel`

Parameters for querying a task, including optional history length.

### `historyLength = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskQueryParams.historyLength "Permanent link")

Number of recent messages to be retrieved.

### `id` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskQueryParams.id "Permanent link")

Task id.

### `metadata = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskQueryParams.metadata "Permanent link")

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskQueryParams.model_config "Permanent link")

## `TaskResubscriptionRequest` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskResubscriptionRequest "Permanent link")

Bases: `A2ABaseModel`

JSON-RPC request model for the 'tasks/resubscribe' method.

### `id` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskResubscriptionRequest.id "Permanent link")

An identifier established by the Client that MUST contain a String, Number. Numbers SHOULD NOT contain fractional parts.

### `jsonrpc = '2.0'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskResubscriptionRequest.jsonrpc "Permanent link")

Specifies the version of the JSON-RPC protocol. MUST be exactly "2.0".

### `method = 'tasks/resubscribe'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskResubscriptionRequest.method "Permanent link")

A String containing the name of the method to be invoked.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskResubscriptionRequest.model_config "Permanent link")

### `params` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskResubscriptionRequest.params "Permanent link")

A Structured value that holds the parameter values to be used during the invocation of the method.

## `TaskState` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskState "Permanent link")

Bases: `str`, `Enum`

Represents the possible states of a Task.

### `auth_required = 'auth-required'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskState.auth_required "Permanent link")

### `canceled = 'canceled'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskState.canceled "Permanent link")

### `completed = 'completed'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskState.completed "Permanent link")

### `failed = 'failed'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskState.failed "Permanent link")

### `input_required = 'input-required'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskState.input_required "Permanent link")

### `rejected = 'rejected'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskState.rejected "Permanent link")

### `submitted = 'submitted'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskState.submitted "Permanent link")

### `unknown = 'unknown'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskState.unknown "Permanent link")

### `working = 'working'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskState.working "Permanent link")

## `TaskStatus` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskStatus "Permanent link")

Bases: `A2ABaseModel`

TaskState and accompanying message.

### `message = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskStatus.message "Permanent link")

Additional status updates for client

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskStatus.model_config "Permanent link")

### `state` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskStatus.state "Permanent link")

### `timestamp = Field(default=None, examples=['2023-10-27T10:00:00Z'])` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskStatus.timestamp "Permanent link")

ISO 8601 datetime string when the status was recorded.

## `TaskStatusUpdateEvent` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskStatusUpdateEvent "Permanent link")

Bases: `A2ABaseModel`

Sent by server during sendStream or subscribe requests

### `contextId` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskStatusUpdateEvent.contextId "Permanent link")

The context the task is associated with

### `final` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskStatusUpdateEvent.final "Permanent link")

Indicates the end of the event stream

### `kind = 'status-update'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskStatusUpdateEvent.kind "Permanent link")

Event type

### `metadata = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskStatusUpdateEvent.metadata "Permanent link")

Extension metadata.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskStatusUpdateEvent.model_config "Permanent link")

### `status` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskStatusUpdateEvent.status "Permanent link")

Current status of the task

### `taskId` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TaskStatusUpdateEvent.taskId "Permanent link")

Task id

## `TextPart` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TextPart "Permanent link")

Bases: `A2ABaseModel`

Represents a text segment within parts.

### `kind = 'text'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TextPart.kind "Permanent link")

Part type - text for TextParts

### `metadata = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TextPart.metadata "Permanent link")

Optional metadata associated with the part.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TextPart.model_config "Permanent link")

### `text` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.TextPart.text "Permanent link")

Text content

## `UnsupportedOperationError` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.UnsupportedOperationError "Permanent link")

Bases: `A2ABaseModel`

A2A specific error indicating the requested operation is not supported by the agent.

### `code = -32004` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.UnsupportedOperationError.code "Permanent link")

A Number that indicates the error type that occurred.

### `data = None` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.UnsupportedOperationError.data "Permanent link")

A Primitive or Structured value that contains additional information about the error. This may be omitted.

### `message = 'This operation is not supported'` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.UnsupportedOperationError.message "Permanent link")

A String providing a short description of the error.

### `model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)` `class-attribute` `instance-attribute` [¶](https://a2a-protocol.org/latest/sdk/python/#a2a.types.UnsupportedOperationError.model_config "Permanent link")