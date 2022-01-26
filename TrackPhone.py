#!/usr/bin/env python3

__version__ = '1.0'

try:
    import sys
    from colorama import Fore, Style
    import atexit
    import argparse
    import random
except KeyboardInterrupt:
    print('[!] Saliendo...')
    sys.exit()
except:
    print('[!] Faltan requisitos. Intente ejecutar python3 -m pip install -r requirements.txt')
    sys.exit()

def banner():
    print(".___________..______          ___       ______  __  ___    .______    __    __    ______   .__   __.  _______ ")
    print("|           ||   _  \        /   \     /      ||  |/  /    |   _  \  |  |  |  |  /  __  \  |  \ |  | |   ____|")
    print("`---|  |----`|  |_)  |      /  ^  \   |  ,----'|  '  /     |  |_)  | |  |__|  | |  |  |  | |   \|  | |  |__   ")
    print("    |  |     |      /      /  /_\  \  |  |     |    <      |   ___/  |   __   | |  |  |  | |  . `  | |   __|  ")
    print("    |  |     |  |\  \----./  _____  \ |  `----.|  .  \     |  |      |  |  |  | |  `--'  | |  |\   | |  |____ ")
    print("    |__|     | _| `._____/__/     \__\ \______||__|\__\    | _|      |__|  |__|  \______/  |__| \__| |_______|")
    print(" TrackPhone Version: {}".format(__version__))
    print(" Coded by SadicX (S4K T34M) ")
    print("\n")

banner()

if sys.version_info[0] < 3:
    print("\033[1m\033[93m(!) Ejecute la herramienta usando Python 3" + Style.RESET_ALL)
    sys.exit()

parser = argparse.ArgumentParser(description=
    "Herramienta avanzada de recopilación de información para números de teléfono (https://github.com/SadicX/) version {}".format(__version__),
                                 usage='%(prog)s -n <number> [options]')

parser.add_argument('-n', '--number', metavar='number', type=str,
                    help='El número de teléfono para escanear (E164 o formato internacional)')

parser.add_argument('-i', '--input', metavar="input_file", type=argparse.FileType('r'),
                    help='Lista de números de teléfono para escanear (uno por línea)')

parser.add_argument('-o', '--output', metavar="output_file", type=argparse.FileType('w'),
                    help='Salida para guardar los resultados del escaneo')

parser.add_argument('-s', '--scanner', metavar="scanner", default="all", type=str,
                    help='El escáner a utilizar')

parser.add_argument('--osint', action='store_true',
                    help='Usar reconocimiento OSINT')

parser.add_argument('-u', '--update', action='store_true',
                    help='Actualizar el proyecto')

args = parser.parse_args()

def resetColors():
    if not args.output:
        print(Style.RESET_ALL)

# Reset text color at exit
atexit.register(resetColors)

# If any param is passed, execute help command
if not len(sys.argv) > 1:
    parser.print_help()
    sys.exit()

try:
    import time
    import hashlib
    import json
    import re
    import requests
    import urllib3
    from bs4 import BeautifulSoup
    import html5lib
    import phonenumbers
    from phonenumbers import carrier
    from phonenumbers import geocoder
    from phonenumbers import timezone
except KeyboardInterrupt:
    print('\033[91m[!] Saliendo...')
    sys.exit()
except:
    print('\033[91m[!] Faltan requisitos. Intente ejecutar python3 -m pip install -r requirements.txt')
    sys.exit()

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
except AttributeError:
    # no pyopenssl support used / needed / available
    pass

if args.update:
    def download_file(url, target_path):
        response = requests.get(url, stream=True)
        handle = open(target_path, "wb")
        for chunk in response.iter_content(chunk_size=512):
            if chunk:  # filter out keep-alive new chunks
                handle.write(chunk)

    print('Actualizando TrackerPhone...')
    print('Version actual: {}'.format(__version__))

    # Fetching last github tag
    new_version = json.loads(requests.get('https://api.github.com/repos/sundowndev/PhoneInfoga/tags').content)[0]['name']
    print('Last version: {}'.format(new_version))

    osintFiles = ['disposable_num_providers.json', 'individuals.json', 'reputation.json', 'social_medias.json']

    try:
        print('[*] Updating OSINT files')

        for file in osintFiles:
            url = 'https://raw.githubusercontent.com/sundowndev/PhoneInfoga/master/osint/{}'.format(file)
            output_directory = 'osint/{}'.format(file)
            download_file(url, output_directory)

        print('[*] Updating python script')

        url = 'https://raw.githubusercontent.com/sundowndev/PhoneInfoga/master/phoneinfoga.py'
        output_directory = 'phoneinfoga.py'
        download_file(url, output_directory)
    except:
        print('Actualización fallida. Intenta usar git pull.')
        sys.exit()

    print('La herramienta se actualizó con éxito.')
    sys.exit()

