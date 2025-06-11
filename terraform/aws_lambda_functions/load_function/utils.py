from botocore.exceptions import ClientError
import polars as pl
import boto3
import json



def get_db_secret(client=None, secretname="toteys_db_credentials"):

    secret_name = secretname
    region_name = "eu-west-2"

    # Create a Secrets Manager client
    if not client:
        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response["SecretString"]
    return json.loads(secret)


def upload_file(client, file, bucket_name, key):
    """Provides packaged error handling and response for client.putobject function

    Args:
        client (client_object): aws s3 client
        file (bytes|string): bytes object to be uploaded or name of file
        bucket_name (string): name of bucket
        key (string): key of item in bucket

    Returns:
        Dict: dictionary with key Status (containing Success or Failed) and Code containing response code
    """
    try:
        response = client.put_object(Body=file, Bucket=bucket_name, Key=key)
        response = {
            "status": "Success",
            "code": response["ResponseMetadata"]["HTTPStatusCode"],
        }
    except ClientError as e:
        response = {"status": "Failed", "code": e.response["Error"]["Code"]}

    return response


def download_file(client, bucket_name, key):
    """provides Error handling and response for get_object

    Args:
        client (client_object): AWS s3 client
        bucket (string): name of bucket to be retrieved from
        key (string): key of object to be retrieved

    Returns:
        dict: dictionary containing keys 'body' containing streaming body ) 'status' (containing Failed or Success) and 'code'(containing the status code)
    """
    # TODO turn body response into file object response possibly
    try:
        response = client.get_object(Bucket=bucket_name, Key=key)
        response = {
            "body": response["Body"],
            "status": "Success",
            "code": response["ResponseMetadata"]["HTTPStatusCode"],
        }

    except ClientError as e:
        response = {"status": "Failed", "code": e.response["Error"]["Code"]}

    return response


