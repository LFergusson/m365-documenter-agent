targetScope = 'resourceGroup'

param location string = resourceGroup().location

param solutionName string = 'BrowserAgent'
param solutionUniqueText string = take(uniqueString(subscription().id, resourceGroup().name, solutionName), 5)
@description('The environment for the resources being deployed.')
@allowed([
  'dev'
  'test'
  'prod'
])
param environment string = 'dev'

// Networking Parameters
@description('The allowed IP ranges that can access the resources being deployed.')
param allowedRangesAllResources array = ['144.6.174.160']


var tags = {
  solution: solutionName
  environment: environment
}
var allTags = union(tags, {
  'azd-env-name': solutionName
})
var aiIpRanges = allowedRangesAllResources
var openAiServiceName = 'aoai-${solutionSuffix}-${environment}'
var solutionSuffix = toLower(trim(replace(
  replace(
    replace(replace(replace(replace('${solutionName}${solutionUniqueText}', '-', ''), '_', ''), '.', ''), '/', ''),
    ' ',
    ''
  ),
  '*',
  ''
)))

// AI Resources
@description('The chat model to use for most chat completions. This should be a model that is balanced for capability and cost.')
param chatModel object = {
  name: 'gpt-4o'
  version: '2024-11-20'
  sku: 'GlobalStandard'
  format: 'OpenAI'
}
@description('The smaller, cheaper chat model to use for less intensive tasks, such as summarization or simple Q&A.')
param smallChatModel object = {
  name: 'gpt-5-mini'
  sku: 'GlobalStandard'
  version: '2025-08-07'
  format: 'OpenAI'
}
@description('The embedding model to use for generating embeddings for documents and other text.')
param embeddingModel object = {
  name: 'text-embedding-3-large'
  sku: 'Standard'
  version: '1'
  format: 'OpenAI'
}

var models = [
  chatModel
  smallChatModel
  embeddingModel
]
var modelsToDeploy = [
  for m in models: {
    deploymentName: toLower('${replace(replace(replace(replace(m.name, '-', ''), '_', ''), ' ', ''), '/', '')}-${solutionSuffix}')
    name: m.name
    version: m.version
    format: m.format
    sku: m.sku
  }
]


// Deploy Azure OpenAI Service
module openAiService 'ai/cognitive-services.bicep' = {
  name: 'deployOpenAiService'
  params: {
    cognitiveServiceName: openAiServiceName
    kind: 'OpenAI'
    skuName: 'S0'
    location: location
    resourceTags: {
      solution: solutionName
      environment: environment
    }
    publicNetworkAccess: 'Enabled'
    networkAcls: {
      defaultAction: 'Deny'
      bypass: 'AzureServices'
      virtualNetworkRules: []
      ipRules: [for ip in aiIpRanges: {
        value: ip
      }]
    }
    enableLocalAuth: false
  }
}

// Deploy Models to Azure OpenAI Service
// Ensure that only one is deployed at a time to avoid resoruce conflict issues.
@batchSize(1)
module modelDeployments 'ai/model.bicep' = [for model in modelsToDeploy: {
  name: model.name
  params: {
    cognitiveServiceName: openAiServiceName
    deploymentName: model.name
    resourceName: model.name
    model: model.name
    modelVersion: model.version
    modelFormat: model.format
    modelSku: model.sku
  }
  dependsOn: [
    openAiService
  ]
}]


// Assign Cognitive Services User Role to Deployer
module roleAssignment 'security/role-assignment.bicep' = {
  name: 'assignCognitiveServicesUserRole'
  params: {
    roleDefinitionId: openAiService.outputs.cognitiveServiceRoles['Cognitive Services Contributor']
    principalId: deployer().objectId
    principalType: 'User'
  }
}
