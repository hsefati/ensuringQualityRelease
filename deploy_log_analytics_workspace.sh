#!/bin/bash

az group create --name RG-LogAnalytics --location eastus
az deployment group create --resource-group RG-LogAnalytics --name LogAnalytics-hs-erq --template-file deploylaworkspacetemplate.json