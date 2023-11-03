# Temporary-Mail
A Python utility to leverage temporary email systems from various providers.

|Site|Supporting Domain|
|:---|:---:|
|temp-mail.io|cloud-mail.top, greencafe24.com, crepeau12.com, appzily.com, coffeetimer24.com, popcornfarm7.com, bestparadize.com, kjkszpjcompany.com, cashflow35.com, crossmailjet.com, kobrandly.com, blondemorkin.com, block521.com, best-john-boats.com, popcornfly.com, plancetose.com|
|ruu.kr|ruu.kr, iralborz.bid, kumli.racing|

||Supporting Site|
|:---|:---:|
|create_mail|temp-mail.io|
|remove_mail|ruu.kr, temp-mail.io (Requires token for temp-mail.io)|
|receive_mail|temp-mail.io, ruu.kr|


## Reference
- This utility utilizes the temporary email systems from ruu.kr and temp-mail.io. Its functionality may be impacted if domains offered by these providers change.
- Domains that support the create_mail function require email creation for reception.
- For receiving emails, ruu.kr doesn't necessitate mail creation, whereas temp-mail.io does.
- I'm open to adding more functionalities or supporting additional email domains in the future.


## Quick Example
```py
import tempmail

DOMAIN = ""  # Example: ruu.kr
ID = ""  # Example: abcde12345

temp_service = tempmail.TemporaryMail(DOMAIN)

# Mail creation feature only available for temp-mail.io
# token = temp_service.create_mail(ID)

print(temp_service.receive_mail(ID))

# Removal only available for ruu.kr, but if you have a token from temp-mail.io, you can use it to remove the mail.
# temp_service.remove_mail(ID, token)
```
