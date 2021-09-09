# pyUSCIS
USCIS Case Status Check

## Version
- v0.2
- Sep 9, 2021

## Description
Retrieve USCIS case status including descriptions by making a POST call to USCIS case status check site.

Response format example.

```
{
    "err"   : "0",
    "status": "Case Was Received",
    "desc"  : "On March 17, 2021, we received your Form I-485,..."
}
```

## History
- v0.2 (Sep 9, 2021):
  - urllib3 version to support AWS Lambda.
  - Separated console app as app.py.
- v0.1 (Jun 3, 2021):
  - Initial version with Requests.
