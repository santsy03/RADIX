#coding: utf8
sample_flow = {
  "flow": {
    "1": {
      "id": 1,
      "revisionId": 1,
      "sequenceCheck": "",
      "name": "madagascar ussd 2.0",
      "type": "postpaid",
      "levels": {
        "1": {
          "id": 0,
          "menus": {
            "1": {
              "id": "1-0-0-1",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "1. My account",
                  "txt2": "1. Ny momba ny kaontiko",
                  "txt3": "1. Mon compte",
                  "key": 1,
                  "source": "",
                  "nextmenuid": "1-0-1-11"
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "2. Additionnal services",
                  "txt2": "2. Tolotra samihafa",
                  "txt3": "2. Services additionnels",
                  "key": 2,
                  "source": "",
                  "nextmenuid": "1-0-1-12"
                },
                "3": {
                  "sequence": 3,
                  "type": "static",
                  "txt1": "3. Roaming",
                  "txt2": "3. Roaming",
                  "txt3": "3. Roaming",
                  "key": 3,
                  "source": "",
                  "nextmenuid": "1-0-1-13"
                },
                "4": {
                  "sequence": 4,
                  "type": "static",
                  "txt1": "4. Airtel money",
                  "txt2": "4. Airtel money",
                  "txt3": "4. Airtel money",
                  "key": 4,
                  "source": "",
                  "nextmenuid": "1-0-1-14"
                },
                "5": {
                  "sequence": 5,
                  "type": "static",
                  "txt1": "5. Internet Offers",
                  "txt2": "5. Internet sy ny tontolony",
                  "txt3": "5. Offre internet",
                  "key": 5,
                  "source": "",
                  "nextmenuid": "1-0-1-15"
                },
                "6": {
                  "sequence": 6,
                  "type": "static",
                  "txt1": "6. Find a store",
                  "txt2": "6. Masoivoho Airtel",
                  "txt3": "6. Les Points Airtel",
                  "key": 6,
                  "source": "",
                  "nextmenuid": "1-0-1-16"
                },
                "7": {
                  "sequence": 7,
                  "type": "static",
                  "txt1": "7. Super Valisoa",
                  "txt2": "7. Super Valisoa",
                  "txt3": "7. Super Valisoa",
                  "key": 7,
                  "source": "",
                  "nextmenuid": "1-0-1-17"
                }
              }
            }
          }
        },
        "2": {
          "id": 0,
          "menus": {
            "11": {
              "id": "1-0-1-11",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "1. Language change",
                  "txt2": "1. Manova fiteny",
                  "txt3": "1. Changement de language ",
                  "key": 1,
                  "source": "",
                  "nextmenuid": "1-0-2-111"
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "2. My number",
                  "txt2": "2. Ny nomeraoko",
                  "txt3": "2. Mon numero",
                  "key": 2,
                  "source": "",
                  "nextmenuid": "1-0-2-112"
                },
                "3": {
                  "sequence": 3,
                  "type": "static",
                  "txt1": "3. Outstanding balance",
                  "txt2": "3. Ambim-bola azonao ampiasaina",
                  "txt3": "3. Reste du plafonnement",
                  "key": 3,
                  "source": "",
                  "nextmenuid": "1-0-2-113"
                },
                "4": {
                  "sequence": 4,
                  "type": "static",
                  "txt1": "4. SMS/ minutes left",
                  "txt2": "4. SMS/ Minitra ambiny",
                  "txt3": "4. Sms/Minutes/restants",
                  "key": 4,
                  "source": "",
                  "nextmenuid": "1-0-2-114"
                },
                "5": {
                  "sequence": 5,
                  "type": "static",
                  "txt1": "5. Credit limit",
                  "txt2": "5. Credit limit",
                  "txt3": "5. Plafonnement des appels",
                  "key": 5,
                  "source": "",
                  "nextmenuid": "1-0-2-115"
                },
                "6": {
                  "sequence": 6,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina @ menu teo aloha",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": 0,
                  "source": "",
                  "nextmenuid": "1-0-2-116"
                }
              }
            },
            "12": {
              "id": "1-0-1-12",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "1. FONEO",
                  "txt2": "1. FONEO",
                  "txt3": "1. FONEO",
                  "key": 1,
                  "source": "",
                  "nextmenuid": "1-0-2-121"
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "2. PUK Request",
                  "txt2": "2. Fijerena Kaody PUK",
                  "txt3": "2. Demande de Code PUK",
                  "key": 2,
                  "source": "",
                  "nextmenuid": "1-0-2-122"
                },
                "3": {
                  "sequence": 3,
                  "type": "static",
                  "txt1": "3. Phone Back up\n#. Previous Menu",
                  "txt2": "3. Phone Back up\n#. Raha hiverina",
                  "txt3": "3. Phone Back up\n#. Menu Precedent",
                  "key": 3,
                  "source": "",
                  "nextmenuid": "1-0-2-123"
                }
              }
            },
            "121": {
              "id": "1-0-2-121",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "any",
              "services": "",
              "package": "",
              "parameter": "recipient",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Enter the Mobile number",
                  "txt2": "Nomerao andefasana FONEO",
                  "txt3": "Entrez le numéro",
                  "key": "",
                  "source": "",
                  "nextmenuid": "1-0-3-1211"
                }
              }
            },
            "122": {
              "id": "1-0-2-122",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "recipient",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Sorry, the service is currently not available. Thank you for your understanding.",
                  "txt2": "Miala tsiny, misy fiatona io tolotra io ankehitriny. Misaotra anao noho ny fampiasanao hatrany ny tambazotra Airtel.",
                  "txt3": "Desole, ce service est momentanement indisponible. Nous vous remercions de votre comprehension",
                  "key": "",
                  "source": ""
                }
              }
            },
            "123": {
              "id": "1-0-2-123",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "PhoneBackupallows Airtel subscribers tosave ontheir mobile,data ,photos, audio files, etc /",
                  "txt2": "Phone backup dia tolotra iray ahafahan ny mpanjifa airtel mitahiry ny sary, repertoire, hira, sns ao @ finday/",
                  "txt3": "Le service permet aux abonnes Airtel de sauvegarder les donnees de leurs mobiles tels que repertoire, photos,fichiers audio,etc./",
                  "key": "",
                  "source": "",
                  "nextmenuid": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0-Tohiny\n#-Raha hiverina @ menu teo aloha",
                  "txt3": "0- Suivant\n#-Menu Precedent",
                  "key": 0,
                  "source": "",
                  "nextmenuid": "1-0-3-1232"
                }
              }
            },
            "142": {
              "id": "1-0-2-142",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Opening an account is free of charge . Please bring a copy of your identity card and fill the provided subscription form",
                  "txt2": "Mamenoa fiche Airtel Money maimaimpoana eny @ masoivoho na mpiara miasa @ Airtel akaiky anao miaraka @ photocopie CIN.",
                  "txt3": "Pour l ouverture d un compte , veuillez vous munir d une photocopie CIN et completer la fiche de souscription qui vous sera presentee .Le service est gratuit",
                  "key": "",
                  "source": ""
                }
              }
            },
            "141": {
              "id": "1-0-2-141",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel money allows you to do money transfer , to proceed to cash in and cash out  and do shopping",
                  "txt2": "Ny Airtel Money dia  tolotra ahafahanao mandefa, mandray na mandoa vola avy @findainao.ahazoanao koa mandoa facktiora",
                  "txt3": "Airtel money vous permet d'effectuer un transfert d argent , des retraits , des depots , des achats et faire des paiements de facture a partir de votre mobile",
                  "key": "",
                  "source": ""
                }
              }
            },
            "14": {
              "id": "1-0-1-14",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "1. Information about Airtel Money",
                  "txt2": "1. Momban ny Airtel Money",
                  "txt3": "1. Informations concernant le service Airtel Money",
                  "key": "1",
                  "source": "",
                  "nextmenuid": "1-0-2-141"
                },
                "2": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "2. Airtel Money subscription",
                  "txt2": "2. Fisoratana anarana @ Airtel Money",
                  "txt3": "2. Souscription a Airtel Money ",
                  "key": "2",
                  "source": "",
                  "nextmenuid": "1-0-2-142"
                },
                "3": {
                  "sequence": 3,
                  "type": "static",
                  "txt1": "3. Airtel Money cash points",
                  "txt2": "3. Ireo Cash Points Airtel Money",
                  "txt3": "3. Les Cash Points Airtel Money",
                  "key": "3",
                  "source": "",
                  "nextmenuid": "1-0-2-143"
                },
                "4": {
                  "sequence": 4,
                  "type": "static",
                  "txt1": "4. Different Airtel Money Cash out & Transaction Cost\n#. Previous Menu",
                  "txt2": "4. Ny saran ny fandefasana sy fanakalozam bola\n#. Raha hiverina @ menu teo aloha",
                  "txt3": "4. Les differents frais de retrait & transaction\n#. Menu Precedent",
                  "key": "4",
                  "source": "",
                  "nextmenuid": "1-0-2-144"
                }
              }
            },
            "15": {
              "id": "1-0-1-15",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "1. Settings",
                  "txt2": "1. Fampidirana",
                  "txt3": "1. Configuration",
                  "key": 1,
                  "source": "",
                  "nextmenuid": "1-0-2-151"
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "2. Bundle Data\n#. Previous Menu",
                  "txt2": "2. Tolotra Internet natao ho an ny abonnement\n#. Raha hiverina @ menu teo aloha",
                  "txt3": "2. Les offres internet dediees a l abonnement\n#. Menu Precedent",
                  "key": 2,
                  "source": "",
                  "nextmenuid": "1-0-2-152"
                }
              }
            },
            "16": {
              "id": "1-0-1-16",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "1. Showroom Airtel",
                  "txt2": "1. Ireo Masoivoho Airtel",
                  "txt3": "1. Les shops Airtel",
                  "key": 1,
                  "source": "",
                  "nextmenuid": "1-0-2-161"
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "2. For products and sim change\n#. Previous Menu",
                  "txt2": "2. Ireo toerana afaka anoloana puce simba na very\n#. Raha hiverina @ menu teo aloha",
                  "txt3": "2. Les points de remplacement sim\n#. Menu Precedent",
                  "key": 2,
                  "source": "",
                  "nextmenuid": "1-0-2-162"
                }
              }
            },
            "17": {
              "id": "1-0-1-17",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "1. Information about Super Valisoa",
                  "txt2": "1. Momba ny Super Valisoa",
                  "txt3": "1. Informations concernat Super Valisoa",
                  "key": 1,
                  "source": "",
                  "nextmenuid": "1-0-2-171"
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "2. Registration",
                  "txt2": "2. Fidirana",
                  "txt3": "2. Souscription ",
                  "key": 2,
                  "source": "",
                  "nextmenuid": "1-0-2-172"
                },
                "3": {
                  "sequence": 3,
                  "type": "static",
                  "txt1": "3. Balance inquery",
                  "txt2": "3. Fijerena ambina isa",
                  "txt3": "3. Verification des points",
                  "key": 3,
                  "source": "",
                  "nextmenuid": "1-0-2-173"
                },
                "4": {
                  "sequence": 4,
                  "type": "static",
                  "txt1": "4. Redemption ",
                  "txt2": "4. Fanakalozana ",
                  "txt3": "4. Echange des ponts",
                  "key": 4,
                  "source": "",
                  "nextmenuid": "1-0-2-174"
                },
                "5": {
                  "sequence": 5,
                  "type": "static",
                  "txt1": "5. Loyalty points transfer",
                  "txt2": "5. Famindrana isa",
                  "txt3": "5. Transfer des points",
                  "key": 5,
                  "source": "",
                  "nextmenuid": "1-0-2-175"
                },
                "6": {
                  "sequence": 6,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-2-177"
                }
              }
            },
            "1-0-1-13": {
              "id": "1-0-1-13",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "1. One Airtel",
                  "txt2": "1. One Airtel",
                  "txt3": "1. One Airtel",
                  "key": 1,
                  "source": "",
                  "nextmenuid": "1-0-2-131"
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "2. Roaming Information",
                  "txt2": "2. Ny tsara ho fantatra momban ny Roaming",
                  "txt3": "2. Informations concernant le Roaming",
                  "key": 2,
                  "source": "",
                  "nextmenuid": "1-0-2-132"
                },
                "3": {
                  "sequence": 3,
                  "type": "static",
                  "txt1": "3. Roaming Partners\n#. Previous Menu",
                  "txt2": "3. Lisitr ireo toerana afaka anaovana Roaming\n#. Raha hiverina @ menu teo aloha.",
                  "txt3": "3. Liste des pays partenaires Roaming\n#.Menu Precedent",
                  "key": 3,
                  "source": "",
                  "nextmenuid": "1-0-2-133"
                }
              }
            }
          }
        },
        "3": {
          "id": 0,
          "menus": {
            "111": {
              "id": "1-0-2-111",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "1. Malagasy",
                  "txt2": "1. Malagasy",
                  "txt3": "1. Malagasy",
                  "key": 1,
                  "source": "",
                  "nextmenuid": "1-0-3-1111"
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "2. Francais",
                  "txt2": "2. Francais",
                  "txt3": "2. Francais",
                  "key": 2,
                  "source": "",
                  "nextmenuid": "1-0-3-1112"
                },
                "3": {
                  "sequence": 3,
                  "type": "static",
                  "txt1": "3. English\n#.Previous Menu",
                  "txt2": "3. English\n#.Raha hiverina @ menu teo aloha",
                  "txt3": "3. English\n#.Menu precedent",
                  "key": 3,
                  "source": "",
                  "nextmenuid": "1-0-3-1113"
                }
              }
            },
            "112": {
              "id": "1-0-2-112",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Dear Customer,your number is $msisdn",
                  "txt2": "Tompoko, ny nomeraonao dia $msisdn",
                  "txt3": "Cher client, votre  numero d'appel est $msisdn",
                  "key": "",
                  "source": ""
                }
              }
            },
            "113": {
              "id": "1-0-2-113",
              "type": "dynamic",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "dynamic",
                  "txt1": "",
                  "txt2": "",
                  "key": "",
                  "source": "http://127.0.0.1:9098/process?msisdn=$msisdn&language=$language&sessionId=$sessionId&action=outstanding"
                }
              }
            },
            "114": {
              "id": "1-0-2-114",
              "type": "dynamic",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "dynamic",
                  "txt1": "",
                  "txt2": "",
                  "key": "",
                  "source": "http://127.0.0.1:9098/process?msisdn=$msisdn&language=$language&sessionId=$sessionId&action=smsminutesbalance"
                }
              }
            },
            "115": {
              "id": "1-0-2-115",
              "type": "dynamic",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "dynamic",
                  "txt1": "",
                  "txt2": "",
                  "key": "",
                  "source": "http://127.0.0.1:9098/process?msisdn=$msisdn&action=creditLimitCheck&sessionId=$sessionId&language=$language"
                }
              }
            },
            "122": {
              "id": "1-0-2-122",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Hello Tunes Text",
                  "txt2": "Hello Tunes Text",
                  "txt3": "Hello Tunes Text",
                  "key": "",
                  "source": ""
                }
              }
            },
            "151": {
              "id": "1-0-2-151",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "1. Internet",
                  "txt2": "1. Internet",
                  "txt3": "1. Internet",
                  "key": 1,
                  "source": "",
                  "nextmenuid": "1-0-3-1511"
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "2. WAP\n#. Previous Menu",
                  "txt2": "2. WAP\n#. Raha hiverina @ menu teo aloha ",
                  "txt3": "2. WAP\n#. Menu Precedent",
                  "key": 2,
                  "source": "",
                  "nextmenuid": "1-0-3-1512"
                }
              }
            },
            "152": {
              "id": "1-0-2-152",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "1. MYMEG200",
                  "txt2": "1. MYMEG200",
                  "txt3": "1. MYMEG200",
                  "key": 1,
                  "source": "",
                  "nextmenuid": "1-0-3-1521"
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "2. MYMEG500",
                  "txt2": "2. MYMEG500",
                  "txt3": "2. MYMEG500",
                  "key": 2,
                  "source": "",
                  "nextmenuid": "1-0-3-1522"
                },
                "3": {
                  "sequence": 3,
                  "type": "static",
                  "txt1": "3. MYGIG1",
                  "txt2": "3. MYGIG1",
                  "txt3": "3. MYGIG1",
                  "key": 3,
                  "source": "",
                  "nextmenuid": "1-0-3-1523"
                },
                "4": {
                  "sequence": 4,
                  "type": "static",
                  "txt1": "4. MYGIG2",
                  "txt2": "4. MYGIG2",
                  "txt3": "4. MYGIG2",
                  "key": 4,
                  "source": "",
                  "nextmenuid": "1-0-3-1524"
                },
                "5": {
                  "sequence": 5,
                  "type": "static",
                  "txt1": "5. MYGIG3",
                  "txt2": "5. MYGIG3",
                  "txt3": "5. MYGIG3",
                  "key": 5,
                  "source": "",
                  "nextmenuid": "1-0-3-1525"
                },
                "6": {
                  "sequence": 6,
                  "type": "static",
                  "txt1": "6. MYGIG5",
                  "txt2": "6. MYGIG5",
                  "txt3": "6. MYGIG5",
                  "key": 6,
                  "source": "",
                  "nextmenuid": "1-0-3-1526"
                },
                "7": {
                  "sequence": 7,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-3-1527"
                }
              }
            },
            "161": {
              "id": "1-0-2-161",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "1. Antananarivo",
                  "txt2": "1. Antananarivo",
                  "txt3": "1. Antananarivo",
                  "key": 1,
                  "source": "",
                  "nextmenuid": "1-0-3-1611"
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "2. Antsirabe",
                  "txt2": "2. Antsirabe",
                  "txt3": "2. Antsirabe",
                  "key": 2,
                  "source": "",
                  "nextmenuid": "1-0-3-1612"
                },
                "3": {
                  "sequence": 3,
                  "type": "static",
                  "txt1": "3. Diego",
                  "txt2": "3. Diego",
                  "txt3": "3. Diego",
                  "key": 3,
                  "source": "",
                  "nextmenuid": "1-0-3-1613"
                },
                "4": {
                  "sequence": 4,
                  "type": "static",
                  "txt1": "4. Fianarantsoa ",
                  "txt2": "4. Fianarantsoa",
                  "txt3": "4. Fianarantsoa",
                  "key": 4,
                  "source": "",
                  "nextmenuid": "1-0-3-1614"
                },
                "5": {
                  "sequence": 5,
                  "type": "static",
                  "txt1": "5. Fort Dauphin",
                  "txt2": "5. Fort Dauphin",
                  "txt3": "5. Fort Dauphin",
                  "key": 5,
                  "source": "",
                  "nextmenuid": "1-0-3-1615"
                },
                "6": {
                  "sequence": 6,
                  "type": "static",
                  "txt1": "6. Majunga",
                  "txt2": "6. Majunga",
                  "txt3": "6. Majunga",
                  "key": 6,
                  "source": "",
                  "nextmenuid": "1-0-3-1616"
                },
                "7": {
                  "sequence": 7,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina @ menu teo aloha",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": 0,
                  "source": "",
                  "nextmenuid": "1-0-3-1617"
                }
              }
            },
            "162": {
              "id": "1-0-2-162",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "1. Antananarivo",
                  "txt2": "1. Antananarivo",
                  "txt3": "1. Antananarivo",
                  "key": 1,
                  "source": "",
                  "nextmenuid": "1-0-3-1621"
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "2. Antsirabe",
                  "txt2": "2. Antsirabe",
                  "txt3": "2. Antsirabe",
                  "key": 2,
                  "source": "",
                  "nextmenuid": "1-0-3-1622"
                },
                "3": {
                  "sequence": 3,
                  "type": "static",
                  "txt1": "3. Diego",
                  "txt2": "3. Diego",
                  "txt3": "3. Diego",
                  "key": 3,
                  "source": "",
                  "nextmenuid": "1-0-3-1623"
                },
                "4": {
                  "sequence": 4,
                  "type": "static",
                  "txt1": "4. Fianarantsoa ",
                  "txt2": "4. Fianarantsoa",
                  "txt3": "4. Fianarantsoa",
                  "key": 4,
                  "source": "",
                  "nextmenuid": "1-0-3-1624"
                },
                "5": {
                  "sequence": 5,
                  "type": "static",
                  "txt1": "5. Fort Dauphin",
                  "txt2": "5. Fort Dauphin",
                  "txt3": "5. Fort Dauphin",
                  "key": 5,
                  "source": "",
                  "nextmenuid": "1-0-3-1625"
                },
                "6": {
                  "sequence": 6,
                  "type": "static",
                  "txt1": "6. Majunga",
                  "txt2": "6. Majunga",
                  "txt3": "6. Majunga",
                  "key": 6,
                  "source": "",
                  "nextmenuid": "1-0-3-1626"
                },
                "7": {
                  "sequence": 7,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina @ menu teo aloha",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": 0,
                  "source": "",
                  "nextmenuid": "1-0-3-1627"
                }
              }
            },
            "171": {
              "id": "1-0-2-171",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "A Loyalty program targeting all Airtel customers. 1 point = Ar100 consumed. Accumulated points could be exchanged into minutes,SMS,internet",
                  "txt2": "Super valisoa dia fankasitrahana ny mpanjifa mampiasa ny tambazotra. Isa iray isaky ny Ar 100 lany no valisoa, azo hatakalo ho minitra, SMS, na internet.",
                  "txt3": "Super Valisoa: Programme de fidelisation dedie aux clients airtel. 1 point = Ar 100 consommes. Les points peuvent etre echanges en minutes,SMS, internet.",
                  "key": "",
                  "source": ""
                }
              }
            },
            "172": {
              "id": "1-0-2-172",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "To subscribe to the program, send SOA by SMS to 466. You will receive an SMS confirming your subscription. Thank you.",
                  "txt2": "Mba ahafahanao miditra @ tolotra dia alefa SMS maimaimpoana any @ 466 ny hoe SOA.Haharay SMS ianao manamafy ny fidiranao @ tolotra. Misaotra Tompoko",
                  "txt3": "Pour souscrire au programme, envoyez gratuitement le mot SOA par SMS au 466. Vous recevrez un SMS confirmant votre souscription. Merci",
                  "key": "",
                  "source": ""
                }
              }
            },
            "173": {
              "id": "1-0-2-173",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "To check your loyalty points, send ISA by SMS to 466. Thank you.",
                  "txt2": "Mba ahafantaranao ny ISA anananao dia alefa SMS maimaimpoana any @ 466 ny hoe: ISA. Misaotra Tompoko.",
                  "txt3": "Pour connaitre le reste de vos points, envoyez gratuitement le mot ISA par SMS au 466.",
                  "key": "",
                  "source": ""
                }
              }
            },
            "174": {
              "id": "1-0-2-174",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "To redeem your points, send MILA / space/ The product code /space/ Your password  by SMS to 466. Eg: MILA 10MN 1705",
                  "txt2": "Raha hanakalo isa ianao, alefaso SMS any @ 466 ny hoe MILA /elanelana /Ny kaody-ny tolotra tianao alaina /elanelana/ Teny miafina. Oh:MILA 10MN 1705",
                  "txt3": "Pour echanger vos points, envoyez MILA /espace/ le code produit /espace/ votre mot de passe au 466. Ex: MILA 10MN 1705",
                  "key": "",
                  "source": ""
                }
              }
            },
            "175": {
              "id": "1-0-2-175",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "To transfer your loyalty points, send AFINDRA /space/ Destination number/space/ Points to be transferred/space/ Your password by SMS to 466",
                  "txt2": "Raha hamindra isa any @ nomerao hafa, alefaso SMS any @ 466 ny hoe: AFINDRA/elanelana/Nomerao andefasana azy/elanelana/Isa afindra/elanelana/Teny miafina",
                  "txt3": "Pour un transfert de points, envoyez AFINDRA/espace/Le numero du destinataire/espace/ Le point a transferer/espace/votre mot de passe par SMS au 466.",
                  "key": "",
                  "source": ""
                }
              }
            },
            "177": {
              "id": "1-0-2-177",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "6. Tier level inquery",
                  "txt2": "6. Fijerana ny sokajy",
                  "txt3": "6. Verification de la categorie",
                  "key": 6,
                  "source": "",
                  "nextmenuid": "1-0-3-1761"
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "7. List of products",
                  "txt2": "7. Lisitry ny fanomezana",
                  "txt3": "7. Liste des produits",
                  "key": 7,
                  "source": "",
                  "nextmenuid": "1-0-3-1762"
                },
                "3": {
                  "sequence": 3,
                  "type": "static",
                  "txt1": "8. PIN change\n#. Previous Menu",
                  "txt2": "8. Fanovana teny miafina\n#. Raha hiverina",
                  "txt3": "8. Changement de mot de passe\n#. Menu Precedent",
                  "key": 8,
                  "source": "",
                  "nextmenuid": "1-0-3-1763"
                }
              }
            },
            "143": {
              "id": "1-0-2-143",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "1. Tananarive",
                  "txt2": "1. Tananarive",
                  "txt3": "1. Tananarive",
                  "key": 1,
                  "source": "",
                  "nextmenuid": "1-0-3-1431"
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "2. Antsirabe",
                  "txt2": "2. Antsirabe",
                  "txt3": "2. Antsirabe",
                  "key": 2,
                  "source": "",
                  "nextmenuid": "1-0-3-1432"
                },
                "3": {
                  "sequence": 3,
                  "type": "static",
                  "txt1": "3. Diego",
                  "txt2": "3. Diego",
                  "txt3": "3. Diego",
                  "key": 3,
                  "source": "",
                  "nextmenuid": "1-0-3-1433"
                },
                "4": {
                  "sequence": 4,
                  "type": "static",
                  "txt1": "4. Fianarantsoa",
                  "txt2": "4. Fianarantsoa",
                  "txt3": "4. Fianarantsoa",
                  "key": 4,
                  "source": "",
                  "nextmenuid": "1-0-3-1434"
                },
                "5": {
                  "sequence": 5,
                  "type": "static",
                  "txt1": "5. Fort Dauphin",
                  "txt2": "5. Fort Dauphin",
                  "txt3": "5. Fort Dauphin",
                  "key": 5,
                  "source": "",
                  "nextmenuid": "1-0-3-1435"
                },
                "6": {
                  "sequence": 6,
                  "type": "static",
                  "txt1": "6. Majunga",
                  "txt2": "6. Majunga",
                  "txt3": "6. Majunga",
                  "key": 6,
                  "source": "",
                  "nextmenuid": "1-0-3-1436"
                },
                "7": {
                  "sequence": 7,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina @ menu teo aloha",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": 0,
                  "source": "",
                  "nextmenuid": "1-0-3-1437"
                }
              }
            },
            "144": {
              "id": "1-0-2-144",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "1. Money Transfer",
                  "txt2": "1. Fandefasam bola",
                  "txt3": "1. Transfert d argent",
                  "key": 1,
                  "source": "",
                  "nextmenuid": "1-0-3-1441"
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "2. Cash out with Airtel Money account",
                  "txt2": "2. Fanakalozam bola misy kaonty Airtel money",
                  "txt3": "2. Retrait avec compte Airtel Money",
                  "key": 2,
                  "source": "",
                  "nextmenuid": "1-0-3-1442"
                },
                "3": {
                  "sequence": 3,
                  "type": "static",
                  "txt1": "3. Cash out without Airtel Money account  or other operator\n#. Previous Menu",
                  "txt2": "3. Fanakalozam bola tsy misy kaonty Airtel money na mankany @ tambazotra hafa.\n#.Raha hiverina",
                  "txt3": "3. Retrait sans compte Airtel Money ou Autre Operateur\n#. Menu Precedent",
                  "key": 3,
                  "source": "",
                  "nextmenuid": "1-0-3-1443"
                }
              }
            },
            "131": {
              "id": "1-0-2-131",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Bahrein/Burkina Faso/ Cong Brazzaville/ Congo RDC/ Gabon/ Ghana/ Irak/ Jordanie/ Kenya/ Afrique du Sud/ Madagascar/ Malawi/",
                  "txt2": "Bahrein/Burkina Faso/ Cong Brazzaville/ Congo RDC/ Gabon/ Ghana/ Irak/ Jordanie/ Kenya/ Afrique du Sud/ Madagascar/ Malawi/",
                  "txt3": "Bahrein/Burkina Faso/ Cong Brazzaville/ Congo RDC/ Gabon/ Ghana/ Irak/ Jordanie/ Kenya/ Afrique du Sud/ Madagascar/ Malawi/",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-3-1310"
                }
              }
            },
            "132": {
              "id": "1-0-2-132",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "With Airtel Roaming service, you can use your number in many foreign countries and make your communications at any times",
                  "txt2": "Ny tolotra Roaming dia ahafahanao mampiasa ny laharana Airtel-nao any @ firenena ivelan i Madagasikara",
                  "txt3": "Avec le service Roaming, vous pouvez utiliser votre numero Airtel dans des pays etrangers et faire des communications a tout moment",
                  "key": "",
                  "source": ""
                }
              }
            },
            "133": {
              "id": "1-0-2-133",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Algeria/Angola/Anguilla/Antigua/Argentine/Armenia/Bahrain/Bangladesh/Barbados/Belarus/Belgium/Benin/Bolivia/",
                  "txt2": "Algeria/Angola/Anguilla/Antigua/Argentine/Armenia/Bahrain/Bangladesh/Barbados/Belarus/Belgium/Benin/Bolivia/",
                  "txt3": "Algeria/Angola/Anguilla/Antigua/Argentine/Armenia/Bahrain/Bangladesh/Barbados/Belarus/Belgium/Benin/Bolivia/",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0.Next Page\n#.Previous Menu",
                  "txt2": "0.Tohiny\n#.Raha hiverina",
                  "txt3": "0.Suivant\n#.Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-3-1330"
                }
              }
            },
            "15114": {
              "id": "1-0-2-15114",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "LE GLACIER Analakely:SICAM/TSINJO Ouest Ambohijanahary: In front of District/SHOP MANIA rasalama:in front of Cllg Rasalama/",
                  "txt2": "LE GLACIER Analakely:ao @SICAM/ TSINJO Andrefana Ambohijanahary: Ampita firaisana /SHOP MANIA rasalama: Ampita Kolejy Rasalama/",
                  "txt3": "LE GLACIER Analakely:Enceinte SICAM/ TSINJO Ouest Ambohijanahary:En face Firaisana/SHOP MANIA rasalama En face college Rasalama/",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-2-15115"
                }
              }
            },
            "16110": {
              "id": "1-0-4-16110",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel Shop Express Ivato Aeroport : Enceinte Aeroport International Airtel Shop Express La city Ivandry/",
                  "txt2": "Airtel Shop Express Ivato Aeroport : Enceinte Aeroport International Airtel Shop Express La city Ivandry/",
                  "txt3": "Airtel Shop Express Ivato Aeroport : Enceinte Aeroport International Airtel Shop Express La city Ivandry/",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-5-161100"
                }
              }
            },
            "116": {
              "id": "1-0-2-116",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "6. Increase credit limit",
                  "txt2": "6. Ampiakatra credit limit",
                  "txt3": "6. Rajout limitation de credit",
                  "key": 6,
                  "source": "",
                  "nextmenuid": "1-0-3-1166"
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "7. Bill amount",
                  "txt2": "7. Faktiora",
                  "txt3": "7. Montant facture",
                  "key": 7,
                  "source": "",
                  "nextmenuid": "1-0-3-1167"
                },
                "3": {
                  "sequence": 3,
                  "type": "static",
                  "txt1": "8. Emergency numbers\n#. Previous Menu",
                  "txt2": "8. Nomerao vonjy taitra\n#. Raha hiverina @ menu teo aloha",
                  "txt3": "8. Numero Urgences\n#. Menu Precedent",
                  "key": 8,
                  "source": "",
                  "nextmenuid": "1-0-3-1168"
                }
              }
            }
          }
        },
        "4": {
          "id": 0,
          "menus": {
            "1111": {
              "id": "1-0-3-1111",
              "type": "dynamic",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "dynamic",
                  "txt1": "",
                  "txt2": "",
                  "key": "",
                  "source": "http://127.0.0.1:9062/language?msisdn=$msisdn&operation=set&msg=txt-2"
                }
              }
            },
            "1112": {
              "id": "1-0-3-1112",
              "type": "dynamic",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "dynamic",
                  "txt1": "",
                  "txt2": "",
                  "key": "",
                  "source": "http://127.0.0.1:9062/language?msisdn=$msisdn&operation=set&msg=txt-3"
                }
              }
            },
            "1113": {
              "id": "1-0-3-1113",
              "type": "dynamic",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "dynamic",
                  "txt1": "",
                  "txt2": "",
                  "key": "",
                  "source": "http://127.0.0.1:9062/language?msisdn=$msisdn&operation=set&msg=txt-1"
                }
              }
            },
            "1161": {
              "id": "1-0-3-1161",
              "type": "dynamic",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "dynamic",
                  "txt1": "",
                  "txt2": "",
                  "key": "",
                  "source": "http://127.0.0.1:9098/process?msisdn=$msisdn&action=increasecreditlimit&sessionId=$sessionId&language=$language&amount=5000"
                }
              }
            },
            "1162": {
              "id": "1-0-3-1162",
              "type": "dynamic",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "dynamic",
                  "txt1": "",
                  "txt2": "",
                  "key": "",
                  "source": "http://127.0.0.1:9098/process?msisdn=$msisdn&action=increasecreditlimit&sessionId=$sessionId&language=$language&amount=10000"
                }
              }
            },
            "1163": {
              "id": "1-0-3-1163",
              "type": "dynamic",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "dynamic",
                  "txt1": "",
                  "txt2": "",
                  "key": "",
                  "source": "http://127.0.0.1:9098/process?msisdn=$msisdn&action=increasecreditlimit&sessionId=$sessionId&language=$language&amount=20000"
                }
              }
            },
            "11781": {
              "id": "1-0-4-11681",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "To join AIRTEL MONEY dedicated Services :Dial 434. To join INTERNET dedicated Services:Dial 454 And to join Airtel customer care service, dial 121.",
                  "txt2": "Raha mila fanampiana mikasika ny AIRTEL MONEY:Antsoy ny 434. Raha fanampiana mikasika ny INTERNET:Antsoy ny 454.Raha mila fanampiana hafa:Antsoy ny 121",
                  "txt3": "Pour une assistance concernant AIRTEL MONEY:Appelez le 434.Pour une assistance sur l Internet:Appelez le 454.Pour d autres informations:Appelez le 121",
                  "key": "",
                  "source": ""
                }
              }
            },
            "11682": {
              "id": "1-0-4-11682",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Please dial 118 to reach fire department",
                  "txt2": "Raha hifandray @ sampana mpamonjy voina, dia antsoy ny 118. Misaotra Tompoko",
                  "txt3": "Pour joindre le service des sapeurs Pompier,  veuillez appeler le 118. Merci",
                  "key": "",
                  "source": ""
                }
              }
            },
            "11683": {
              "id": "1-0-4-11683",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Please dial 0202222735 to reach POLICE department",
                  "txt2": "Raha mila fanampiana @ Polisy vonjy maika, dia antsoy ny 0202222735. Misaotra Tompoko",
                  "txt3": "Pour rejoindre la police nationale en cas d urgence, veuillez appeler le 0202222735. Merci",
                  "key": "",
                  "source": ""
                }
              }
            },
            "11684": {
              "id": "1-0-4-11684",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Please dial 033547 to reach JIRAMA department",
                  "txt2": "Raha hifandray @ JIRAMA, dia antsoy ny 033547. Misaotra Tompoko.",
                  "txt3": "Pour joindre le service d urgence de la JIRAMA, veuillez appeler le 033547. Merci",
                  "key": "",
                  "source": ""
                }
              }
            },
            "13300": {
              "id": "1-0-4-13300",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Cape Vert/Cayman Islands/Centrafrique/China/Comore/Congo/Congo Brazaville/Congo RDC (Congo Kinshasa)/Croatia/Cuba/Curacao/",
                  "txt2": "Cape Vert/Cayman Islands/Centrafrique/China/Comore/Congo/Congo Brazaville/Congo RDC (Congo Kinshasa)/Croatia/Cuba/Curacao/",
                  "txt3": "Cape Vert/Cayman Islands/Centrafrique/China/Comore/Congo/Congo Brazaville/Congo RDC (Congo Kinshasa)/Croatia/Cuba/Curacao/",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-5-133000"
                }
              }
            },
            "14310": {
              "id": "1-0-4-14310",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "TANA PHONE Mahazo:Arret Ligne Manjakandriana/ KIOSK Ambohitsoa:Arret Bus 151/ Shop GRAND Nanisana:Croisement Nanisana/",
                  "txt2": "TANA PHONE Mahazo:Arret Ligne Manjakandriana/ KIOSK Ambohitsoa:Arret Bus 151/ Shop GRAND Nanisana:Croisement Nanisana/",
                  "txt3": "TANA PHONE Mahazo:Arret Ligne Manjakandriana/ KIOSK Ambohitsoa:Arret Bus 151/ Shop GRAND Nanisana:Croisement Nanisana/",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": 0,
                  "source": "",
                  "nextmenuid": "1-0-5-143100"
                }
              }
            },
            "14320": {
              "id": "1-0-4-14320",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "SPACE MUSIC Antsirabe:En face YAMAHA Distribution/AINA Service Ambatolampy: Pres PAOSITRA MALAGASY/JAO Ambatolampy: face BOA/",
                  "txt2": "SPACE MUSIC Antsirabe:En face YAMAHA Distribution/AINA Service Ambatolampy: Pres PAOSITRA MALAGASY/JAO Ambatolampy: face BOA/",
                  "txt3": "SPACE MUSIC Antsirabe:En face YAMAHA Distribution/AINA Service Ambatolampy: Pres PAOSITRA MALAGASY/JAO Ambatolampy: face BOA/",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-5-143200"
                }
              }
            },
            "14330": {
              "id": "1-0-4-14330",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": " Airtel Shop Express Center Phone: Analamandrorofo SAMBAVA (en face de la Pharmacie RAVINALA)/",
                  "txt2": " Airtel Shop Express Center Phone: Analamandrorofo SAMBAVA (en face de la Pharmacie RAVINALA)/",
                  "txt3": "Airtel Shop Express Center Phone: Analamandrorofo SAMBAVA (en face de la Pharmacie RAVINALA)/",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-5-143300"
                }
              }
            },
            "14340": {
              "id": "1-0-4-14340",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "INTERCENTER Antarandolo : En face GALANA / LEONG JOSE Ihosy : Pres marche Tanambao Ihosy /",
                  "txt2": "INTERCENTER Antarandolo : En face GALANA / LEONG JOSE Ihosy : Pres marche Tanambao Ihosy /",
                  "txt3": "INTERCENTER Antarandolo : En face GALANA / LEONG JOSE Ihosy : Pres marche Tanambao Ihosy /",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-5-143400"
                }
              }
            },
            "14350": {
              "id": "1-0-4-14350",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Hotel LA SOURCE Ambovombe / LAYLAH Ambovombe : En face Tribunal / LE BON SAMARITAIN Amboasary / EPICERIE SAHONDRA Amboasary /",
                  "txt2": "Hotel LA SOURCE Ambovombe / LAYLAH Ambovombe : En face Tribunal / LE BON SAMARITAIN Amboasary / EPICERIE SAHONDRA Amboasary /",
                  "txt3": "Hotel LA SOURCE Ambovombe / LAYLAH Ambovombe : En face Tribunal / LE BON SAMARITAIN Amboasary / EPICERIE SAHONDRA Amboasary /",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-5-143500"
                }
              }
            },
            "14360": {
              "id": "1-0-4-14360",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "MADIS Majunga : En face BMOI/ EPI JACKY Tsaramandroso : 50m apres EKAR/ TRACE GSM Majunga : a cote stade Rabemananjara /",
                  "txt2": "MADIS Majunga : En face BMOI/ EPI JACKY Tsaramandroso : 50m apres EKAR/ TRACE GSM Majunga : a cote stade Rabemananjara /",
                  "txt3": "MADIS Majunga : En face BMOI/ EPI JACKY Tsaramandroso : 50m apres EKAR/ TRACE GSM Majunga : a cote stade Rabemananjara /",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-5-143600"
                }
              }
            },
            "14377": {
              "id": "1-0-4-14377",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel Shop Express NIKARDIST : Carrefour Hazomidiroboka MORAMANGA",
                  "txt2": "Airtel Shop Express NIKARDIST : Carrefour Hazomidiroboka MORAMANGA",
                  "txt3": "Airtel Shop Express NIKARDIST: Carrefour Hazomidiroboka MORAMANGA",
                  "key": "",
                  "source": ""
                }
              }
            },
            "14378": {
              "id": "1-0-4-14378",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "ROSEMINE Sainte Marie Ville / PAOSITRA MALAGASY / MICROCRED /",
                  "txt2": "ROSEMINE Sainte Marie Ville / PAOSITRA MALAGASY / MICROCRED /",
                  "txt3": "ROSEMINE Sainte Marie Ville / PAOSITRA MALAGASY / MICROCRED /",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\nRaha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-5-143080"
                }
              }
            },
            "14379": {
              "id": "1-0-4-14379",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel Shop Express SITENY : Immeuble Siteny a Andaboly : A cote du college francais /PAOSITRA MALAGASY Ranohira / MICROCRED /",
                  "txt2": "Airtel Shop Express SITENY : Immeuble Siteny a Andaboly : A cote du college francais /PAOSITRA MALAGASY Ranohira / MICROCRED /",
                  "txt3": "Airtel Shop Express SITENY : Immeuble Siteny a Andaboly : A cote du college francais /PAOSITRA MALAGASY Ranohira / MICROCRED /",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-5-143790"
                }
              }
            },
            "14412": {
              "id": "1-0-4-14412",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "100 001 a 250 000: 1 500Ar /250 001 a 500 000: 2 800Ar /500 001 a 1 000 000: 4 000Ar  /1 000 001 a 2 000 000: 5 000Ar /",
                  "txt2": "100 001 a 250 000: 1 500Ar /250 001 a 500 000: 2 800Ar /500 001 a 1 000 000: 4 000Ar  /1 000 001 a 2 000 000: 5 000Ar /",
                  "txt3": "100 001 a 250 000: 1 500Ar /250 001 a 500 000: 2 800Ar /500 001 a 1 000 000: 4 000Ar  /1 000 001 a 2 000 000: 5 000Ar /",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0- Next Page\n#- Previous Menu",
                  "txt2": "0- Tohiny\n#- Raha hiverina",
                  "txt3": "0- Suivant\n#- Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-5-144122"
                }
              }
            },
            "14422": {
              "id": "1-0-4-14422",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "100 001 a 250 000: 3 500Ar /250 001 a 500 000: 4 200Ar /500 001 a 1 000 000: 6 000Ar  /1 000 001 a 2 000 000: 10 000Ar",
                  "txt2": "100 001 a 250 000: 3 500Ar /250 001 a 500 000: 4 200Ar /500 001 a 1 000 000: 6 000Ar  /1 000 001 a 2 000 000: 10 000Ar",
                  "txt3": "100 001 a 250 000: 3 500Ar /250 001 a 500 000: 4 200Ar /500 001 a 1 000 000: 6 000Ar  /1 000 001 a 2 000 000: 10 000Ar /",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0- Next Page\n#- Previous Menu",
                  "txt2": "0- Tohiny\n#- Raha hiverina",
                  "txt3": "0- Suivant\n#- Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-5-144222"
                }
              }
            },
            "14432": {
              "id": "1-0-4-14432",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "100 001 a 250 000: 9 500Ar /250 001 a 500 000: 12 500Ar /500 001 a 1 000 000: 17 000Ar  /1 000 001 a 2 000 000: 29 000Ar /",
                  "txt2": "100 001 a 250 000: 9 500Ar /250 001 a 500 000: 12 500Ar /500 001 a 1 000 000: 17 000Ar  /1 000 001 a 2 000 000: 29 000Ar /",
                  "txt3": "100 001 a 250 000: 9 500Ar /250 001 a 500 000: 12 500Ar /500 001 a 1 000 000: 17 000Ar  /1 000 001 a 2 000 000: 29 000Ar /",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0- Next Page\n#- Previous Menu",
                  "txt2": "0- Tohiny\n#- Raha hiverina",
                  "txt3": "0- Suivant\n#- Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-5-144322"
                }
              }
            },
            "161100": {
              "id": "1-0-5-161100",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel SHOP Express Ambohijatovo /Airtel SHOP Express, Nanisana Ampasampito / Airtel SHOP Express 67 Ha Nord Est /",
                  "txt2": "Airtel SHOP Express Ambohijatovo /Airtel SHOP Express, Nanisana Ampasampito / Airtel SHOP Express 67 Ha Nord Est /",
                  "txt3": "Airtel SHOP Express Ambohijatovo /Airtel SHOP Express, Nanisana Ampasampito / Airtel SHOP Express 67 Ha Nord Est",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-6-1611000"
                }
              }
            },
            "162100": {
              "id": "1-0-5-162100",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel SHOP Express Ambohijatovo /Airtel SHOP Express, Nanisana Ampasampito / Airtel SHOP Express 67 Ha Nord Est /",
                  "txt2": "Airtel SHOP Express Ambohijatovo /Airtel SHOP Express, Nanisana Ampasampito / Airtel SHOP Express 67 Ha Nord Est",
                  "txt3": "Airtel SHOP Express Ambohijatovo /Airtel SHOP Express, Nanisana Ampasampito / Airtel SHOP Express 67 Ha Nord Est /",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-6-1621000"
                }
              }
            },
            "15271": {
              "id": "1-0-4-15271",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Take advantage of 10Go of Internet available 1 month for Ar 135 000. To subscribe,  please visit the nearest  Airtel shop.",
                  "txt2": "Ahazoanao 10Go Internet ampiasaina mandritra ny 1 volana @ sarany Ar 135 000. Ho fidirana ao @ tolotra, manantona ny Shop Airtel Akaiky anao.",
                  "txt3": "Beneficiez de 10Go de connexion internet mensuelle pour  Ar 135 000. Pour y souscrire, nous vous invitons a passer aupres de nos shops Airtel. Merci",
                  "key": "",
                  "source": ""
                }
              }
            },
            "15272": {
              "id": "1-0-4-15272",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Take advantage of 30Go of Internet available 1 month for Ar 180 000. To subscribe,  please visit the nearest  Airtel shop.",
                  "txt2": "Ahazoanao 30Go Internet ampiasaina mandritra ny 1 volana @ sarany Ar 180 000. Ho fidirana ao @ tolotra, manantona ny Shop Airtel Akaiky anao.",
                  "txt3": "Beneficiez de 30Go de connexion internet mensuelle pour  Ar 180 000. Pour y souscrire, nous vous invitons a passer aupres de nos shops Airtel. Merci",
                  "key": "",
                  "source": ""
                }
              }
            },
            "1232": {
              "id": "1-0-3-1232",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "To subscribe : send CONTACT to 238 , then dowload the application .Your password will be sent per sms and login will be your number",
                  "txt2": "Alefaso maimaimpoana any @ 238 ny hoe: CONTACT, ahafahanao misintona ny application",
                  "txt3": "Pour l activer,envoyez CONTACT gratuitement au 238 et telechargez l application",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0-Next Page\n#-Previous Menu",
                  "txt2": "0-Tohiny\n#-Raha hiverina",
                  "txt3": "0-Suivant\n#-Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-4-12322"
                }
              }
            },
            "1511": {
              "id": "1-0-3-1511",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "APN: internet",
                  "txt2": "APN: internet",
                  "txt3": "APN: internet",
                  "key": "",
                  "source": ""
                }
              }
            },
            "1512": {
              "id": "1-0-3-1512",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Apn: wap\nProxy:172.025.156.136\nPort: 8080",
                  "txt2": "Apn: wap\n Proxy:172.025.156.136\nPort: 8080",
                  "txt3": "Apn: wap\nProxy:172.025.156.136\nPort: 8080",
                  "key": "",
                  "source": ""
                }
              }
            },
            "1521": {
              "id": "1-0-3-1521",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Take advantage of 200Mo of Internet available 1 month for Ar 11 000. To subscribe,  please visit the nearest  Airtel shop.",
                  "txt2": "Ahazoanao 200Mo Internet ampiasaina mandritra ny 1 volana @ sarany Ar 11000. Ho fidirana ao @ tolotra, manantona ny Shop Airtel Akaiky anao.",
                  "txt3": "Beneficiez 200Mo de connexion internet mensuelle pour  Ar 11 000. Pour y souscrire, nous vous invitons a passer aupres de nos shops Airtel. Merci",
                  "key": "",
                  "source": ""
                }
              }
            },
            "1522": {
              "id": "1-0-3-1522",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Take advantage of 500Mo of Internet available 1 month for Ar 24 000. To subscribe,  please visit the nearest  Airtel shop.",
                  "txt2": "Ahazoanao 500Mo Internet ampiasaina mandritra ny 1 volana @ sarany Ar 24 000. Ho fidirana ao @ tolotra, manantona ny Shop Airtel Akaiky anao.",
                  "txt3": "Beneficiez  de 500Mo de connexion internet mensuelle pour  Ar 24 000. Pour y souscrire, nous vous invitons a passer aupres de nos shops Airtel. Merci",
                  "key": "",
                  "source": ""
                }
              }
            },
            "1523": {
              "id": "1-0-3-1523",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Take advantage of 1Go of Internet available 1 month for Ar 44 500. To subscribe,  please visit the nearest  Airtel shop.",
                  "txt2": "Ahazoanao 1Go Internet ampiasaina mandritra ny 1 volana @ sarany Ar 44 500. Ho fidirana ao @ tolotra, manantona ny Shop Airtel Akaiky anao.",
                  "txt3": "Beneficiez de 1Go de connexion internet mensuelle pour  Ar 44 500. Pour y souscrire, nous vous invitons a passer aupres de nos shops Airtel. Merci",
                  "key": "",
                  "source": ""
                }
              }
            },
            "1524": {
              "id": "1-0-3-1524",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Take advantage of 2Go of Internet available 1 month for Ar 66 000. To subscribe,  please visit the nearest  Airtel shop.",
                  "txt2": "Ahazoanao 2Go Internet ampiasaina mandritra ny 1 volana @ sarany Ar 66 000. Ho fidirana ao @ tolotra, manantona ny Shop Airtel Akaiky anao.",
                  "txt3": "Beneficiez de 2Go de connexion internet mensuelle pour  Ar 66 000. Pour y souscrire, nous vous invitons a passer aupres de nos shops Airtel. Merci",
                  "key": "",
                  "source": ""
                }
              }
            },
            "1525": {
              "id": "1-0-3-1525",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Take advantage of 3Go of Internet available 1 month for Ar 72 500. To subscribe,  please visit the nearest  Airtel shop.",
                  "txt2": "Ahazoanao 3Go Internet ampiasaina mandritra ny 1 volana @ sarany Ar 72 500. Ho fidirana ao @ tolotra, manantona ny Shop Airtel Akaiky anao.",
                  "txt3": "Beneficiez de 3Go de connexion internet mensuelle pour  Ar 72 500. Pour y souscrire, nous vous invitons a passer aupres de nos shops Airtel. Merci",
                  "key": "",
                  "source": ""
                }
              }
            },
            "1526": {
              "id": "1-0-3-1526",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Take advantage of 5Go of Internet available 1 month for Ar 85 500. To subscribe,  please visit the nearest  Airtel shop.",
                  "txt2": "Ahazoanao 5Go Internet ampiasaina mandritra ny 1 volana @ sarany Ar 85 500. Ho fidirana ao @ tolotra, manantona ny Shop Airtel Akaiky anao.",
                  "txt3": "Beneficiez de 5Go de connexion internet mensuelle pour  Ar 85 500. Pour y souscrire, nous vous invitons a passer aupres de nos shops Airtel. Merci",
                  "key": "",
                  "source": ""
                }
              }
            },
            "1527": {
              "id": "1-0-3-1527",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "7. MYGIG10",
                  "txt2": "7. MYGIG10",
                  "txt3": "7. MYGIG10",
                  "key": "7",
                  "source": "",
                  "nextmenuid": "1-0-4-15271"
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "8. MYGIG30\n#. Previous Menu",
                  "txt2": "8. MYGIG30\n#. Raha hiverina",
                  "txt3": "8. MYGIG30\n#. Menu Precedent",
                  "key": "8",
                  "source": "",
                  "nextmenuid": "1-0-4-15272"
                }
              }
            },
            "1611": {
              "id": "1-0-3-1611",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel Shop Ankorondrano : Explorer Business Park B3 Ankorondrano / Airtel Shop Express Analakely: Digital World Center /",
                  "txt2": "Airtel Shop Ankorondrano : Explorer Business Park B3 Ankorondrano / Airtel Shop Express Analakely: Digital World Center /",
                  "txt3": "Airtel Shop Ankorondrano : Explorer Business Park B3 Ankorondrano / Airtel Shop Express Analakely: Digital World Center /",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-4-16110"
                }
              }
            },
            "1612": {
              "id": "1-0-3-1612",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel Shop Express SOA SERVICE: Ny Havana Immeuble La Planete.",
                  "txt2": "Airtel Shop Express SOA SERVICE: Ny Havana Immeuble La Planete.",
                  "txt3": "Airtel Shop Express SOA SERVICE: Ny Havana Immeuble La Planete.",
                  "key": "",
                  "source": ""
                }
              }
            },
            "1613": {
              "id": "1-0-3-1613",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel SHOP Express , 11 Rue Lafayette Diego / Airtel SHOP Express, Sambava Centre / Airtel SHOP Express Nosibe, Rue Boulevard point carree Helville.",
                  "txt2": "Airtel SHOP Express , 11 Rue Lafayette Diego / Airtel SHOP Express, Sambava Centre / Airtel SHOP Express Nosibe, Rue Boulevard point carree Helville.",
                  "txt3": "Airtel SHOP Express , 11 Rue Lafayette Diego / Airtel SHOP Express, Sambava Centre / Airtel SHOP Express Nosibe, Rue Boulevard point carree Helville.",
                  "key": "",
                  "source": ""
                }
              }
            },
            "1614": {
              "id": "1-0-3-1614",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel Shop Express ANNICK SERVICE: Tambohobe Fianarantsoa ville",
                  "txt2": "Airtel Shop Express ANNICK SERVICE: Tambohobe Fianarantsoa ville",
                  "txt3": "Airtel Shop Express ANNICK SERVICE: Tambohobe Fianarantsoa ville",
                  "key": "",
                  "source": ""
                }
              }
            },
            "1627": {
              "id": "1-0-3-1627",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "7. Moramanga",
                  "txt2": "7. Moramanga",
                  "txt3": "7. Moramanga",
                  "key": 7,
                  "source": "",
                  "nextmenuid": "1-0-4-16277"
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "8. Tamatave",
                  "txt2": "8. Tamatave",
                  "txt3": "8. Tamatave",
                  "key": 8,
                  "source": "",
                  "nextmenuid": "1-0-4-16278"
                },
                "3": {
                  "sequence": 3,
                  "type": "static",
                  "txt1": "9. Tulear\n#. Previous Menu",
                  "txt2": "9. Tulear\n#. Raha hiverina",
                  "txt3": "9. Tulear\n#. Menu Precedent",
                  "key": 9,
                  "source": "",
                  "nextmenuid": "1-0-4-16279"
                }
              }
            },
            "1615": {
              "id": "1-0-3-1615",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel Shop Express Fort Dauphin: Immeuble Martial BAZARY BE",
                  "txt2": "Airtel Shop Express Fort Dauphin: Immeuble Martial BAZARY BE",
                  "txt3": "Airtel Shop Express Fort Dauphin: Immeuble Martial BAZARY BE",
                  "key": "",
                  "source": ""
                }
              }
            },
            "1616": {
              "id": "1-0-3-1616",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel Shop Express Antso Speed: Villa Cosmos, Mangarivotra",
                  "txt2": "Airtel Shop Express Antso Speed: Villa Cosmos, Mangarivotra",
                  "txt3": "Airtel Shop Express Antso Speed: Villa Cosmos, Mangarivotra",
                  "key": "",
                  "source": ""
                }
              }
            },
            "12211": {
              "id": "1-0-4-12211",
              "type": "dynamic",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "dynamic",
                  "txt1": "",
                  "txt2": "",
                  "txt3": "",
                  "key": "",
                  "source": "http://127.0.0.1:9890/process?msisdn=$msisdn&language=$language&sessionId=$sessionId&action=puk&called_msisdn=$called_msisdn&recipient=$recipient"
                }
              }
            },
            "12322": {
              "id": "1-0-4-12322",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "RESTORE option will allow to upload the data saved in your phone.You will becharged according to theinternetpackageused for downloadingdata.#-Previous Menu",
                  "txt2": "Haharay ny teny miafina @ SMS ianao ary ny nomeraonao no ho famantarana anao /#-raha hiverina",
                  "txt3": "Votre mot de passe sera envoye par SMS, et votre identifiant est le numero 26133XXXXXXX #-Menu precedent",
                  "key": "",
                  "source": ""
                }
              }
            },
            "16177": {
              "id": "1-0-4-16177",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel Shop Express NIKARDIST : Carrefour Hazomidiroboka MORAMANGA",
                  "txt2": "Airtel Shop Express NIKARDIST : Carrefour Hazomidiroboka MORAMANGA",
                  "txt3": "Airtel Shop Express NIKARDIST : Carrefour Hazomidiroboka MORAMANGA",
                  "key": "",
                  "source": ""
                }
              }
            },
            "16178": {
              "id": "1-0-4-16178",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel  Shop Express 033MOBILE : B2 Cite Procopse, Tanambao 5",
                  "txt2": "Airtel  Shop Express 033MOBILE : B2 Cite Procopse, Tanambao 5",
                  "txt3": "Airtel  Shop Express 033MOBILE : B2 Cite Procopse, Tanambao 5",
                  "key": "",
                  "source": ""
                }
              }
            },
            "16179": {
              "id": "1-0-4-16179",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel SHOP Express , Immeuble SITENY Andaboly.",
                  "txt2": "Airtel SHOP Express , Immeuble SITENY Andaboly.",
                  "txt3": "Airtel SHOP Express , Immeuble SITENY Andaboly.",
                  "key": "",
                  "source": ""
                }
              }
            },
            "16210": {
              "id": "1-0-4-16210",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel Shop Express Ivato Aeroport : Enceite Aeroport International Airtel Shop Express La city Ivandry/",
                  "txt2": "Airtel Shop Express Ivato Aeroport : Enceinte Aeroport International Airtel Shop Express La city Ivandry/",
                  "txt3": "Airtel Shop Express Ivate Aeroport : Enceinte Aeroport International Airtel Shop Express La city Ivandry/",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-5-162100"
                }
              }
            },
            "1622": {
              "id": "1-0-3-1622",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel Shop Express SOA SERVICE: Ny Havana Immeuble La Planete.",
                  "txt2": "Airtel Shop Express SOA SERVICE: Ny Havana Immeuble La Planete.",
                  "txt3": "Airtel Shop Express SOA SERVICE: Ny Havana Immeuble La Planete.",
                  "key": "",
                  "source": ""
                }
              }
            },
            "1621": {
              "id": "1-0-3-1621",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel Shop Ankorondrano : Explorer Business Park B3 Ankorondrano / Airtel Shop Express Analakely: Digital World Center /",
                  "txt2": "Airtel Shop Ankorondrano : Explorer Business Park B3 Ankorondrano / Airtel Shop Express Analakely: Digital World Center/",
                  "txt3": "Airtel Shop Ankorondrano : Explorer Business Park B3 Ankorondrano / Airtel Shop Express Analakely: Digital World Center /",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-4-16210"
                }
              }
            },
            "1623": {
              "id": "1-0-3-1623",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel SHOP Express , 11 Rue Lafayette Diego / Airtel SHOP Express, Sambava Centre / Airtel SHOP Express Nosibe, Rue Boulevard point carree Helville.",
                  "txt2": "Airtel SHOP Express , 11 Rue Lafayette Diego / Airtel SHOP Express, Sambava Centre / Airtel SHOP Express Nosibe, Rue Boulevard point carree Helville.",
                  "txt3": "Airtel SHOP Express , 11 Rue Lafayette Diego / Airtel SHOP Express, Sambava Centre / Airtel SHOP Express Nosibe, Rue Boulevard point carree Helville.",
                  "key": "",
                  "source": ""
                }
              }
            },
            "1624": {
              "id": "1-0-3-1624",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel Shop Express ANNICK SERVICE: Tambohobe Fianarantsoa ville",
                  "txt2": "Airtel Shop Express ANNICK SERVICE: Tambohobe Fianarantsoa ville",
                  "txt3": "Airtel Shop Express ANNICK SERVICE: Tambohobe Fianarantsoa ville",
                  "key": "",
                  "source": ""
                }
              }
            },
            "1625": {
              "id": "1-0-3-1625",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel Shop Express Fort Dauphin: Immeuble Martial BAZARY BE",
                  "txt2": "Airtel Shop Express Fort Dauphin: Immeuble Martial BAZARY BE",
                  "txt3": "Airtel Shop Express Fort Dauphin: Immeuble Martial BAZARY BE",
                  "key": "",
                  "source": ""
                }
              }
            },
            "1626": {
              "id": "1-0-3-1626",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel Shop Express Antso Speed: Villa Cosmos, Mangarivotra",
                  "txt2": "Airtel Shop Express Antso Speed: Villa Cosmos, Mangarivotra",
                  "txt3": "Airtel Shop Express Antso Speed: Villa Cosmos, Mangarivotra",
                  "key": "",
                  "source": ""
                }
              }
            },
            "1-0-4-16277": {
              "id": "1-0-4-16277",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel Shop Express NIKARDIST : Carrefour Hazomidiroboka MORAMANGA",
                  "txt2": "Airtel Shop Express NIKARDIST : Carrefour Hazomidiroboka MORAMANGA",
                  "txt3": "Airtel Shop Express NIKARDIST : Carrefour Hazomidiroboka MORAMANG",
                  "key": "",
                  "source": ""
                }
              }
            },
            "16278": {
              "id": "1-0-4-16278",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel  Shop Express 033MOBILE : B2 Cite Procopse, Tanambao 5",
                  "txt2": "Airtel  Shop Express 033MOBILE : B2 Cite Procopse, Tanambao 5",
                  "txt3": "Airtel  Shop Express 033MOBILE : B2 Cite Procopse, Tanambao 5",
                  "key": "",
                  "source": ""
                }
              }
            },
            "16279": {
              "id": "1-0-4-16279",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel SHOP Express , Immeuble SITENY Andaboly.",
                  "txt2": "Airtel SHOP Express , Immeuble SITENY Andaboly.",
                  "txt3": "Airtel SHOP Express , Immeuble SITENY Andaboly.",
                  "key": "",
                  "source": ""
                }
              }
            },
            "1431": {
              "id": "1-0-3-1431",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel Shop Ankorondrano : Explorer Business Park B3 Ankorondrano / Airtel Shop Express Ambodifilao: Au Digital World Cente",
                  "txt2": "Airtel Shop Ankorondrano : Explorer Business Park B3 Ankorondrano / Airtel Shop Express Ambodifilao: Au Digital World Center",
                  "txt3": "Airtel Shop Ankorondrano : Explorer Business Park B3 Ankorondrano / Airtel Shop Express Ambodifilao: Au Digital World Center",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-4-14310"
                }
              }
            },
            "1432": {
              "id": "1-0-3-1432",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "SOA DISTRIBUTION Ambavahadimangatsiaka : En face SOPROMER / ARC DISTRIBUTION Mahazoarivo : En face Cenacle /",
                  "txt2": "SOA DISTRIBUTION Ambavahadimangatsiaka : En face SOPROMER / ARC DISTRIBUTION Mahazoarivo : En face Cenacle /",
                  "txt3": "SOA DISTRIBUTION Ambavahadimangatsiaka : En face SOPROMER / ARC DISTRIBUTION Mahazoarivo : En face Cenacle /",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina @ menu teo aloha",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-4-14320"
                }
              }
            },
            "1433": {
              "id": "1-0-3-1433",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel Shop Phone  Center:11 Rue Lafayette Diego ville/Airtel Shop Express FILEMS:Rue Boulevard point carree Nosy Be/",
                  "txt2": "Airtel Shop Phone  Center:11 Rue Lafayette Diego ville/Airtel Shop Express FILEMS:Rue Boulevard point carree Nosy Be/",
                  "txt3": "Airtel Shop Phone  Center:11 Rue Lafayette Diego ville/Airtel Shop Express FILEMS:Rue Boulevard point carree Nosy Be/",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-4-14330"
                }
              }
            },
            "1434": {
              "id": "1-0-3-1434",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "ENTREPRISE FELANA Ambositra:A cote Hotel MANIA /MME LANTO Ambositra:A cote Hotel Fihaonana /GOURMANO Manaraka :En face VULCA /",
                  "txt2": "ENTREPRISE FELANA Ambositra:A cote Hotel MANIA /MME LANTO Ambositra:A cote Hotel Fihaonana /GOURMANO Manaraka :En face VULCA /",
                  "txt3": "ENTREPRISE FELANA Ambositra:A cote Hotel MANIA /MME LANTO Ambositra:A cote Hotel Fihaonana /GOURMANO Manaraka :En face VULCA /",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-4-14340"
                }
              }
            },
            "1545": {
              "id": "1-0-3-1435",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "FIDEL : Devant Gendarmerie Taolagnaro / LAMINA FujiFilm Esokaka / PAOSITRA MALAGASY/",
                  "txt2": "FIDEL : Devant Gendarmerie Taolagnaro / LAMINA FujiFilm Esokaka / PAOSITRA MALAGASY/",
                  "txt3": "FIDEL : Devant Gendarmerie Taolagnaro / LAMINA FujiFilm Esokaka / PAOSITRA MALAGASY/",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-4-14350"
                }
              }
            },
            "1436": {
              "id": "1-0-3-1436",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel Shop Express Antso Speed: Villa Cosmos, pav no 3 en face Stade Rabemananjara, Mangarivotra/",
                  "txt2": "Airtel Shop Express Antso Speed: Villa Cosmos, pav no 3 en face Stade Rabemananjara, Mangarivotra/",
                  "txt3": "Airtel Shop Express Antso Speed: Villa Cosmos, pav no 3 en face Stade Rabemananjara, Mangarivotra/",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-4-14360"
                }
              }
            },
            "1176": {
              "id": "1-0-3-1166",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "1. Ar 5000",
                  "txt2": "1. Ar 5000",
                  "txt3": "1. Ar 5000",
                  "key": "1",
                  "source": "",
                  "nextmenuid": "1-0-4-11661"
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "2. Ar 10 000",
                  "txt2": "2. Ar 10 000",
                  "txt3": "2. Ar 10 000",
                  "key": 2,
                  "source": "",
                  "nextmenuid": "1-0-4-11662"
                },
                "3": {
                  "sequence": 3,
                  "type": "static",
                  "txt1": "3. Ar 20 000\n#. Previous Menu",
                  "txt2": "3. Ar 20 000\n#. Raha hiverina @ menu teo aloha",
                  "txt3": "3. Ar 20 000\n#. Menu Precedent",
                  "key": 3,
                  "source": "",
                  "nextmenuid": "1-0-4-11663"
                }
              }
            },
            "1167": {
              "id": "1-0-3-1167",
              "type": "dynamic",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "dynamic",
                  "txt1": "",
                  "txt2": "",
                  "txt3": "",
                  "key": "",
                  "source": "http://127.0.0.1:9098/process?msisdn=$msisdn&language=$language&sessionId=$sessionId&action=billamount"
                }
              }
            },
            "1168": {
              "id": "1-0-3-1168",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "1. Customer service",
                  "txt2": "1. Sampana mpikarakara ny mpanjifa",
                  "txt3": "1. Service Clientele",
                  "key": 1,
                  "source": "",
                  "nextmenuid": "1-0-4-11681"
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "2. Fire department",
                  "txt2": "2. Pompier",
                  "txt3": "2. Pompier",
                  "key": 2,
                  "source": "",
                  "nextmenuid": "1-0-4-11682"
                },
                "3": {
                  "sequence": 3,
                  "type": "static",
                  "txt1": "3. Police",
                  "txt2": "3. Police",
                  "txt3": "3. Police",
                  "key": 3,
                  "source": "",
                  "nextmenuid": "1-0-4-11683"
                },
                "4": {
                  "sequence": 4,
                  "type": "static",
                  "txt1": "4. JIRAMA\n#.Previous Menu",
                  "txt2": "4. JIRAMA\n#. Raha hiverina @ menu teo aloha",
                  "txt3": "4. JIRAMA\n#. Menu Precedent",
                  "key": 4,
                  "source": "",
                  "nextmenuid": "1-0-4-11684"
                }
              }
            },
            "1211": {
              "id": "1-0-3-1211",
              "type": "dynamic",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "dynamic",
                  "txt1": "",
                  "txt2": "",
                  "txt3": "",
                  "key": "",
                  "source": "http://127.0.0.1:9098/process?msisdn=$msisdn&language=$language&sessionId=$sessionId&action=cmb&recipient=$recipient"
                }
              }
            },
            "1221": {
              "id": "1-0-3-1221",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "any",
              "services": "",
              "package": "",
              "parameter": "called_msisdn",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Enter a frequently dialed number",
                  "txt2": "Ampidiro ny nomerao fiantso matetika iray",
                  "txt3": "Entrez un Numero que vous appelez frequemment",
                  "key": "",
                  "source": "",
                  "nextmenuid": "1-0-4-12211"
                }
              }
            },
            "1310": {
              "id": "1-0-3-1310",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Niger/ Ouganda/ Sierra Leone/ Soudan/ Tanzanie/ Tchad/ Zambie",
                  "txt2": "Niger/ Ouganda/ Sierra Leone/ Soudan/ Tanzanie/ Tchad/ Zambie",
                  "txt3": "Niger/ Ouganda/ Sierra Leone/ Soudan/ Tanzanie/ Tchad/ Zambie",
                  "key": "",
                  "source": ""
                }
              }
            },
            "1330": {
              "id": "1-0-3-1330",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "Bosnia Herzegovine/Botswana/Bratislava/Brazil/Bulgarie/Cambodia/Cameroon/Canada - 3G/Canada, quad band mobile required/",
                  "txt2": "Bosnia Herzegovine/Botswana/Bratislava/Brazil/Bulgarie/Cambodia/Cameroon/Canada - 3G/Canada, quad band mobile required",
                  "txt3": "Bosnia Herzegovine/Botswana/Bratislava/Brazil/Bulgarie/Cambodia/Cameroon/Canada - 3G/Canada, quad band mobile required/",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-4-13300"
                }
              }
            },
            "1617": {
              "id": "1-0-3-1617",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "7. Moramanga",
                  "txt2": "7. Moramanga",
                  "txt3": "7. Moramanga",
                  "key": 7,
                  "source": "",
                  "nextmenuid": "1-0-4-16177"
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "8. Tamatave",
                  "txt2": "8. Tamatave",
                  "txt3": "8. Tamatave",
                  "key": 8,
                  "source": "",
                  "nextmenuid": "1-0-4-16178"
                },
                "3": {
                  "sequence": 3,
                  "type": "static",
                  "txt1": "9. Tulear\n#. Previous Menu",
                  "txt2": "9. Tulear\n#. Raha hiverina @ menu teo aloha",
                  "txt3": "9. Tulear\n#. Menu Precedent",
                  "key": 9,
                  "source": "",
                  "nextmenuid": "1-0-4-16179"
                }
              }
            },
            "1761": {
              "id": "1-0-3-1761",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "To check your Tier Level, Send : ZA by SMS to 466. Thank you",
                  "txt2": "Mba hahafantaranao ny sokajy misy anao dia alefa SMS any @ 466 ny hoe : ZA. Misaotra Tompoko",
                  "txt3": "Pour connaitre votre categorie actuelle, envoyez gratuitement au 466 le mot : ZA. Merci",
                  "key": "",
                  "source": ""
                }
              }
            },
            "1762": {
              "id": "1-0-3-1762",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "To check the list of products available, send KADO by SMS to 466. Thank you",
                  "txt2": "Ahafantaranao ny lisitry ny fanomezana azo isafidianana dia alefaso SMS any @ 466 ny hoe: KADO . Misaotra Tompoko",
                  "txt3": "Pour avoir la liste des produits, envoyez gratuitement au 466 le mot: KADO. Merci",
                  "key": "",
                  "source": ""
                }
              }
            },
            "1763": {
              "id": "1-0-3-1763",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "For PIN change, send: CODE /space/ Old password /space/ New password by SMS to 466",
                  "txt2": "Raha hanova teny miafina, alefaso SMS any @ 466 ny hoe : CODE /elanelana/ Teny miafina teo aloha /elanelana / Teny miafina vaovao",
                  "txt3": "Pour modifier votre mot de passe, envoyez par SMS au 466 le mot : CODE /espace/ Votre ancien mot de passe /espace/ Votre nouveau mot de passe",
                  "key": "",
                  "source": ""
                }
              }
            },
            "1437": {
              "id": "1-0-3-1437",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "7. Moramanga",
                  "txt2": "7. Moramanga",
                  "txt3": "7. Moramanga",
                  "key": "7",
                  "source": "",
                  "nextmenuid": "1-0-4-14377"
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "8. Tamatave",
                  "txt2": "8. Tamatave",
                  "txt3": "8. Tamatave",
                  "key": "8",
                  "source": "",
                  "nextmenuid": "1-0-4-14378"
                },
                "3": {
                  "sequence": 3,
                  "type": "static",
                  "txt1": "9. Tulear\n#. Previous Menu",
                  "txt2": "9. Tulear\n#. Raha hiverina @ menu teo aloha",
                  "txt3": "9. Tulear\n#. Menu Precedent",
                  "key": "9",
                  "source": "",
                  "nextmenuid": "1-0-4-14379"
                }
              }
            },
            "1441": {
              "id": "1-0-3-1441",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "300 a 49999: 0Ar  /50 001 a 100 000: 800Ar /",
                  "txt2": "300 a 49999: 0Ar /50 001 a 100 000: 800Ar /",
                  "txt3": "300 a 49999: 0 Ar /50 001 a 100 000: 800Ar /",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0- Next Page\n#- Previous Menu",
                  "txt2": "0- Tohiny\n#- Raha hiverina",
                  "txt3": "0- Suivant\n#- Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-4-14412"
                }
              }
            },
            "1442": {
              "id": "1-0-3-1442",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "300 a 5000: 150Ar /5001 a 10 000: 300Ar /10 001 a 25 000: 700Ar /25 001 a 50 000: 1 500Ar /50 001 a 100 000: 1 600Ar",
                  "txt2": "300 a 5000: 150Ar /5001 a 10 000: 300Ar /10 001 a 25 000: 700Ar /25 001 a 50 000: 1 500Ar /50 001 a 100 000: 1 600Ar /",
                  "txt3": "300 a 5000: 150Ar /5001 a 10 000: 300Ar /10 001 a 25 000: 700Ar /25 001 a 50 000: 1 500Ar /50 001 a 100 000: 1 600Ar",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0- Next Page\n#- Previous Menu",
                  "txt2": "0- Tohiny\n#- Raha hiverina",
                  "txt3": "0- Suivant\n#- Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-4-14422"
                }
              }
            },
            "1443": {
              "id": "1-0-3-1443",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "300 a 5000: 0Ar /5001 a 10 000: 1000Ar /10 001 a 20 000: 1 500Ar /20 001 a 25 000: 1 800Ar /25 001 a 50 000: 3 500Ar /50 001 a 100 000: 4 500Ar /",
                  "txt2": "300 a 5000: 0Ar /5001 a 10 000: 1000Ar /10 001 a 20 000: 1 500Ar /20 001 a 25 000: 1 800Ar /25 001 a 50 000: 3 500Ar /50 001 a 100 000: 4 500Ar /",
                  "txt3": "300 a 5000: 0Ar /5001 a 10 000: 1000Ar /10 001 a 20 000: 1 500Ar /20 001 a 25 000: 1 800Ar /25 001 a 50 000: 3 500Ar /50 001 a 100 000: 4 500Ar /",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0- Next Page\n#- Previous Menu",
                  "txt2": "0- Tohiny\n#- Raha hiverina",
                  "txt3": "0- Suivant\n#- Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-4-14432"
                }
              }
            }
          }
        },
        "5": {
          "id": 0,
          "menus": {
            "11661": {
              "id": "1-0-4-11661",
              "type": "dynamic",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "dynamic",
                  "txt1": "",
                  "txt2": "",
                  "txt3": "",
                  "key": "",
                  "source": "http://127.0.0.1:9098/process?msisdn=$msisdn&action=increasecreditlimit&sessionId=$sessionId&language=$language&amount=5000"
                }
              }
            },
            "11662": {
              "id": "1-0-4-11662",
              "type": "dynamic",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "dynamic",
                  "txt1": "",
                  "txt2": "",
                  "txt3": "",
                  "key": "",
                  "source": "http://127.0.0.1:9098/process?msisdn=$msisdn&action=increasecreditlimit&sessionId=$sessionId&language=$language&amount=10000"
                }
              }
            },
            "11663": {
              "id": "1-0-4-11663",
              "type": "dynamic",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "dynamic",
                  "txt1": "",
                  "txt2": "",
                  "txt3": "",
                  "key": "",
                  "source": "http://127.0.0.1:9098/process?msisdn=$msisdn&action=increasecreditlimit&sessionId=$sessionId&language=$language&amount=20000"
                }
              }
            },
            "143600": {
              "id": "1-0-5-143600",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "AMAR STORE Majunga : En face magasin luna / MOUSSA BAPU Tsararanoanosikely: En face glace bolo /",
                  "txt2": "AMAR STORE Majunga : En face magasin luna / MOUSSA BAPU Tsararanoanosikely: En face glace bolo /",
                  "txt3": "AMAR STORE Majunga : En face magasin luna / MOUSSA BAPU Tsararanoanosikely: En face glace bolo /",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-6-1436000"
                }
              }
            },
            "133000": {
              "id": "1-0-5-133000",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Dominican Republic/Ecuador/Egypt/El Salvador/Estonia/Ethiopia/Finland/France/French Indies/Gabon/Gambia/Georgia/Germany/Ghana/",
                  "txt2": "Dominican Republic/Ecuador/Egypt/El Salvador/Estonia/Ethiopia/Finland/France/French Indies/Gabon/Gambia/Georgia/Germany/Ghana/",
                  "txt3": "Dominican Republic/Ecuador/Egypt/El Salvador/Estonia/Ethiopia/Finland/France/French Indies/Gabon/Gambia/Georgia/Germany/Ghana/",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-6-1330000"
                }
              }
            },
            "143100": {
              "id": "1-0-5-143100",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "LE GLACIER Analakely:Enceinte SICAM/ TSINJO Ouest Ambohijanahary:En face Firaisana/SHOP MANIA rasalama En face college Rasalama/",
                  "txt2": "LE GLACIER Analakely:Enceinte SICAM/ TSINJO Ouest Ambohijanahary:En face Firaisana/SHOP MANIA rasalama En face college Rasalama/",
                  "txt3": "LE GLACIER Analakely:Enceinte SICAM/ TSINJO Ouest Ambohijanahary:En face Firaisana/SHOP MANIA rasalama En face college Rasalama/",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-6-1431000"
                }
              }
            },
            "143200": {
              "id": "1-0-5-143200",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "PHOTO EXPRESS Fety Ambatolampy: En face Mpivarokazo / KIOSK HARILANTO Andranomanelatra : En face bureau Fokontany /",
                  "txt2": "PHOTO EXPRESS Fety Ambatolampy: En face Mpivarokazo / KIOSK HARILANTO Andranomanelatra : En face bureau Fokontany/",
                  "txt3": "PHOTO EXPRESS Fety Ambatolampy: En face Mpivarokazo / KIOSK HARILANTO Andranomanelatra : En face bureau Fokontany /",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-6-1432000"
                }
              }
            },
            "143300": {
              "id": "1-0-5-143300",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Station TOTAL Ambilobe / SYMPHOROSE  Diego : A cote college ABC / RAVELOSON OLIVIENNE Ambilobe : enceinte SIRAMA /",
                  "txt2": "Station TOTAL Ambilobe / SYMPHOROSE  Diego : A cote college ABC / RAVELOSON OLIVIENNE Ambilobe : enceinte SIRAMA /",
                  "txt3": "Station TOTAL Ambilobe / SYMPHOROSE  Diego : A cote college ABC / RAVELOSON OLIVIENNE Ambilobe : enceinte SIRAMA /",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-6-1433000"
                }
              }
            },
            "143400": {
              "id": "1-0-5-143400",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "LE GRILLON Mananjary : En face BFV / PAOSITRA MALAGASY / MICROCRED/",
                  "txt2": "LE GRILLON Mananjary : En face BFV / PAOSITRA MALAGASY / MICROCRED/",
                  "txt3": "LE GRILLON Mananjary : En face BFV / PAOSITRA MALAGASY / MICROCRED/",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-6-1434000"
                }
              }
            },
            "143500": {
              "id": "1-0-5-143500",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "SHOP AIRTEL Esokaka : En face marche pres SHELL / HAJA Taolagnaro : EN face SICAM / LAFA SERVICE Bazary BE : En face SHOP /",
                  "txt2": "SHOP AIRTEL Esokaka : En face marche pres SHELL / HAJA Taolagnaro : EN face SICAM / LAFA SERVICE Bazary BE : En face SHOP /",
                  "txt3": "SHOP AIRTEL Esokaka : En face marche pres SHELL / HAJA Taolagnaro : EN face SICAM / LAFA SERVICE Bazary BE : En face SHOP /",
                  "key": "",
                  "source": ""
                }
              }
            },
            "143080": {
              "id": "1-0-5-143080",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "SARIAKA Mangarano:Vers Universite/ STEECOM Tanmbao V en face epicerie boeing 747 /MALAGASY INFO Anjoma:En face ecole notre dame/",
                  "txt2": "SARIAKA Mangarano:Vers Universite/ STEECOM Tanmbao V en face epicerie boeing 747 /MALAGASY INFO Anjoma:En face ecole notre dame",
                  "txt3": "SARIAKA Mangarano:Vers Universite/ STEECOM Tanmbao V en face epicerie boeing 747 /MALAGASY INFO Anjoma:En face ecole notre dame/",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-6-1430800"
                }
              }
            },
            "143790": {
              "id": "1-0-5-143790",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "BILLY Tanambao I : En face Bonne Soupe / EPI LOVA Ankisirasira Nord : EN face Bonne Soupe / SERGE Andakabe /",
                  "txt2": "BILLY Tanambao I : En face Bonne Soupe / EPI LOVA Ankisirasira Nord : EN face Bonne Soupe / SERGE Andakabe /",
                  "txt3": "BILLY Tanambao I : En face Bonne Soupe / EPI LOVA Ankisirasira Nord : EN face Bonne Soupe / SERGE Andakabe /",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-6-1437900"
                }
              }
            },
            "144122": {
              "id": "1-0-5-144122",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "2 000 001 a 3 000 000: 7 000Ar /3 000 001 a 4 000 000: 9 000Ar /4 000 001 a 5 000 000: 10000Ar/",
                  "txt2": "2 000 001 a 3 000 000: 7 000Ar /3 000 001 a 4 000 000: 9 000Ar /4 000 001 a 5 000 000: 10000Ar/",
                  "txt3": "2 000 001 a 3 000 000: 7 000Ar /3 000 001 a 4 000 000: 9 000Ar /4 000 001 a 5 000 000: 10 000Ar/",
                  "key": "",
                  "source": ""
                }
              }
            },
            "144222": {
              "id": "1-0-5-144222",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "2 000 001 a 3 000 000: 13 000Ar /3 000 001 a 4 000 000: 16 000Ar /4 000 001 a 5 000 000: 19 000Ar  /",
                  "txt2": "2 000 001 a 3 000 000: 13 000Ar /3 000 001 a 4 000 000: 16 000Ar /4 000 001 a 5 000 000: 19 000Ar  / ",
                  "txt3": "2 000 001 a 3 000 000: 13 000Ar /3 000 001 a 4 000 000: 16 000Ar /4 000 001 a 5 000 000: 19 000Ar/",
                  "key": "",
                  "source": ""
                }
              }
            },
            "144322": {
              "id": "1-0-5-144322",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "2 000 001 a 3 000 000: 37 500Ar /3 000 001 a 4 000 000: 47 500Ar /4 000 001 a 5 000 000: 55 000Ar  /",
                  "txt2": "2 000 001 a 3 000 000: 37 500Ar /3 000 001 a 4 000 000: 47 500Ar /4 000 001 a 5 000 000: 55 000Ar  /",
                  "txt3": "2 000 001 a 3 000 000: 37 500Ar /3 000 001 a 4 000 000: 47 500Ar /4 000 001 a 5 000 000: 55 000Ar  /",
                  "key": "",
                  "source": ""
                }
              }
            },
            "1330000": {
              "id": "1-0-6-1330000",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Gibraltar/Greece/Greenland/Grenada/Guatemala/Guinea/Guinea Bissau/Honduras/Hong Kong/Hungary/Iceland/India/India - Chennai/India - Delhi/",
                  "txt2": "Gibraltar/Greece/Greenland/Grenada/Guatemala/Guinea/Guinea Bissau/Honduras/Hong Kong/Hungary/Iceland/India/India-Chennai/India-Delhi/",
                  "txt3": "Gibraltar/Greece/Greenland/Grenada/Guatemala/Guinea/Guinea Bissau/Honduras/Hong Kong/Hungary/Iceland/India/India - Chennai/India - Delhi/",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-7-13300000"
                }
              }
            },
            "1431000": {
              "id": "1-0-6-1431000",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "BUROSCO behoririka:Kiosque Taxi Phone Lac Behoririka/ KIOSQUE VALISOA 2 ambodivona : En face WC Public/",
                  "txt2": "BUROSCO behoririka:Kiosque Taxi Phone Lac Behoririka/ KIOSQUE VALISOA 2 ambodivona : En face WC Public/",
                  "txt3": "BUROSCO behoririka:Kiosque Taxi Phone Lac Behoririka/ KIOSQUE VALISOA 2 ambodivona : En face WC Public/",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-7-14310000"
                }
              }
            },
            "15": {
              "id": "1-0-6-1433000",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "FELICITE Ambanja : En face clinique / PAOSITRA MALAGASY / MICROCRED/",
                  "txt2": "FELICITE Ambanja : En face clinique / PAOSITRA MALAGASY / MICROCRED/",
                  "txt3": "FELICITE Ambanja : En face clinique / PAOSITRA MALAGASY / MICROCRED/",
                  "key": "",
                  "source": ""
                }
              }
            },
            "16": {
              "id": "1-0-6-1432000",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "TAXI PHONE Fanja Antsirabe:Pres Tribunal/ PAOSITRA MALAGASY/MICROCRED/Airtel Shop SOA SERVICE:Ny Havana Immeuble La Planete,1ere etage/",
                  "txt2": "TAXI PHONE Fanja Antsirabe:Pres Tribunal/ PAOSITRA MALAGASY/MICROCRED/Airtel Shop SOA SERVICE:Ny Havana Immeuble La Planete,1ere etage/",
                  "txt3": "TAXI PHONE Fanja Antsirabe:Pres Tribunal/ PAOSITRA MALAGASY/MICROCRED/Airtel Shop SOA SERVICE:Ny Havana Immeuble La Planete,1ere etage/",
                  "key": "",
                  "source": ""
                }
              }
            },
            "17": {
              "id": "1-0-6-1434000",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel Shop Express ANNICK SERVICE: Lot II P 35 Tambohobe Fianarantsoa ville/",
                  "txt2": "Airtel Shop Express ANNICK SERVICE: Lot II P 35 Tambohobe Fianarantsoa ville/",
                  "txt3": "Airtel Shop Express ANNICK SERVICE: Lot II P 35 Tambohobe Fianarantsoa ville",
                  "key": "",
                  "source": ""
                }
              }
            },
            "1436000": {
              "id": "1-0-6-1436000",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "MINI BOUTIQUE Antanimalandy : 30m avant PAOSITRA MALAGASY / TOMBOZARA ANDRE Mandritsara : A cote espace G / PAOSITRA MALAGASY / MICROCRED/",
                  "txt2": "MINI BOUTIQUE Antanimalandy : 30m avant PAOSITRA MALAGASY / TOMBOZARA ANDRE Mandritsara : A cote espace G / PAOSITRA MALAGASY / MICROCRED/",
                  "txt3": "MINI BOUTIQUE Antanimalandy : 30m avant PAOSITRA MALAGASY / TOMBOZARA ANDRE Mandritsara : A cote espace G / PAOSITRA MALAGASY / MICROCRED/",
                  "key": "",
                  "source": ""
                }
              }
            },
            "1430800": {
              "id": "1-0-6-1430800",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "DERECK mobil Bazary be :Face maison lux/SHOP Mananara:Bazar Mananara/ SHOP ambatondrazaka:Route de la gare (madio tsifafana)/",
                  "txt2": "DERECK mobil Bazary be :Face maison lux/SHOP Mananara:Bazar Mananara/ SHOP ambatondrazaka:Route de la gare (madio tsifafana)/",
                  "txt3": "DERECK mobil Bazary be :Face maison lux/SHOP Mananara:Bazar Mananara/ SHOP ambatondrazaka:Route de la gare (madio tsifafana)/",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-7-14308000"
                }
              }
            },
            "1437900": {
              "id": "1-0-6-1437900",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "ROGER Ankilivalo Mahabo:Pres Lovasoa hotel/Syncro Bazar Be pres librairie saint paul/HERINIAINA Sanfil TSF SUD:pres magasin alpha/",
                  "txt2": "ROGER Ankilivalo Mahabo:Pres Lovasoa hotel/Syncro Bazar Be pres librairie saint paul/HERINIAINA Sanfil TSF SUD:pres magasin alpha/",
                  "txt3": "ROGER Ankilivalo Mahabo:Pres Lovasoa hotel/Syncro Bazar Be pres librairie saint paul/HERINIAINA Sanfil TSF SUD:pres magasin alpha/",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-7-14379000"
                }
              }
            },
            "1611000": {
              "id": "1-0-6-1611000",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel SHOP Express Mahazo Ankadindramamy / Airtel Shop Express Jumbo Score : Enceinte Jumbo Score ANKORONDRANO /",
                  "txt2": "Airtel SHOP Express Mahazo Ankadindramamy / Airtel Shop Express Jumbo Score : Enceinte Jumbo Score ANKORONDRANO /",
                  "txt3": "Airtel SHOP Express Mahazo Ankadindramamy / Airtel Shop Express Jumbo Score : Enceinte Jumbo Score ANKORONDRANO / ",
                  "key": "",
                  "source": ""
                }
              }
            },
            "1621000": {
              "id": "1-0-6-1621000",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel SHOP Express Mahazo Ankadindramamy / Airtel Shop Express Jumbo Score : Enceinte Jumbo Score ANKORONDRANO / ",
                  "txt2": "Airtel SHOP Express Mahazo Ankadindramamy / Airtel Shop Express Jumbo Score :  Enceinte Jumbo Score ANKORONDRANO / ",
                  "txt3": "Airtel SHOP Express Mahazo Ankadindramamy / Airtel Shop Express Jumbo Score : Enceinte Jumbo Score ANKORONDRANO /",
                  "key": "",
                  "source": ""
                }
              }
            },
            "13300000": {
              "id": "1-0-7-13300000",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Haryana/India - Kerala/India - Mumbai/India - Punjab/India - Tamil Nadu/India - Uttar Pradesh/India Karnataka/Iran/Iraq/",
                  "txt2": "Haryana/India - Kerala/India - Mumbai/India - Punjab/India - Tamil Nadu/India - Uttar Pradesh/India Karnataka/Iran/Iraq/",
                  "txt3": "Haryana/India - Kerala/India - Mumbai/India - Punjab/India - Tamil Nadu/India - Uttar Pradesh/India Karnataka/Iran/Iraq/",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-8-133000000"
                }
              }
            },
            "12": {
              "id": "1-0-7-14310000",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "LIVE SERVICE Cenam : En face BNI / CYBER CITY ampefiloha : A cote Auto Piece 3 chemins / PAOSITRA MALAGASY / MICROCRED /",
                  "txt2": "LIVE SERVICE Cenam : En face BNI / CYBER CITY ampefiloha : A cote Auto Piece 3 chemins / PAOSITRA MALAGASY / MICROCRED /",
                  "txt3": "LIVE SERVICE Cenam : En face BNI / CYBER CITY ampefiloha : A cote Auto Piece 3 chemins / PAOSITRA MALAGASY / MICROCRED /",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-8-143100000"
                }
              }
            },
            "110": {
              "id": "1-0-7-14308000",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "SHOP Mahanoro : Ampampanambo / NEREA bazar Vatomandry / SANDY Brickaville apres le Pont / CRISTAL com : Bazar Fenerive est /",
                  "txt2": "SHOP Mahanoro : Ampampanambo / NEREA bazar Vatomandry / SANDY Brickaville apres le Pont / CRISTAL com : Bazar Fenerive est /",
                  "txt3": "SHOP Mahanoro : Ampampanambo / NEREA bazar Vatomandry / SANDY Brickaville apres le Pont / CRISTAL com : Bazar Fenerive est /",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-8-143080000"
                }
              }
            },
            "14379000": {
              "id": "1-0-7-14379000",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "VAL MOTEL Isoanala/KIOSK sans FIU:En face station shell / HOTEL VATSY A Betroka Centre / HAJA Betroka : En face Informatika Service /",
                  "txt2": "VAL MOTEL Isoanala/KIOSK sans FIU:En face station shell / HOTEL VATSY A Betroka Centre / HAJA Betroka : En face Informatika Service /",
                  "txt3": "VAL MOTEL Isoanala/KIOSK sans FIU:En face station shell / HOTEL VATSY A Betroka Centre / HAJA Betroka : En face Informatika Service /",
                  "key": "",
                  "source": ""
                }
              }
            },
            "133000000": {
              "id": "1-0-8-133000000",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Ireland/Israel/Italy/Ivory Coast/Jamaica/Japan, 3G handset required//Kenya/Korea, 3G handset required/Kuwait/La Réunion/",
                  "txt2": "Ireland/Israel/Italy/Ivory Coast/Jamaica/Japan, 3G handset required//Kenya/Korea, 3G handset required/Kuwait/La Réunion/",
                  "txt3": "Ireland/Israel/Italy/Ivory Coast/Jamaica/Japan, 3G handset required//Kenya/Korea, 3G handset required/Kuwait/La Réunion/",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-9-1330000000"
                }
              }
            },
            "143100000": {
              "id": "1-0-8-143100000",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "SHOP AMPAHATEZA 67ha sud:Arret poste 67Ha,100m Poste vers Cenam/KIOSK Andavamanba:25m du JIRAMA/LA CITY Ivandry /",
                  "txt2": "SHOP AMPAHATEZA 67ha sud:Arret poste 67Ha,100m Poste vers Cenam/KIOSK Andavamanba:25m du JIRAMA/LA CITY Ivandry /",
                  "txt3": "SHOP AMPAHATEZA 67ha sud:Arret poste 67Ha,100m Poste vers Cenam/KIOSK Andavamanba:25m du JIRAMA/LA CITY Ivandry /",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-9-1431000000"
                }
              }
            },
            "111": {
              "id": "1-0-8-143080000",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Airtel  Shop Express 033MOBILE : B2 Cite Procopse, Tanambao 5 (en face station shell, gare routiere)/",
                  "txt2": "Airtel  Shop Express 033MOBILE : B2 Cite Procopse, Tanambao 5 (en face station shell, gare routiere)/",
                  "txt3": "Airtel  Shop Express 033MOBILE : B2 Cite Procopse, Tanambao 5 (en face station shell, gare routiere)/",
                  "key": "",
                  "source": ""
                }
              }
            },
            "4": {
              "id": "1-0-9-1330000000",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Latvia/Lebanon/Lesotho/Liberia/Libya//Macau/Macedonia/Malawi/Malaysia/Maldives/Mali/Malta/Mauritania/Mauritius/Mayotte/Mexico/",
                  "txt2": "Latvia/Lebanon/Lesotho/Liberia/Libya//Macau/Macedonia/Malawi/Malaysia/Maldives/Mali/Malta/Mauritania/Mauritius/Mayotte/Mexico/",
                  "txt3": "Latvia/Lebanon/Lesotho/Liberia/Libya//Macau/Macedonia/Malawi/Malaysia/Maldives/Mali/Malta/Mauritania/Mauritius/Mayotte/Mexico/",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-10-13300000000"
                }
              }
            },
            "1431000000": {
              "id": "1-0-9-1431000000",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "SHOP LA MATRICE Itaosy : 10m avant PAOSITRA MALAGASY / FUN TECHNO Ambohibao : En face Pharmacie Ambohibao vers Talatamaty /",
                  "txt2": "SHOP LA MATRICE Itaosy : 10m avant PAOSITRA MALAGASY / FUN TECHNO Ambohibao : En face Pharmacie Ambohibao vers Talatamaty /",
                  "txt3": "SHOP LA MATRICE Itaosy : 10m avant PAOSITRA MALAGASY / FUN TECHNO Ambohibao : En face Pharmacie Ambohibao vers Talatamaty /",
                  "key": "",
                  "source": ""
                }
              }
            },
            "1300000000": {
              "id": "1-0-10-13300000000",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Montserrat/Morocco/Mozambique/Namibia/Netherlands/New Zealand/Niger/Nigeria/Norway/Oman/Pakistan/Palestine/Papua New Guinea/",
                  "txt2": "Montserrat/Morocco/Mozambique/Namibia/Netherlands/New Zealand/Niger/Nigeria/Norway/Oman/Pakistan/Palestine/Papua New Guinea/",
                  "txt3": "Montserrat/Morocco/Mozambique/Namibia/Netherlands/New Zealand/Niger/Nigeria/Norway/Oman/Pakistan/Palestine/Papua New Guinea/",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-11-133000000000"
                }
              }
            },
            "6": {
              "id": "1-0-11-133000000000",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Paraguay/Philippines/Poland/Portugal/Qatar/Rwanda/Saudi Arabia/Senegal/Serbia & Montenegro/Seychelles/Sierra Leone/Singapore/",
                  "txt2": "Paraguay/Philippines/Poland/Portugal/Qatar/Rwanda/Saudi Arabia/Senegal/Serbia & Montenegro/Seychelles/Sierra Leone/Singapore/",
                  "txt3": "Paraguay/Philippines/Poland/Portugal/Qatar/Rwanda/Saudi Arabia/Senegal/Serbia & Montenegro/Seychelles/Sierra Leone/Singapore/",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-12-1330000000000"
                }
              }
            },
            "7": {
              "id": "1-0-12-1330000000000",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Slovenia/South Africa/Spain/Sri Lanka/St Kitts & Nevis/St. Lucia/St. Vincent./Sudan/Suriname/Swaziland/Sweden/Tanzania/",
                  "txt2": "Slovenia/South Africa/Spain/Sri Lanka/St Kitts & Nevis/St. Lucia/St. Vincent./Sudan/Suriname/Swaziland/Sweden/Tanzania/",
                  "txt3": "Slovenia/South Africa/Spain/Sri Lanka/St Kitts & Nevis/St. Lucia/St. Vincent./Sudan/Suriname/Swaziland/Sweden/Tanzania/",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-13-13300000000000"
                }
              }
            },
            "8": {
              "id": "1-0-13-13300000000000",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Tchad/Thailand/Togo/Tunisiana/Turkey/Turks and Caicos/U.A.E/Uganda/Ukraine/USA/Uzbekistan/Vietnam/W Indies/Yemen/Zambia/Zimbabwe/",
                  "txt2": "Tchad/Thailand/Togo/Tunisiana/Turkey/Turks and Caicos/U.A.E/Uganda/Ukraine/USA/Uzbekistan/Vietnam/W Indies/Yemen/Zambia/Zimbabwe/",
                  "txt3": "Tchad/Thailand/Togo/Tunisiana/Turkey/Turks and Caicos/U.A.E/Uganda/Ukraine/USA/Uzbekistan/Vietnam/W Indies/Yemen/Zambia/Zimbabwe/",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-14-133000000000000"
                }
              }
            },
            "9": {
              "id": "1-0-14-133000000000000",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 0,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "Indonesia/Jersey/Jordany/Kazakhstan/Liechtenstein/Luxembourg/Mongolia/Roumania//Switzerland/Syria/Taiwan/U Kingdom/Uruguay/",
                  "txt2": "Indonesia/Jersey/Jordany/Kazakhstan/Liechtenstein/Luxembourg/Mongolia/Roumania//Switzerland/Syria/Taiwan/U Kingdom/Uruguay/",
                  "txt3": "Indonesia/Jersey/Jordany/Kazakhstan/Liechtenstein/Luxembourg/Mongolia/Roumania//Switzerland/Syria/Taiwan/U Kingdom/Uruguay/",
                  "key": "",
                  "source": ""
                },
                "2": {
                  "sequence": 2,
                  "type": "static",
                  "txt1": "0. Next Page\n#. Previous Menu",
                  "txt2": "0. Tohiny\n#. Raha hiverina",
                  "txt3": "0. Suivant\n#. Menu Precedent",
                  "key": "0",
                  "source": "",
                  "nextmenuid": "1-0-15-1330000000000000"
                }
              }
            },
            "10": {
              "id": "1-0-15-1330000000000000",
              "type": "static",
              "title": "",
              "footer": "",
              "checkpoint": 0,
              "response": "key",
              "services": "",
              "package": "",
              "parameter": "",
              "leaf": 1,
              "entries": {
                "1": {
                  "sequence": 1,
                  "type": "static",
                  "txt1": "India /Russia/Australia/Austria/Azerbaijan/Burkina Faso/Burundi/BVI/Cyprus/Czech/Denmark/Equatorial Guinea/",
                  "txt2": "India /Russia/Australia/Austria/Azerbaijan/Burkina Faso/Burundi/BVI/Cyprus/Czech/Denmark/Equatorial Guinea/",
                  "txt3": "India /Russia/Australia/Austria/Azerbaijan/Burkina Faso/Burundi/BVI/Cyprus/Czech/Denmark/Equatorial Guinea/",
                  "key": "",
                  "source": ""
                }
              }
            }
          }
        }
      }
    }
  }
}
