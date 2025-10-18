metadata description = 'This module deploys a model on an Azure OpenAI Service resource.'

@description('The name of the Cognitive Service resource to deploy the model to.')
param cognitiveServiceName string

@description('The deployment name for the model.')
param deploymentName string = 'gpt-4'

@description('The name of the model resource.')
param resourceName string = deploymentName

@description('The model to deploy. For example: "gpt-4", "gpt-4o", "gpt-4o-mini", "gpt-35-turbo", "gpt-35-turbo-16k", "gpt-35-turbo-0613", "gpt-35-turbo-16k-0613", "text-davinci-003", "text-davinci-002", "code-davinci-002", "text-curie-001", "text-babbage-001", "text-ada-001". See https://learn.microsoft.com/en-us/azure/cognitive-services/openai/concepts/models for the full list of available models.')
param model string = 'gpt-4'

@allowed(
  [
    'Standard'
    'GlobalStandard'
  ]
)
param modelSku string = 'Standard'

param modelVersion string = '1.0'

param modelFormat string = 'OpenAI'

resource cognitiveService 'Microsoft.CognitiveServices/accounts@2025-06-01' existing = {
  name: cognitiveServiceName
}

resource modelDeployment 'Microsoft.CognitiveServices/accounts/deployments@2025-06-01' = {
  parent: cognitiveService
  name: resourceName
  properties: {
    model: {
      name: model
      version: modelVersion
      format: modelFormat
    }
  }
  sku: {
    name: modelSku
    capacity: 1
  }
}
