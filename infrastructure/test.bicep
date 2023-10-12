targetScope = 'subscription'

// enter the subscription id 
param otherSubscriptionID string
param location string
// module deployed at subscription level but in a different subscription
module exampleModule 'main1.bicep' = {
  name: 'deployToDifferentSub'
  scope: subscription(otherSubscriptionID)
  params: {
    location: location
  }
}
