# Temporary-Mail
Using the temporary mail system provided by several sites in Python

||Supporting Domain|
|:---|:---:|
|create_mail|cloud-mail.top, greencafe24.com, crepeau12.com, appzily.com, coffeetimer24.com, popcornfarm7.com, bestparadize.com, kjkszpjcompany.com, cashflow35.com, crossmailjet.com, kobrandly.com, blondemorkin.com, block521.com, best-john-boats.com, popcornfly.com, plancetose.com (temp-mail.io)|
|remove_mail|ruu.kr, iralborz.bid, kumli.racing (ruu.kr)|
|receive_mail|All mail above|


## Reference
- This code is based on the temporary email system provided by ruu.kr and temp-mail.io, and will not be available when the domain provided by both sites expires.
- The domain that supports create_mail must create the email to receive it.
- In order to receive mail, ruu.kr does not need to create mail, and temp-mail.io needs to create mail.
- I can add additional functions or mail domains.


## Use
```
import tempmail

domain = ""  # Ex. ruu.kr
name = ""  # Ex. abcde12345
tm = tempmail.TemporaryMail(domain)

# tm.create_mail(name) # only temp-mail.io
print(tm.receive_mail(name))
# tm.remove_mail(name) # only ruu.kr
```
