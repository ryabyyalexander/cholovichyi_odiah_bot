name_bot = 'ClothForYou'

main_icon = '☀️'
start_message = '''
Вітаємо вас у боті "Одяг для Вас"!
'''

MENU_COMMANDS: dict[str, str] = {
    '/start': 'с т а р т'
}
CATEGORY_min = ('куртки', 'джинси', 'трикотаж', 'шорти', 'поло', 'рубашки', 'головні убори')
CATEGORY = ('куртки', 'трикотаж', 'джинси')
CATEGORY_BTN = ['куртки', 'трикотаж', 'джинси']
BRANDS = ('alberto', 'milestone', 'lorenzoni', 'impulso', 'monteqiaro', 'Red Point', 'свєтри', 'футболки', 'штани')
BRANDS_BTN = ['Red Point • Germany', 'Milestone • Germany', 'ALBERTO • Germany', 'Lorenzoni • Italy', 'IMPULSO • Italy',
              'MONTECHIARO • Italy']

SIZE = ('46', '48', '50', '52', '54', '56', '58', '60')
size_letter = ('xs', 's', 'm', 'l', 'xl', '2xl', '3xl', '4xl')
size_jeans = ('32', '33', '34', '35', '36', '38', '40', '42')

btn = {
    'star_cl': '☆',
    'star_fl': '★',
    '<<': '←',
    '>>': '→',
    'x': '╳',
    'favorite_off': '✏️',
    'album': '▢',
    'red': '®️',
    'close': '✖️ закрити бота',
    '<': 'ᐊ',
    '>': 'ᐅ',
    'close_filters': '—',
    'filters': '🔎',
    '+': '+',
    '-': '-'
}

RED = ('➖', '©️', '🔝', '✔️', '®️', '➕')

'''
©️®️🔝❌❗️❓⁉️🆔🌀✔️🔺🔻⭕️🔔🔕📣📢 ✖️ ➖ ➕ ❌ ✣ ✘ · • ╳ ➜ ➜ « » ← → ︽ ︾ ↑ ↓ ᐊ ᐅ ▤ 👁‍🗨 
❎ ▢ '🧥', '👖', '👕', '👔', '🧢', '🩳'
,
                       'кур', 'дж', 'фут', 'пол', 'руб', 'свт', 'кфт','штн'
                       ,
    'ring': '▤',
    '!': '❗️',
    '_!': '❕',
    '?': '↓',
    '_?': '↑',
    'cat': '©️',
    'red': '®️',
    'upd': '🔄',
    'plus': '+',
    'minus': '-',
    'brn': '™️',
    'ok': '✔️',
    'f': '▤',
    'ex': 'x',
    'sim': '▢',
    'qw': '📚'
'''
man = 'AgACAgIAAxkBAAJaCmfSeWU1ePwcQhN_3uuqjjmYKuYzAAJn7DEbRiSRSm1rU4G2E94fAQADAgADeAADNgQ'
city25club = 'AgACAgIAAxkBAAId9WailtiaeNBhWnRfZm-rpQjgY8IfAAIy3jEb-rgYSb-gOT1rz7rsAQADAgADeAADNQQ'
men = 'AgACAgIAAxkBAAIl92at3Oq5E1weolkgUpoh22Fl6ZBMAAIO5TEbW7lwSegu9eZMW3fQAQADAgADeQADNQQ'
cat = 'AgACAgIAAxkBAAJJ92bWlMNj5Xyz41BhHGB3CyyULzM-AAJ-2jEbI2G4Sr_PVnV4aUODAQADAgADeAADNQQ'
blank = 'AgACAgIAAxkBAAJAmmbC_H5W8NJd7TGh7suzywshWYqpAAK-3TEbTsgZSu_IcTGPNq6DAQADAgADeAADNQQ'
intro = 'BAACAgIAAxkBAAJCpmbGq44TuusopbEPouBBRhgrJtheAAIDWQACPRgxSlezvoiBAprvNQQ'
caption_intro = '''<b>M️агазин чоловічого одягу</b>
<b>⚓️  Місто Одеса</b>
📍 <b>Вул. Інглезі 11/7 </b>
<b>Торговельне місто Сіті 25 </b>
<b>Орієнтир ➔ ресторан  🎪 🤡️  "Цирк" </b>
🚕 🚖 🚗   🚘🚖       <b>Зручна парковка</b>
<b>Монмартр 158         🏃🏻‍♂️🚶🏻👫 🚶‍♂️</b>
✔️  <b>Комфортний шопінг</b>
<b>Milestone  •  куртки  🇩🇪  Німеччина</b>
<b>ALBERTO  •  джинси  🇩🇪  Німеччина</b>
<b>Lorenzoni  •  трикотаж  🇮🇹  Італія</b>'''