def currency_code_converter(currency_code):
    currency_dict = {
        "AFN": {"Currency": "Afghani"},
        "AFA": {"Currency": "Afghani"},
        "ALL": {"Currency": "Lek"},
        "ALK": {"Currency": "Old Lek"},
        "DZD": {"Currency": "Algerian Dinar"},
        "USD": {"Currency": "US Dollar"},
        "EUR": {"Currency": "Euro"},
        "ADP": {"Currency": "Andorran Peseta"},
        "ESP": {"Currency": "Spanish Peseta"},
        "FRF": {"Currency": "French Franc"},
        "AOA": {"Currency": "Kwanza"},
        "AOK": {"Currency": "Kwanza"},
        "AON": {"Currency": "New Kwanza"},
        "AOR": {"Currency": "Kwanza Reajustado"},
        "XCD": {"Currency": "East Caribbean Dollar"},
        "null": {"Currency": "No universal currency"},
        "ARS": {"Currency": "Argentine Peso"},
        "ARA": {"Currency": "Austral"},
        "ARP": {"Currency": "Peso Argentino"},
        "ARY": {"Currency": "Peso"},
        "AMD": {"Currency": "Armenian Dram"},
        "RUR": {"Currency": "Russian Ruble"},
        "AWG": {"Currency": "Aruban Florin"},
        "AUD": {"Currency": "Australian Dollar"},
        "ATS": {"Currency": "Schilling"},
        "AZN": {"Currency": "Azerbaijan Manat"},
        "AYM": {"Currency": "Azerbaijan Manat"},
        "AZM": {"Currency": "Azerbaijanian Manat"},
        "BSD": {"Currency": "Bahamian Dollar"},
        "BHD": {"Currency": "Bahraini Dinar"},
        "BDT": {"Currency": "Taka"},
        "BBD": {"Currency": "Barbados Dollar"},
        "BYN": {"Currency": "Belarusian Ruble"},
        "BYB": {"Currency": "Belarusian Ruble"},
        "BYR": {"Currency": "Belarusian Ruble"},
        "BEC": {"Currency": "Convertible Franc"},
        "BEF": {"Currency": "Belgian Franc"},
        "BEL": {"Currency": "Financial Franc"},
        "BZD": {"Currency": "Belize Dollar"},
        "XOF": {"Currency": "CFA Franc BCEAO"},
        "BMD": {"Currency": "Bermudian Dollar"},
        "INR": {"Currency": "Indian Rupee"},
        "BTN": {"Currency": "Ngultrum"},
        "BOP": {"Currency": "Peso boliviano"},
        "BOB": {"Currency": "Boliviano"},
        "BOV": {"Currency": "Mvdol"},
        "BAM": {"Currency": "Convertible Mark"},
        "BAD": {"Currency": "Dinar"},
        "BWP": {"Currency": "Pula"},
        "NOK": {"Currency": "Norwegian Krone"},
        "BRL": {"Currency": "Brazilian Real"},
        "BRB": {"Currency": "Cruzeiro"},
        "BRC": {"Currency": "Cruzado"},
        "BRE": {"Currency": "Cruzeiro"},
        "BRN": {"Currency": "New Cruzado"},
        "BRR": {"Currency": "Cruzeiro Real"},
        "BND": {"Currency": "Brunei Dollar"},
        "BGN": {"Currency": "Bulgarian Lev"},
        "BGJ": {"Currency": "Lev A/52"},
        "BGK": {"Currency": "Lev A/62"},
        "BGL": {"Currency": "Lev"},
        "BUK": {"Currency": "Kyat"},
        "BIF": {"Currency": "Burundi Franc"},
        "CVE": {"Currency": "Cabo Verde Escudo"},
        "KHR": {"Currency": "Riel"},
        "XAF": {"Currency": "CFA Franc BEAC"},
        "CAD": {"Currency": "Canadian Dollar"},
        "KYD": {"Currency": "Cayman Islands Dollar"},
        "CLP": {"Currency": "Chilean Peso"},
        "CLF": {"Currency": "Unidad de Fomento"},
        "CNY": {"Currency": "Yuan Renminbi"},
        "COP": {"Currency": "Colombian Peso"},
        "COU": {"Currency": "Unidad de Valor Real"},
        "KMF": {"Currency": "Comorian Franc"},
        "CDF": {"Currency": "Congolese Franc"},
        "NZD": {"Currency": "New Zealand Dollar"},
        "CRC": {"Currency": "Costa Rican Colon"},
        "HRD": {"Currency": "Croatian Dinar"},
        "HRK": {"Currency": "Kuna"},
        "CUP": {"Currency": "Cuban Peso"},
        "CUC": {"Currency": "Peso Convertible"},
        "XCG": {"Currency": "Caribbean Guilder"},
        "ANG": {"Currency": "Netherlands Antillean Guilder"},
        "CYP": {"Currency": "Cyprus Pound"},
        "CZK": {"Currency": "Czech Koruna"},
        "CSJ": {"Currency": "Krona A/53"},
        "CSK": {"Currency": "Koruna"},
        "DKK": {"Currency": "Danish Krone"},
        "DJF": {"Currency": "Djibouti Franc"},
        "DOP": {"Currency": "Dominican Peso"},
        "ECS": {"Currency": "Sucre"},
        "ECV": {"Currency": "Unidad de Valor Constante (UVC)"},
        "EGP": {"Currency": "Egyptian Pound"},
        "SVC": {"Currency": "El Salvador Colon"},
        "GQE": {"Currency": "Ekwele"},
        "ERN": {"Currency": "Nakfa"},
        "EEK": {"Currency": "Kroon"},
        "SZL": {"Currency": "Lilangeni"},
        "ETB": {"Currency": "Ethiopian Birr"},
        "XEU": {"Currency": "European Currency Unit (E.C.U)"},
        "FKP": {"Currency": "Falkland Islands Pound"},
        "FJD": {"Currency": "Fiji Dollar"},
        "FIM": {"Currency": "Markka"},
        "XPF": {"Currency": "CFP Franc"},
        "GMD": {"Currency": "Dalasi"},
        "GEL": {"Currency": "Lari"},
        "GEK": {"Currency": "Georgian Coupon"},
        "DDM": {"Currency": "Mark der DDR"},
        "DEM": {"Currency": "Deutsche Mark"},
        "GHS": {"Currency": "Ghana Cedi"},
        "GHC": {"Currency": "Cedi"},
        "GHP": {"Currency": "Ghana Cedi"},
        "GIP": {"Currency": "Gibraltar Pound"},
        "GRD": {"Currency": "Drachma"},
        "GTQ": {"Currency": "Quetzal"},
        "GBP": {"Currency": "Pound Sterling"},
        "GNF": {"Currency": "Guinean Franc"},
        "GNE": {"Currency": "Syli"},
        "GNS": {"Currency": "Syli"},
        "GWE": {"Currency": "Guinea Escudo"},
        "GWP": {"Currency": "Guinea-Bissau Peso"},
        "GYD": {"Currency": "Guyana Dollar"},
        "HTG": {"Currency": "Gourde"},
        "ITL": {"Currency": "Italian Lira"},
        "HNL": {"Currency": "Lempira"},
        "HKD": {"Currency": "Hong Kong Dollar"},
        "HUF": {"Currency": "Forint"},
        "ISK": {"Currency": "Iceland Krona"},
        "ISJ": {"Currency": "Old Krona"},
        "IDR": {"Currency": "Rupiah"},
        "XDR": {"Currency": "SDR (Special Drawing Right)"},
        "IRR": {"Currency": "Iranian Rial"},
        "IQD": {"Currency": "Iraqi Dinar"},
        "IEP": {"Currency": "Irish Pound"},
        "ILS": {"Currency": "New Israeli Sheqel"},
        "ILP": {"Currency": "Pound"},
        "ILR": {"Currency": "Old Shekel"},
        "JMD": {"Currency": "Jamaican Dollar"},
        "JPY": {"Currency": "Yen"},
        "JOD": {"Currency": "Jordanian Dinar"},
        "KZT": {"Currency": "Tenge"},
        "KES": {"Currency": "Kenyan Shilling"},
        "KPW": {"Currency": "North Korean Won"},
        "KRW": {"Currency": "Won"},
        "KWD": {"Currency": "Kuwaiti Dinar"},
        "KGS": {"Currency": "Som"},
        "LAJ": {"Currency": "Pathet Lao Kip"},
        "LAK": {"Currency": "Lao Kip"},
        "LVL": {"Currency": "Latvian Lats"},
        "LVR": {"Currency": "Latvian Ruble"},
        "LBP": {"Currency": "Lebanese Pound"},
        "LSL": {"Currency": "Loti"},
        "ZAR": {"Currency": "Rand"},
        "LSM": {"Currency": "Loti"},
        "ZAL": {"Currency": "Financial Rand"},
        "LRD": {"Currency": "Liberian Dollar"},
        "LYD": {"Currency": "Libyan Dinar"},
        "CHF": {"Currency": "Swiss Franc"},
        "LTL": {"Currency": "Lithuanian Litas"},
        "LTT": {"Currency": "Talonas"},
        "LUC": {"Currency": "Luxembourg Convertible Franc"},
        "LUF": {"Currency": "Luxembourg Franc"},
        "LUL": {"Currency": "Luxembourg Financial Franc"},
        "MOP": {"Currency": "Pataca"},
        "MGA": {"Currency": "Malagasy Ariary"},
        "MGF": {"Currency": "Malagasy Franc"},
        "MWK": {"Currency": "Kwacha"},
        "MYR": {"Currency": "Malaysian Ringgit"},
        "MVR": {"Currency": "Rufiyaa"},
        "MVQ": {"Currency": "Maldive Rupee"},
        "MLF": {"Currency": "Mali Franc"},
        "MTL": {"Currency": "Maltese Lira"},
        "MTP": {"Currency": "Maltese Pound"},
        "MRU": {"Currency": "Ouguiya"},
        "MRO": {"Currency": "Ouguiya"},
        "MUR": {"Currency": "Mauritius Rupee"},
        "XUA": {"Currency": "ADB Unit of Account"},
        "MXN": {"Currency": "Mexican Peso"},
        "MXV": {"Currency": "Mexican Unidad de Inversion (UDI)"},
        "MXP": {"Currency": "Mexican Peso"},
        "MDL": {"Currency": "Moldovan Leu"},
        "MNT": {"Currency": "Tugrik"},
        "MAD": {"Currency": "Moroccan Dirham"},
        "MZN": {"Currency": "Mozambique Metical"},
        "MZE": {"Currency": "Mozambique Escudo"},
        "MZM": {"Currency": "Mozambique Metical"},
        "MMK": {"Currency": "Kyat"},
        "NAD": {"Currency": "Namibia Dollar"},
        "NPR": {"Currency": "Nepalese Rupee"},
        "NLG": {"Currency": "Netherlands Guilder"},
        "NIO": {"Currency": "Cordoba Oro"},
        "NIC": {"Currency": "Cordoba"},
        "NGN": {"Currency": "Naira"},
        "MKD": {"Currency": "Denar"},
        "OMR": {"Currency": "Rial Omani"},
        "PKR": {"Currency": "Pakistan Rupee"},
        "PAB": {"Currency": "Balboa"},
        "PGK": {"Currency": "Kina"},
        "PYG": {"Currency": "Guarani"},
        "PEN": {"Currency": "Nuevo Sol"},
        "PEH": {"Currency": "Sol"},
        "PEI": {"Currency": "Inti"},
        "PES": {"Currency": "Sol"},
        "PHP": {"Currency": "Philippine Peso"},
        "PLN": {"Currency": "Zloty"},
        "PLZ": {"Currency": "Zloty"},
        "PTE": {"Currency": "Portuguese Escudo"},
        "QAR": {"Currency": "Qatari Rial"},
        "RON": {"Currency": "New Romanian Leu"},
        "ROK": {"Currency": "Leu A/52"},
        "ROL": {"Currency": "Old Leu"},
        "RUB": {"Currency": "Russian Ruble"},
        "RWF": {"Currency": "Rwanda Franc"},
        "SHP": {"Currency": "Saint Helena Pound"},
        "WST": {"Currency": "Tala"},
        "STN": {"Currency": "Dobra"},
        "STD": {"Currency": "Dobra"},
        "SAR": {"Currency": "Saudi Riyal"},
        "RSD": {"Currency": "Serbian Dinar"},
        "CSD": {"Currency": "Serbian Dinar"},
        "SCR": {"Currency": "Seychelles Rupee"},
        "SLE": {"Currency": "Leone"},
        "SLL": {"Currency": "Leone"},
        "SGD": {"Currency": "Singapore Dollar"},
        "XSU": {"Currency": "Sucre"},
        "SKK": {"Currency": "Slovak Koruna"},
        "SIT": {"Currency": "Tolar"},
        "SBD": {"Currency": "Solomon Islands Dollar"},
        "SOS": {"Currency": "Somali Shilling"},
        "SSP": {"Currency": "South Sudanese Pound"},
        "SDG": {"Currency": "Sudanese Pound"},
        "RHD": {"Currency": "Rhodesian Dollar"},
        "ESA": {"Currency": "Spanish Peseta"},
        "ESB": {"Currency": '"A" Account (convertible Peseta Account)'},
        "LKR": {"Currency": "Sri Lanka Rupee"},
        "SDD": {"Currency": "Sudanese Dinar"},
        "SDP": {"Currency": "Sudanese Pound"},
        "SRD": {"Currency": "Surinam Dollar"},
        "SRG": {"Currency": "Surinam Guilder"},
        "SEK": {"Currency": "Swedish Krona"},
        "CHE": {"Currency": "WIR Euro"},
        "CHW": {"Currency": "WIR Franc"},
        "CHC": {"Currency": "WIR Franc (for electronic)"},
        "SYP": {"Currency": "Syrian Pound"},
        "TWD": {"Currency": "New Taiwan Dollar"},
        "TJS": {"Currency": "Somoni"},
        "TJR": {"Currency": "Tajik Ruble"},
        "TZS": {"Currency": "Tanzanian Shilling"},
        "THB": {"Currency": "Baht"},
        "TPE": {"Currency": "Timor Escudo"},
        "TOP": {"Currency": "Pa’anga"},
        "TTD": {"Currency": "Trinidad and Tobago Dollar"},
        "TND": {"Currency": "Tunisian Dinar"},
        "TRL": {"Currency": "Old Turkish Lira"},
        "TRY": {"Currency": "Turkish Lira"},
        "TMT": {"Currency": "Turkmenistan New Manat"},
        "TMM": {"Currency": "Turkmenistan Manat"},
        "UGX": {"Currency": "Uganda Shilling"},
        "UGS": {"Currency": "Uganda Shilling"},
        "UGW": {"Currency": "Old Shilling"},
        "UAH": {"Currency": "Hryvnia"},
        "UAK": {"Currency": "Karbovanet"},
        "SUR": {"Currency": "Rouble"},
        "AED": {"Currency": "UAE Dirham"},
        "USS": {"Currency": "US Dollar (Same day)"},
        "USN": {"Currency": "US Dollar (Next day)"},
        "UYU": {"Currency": "Peso Uruguayo"},
        "UYI": {"Currency": "Uruguay Peso en Unidades Indexadas (UI)"},
        "UYW": {"Currency": "Unidad Previsional"},
        "UYN": {"Currency": "Old Uruguay Peso"},
        "UYP": {"Currency": "Uruguayan Peso"},
        "UZS": {"Currency": "Uzbekistan Sum"},
        "VUV": {"Currency": "Vatu"},
        "VEB": {"Currency": "Bolivar"},
        "VEF": {"Currency": "Bolívar"},
        "VES": {"Currency": "Bolívar Soberano"},
        "VED": {"Currency": "Bolívar Soberano"},
        "VND": {"Currency": "Dong"},
        "VNC": {"Currency": "Old Dong"},
        "YER": {"Currency": "Yemeni Rial"},
        "YDD": {"Currency": "Yemeni Dinar"},
        "YUD": {"Currency": "New Yugoslavian Dinar"},
        "YUM": {"Currency": "New Dinar"},
        "YUN": {"Currency": "Yugoslavian Dinar"},
        "ZRN": {"Currency": "New Zaire"},
        "ZRZ": {"Currency": "Zaire"},
        "ZMW": {"Currency": "Zambian Kwacha"},
        "ZMK": {"Currency": "Zambian Kwacha"},
        "ZWG": {"Currency": "Zimbabwe Gold"},
        "ZWC": {"Currency": "Rhodesian Dollar"},
        "ZWD": {"Currency": "Zimbabwe Dollar"},
        "ZWN": {"Currency": "Zimbabwe Dollar (new)"},
        "ZWR": {"Currency": "Zimbabwe Dollar"},
        "ZWL": {"Currency": "Zimbabwe\xa0Dollar"},
        "XBA": {"Currency": "Bond Markets Unit European Composite Unit (EURCO)"},
        "XFO": {"Currency": "Gold-Franc"},
        "XBB": {"Currency": "Bond Markets Unit European Monetary Unit (E.M.U.-6)"},
        "XRE": {"Currency": "RINET Funds Code"},
        "XBC": {"Currency": "Bond Markets Unit European Unit of Account 9 (E.U.A.-9)"},
        "XBD": {
            "Currency": "Bond Markets Unit European Unit of Account 17 (E.U.A.-17)"
        },
        "XFU": {"Currency": "UIC-Franc"},
        "XTS": {"Currency": "Codes specifically reserved for testing purposes"},
        "XXX": {
            "Currency": "The codes assigned for transactions where no currency is involved"
        },
        "XAU": {"Currency": "Gold"},
        "XPD": {"Currency": "Palladium"},
        "XPT": {"Currency": "Platinum"},
        "XAG": {"Currency": "Silver"},
    }
    response = currency_dict.get(
        currency_code.upper(), {"Currency": "currency not available"}
    )
    return response["Currency"]
