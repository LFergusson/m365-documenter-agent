@description('The scope at which the role assignment applies.')
param roleDefinitionId string

@description('The principal ID of the user, group, or service principal to assign the role to.')
param principalId string = deployer().objectId

@allowed([
  'User'
  'Group'
  'ServicePrincipal'
])
param principalType string = 'User'

resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(roleDefinitionId, principalId)
  properties: {
    roleDefinitionId: roleDefinitionId
    principalId: principalId
    principalType: principalType
  }
}