scanners = ['any', 'all', 'numverify', 'ovh']

uagent = []
uagent.append("Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14")
uagent.append("Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:26.0) Gecko/20100101 Firefox/26.0")
uagent.append("Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3")
uagent.append("Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)")
uagent.append("Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.7 (KHTML, like Gecko) Comodo_Dragon/16.1.1.0 Chrome/16.0.912.63 Safari/535.7")
uagent.append("Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)")
uagent.append("Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1")
uagent.append("Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0")

number = '' # Full number format
localNumber = '' # Local number format
internationalNumber = '' # International numberformat
numberCountryCode = '' # Dial code; e.g:"+33"
numberCountry = '' # Country; e.g:France

googleAbuseToken = ''
customFormatting = ''

def search(req, stop):
    global googleAbuseToken
    global uagent

    chosenUserAgent = random.choice(uagent)

    s = requests.Session()
    headers = {
        'User-Agent': chosenUserAgent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-us,en;q=0.5',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
        'Keep-Alive': '115',
        'Connection': 'keep-alive',
        'Cookie': 'Cookie: CGIC=Ij90ZXh0L2h0bWwsYXBwbGljYXRpb24veGh0bWwreG1sLGFwcGxpY2F0aW9uL3htbDtxPTAuOSwqLyo7cT0wLjg; CONSENT=YES+RE.fr+20150809-08-0; 1P_JAR=2018-11-28-14; NID=148=aSdSHJz71rufCokaUC93nH3H7lOb8E7BNezDWV-PyyiHTXqWK5Y5hsvj7IAzhZAK04-QNTXjYoLXVu_eiAJkiE46DlNn6JjjgCtY-7Fr0I4JaH-PZRb7WFgSTjiFqh0fw2cCWyN69DeP92dzMd572tQW2Z1gPwno3xuPrYC1T64wOud1DjZDhVAZkpk6UkBrU0PBcnLWL7YdL6IbEaCQlAI9BwaxoH_eywPVyS9V; SID=uAYeu3gT23GCz-ktdGInQuOSf-5SSzl3Plw11-CwsEYY0mqJLSiv7tFKeRpB_5iz8SH5lg.; HSID=AZmH_ctAfs0XbWOCJ; SSID=A0PcRJSylWIxJYTq_; APISID=HHB2bKfJ-2ZUL5-R/Ac0GK3qtM8EHkloNw; SAPISID=wQoxetHBpyo4pJKE/A2P6DUM9zGnStpIVt; SIDCC=ABtHo-EhFAa2AJrJIUgRGtRooWyVK0bAwiQ4UgDmKamfe88xOYBXM47FoL5oZaTxR3H-eOp7-rE; OTZ=4671861_52_52_123900_48_436380; OGPC=873035776-8:; OGP=-873035776:;'
    }

    try:
        URL = 'https://www.google.com/search?tbs=li:1&q={}&amp;gws_rd=ssl'.format(req)
        r = s.get(URL + googleAbuseToken, headers=headers)

        while r.status_code == 503:
            print(code_warning + 'Estás en la lista negra temporal de la búsqueda de Google. Complete el captcha en la siguiente URL y copie/pegue el contenido de GOOGLE_ABUSE_EXEMPTION cookie : {}'.format(URL))
            print('\n' + code_info + 'Necesitas ayuda ? Read https://github.com/sundowndev/PhoneInfoga#dealing-with-google-captcha')
            token = input('\nGOOGLE_ABUSE_EXEMPTION=')
            googleAbuseToken = '&google_abuse=' + token
            r = s.get(URL + googleAbuseToken, headers=headers)

        soup = BeautifulSoup(r.content, 'html.parser')
        results = soup.find("div", id="search").find_all("div", class_="g")

        links = []
        counter = 0

        for result in results:
            counter += 1

            if int(counter) > int(stop):
                break

            url = result.find("a").get('href')
            url = re.sub(r'(?:\/url\?q\=)', '', url)
            url = re.sub(r'(?:\/url\?url\=)', '', url)
            url = re.sub(r'(?:\&sa\=)(?:.*)', '', url)
            url = re.sub(r'(?:\&rct\=)(?:.*)', '', url)

            if re.match(r"^(?:\/search\?q\=)", url) is not None:
                url = 'https://google.com' + url

            links.append(url)

        return links
    except:
        print(code_error + 'Solicitud fallida. Vuelva a intentarlo o abra un problema en GitHub.')

