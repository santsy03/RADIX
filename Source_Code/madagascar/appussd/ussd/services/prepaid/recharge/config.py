from string import Template

resp = {}
resp['txt-1'] = Template("Your account has been recharged by $amt MGA with 5% bonus. To check your balance, press *999#")
resp['txt-2'] = Template("Tafiditra ny fahana $amt Ar miaraka @ bonus 5%. Fijerena ambina fahana, antsoy ny *999#")
resp['txt-3'] = Template("Votre compte a ete recharge de $amt Ar avec un bonus de 5%. Consultation solde: *999#")



wrong_voucher = {}
wrong_voucher['txt-1'] = "Sorry recharge code introduced are less than 15"
wrong_voucher['txt-2'] = "Azafady, le tsy ampy 15 ny tarehimarika nampidrinao."
wrong_voucher['txt-3'] = "Desole, le nombre de code introduits est inferieur a 15"

more_digits = {}
more_digits['txt-1'] = 'The code you have entered is wrong, please check again.'
more_digits['txt-2'] = 'Misy diso ny kaody nampidirinao.Hamarino azafady.'
more_digits['txt-3'] = 'Le code que vous avez introduit est incorrect. Veuillez verifier s il vous plait.'

failureTxt = "Dear customer your request could not be processed now. Try again later or Contact customer care."
