targetScope = 'subscription'

param location string = 'eastus2'
param prefix string = 'komma'
// param postfix string = '01'
param env string = 'dev'

param tags object = {
  Owner: 'mlops-v2'
  Project: 'mlops-v2'
  Environment: env
  Toolkit: 'bicep'
  Name: prefix
}

// var baseName  = 'akom03dev'
var resourceGroupName = 'rg-akom-03dev'


resource rg 'Microsoft.Resources/resourceGroups@2020-06-01' = {
  name: resourceGroupName
  location: location

  tags: tags
}
