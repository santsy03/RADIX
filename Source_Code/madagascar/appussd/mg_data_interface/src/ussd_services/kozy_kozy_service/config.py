'''
kozy-kozy specific configuration parameters
'''
FAF_INDICATOR = 2
SERVICE_NAME = 'kozykozy'

MAX_FAF_LIST = 3

eng = 'txt-1'
fr = 'txt-3'
mal = 'txt-2'

MESSAGES = {}
MESSAGES['failed'] = 'Tsy tontosa ny fangatahanao hampiasa ny Kozy Kozy Mix. Hamarino ny fahana ao @ kaontinao ary avereno ny fangatahanao afaka fotoana fohy. Misaotra tompoko.'

MESSAGES['max_faf'] = {}
MESSAGES['max_faf'][eng] = 'You already have 3 friends numbers. If you wish to modify, please call *121# and follow the instructions. Thank you'
MESSAGES['max_faf'][fr] = 'Vous possedez deja 3 numeros friends. Si vous souhaiteriez en modifier, veuillez composer *121# et suivre l instruction. Merci'
MESSAGES['max_faf'][mal] = 'Efa manana nomerao friends miisa 3 ianao. Raha tianao ny hanova izany dia manasa anao hiditra ao @ *121# ary araho ny toromarika. Misaotra tompoko'

MESSAGES['130'] = {}
MESSAGES['130'][eng] = 'Dear customer, this number can\'t be added as a Friends. Please add another airtel number'
MESSAGES['130'][fr] = 'Cher client, ce numero ne peut etre rajoute comme Friends. Veuillez choisir un autre numero'
MESSAGES['130'][mal] = 'Ry mpanjifa hajaina, tsy afaka safidiana ho nomerao Friends ny nomerao nampidirinao. Iangaviana ianao hisafidy nomerao airtel hafa. Misaotra tompoko'

MESSAGES['124'] = {}
MESSAGES['124'][eng] = 'Your account balance is insufficient, please refill your account and subscribe to kozy kozy Mix. Thank you'
MESSAGES['124'][fr] = 'Votre solde est insuffisant, veuillez recharger et vous souscrire a kozy kozy Mix. Merci'
MESSAGES['124'][mal] = 'Azafady, hamarino ny fahana ao @ kaontinao ary avereno ny fangatahanao. Misaotra tompoko'

MESSAGES['error'] = 'Subscription failed. There was an error processing your request.'
MESSAGES['incorrect_b_number'] = 'Error. Please enter a valid preferred number'
MESSAGES['incorrect_format'] = 'Misy diso ny fangatahanao. Raha hampiasa ny Kozy Kozy  Mix, tsindrio ny *103*033xxxx#. Misaotra tompoko'
