# lunchmoney-share-price-tracker
The idea is to have a manually created account(s) in [lunchmoney.app](https://lunchmoney.app) updated with stock prices from last day trade prices.

- Create a manual account in [lunchmoney.app](https://lunchmoney.app)
- Get the AssetID for the account. The easiest way is to open a transaction window and copy paste it from URL. Example: https://my.lunchmoney.app/transactions/2024/12?time=all&match=any&asset=12345
- Get the API key for [lunchmoney.app](https://lunchmoney.app) here https://my.lunchmoney.app/developers (free)
- Get the API key for [polygon.io](https://polygon.io). Just register and they will give you one
- Fork the repository
- Create two new secreats in Settings - Secrets and variables - Actions - Repository secrets ([https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions](official guide)
  - LUNCHMONEY_API
  - POLIGON_API  
- Populate the [config.yaml](https://github.com/MelHiour/lunchmoney-share-price-tracker/blob/main/config.yaml) with data
  ```
  stocks:
   - asset_id: 12345 < Asset ID from lunchmoney.app
     stock_code: AMZN < Stock you own
     amount: 60 < The amount of stocks
   - asset_id: 12343 < Next Asset
     stock_code: AMZN
     amount: 60  
  ```
- CI/CD pipeline will run at midnight everyday and on push to master