rest = ['🚶🏻👫🚶🏻👫🚶🏻👫🏃🏻🕺🏻🚶‍♂️🚶‍♀️',
        '🏃🏻‍♂️🧍🏻🧍‍♀️🧍🏻🧍🏽‍♂️👫👭👬🧍🏽‍♂️🧍‍♀️🧍🏻',
        '🏃🏻‍👫👭👫🚶🏻🚘 👬️',
        '🏃🏻‍🏃🏼‍♂👫👭👬🧍🧍🏼‍♂️🏃🏻‍♀️',
        '🚶🏻👫🏃🏻‍♂️🚶🏻👫🚶🏻👫🚶🏻🚘🚖👫',
        '👫🚶🏻👫🚶🏻🚘🚘🚖👫',
        '👫👫🚶🏻🏃🏻']
menu_user = '''
➔  /start - Меню
➔  /excursion - Ознайомча екскурсія.
➔  /photo_album - Фотоальбом СІТІ 25.
➔  /all_photo - Усі фото одним альбомом.
'''

menu_admin = '''
➔  /start - Меню
➔  /excursion - Екскурсія
➔  /photo_album - Фотоальбом
➔  /all_photo - Усі фото разом
'''

'''
➔  /login - Вход в систему.
➔  /add_product - Добавити товар.
➔  /manage_products - Управління товарами.
➔  /notifications - Налаштування сповіщень.
➔  /profile - Перегляд профілю.
'''

ALBERTO = [
    ('1935-6286', 'ROB – WR REVOLUTIONAL', '999', 49.80, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 159, 19, 946.20),
    ('1533-5427', 'ROB-J – SMART LINEN MIX', '899', 49.80, 1, 1, 2, 2, 3, 2, 1, 1, 0, 0, 0, 159, 13, 647.40),
    ('1533-5427', 'ROB-J – SMART LINEN MIX', '905', 49.80, 1, 1, 2, 2, 3, 2, 1, 1, 0, 0, 0, 13, 159, 647.40),
    ('1533-5427', 'ROB-J – SMART LINEN MIX', '805', 49.80, 1, 1, 2, 2, 3, 2, 1, 1, 0, 0, 0, 13, 159, 647.40),
    ('1969-8027', 'SLIPE-K – DS BLUE VINTAGE', '873', 36.00, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 18, 159, 648.00),
    ('1505-6507', 'ROB-K – LIGHT ORGANIC COTTON', '899', 36.00, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 159, 16, 576.00),
    ('1505-6507', 'ROB-K – LIGHT ORGANIC COTTON', '900', 36.00, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 159, 16, 576.00),
    ('1505-6137', 'HOUSE-K – LIGHT ORGANIC COTTON', '100', 39.80, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 159, 16, 636.80),
    ('1528-6137', 'HOUSE-K – PURE LINEN', '900', 36.00, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 159, 16, 576.00),
    ('1577-6457', 'PIPE – LIGHT TENCEL DENIM', '825', 44.00, 1, 2, 2, 3, 2, 3, 2, 2, 2, 0, 0, 159, 19, 836.00),
    ('1577-6457', 'PIPE – LIGHT TENCEL DENIM', '875', 44.00, 1, 2, 2, 3, 2, 3, 2, 2, 2, 0, 0, 159, 19, 836.00),
    ('1577-6457', 'PIPE – LIGHT TENCEL DENIM', '885', 44.00, 1, 2, 2, 3, 2, 3, 2, 2, 2, 0, 0, 159, 19, 836.00),
    ('1588-7057', 'SLIM – DS BI STRECH DENIM', '815', 56.00, 1, 1, 2, 2, 3, 2, 1, 1, 0, 0, 0, 159, 13, 728.00),
    ('1381-7057', 'SLIM – ORGANIC DENIM', '825', 44.00, 1, 1, 2, 2, 3, 2, 1, 1, 0, 0, 0, 13, 159, 572.00),
    ('1505-6287', 'ROB – LIGHT ORGANIC COTTON', '660', 44.00, 1, 1, 2, 2, 3, 2, 1, 1, 0, 0, 0, 159, 13, 572.00),
    ('1505-6287', 'ROB – LIGHT ORGANIC COTTON', '800', 44.00, 1, 1, 2, 2, 3, 2, 1, 1, 0, 0, 0, 159, 13, 572.00),
    ('1935-6286', 'ROB – WR REVOLUTIONAL', '899', 49.80, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 159, 19, 946.20),
    ('1506-6287', 'ROB – LIGHT COTTON', '520', 44.00, 1, 1, 2, 2, 3, 2, 1, 1, 0, 0, 0, 159, 13, 572.00)
]

MILESTONE = [
    ('1506-6287', 'jackets', '520', 144.00, 0, 1, 2, 2, 3, 2, 1, 1, 300, 13, 572.00),
    ('1506-6287', 'jackets', '520', 144.00, 0, 1, 2, 2, 3, 2, 1, 1, 400, 13, 572.00),
    ('1506-6287', 'jackets', '520', 144.00, 0, 1, 2, 2, 3, 2, 1, 1, 200, 13, 572.00)
]
