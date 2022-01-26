# S4K TRACKPHONES

![](https://img.shields.io/badge/python-3-blue.svg)
![](https://img.shields.io/github/tag/SundownDEV/PhoneInfoga.svg)

Herramienta de recopilación de información y reconocimiento OSINT para números de teléfono.

Una de las herramientas más avanzadas para escanear números de teléfono usando solo recursos gratuitos. El objetivo es recopilar primero información básica como país, área, operador y tipo de línea en cualquier número de teléfono internacional con muy buena precisión. Luego intente determinar el proveedor de VoIP o busque huellas en los motores de búsqueda para intentar identificar al propietario.

### [Tutorial OSINT: Creación de una herramienta de reconocimiento OSINT desde cero](https://medium.com/@SundownDEV/phone-number-scanning-osint-recon-tool-6ad8f0cac27b)

## Características

- Comprobar si el número de teléfono existe y es posible
- Recopile información estándar como país, tipo de línea y operador
- Comprobar varios números a la vez
- Reconocimiento OSINT utilizando API externas, Google Hacking, directorios telefónicos y motores de búsqueda
- Use formato personalizado para un reconocimiento OSINT más efectivo

## Formatos

La herramienta solo acepta formatos E164 e internacionales como entrada.

- E164: +3396360XXXX
- Internacional: +33 9 63 60 XX XX
- Nacional: 09 63 60 XX XX
- RFC3966: teléfono:+33-9-63-60-XX-XX
- Formato fuera del país desde EE. UU.: 011 33 9 63 60 XX XX

## Escáneres disponibles

Use `any` para deshabilitar esta característica. Valor por defecto: `all`

- numverify
- ovh

## Instalacion

```bash
git clone https://github.com/SadicX/S4K-TrackPhone
cd S4K-TrackPhone
python3 -m pip install -r requirements.txt 
(O usar el instalador)
```

## Uso

```
uso: TrackPhone.py -n <número> [opciones]

optional arguments:
  -h, --help            mostrar este mensaje de ayuda y salir
  -n number, --number number
                        El número de teléfono para escanear (E164 o Internacional
                        formato)
  -i input_file, --input input_file
                        Lista de números de teléfono para escanear (uno por línea)
  -o output_file, --output output_file
                        Salida para guardar los resultados del escaneo
  -s scanner, --scanner scanner 
                              El escáner a utilizar(cualquiera para omitir, predeterminado: all)
  --osint               Usar reconocimiento OSINT
  -u, --update          Actualizar la herramienta y las bases de datos
```

Ejemplo (las comillas son opcionales, utilícelas cuando escriba formatos especiales):

```
python3 TrackPhone.py -n "(+42)837544833"
```

Verifique un rango de números en OVH:

```
python3 TrackPhone.py -n +42837544833 -s ovh
```

Consulta varios números a la vez:
```
python3 TrackPhone.py -i numbers.txt -o results.txt
```

**Nota: `--osint` no es compatible con la opción `--output`**

Use todos los escáneres y ejecute el reconocimiento OSINT:

```
python3 TrackPhone.py -n +42837544833 -s all --osint
```

## Formateo

El formato E.164 para números de teléfono implica lo siguiente:

- Un signo + (más)
- Código de llamada de país internacional
- Código de área local
- Número de teléfono local

Por ejemplo, este es un número de EE. UU. en formato local estándar: (415) 555-2671

![](https://i.imgur.com/0e2SMdL.png)

Aquí está el mismo número de teléfono en formato E.164: +14155552671

![](https://i.imgur.com/KfrvacR.png)

En el Reino Unido y muchos otros países a nivel internacional, la marcación local puede requerir la adición de un '0' delante del número de suscriptor. Con el formato E.164, este '0' generalmente debe eliminarse.

Por ejemplo, este es un número del Reino Unido en formato local estándar: 020 7183 8750

Aquí está el mismo número de teléfono en formato E.164: +442071838750

## Tratar con el captcha de Google

TrackPhone usa una solución alternativa para manejar la detección de bots de Google. Al ejecutar el escaneo OSINT, Google generalmente lo incluirá en la lista negra muy fácilmente, lo que le pedirá a la herramienta que complete un captcha.

> Cuando busca en Google utilizando solicitudes personalizadas (Google Dorks), es muy fácil que lo incluyan en la lista negra. Entonces, Google muestra una página en la que debe completar un captcha para continuar. Tan pronto como se completa el captcha, Google crea una cookie llamada "GOOGLE_ABUSE_EXEMPTION" que se utiliza para incluir en la lista blanca su navegador y su dirección IP durante algunos minutos. Esta lista blanca temporal es suficiente para permitirle recopilar mucha información de muchas fuentes. Así que decidí agregar una manipulación simple por parte del usuario para evitar esta detección de bot. [...] Así que trataré de hacer solicitudes y esperaré hasta que obtenga un error 503, lo que significa que me incluyeron en la lista negra. Luego le pido al usuario que siga una URL para completar manualmente el captcha y copie el token de la lista blanca para pegarlo en la CLI. ¡La herramienta ahora puede continuar escaneando!
![](https://i.imgur.com/qbFZa1m.png)

### Cómo manejar el captcha
- Seguir la URL
- Complete el captcha si es necesario
- Abra la herramienta de desarrollo (F12 en la mayoría de los navegadores)
- Ve a **Almacenamiento**, luego **Cookies**
- Copie el valor de la cookie *GOOGLE_ABUSE_EXEMPTION* y simplemente péguelo en la CLI

![](https://i.imgur.com/KkE1EM5.png)

### Solución de problemas

La cookie debe crearse después de completar el captcha. Si no hay captcha ni la cookie *GOOGLE_ABUSE_EXEMPTION*, intente presionar F5 para actualizar la página. La cookie debería haber sido creada. Si actualizar la página no ayuda, cambie la consulta a algo diferente (cambie el número o agregue texto). Google no necesariamente le pedirá que complete un captcha si su solicitud es exactamente la misma que la anterior, porque generalmente se almacenará en caché.

## Formato personalizado

A veces, el número de teléfono tiene huellas pero se usa con un formato diferente. Esto es un problema porque, por ejemplo, si buscamos "+15417543010", no encontraremos páginas web que lo escriban así: "(541) 754–3010". Entonces, la herramienta usa un formato personalizado (opcional) proporcionado por el usuario para encontrar resultados más precisos. Para usar esta función correctamente y hacer que los resultados sean más valiosos, intente usar un formato que alguien del país del número usaría normalmente para compartir el número de teléfono en línea. Por ejemplo, los franceses suelen escribir números de esa manera en línea: *06.20.30.40.50*, *06 20 30 40 50*.
