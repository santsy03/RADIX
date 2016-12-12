OFFER_ID = 8

WHITELIST = ['261330465390','261330770007','261330891190', '261330722156']

MESSAGES = {}
MESSAGES['success'] = {}
MESSAGES['success']['txt-1'] = ('Your subscription was performed with success:'
                                ' 10 Mb valid until 06AM59. Thank you.')
MESSAGES['success']['txt-2'] = ("Tontosa ny fangatahanao: 10 Mo azonao "
                                "ampiasaina hatr@ 06ora59 maraina. "
                                "Misaotra tompoko")

MESSAGES['success']['txt-3'] = ("Votre souscription a ete effectuee avec "
                                "succes: 10Mo valable jusqu a 06h59 du matin. "
                                "Merci.")

MESSAGES['notallowed'] = {}
MESSAGES['notallowed']['txt-1'] = ("This promo has ended. Please subscribe to "
                                   "Mymeg15 at only Ar100 and win 10 points "
                                   "for promo fety55. Thank you")

MESSAGES['notallowed']['txt-2'] = ("Nifarana io promotion io. Manasa anao "
                                   "hampiasa MyMeg15 *114*40# @ sarany "
                                   "Ar100 monja ary mahazoa isa 10 @ promo "
                                   "fety55. Misaotra tompoko")

MESSAGES['notallowed']['txt-3'] = ("Cette promotion a pris fin. Vous pouvez "
                                   "souscrire a MyMeg15 pour seulement Ar 100 "
                                   "et gagnez 10 points pour la promo fety55. "
                                   "Merci")


MESSAGES['error'] = ("Dear customer, there was an error processing you "
                     "request. Please try again.")

MESSAGES['active'] = {}
MESSAGES['active']['txt-1'] = ("You have reached the maximum count of "
                               "subscriptions authorized today. Thank you")
MESSAGES['active']['txt-2'] = ("Efa tratra ny fetra hahafahanao mampiasa "
                               "an'io tolotra io anio. Misaotra tompoko.")
MESSAGES['active']['txt-3'] = ("Vous avez atteint le nombre de souscription "
                               "autorise pour ce jour. Merci")

HIT = 'application.goodmorning.hit'
TIMER = 'application.goodmorning.time.%s'

STATUS = {}
STATUS['success'] = 1
STATUS['active'] = 2
STATUS['notallowed'] = 4
STATUS['error'] = 3
