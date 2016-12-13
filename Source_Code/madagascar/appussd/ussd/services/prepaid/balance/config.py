from string import Template

da = {}

da['modular'] = ['18','21','26','27','30','40','41','53','54','55']

da['bonus'] = ['3','4','5','6','10','16','50']

da['mn'] = ['9','51']

da['sec'] = ['7','43','44','48','49', '52','20']

da['sms'] = ['2']

da['data'] = ['8','13','15','10111','1011','1013','1014','1018','1019','1020','1021']


failureTxt = 'Dear customer your request could not be processed now. Try again later or contact customer care.'

resp = {}

resp['txt-1'] = Template("Your balance is $ma Ar, modular: $mod Ar, bonus: $bon Ar, $min min $sec sec, $sms sms  and $data MB.Thank you.")
resp['txt-2'] = Template("Manana $ma Ar ianao ao aminy kaontinao , modulaire: $mod Ar, bonus: $bon Ar, $min min $sec seg, sms $sms, ary $data Mo. Misaotra tompoko.")
resp['txt-3'] = Template("Vous avez $ma Ar de credit, modulaire $mod Ar, bonus: $bon Ar, $min min $sec sec, sms $sms et $data Mo d\'internet. Merci.")