def formatNumber(InputNumber):
    return re.sub("(?:\+)?(?:[^[0-9]*)", "", InputNumber)

def localScan(InputNumber):
    global number
    global localNumber
    global internationalNumber
    global numberCountryCode
    global numberCountry

    print(code_info + 'Ejecutando escaneo local...')

    FormattedPhoneNumber = "+" + formatNumber(InputNumber)

    try:
        PhoneNumberObject = phonenumbers.parse(FormattedPhoneNumber, None)
    except:
        return False
    else:
        if not phonenumbers.is_valid_number(PhoneNumberObject):
            return False

        number = phonenumbers.format_number(PhoneNumberObject, phonenumbers.PhoneNumberFormat.E164).replace('+', '')
        numberCountryCode = phonenumbers.format_number(PhoneNumberObject, phonenumbers.PhoneNumberFormat.INTERNATIONAL).split(' ')[0]

        countryRequest = json.loads(requests.request('GET', 'https://restcountries.eu/rest/v2/callingcode/{}'.format(numberCountryCode.replace('+', ''))).content)
        numberCountry = countryRequest[0]['alpha2Code']

        localNumber = phonenumbers.format_number(PhoneNumberObject, phonenumbers.PhoneNumberFormat.E164).replace(numberCountryCode, '')
        internationalNumber = phonenumbers.format_number(PhoneNumberObject, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

        print(code_result + 'International format: {}'.format(internationalNumber))
        print(code_result + 'Local format: 0{}'.format(localNumber))
        print(code_result + 'Country code: {}'.format(numberCountryCode))
        print(code_result + 'Location: {}'.format(geocoder.description_for_number(PhoneNumberObject, "en")))
        print(code_result + 'Carrier: {}'.format(carrier.name_for_number(PhoneNumberObject, 'en')))
        print(code_result + 'Area: {}'.format(geocoder.description_for_number(PhoneNumberObject, 'en')))
        for timezoneResult in timezone.time_zones_for_number(PhoneNumberObject):
            print(code_result + 'Timezone: {}'.format(timezoneResult))

        if phonenumbers.is_possible_number(PhoneNumberObject):
            print(code_info + 'El número es válido y posible.')
        else:
            print(code_warning + 'El número es válido pero podría no ser posible.')

def numverifyScan():
    global number

    if not args.scanner == 'numverify' and not args.scanner == 'all':
        return -1

    print(code_info + 'Ejecutando Numverify.com escaneo...')

    requestSecret = ''
    resp = requests.get('https://numverify.com/')
    soup = BeautifulSoup(resp.text, "html5lib")
    for tag in soup.find_all("input", type="hidden"):
        if tag['name'] == "scl_request_secret":
            requestSecret = tag['value']
            break

    apiKey = hashlib.md5((number + requestSecret).encode('utf-8')).hexdigest()

    headers = {
        'host': "numverify.com",
        'connection': "keep-alive",
        'content-length': "49",
        'accept': "application/json",
        'origin': "https://numverify.com",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'referer': "https://numverify.com/",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "en-US,en;q=0.9,fr;q=0.8,la;q=0.7,es;q=0.6,zh-CN;q=0.5,zh;q=0.4",
        'cache-control': "no-cache"
    }

    response = requests.request("GET", "https://numverify.com/php_helper_scripts/phone_api.php?secret_key={}&number={}".format(apiKey, number), data="", headers=headers)

    if response.content == "No autorizado" or response.status_code != 200:
        print((code_error + "Se produjo un error al llamar a la API (solicitud incorrecta o clave de API incorrecta)."))
        return -1

    data = json.loads(response.content)

    if data["valid"] == False:
        print((code_error + "Error: especifique un número de teléfono válido. Ejemplo: +6464806649"))
        sys.exit()

    InternationalNumber = '({}){}'.format(data["country_prefix"], data["local_format"])

    print((code_result + "Number: ({}) {}").format(data["country_prefix"],data["local_format"]))
    print((code_result + "Country: {} ({})").format(data["country_name"],data["country_code"]))
    print((code_result + "Location: {}").format(data["location"]))
    print((code_result + "Carrier: {}").format(data["carrier"]))
    print((code_result + "Line type: {}").format(data["line_type"]))

    if data["line_type"] == 'landline':
        print((code_warning + "Lo más probable es que sea un teléfono fijo, pero aún puede ser un número de VoIP fijo."))
    elif data["line_type"] == 'mobile':
        print((code_warning + "Lo más probable es que sea un número de teléfono móvil, pero aún puede ser un número de VoIP."))

def ovhScan():
    global localNumber
    global numberCountry

    if not args.scanner == 'ovh' and not args.scanner == 'all':
        return -1

    print(code_info + 'Ejecutando escaneo OVH...')

    querystring = { "country": numberCountry.lower() }

    headers = {
        'accept': "application/json",
        'cache-control': "no-cache"
    }

    response = requests.request("GET", "https://api.ovh.com/1.0/telephony/number/detailedZones", data="", headers=headers, params=querystring)

    data = json.loads(response.content)

    if isinstance(data, list):
        askedNumber = "0" + localNumber.replace(localNumber[-4:], 'xxxx')

        for voip_number in data:
            if voip_number['number'] == askedNumber:
                print((code_info + "1 result found in OVH database"))
                print((code_result + "Number range: {}".format(voip_number['number'])))
                print((code_result + "City: {}".format(voip_number['city'])))
                print((code_result + "Zip code: {}".format(voip_number['zipCode'] if voip_number['zipCode'] is not None else '')))
                askForExit()

def replaceVariables(string):
    global number
    global internationalNumber
    global localNumber

    string = string.replace('$n', number)
    string = string.replace('$i', internationalNumber)
    string = string.replace('$l', localNumber)

    return string

def osintIndividualScan():
    global number
    global internationalNumber
    global numberCountryCode
    global customFormatting

    dorks = json.load(open('osint/individuals.json'))

    for dork in dorks:
        if dork['dialCode'] is None or dork['dialCode'] == numberCountryCode:
            if customFormatting:
                dorkRequest = replaceVariables(dork['request']) + ' | intext:"{}"'.format(customFormatting)
            else:
                dorkRequest = replaceVariables(dork['request'])

            print((code_info + "Searching for footprints on {}...".format(dork['site'])))
            for result in search(dorkRequest, stop=dork['stop']):
                if result:
                    print((code_result + "URL: " + result))
        else:
            return -1

def osintReputationScan():
    global number
    global internationalNumber
    global customFormatting

    dorks = json.load(open('osint/reputation.json'))

    for dork in dorks:
        if customFormatting:
            dorkRequest = replaceVariables(dork['request']) + ' | intext:"{}"'.format(customFormatting)
        else:
            dorkRequest = replaceVariables(dork['request'])

        print((code_info + "Buscando {}...".format(dork['title'])))
        for result in search(dorkRequest, stop=dork['stop']):
            if result:
                print((code_result + "URL: " + result))

def osintSocialMediaScan():
    global number
    global internationalNumber
    global customFormatting

    dorks = json.load(open('osint/social_medias.json'))

    for dork in dorks:
        if customFormatting:
            dorkRequest = replaceVariables(dork['request']) + ' | intext:"{}"'.format(customFormatting)
        else:
            dorkRequest = replaceVariables(dork['request'])

        print((code_info + "Buscando huellas en {}...".format(dork['site'])))
        for result in search(dorkRequest, stop=dork['stop']):
            if result:
                print((code_result + "URL: " + result))

def osintDisposableNumScan():
    global number

    dorks = json.load(open('osint/disposable_num_providers.json'))

    for dork in dorks:
        dorkRequest = replaceVariables(dork['request'])

        print((code_info + "Buscando huellas en {}...".format(dork['site'])))
        for result in search(dorkRequest, stop=dork['stop']):
            if result:
                print((code_result + "Result found: {}".format(dork['site'])))
                print((code_result + "URL: " + result))
                askForExit()

def osintScan():
    global number
    global localNumber
    global internationalNumber
    global numberCountryCode
    global numberCountry
    global customFormatting

    if not args.osint:
        return -1

    print(code_info + 'Ejecutando reconocimiento de huella OSINT...')

    # Whitepages
    print((code_info + "Generando URL de escaneo en 411.com..."))
    print(code_result + "Scan URL: https://www.411.com/phone/{}".format(internationalNumber.replace('+', '').replace(' ', '-')))

    askingCustomPayload = input(code_info + 'Le gustaría utilizar un formato adicional para este número? (y/N) ')

    if askingCustomPayload == 'y' or askingCustomPayload == 'yes':
        customFormatting = input(code_info + 'Custom format: ')

    print((code_info + '---- huellas de paginas web ----'))

    print((code_info + "Buscando huellas en páginas web... (limit=5)"))
    if customFormatting:
        req = '{} | intext:"{}" | intext:"{}" | intext:"{}"'.format(number,number,internationalNumber,customFormatting)
    else:
        req = '{} | intext:"{}" | intext:"{}"'.format(number,number,internationalNumber)
    for result in search(req, stop=5):
        if result:
            print((code_result + "Resultado encontrado: " + result))

    # Documents
    print((code_info + "Buscando documentos... (limit=10)"))
    if customFormatting:
        req = 'intext:"{}" | intext:"{}" | intext:"{}" ext:doc | ext:docx | ext:odt | ext:pdf | ext:rtf | ext:sxw | ext:psw | ext:ppt | ext:pptx | ext:pps | ext:csv | ext:txt'.format(number,internationalNumber,customFormatting)
    else:
        req = 'intext:"{}" | intext:"{}" ext:doc | ext:docx | ext:odt | ext:pdf | ext:rtf | ext:sxw | ext:psw | ext:ppt | ext:pptx | ext:pps | ext:csv | ext:txt'.format(number,internationalNumber)
    for result in search('intext:"{}" | intext:"{}" ext:doc | ext:docx | ext:odt | ext:pdf | ext:rtf | ext:sxw | ext:psw | ext:ppt | ext:pptx | ext:pps | ext:csv | ext:txt'.format(number,internationalNumber), stop=10):
        if result:
            print((code_result + "Resultado encontrado: " + result))

    print((code_info + '---- Huellas de reputación ----'))

    osintReputationScan()

    print((code_info + "Generando URL en scamcallfighters.com..."))
    print(code_result + 'http://www.scamcallfighters.com/search-phone-{}.html'.format(number))

    tmpNumAsk = input(code_info + "Le gustaría buscar huellas de proveedores de números temporales? (Y/n) ")

    if tmpNumAsk.lower() != 'n' and tmpNumAsk.lower() != 'no':
        print((code_info + '---- Huellas de proveedores de números temporales ----'))

        print((code_info + "Buscando número de teléfono en tempophone.com..."))
        response = requests.request("GET", "https://tempophone.com/api/v1/phones")
        data = json.loads(response.content)
        for voip_number in data['objects']:
            if voip_number['phone'] == formatNumber(number):
                print((code_result + "Encontrado un proveedor de número temporal: tempophone.com"))
                askForExit()

        osintDisposableNumScan()

    print((code_info + '---- Huellas en las redes sociales ----'))

    osintSocialMediaScan()

    print((code_info + '---- Huellas de guías telefónicas ----'))

    if numberCountryCode == '+1':
        print((code_info + "Generando URL en Personas Verdaderas... "))
        print(code_result + 'https://www.truepeoplesearch.com/results?phoneno={}'.format(internationalNumber.replace(' ', '')))

    osintIndividualScan()

def askForExit():
    if not args.output:
        user_input = input(code_info + "Continuar escaneando? (y/N) ")

        if user_input.lower() == 'y' or user_input.lower() == 'yes':
            return -1
        else:
            print(code_info + "Adios!")
            sys.exit()

def scanNumber(InputNumber):
    print(code_title + "[!] ---- Obtención de información para {} ---- [!]".format(formatNumber(InputNumber)))

    localScan(InputNumber)

    global number
    global localNumber
    global internationalNumber
    global numberCountryCode
    global numberCountry

    if not number:
        print((code_error + "Error: el número {} no es válido. Skipping".format(formatNumber(InputNumber))))
        sys.exit()

    numverifyScan()
    ovhScan()
    osintScan()

    print(code_info + "Scaner finalizado")

    print('\n' + Style.RESET_ALL)

try:
    if args.output:
        code_info = '[*] '
        code_warning = '(!) '
        code_result = '[+] '
        code_error = '[!] '
        code_title = ''

        if args.osint:
            print('\033[91m[!] El escáner OSINT no está disponible usando la opción de salida (lo siento).')
            sys.exit()

        sys.stdout = args.output
        banner()
    else:
        code_info = Fore.RESET + Style.BRIGHT + '[*] '
        code_warning = Fore.YELLOW + Style.BRIGHT + '(!) '
        code_result = Fore.GREEN + Style.BRIGHT + '[+] '
        code_error = Fore.RED + Style.BRIGHT + '[!] '
        code_title = Fore.YELLOW + Style.BRIGHT

    # Verify scanner option
    if not args.scanner in scanners:
        print((code_error + "Error: el escáner no existe."))
        sys.exit()

    if args.number:
        scanNumber(args.number)
    elif args.input:
        for line in args.input.readlines():
            scanNumber(line)

    if args.output:
        args.output.close()
except KeyboardInterrupt:
    print(("\n" + code_error + "Scaner interrumpido. ¡Adiós!"))
    sys.exit()
