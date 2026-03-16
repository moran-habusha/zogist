from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import json, random, time, asyncio

app = FastAPI()

# ── QUESTION BANKS ──
S1_BANK = [
    {"m": "אתה אוהב לבשל", "f": "את אוהבת לבשל", "wo": False},
    {"m": "אתה מעדיף טיול על פני ישיבה בבית", "f": "את מעדיפה טיול על פני ישיבה בבית", "wo": False},
    {"m": "אתה אדם של בוקר", "f": "את אדם של בוקר", "wo": False},
    {"m": "אתה אוהב מסיבות גדולות", "f": "את אוהבת מסיבות גדולות", "wo": False},
    {"m": 'אתה חולם לגור בחו"ל יום אחד', "f": 'את חולמת לגור בחו"ל יום אחד', "wo": False},
    {"m": "אתה רואה הרבה טלוויזיה וסדרות", "f": "את רואה הרבה טלוויזיה וסדרות", "wo": False},
    {"m": "אתה מוציא כסף בקלות", "f": "את מוציאה כסף בקלות", "wo": False},
    {"m": "אתה אוהב חיות מחמד", "f": "את אוהבת חיות מחמד", "wo": False},
    {"m": "אתה נוטה לאחר למקומות ופגישות", "f": "את נוטה לאחר למקומות ופגישות", "wo": False},
    {"m": "אתה אוהב לצאת לטיולים ספונטניים", "f": "את אוהבת לצאת לטיולים ספונטניים", "wo": False},
    {"m": "אתה ישן עם המזגן דלוק", "f": "את ישנה עם המזגן דלוק", "wo": False},
    {"m": "אתה אוהב אוכל חריף", "f": "את אוהבת אוכל חריף", "wo": False},
    {"m": "אתה שומר את הבית מסודר", "f": "את שומרת את הבית מסודר", "wo": False},
    {"m": "אתה אוהב לקום מוקדם בסוף שבוע", "f": "את אוהבת לקום מוקדם בסוף שבוע", "wo": False},
    {"m": "אתה אוהב ספורט", "f": "את אוהבת ספורט", "wo": False},
    {"m": "אתה אוהב לצאת לאירועים חברתיים", "f": "את אוהבת לצאת לאירועים חברתיים", "wo": False},
    {"m": "אתה שותה קפה כל יום", "f": "את שותה קפה כל יום", "wo": False},
    {"m": "אתה נוטה לדאוג יותר מדי", "f": "את נוטה לדאוג יותר מדי", "wo": False},
    {"m": "אתה אוהב לתת מתנות", "f": "את אוהבת לתת מתנות", "wo": False},
    {"m": "אתה מעדיף חוף ים על פני הרים", "f": "את מעדיפה חוף ים על פני הרים", "wo": False},
    {"m": "אתה אוהב מוזיקה חזקה", "f": "את אוהבת מוזיקה חזקה", "wo": False},
    {"m": "אתה חוגג ימי הולדת בגדול", "f": "את חוגגת ימי הולדת בגדול", "wo": False},
    {"m": "אתה צופה בחדשות באופן קבוע", "f": "את צופה בחדשות באופן קבוע", "wo": False},
    {"m": "אתה מתקשה להגיד לא לאנשים", "f": "את מתקשה להגיד לא לאנשים", "wo": False},
    {"m": "אתה אוהב לקרוא ספרים", "f": "את אוהבת לקרוא ספרים", "wo": False},
    {"m": "אתה אוהב לטייל ברגל בעיר", "f": "את אוהבת לטייל ברגל בעיר", "wo": False},
    {"m": "אתה אוהב לצלם תמונות", "f": "את אוהבת לצלם תמונות", "wo": False},
    {"m": "אתה מוצא את עצמך בטלפון יותר מדי", "f": "את מוצאת את עצמך בטלפון יותר מדי", "wo": False},
    {"m": "אתה אוהב לשחק משחקי קופסה", "f": "את אוהבת לשחק משחקי קופסה", "wo": False},
    {"m": "אתה חולם על בית עם גינה", "f": "את חולמת על בית עם גינה", "wo": False},
    {"m": "אתה מעדיף ללכת לישון מוקדם", "f": "את מעדיפה ללכת לישון מוקדם", "wo": False},
    {"m": "אתה אוהב סרטי אימה", "f": "את אוהבת סרטי אימה", "wo": False},
    {"m": "אתה זוכר ימי הולדת של אנשים קרובים", "f": "את זוכרת ימי הולדת של אנשים קרובים", "wo": False},
    {"m": "אתה אוהב שוקולד", "f": "את אוהבת שוקולד", "wo": False},
    {"m": "אתה נוטה לשמור טינה אחר ויכוחים", "f": "את נוטה לשמור טינה אחר ויכוחים", "wo": False},
    {"m": "אתה מעדיף בילוי שקט על פני יציאה לאנשים", "f": "את מעדיפה בילוי שקט על פני יציאה לאנשים", "wo": False},
    {"m": "אתה אוהב לבשל ארוחות גדולות לאנשים שאוהבים", "f": "את אוהבת לבשל ארוחות גדולות לאנשים שאוהבים", "wo": False},
    {"m": "אתה שם לב לפרטים קטנים בסביבה שלך", "f": "את שמה לב לפרטים קטנים בסביבה שלך", "wo": False},
    {"m": "אתה אוהב לנסוע ברכב ולהאזין למוזיקה", "f": "את אוהבת לנסוע ברכב ולהאזין למוזיקה", "wo": False},
    {"m": "אתה מתכנן דברים מראש ולא ברגע האחרון", "f": "את מתכננת דברים מראש ולא ברגע האחרון", "wo": False},
    {"m": "אתה אוהב לאכול בחוץ במסעדות", "f": "את אוהבת לאכול בחוץ במסעדות", "wo": False},
    {"m": "אתה מרגיש נוח לדבר על הרגשות שלך", "f": "את מרגישה נוח לדבר על הרגשות שלך", "wo": False},
    {"m": "אתה אוהב אנשים שמאתגרים אותך אינטלקטואלית", "f": "את אוהבת אנשים שמאתגרים אותך אינטלקטואלית", "wo": False},
    {"m": "אתה מסוגל לעשות כלום ולנוח בלי להרגיש אשמה", "f": "את מסוגלת לעשות כלום ולנוח בלי להרגיש אשמה", "wo": False},
    {"m": "אתה עורך קניות בצורה מסודרת עם רשימה", "f": "את עורכת קניות בצורה מסודרת עם רשימה", "wo": False},
    {"m": "אתה בדרך כלל עונה להודעות מהר", "f": "את בדרך כלל עונה להודעות מהר", "wo": False},
    {"m": "אתה אוהב לצפות בספורט", "f": "את אוהבת לצפות בספורט", "wo": False},
    {"m": "אתה רוצה ילדים", "f": "את רוצה ילדים", "wo": False},
    {"m": "אתה יכול לעבוד מהבית ביעילות", "f": "את יכולה לעבוד מהבית ביעילות", "wo": False},
    {"m": "אתה מעדיף לישון בחושך מוחלט", "f": "את מעדיפה לישון בחושך מוחלט", "wo": False},
]

S2_BANK = [
    {"q": "איזה צבעים מופיעים בדגל איטליה?", "a": "ירוק, לבן, אדום", "h": "3 פסים אנכיים"},
    {"q": "כמה שחקנים יש בקבוצת כדורגל?", "a": "11", "h": "לא כולל שחקני החלפה"},
    {"q": "מה הבירה של אוסטרליה?", "a": "קנברה", "h": "לא סידני ולא מלבורן!"},
    {"q": "כמה שניות יש בשעה?", "a": "3,600", "h": "60×60"},
    {"q": "מה הנהר הארוך בעולם?", "a": "הנילוס", "h": "עובר דרך מצרים"},
    {"q": "כמה פיאות יש לקובייה?", "a": "6", "h": "צד אחד לכל כיוון"},
    {"q": "מה הבירה של ברזיל?", "a": "ברזיליה", "h": "לא ריו ולא סאו פאולו!"},
    {"q": "כמה מיתרים יש לגיטרה קלאסית?", "a": "6", "h": "שלושה נמוכים שלושה גבוהים"},
    {"q": "מה הנוסחה הכימית של מים?", "a": "H₂O", "h": "שני מימן אחד חמצן"},
    {"q": "כמה שחקנים יש בקבוצת כדורסל?", "a": "5", "h": "בניגוד לכדורגל"},
    {"q": "מה הבירה של קנדה?", "a": "אוטווה", "h": "לא טורונטו!"},
    {"q": "כמה גרם יש בקילוגרם?", "a": "1,000", "h": "קילו = אלף ביוונית"},
    {"q": "מה הכוכב הקרוב ביותר לכדור הארץ?", "a": "השמש", "h": "כוכב שמשי"},
    {"q": "כמה ימים יש בשנה רגילה?", "a": "365", "h": "שנה מעוברת יש 366"},
    {"q": "באיזו יבשת נמצאת ישראל?", "a": "אסיה", "h": "המזרח התיכון"},
    {"q": "מה הצבע שנוצר מערבוב כחול וצהוב?", "a": "ירוק", "h": "צבע הטבע"},
    {'q': 'כמה אותיות יש בא"ב העברי?', "a": "22", "h": "מאלף עד תו"},
    {"q": "מה כוכב הלכת הגדול ביותר במערכת השמש?", "a": "צדק", "h": "כוכב לכת גזי ענק"},
    {"q": "כמה צלעות יש לחמשושה?", "a": "5", "h": "כמו כוכב ים"},
    {"q": "מה הבירה של ספרד?", "a": "מדריד", "h": "לא ברצלונה!"},
    {"q": "מה הים הגדול בעולם?", "a": "האוקיינוס השקט", "h": "גדול מכל היבשות יחד"},
    {"q": "כמה שעות יש ביום?", "a": "24", "h": "12 בוקר ו-12 לילה"},
    {'q': 'כמה ק"ג יש בטון?', "a": "1,000", "h": "אלף קילוגרם"},
    {"q": "מה הבירה של יפן?", "a": "טוקיו", "h": "אחת הערים הגדולות בעולם"},
    {"q": "מה הצבע שנוצר מערבוב אדום וצהוב?", "a": "כתום", "h": "צבע פרי מוכר"},
    {"q": "איזה כיוון השמש שוקעת?", "a": "מערב", "h": "הנגדי למזרח"},
    {'q': 'כמה זמן לוקח לאור מהשמש להגיע לכדור הארץ?', "a": "כ-8 דקות", "h": 'מהירות האור 300,000 ק"מ/שנייה'},
    {"q": "אם חצינו את האוקיינוס האטלנטי – לאיזה יבשת הגענו?", "a": "אמריקה", "h": "ממזרח לאירופה"},
    {"q": "כמה ריאות יש לבני אדם?", "a": "2", "h": "ימנית ושמאלית"},
    {"q": "מה קורה למים ב-100 מעלות צלזיוס?", "a": "רותחים ומתאדים", "h": "נקודת רתיחה"},
    {"q": "כמה עצמות יש בגוף האדם הבוגר?", "a": "206", "h": "תינוק נולד עם יותר"},
    {"q": "מה שם הכוח שמושך חפצים לכדור הארץ?", "a": "כבידה", "h": "גילה ניוטון"},
    {"q": "כמה שעות שינה מומלץ לבוגר ממוצע?", "a": "7-9 שעות", "h": "מדעי השינה"},
    {"q": "מה המכנה המשותף לכלב, חתול, וסוס?", "a": "יונקים", "h": "מניקים את ולדותיהם"},
    {"q": "כמה פעמים הלב פועם בדקה בממוצע?", "a": "60-100 פעמים", "h": "דופק תקין"},
    {"q": "איזה גז מהווה את רוב האטמוספירה?", "a": "חנקן (78%)", "h": "לא חמצן!"},
    {"q": "כמה מדינות גובלות בישראל?", "a": "4", "h": "לבנון, סוריה, ירדן, מצרים"},
    {"q": "מה קורה לנפח של מים כשהם קופאים?", "a": "הם מתרחבים", "h": "לכן בקבוקים מתפוצצים"},
    {"q": "כמה קלוריות מכיל גרם שומן?", "a": "9 קלוריות", "h": "יותר מחלבון ופחמימות"},
    {"q": "מה שם הגדר הגדולה שנבנתה בסין?", "a": "החומה הגדולה של סין", "h": "נמתחת אלפי קילומטרים"},
]

S3_BANK = [
    "עדיף להיות עשיר ובודד מאשר עני ומאושר",
    "כלבים עדיפים על חתולים",
    "אפשר להיות חברים טובים עם אקסים",
    "צריך לומר את האמת תמיד, גם אם היא כואבת",
    "נטפליקס עדיף על יציאה לסינמה",
    "עדיף שהילד הראשון יהיה בן",
    "עדיף לחיות בעיר גדולה מאשר בפריפריה",
    "כסף קונה אושר",
    "חייב לחיות ביחד לפני נישואין",
    "עדיף חבר אחד טוב מעשרה מכרים",
    "ריב קטן בריא לזוגיות",
    "צריך לדעת לבשל לפני שנכנסים לזוגיות",
    "עדיף לתת מתנת כסף מאשר מתנה אישית",
    "חיסכון חשוב יותר מטיולים",
    "הפרש הגילאים בין בני הזוג משנה בזוגיות",
    "ההורים צריכים להיות מעורבים בכל מה שעובר עלייך",
    "אפשר לאהוב יותר מאדם אחד בחיים",
    "ילדים צריכים ללמוד שתי שפות מגיל צעיר",
    "עדיף עבודה שאוהבים על פני עבודה שמשלמת טוב",
    "ללכת לישון כועסים הורס יחסים",
    "צריך לחלוק חשבונות בנק בזוגיות",
    "הראשון שמתעורר מכין קפה",
    "גלידת שוקולד עדיפה על וניל",
    "בגידה רגשית גרועה מבגידה פיזית",
    "עדיף לגור קרוב למשפחה",
    "לישון מאוחר בסוף שבוע זה חיוני",
    "חתונה גדולה עדיפה על טקס קטן",
    "אפשר לנהל זוגיות מרחוק לטווח ארוך",
    "לא נוגעים בטלפון בזמן איכות עם בן/בת הזוג",
    "שתיקה יכולה להיות תשובה",
    "אדם לא יכול לשנות את אופיו הבסיסי",
    "עדיף להתנצל ולהמשיך הלאה מאשר להסביר",
    "כדאי לקרוא חדשות כל יום",
    "הראשון שמתנצל בויכוח הוא החזק יותר",
    "אני רוצה לדעת על כל האקסים של בן/בת הזוג שלי",
    "קשר ארוך טווח עדיף על קשרים קצרים וחדשים",
    "חשוב שלבני הזוג יהיו תחומי עניין משותפים",
    "הרומנטיקה חייבת להישמר גם אחרי שנים יחד",
    "אי-אפשר לאהוב מישהו אם לא אוהבים את עצמך קודם",
    "קנאה בזוגיות היא סימן לאהבה",
    "חשוב שבני זוג יישנו באותו חדר תמיד",
    "מערכת יחסים ראשונה תמיד משפיעה על כל הקשרים הבאים",
    "בזוגיות צריך לשמור על מרחב אישי וחברים נפרדים",
    "עדיף להביע ביקורת ישירות מאשר לרמוז",
    "טיפול זוגי הוא סימן לבעיה, לא לחוזק",
    "חשוב שלבני הזוג יהיו ערכים דתיים או רוחניים דומים",
    "עדיף לחיות בזוג בלי ילדים מאשר להביא ילדים בזוגיות לא יציבה",
    "הזמן הגרוע ביותר לריב הוא בפני אחרים",
    "אם אין כימיה פיזית, הקשר לא יצליח לאורך זמן",
    "חשוב שבני הזוג יסכימו על כמה ילדים הם רוצים לפני שמתחייבים",
]

S4_BANK = [
    {"q": "מה היית מעדיף/ה לאכול עכשיו?", "o": ["פיצה 🍕", "סושי 🍣", "בורגר 🍔", "גלידה 🍦"]},
    {"q": "איזה חופשה הכי מושכת אותך?", "o": ["חוף ים 🏖️", "הרים ⛰️", "עיר גדולה 🌆", "בית עם נטפליקס 🛋️"]},
    {"q": "איזה ז'אנר סרטים אתה/ת הכי אוהב/ת?", "o": ["אקשן 💥", "רומנטיקה 💕", "קומדיה 😂", "אימה 👻"]},
    {"q": "מה הכי חשוב בזוגיות?", "o": ["הומור 😂", "כימיה 💫", "ערכים משותפים 🤝", "ביטחון כלכלי 💰"]},
    {"q": "איך נראה הדייט המושלם?", "o": ["מסעדה יוקרתית 🍽️", "טיול בטבע 🌿", "מסיבה עם חברים 🎉", "בישול ביחד 👨‍🍳"]},
    {"q": "איזה בעל חיים היית רוצה להיות?", "o": ["אריה 🦁", "דולפין 🐬", "נשר 🦅", "חתול 🐱"]},
    {"q": "איזה כוח-על היית בוחר/ת?", "o": ["לעוף ✈️", "לקרוא מחשבות 🧠", "לעצור זמן ⏸️", "להשתגר ממקום למקום 🌀"]},
    {"q": "איזה ז'אנר מוזיקה אתה/ת הכי אוהב/ת?", "o": ["פופ 🎤", "ראפ 🎧", "רוק 🎸", "מזרחית 🎵"]},
    {"q": "מה הופך סוף שבוע למושלם?", "o": ["נסיעה ספונטנית 🚗", "פיקניק בפארק 🌳", "ספא וסדרות 🛁", "מסיבה עם חברים 🎊"]},
    {"q": "מה התכונה הכי חשובה בבן/בת זוג?", "o": ["הומור 😄", "יושר 💎", "אמביציה 🚀", "רגישות 💞"]},
    {"q": "מה הייתם קונים עם מיליון שקל?", "o": ["דירה 🏠", "טיול בעולם ✈️", "רכב יוקרה 🚗", "השקעות 📈"]},
    {"q": "איזה ארוחת בוקר אתה/ת הכי אוהב/ת?", "o": ["שקשוקה 🍳", "טוסט עם ממרח 🍞", "חביתה עם ירקות 🥗", "קפה ודי ☕"]},
    {"q": "איזה תחביב היית רוצה לפתח?", "o": ["לנגן כלי 🎸", "לצייר ✏️", "לבשל ולאפות 🍰", "לצלם 📸"]},
    {"q": "מה הופך יום חופש למושלם?", "o": ["לישון עד מאוחר 😴", "לצאת לטבע או לים 🌊", "להיות עם האנשים הנכונים 👫", "אוכל טוב וקניות 🛍️"]},
    {"q": "איזה קינוח אתה/ת הכי אוהב/ת?", "o": ["שוקולד 🍫", "גלידה 🍦", "עוגה 🎂", "פירות טריים 🍓"]},
    {"q": "אם מחר היית מתחיל/ה דיאטה, מה הדבר שהיית אוכל/ת אחרון?", "o": ["פיצה 🍕", "שוקולד 🍫", "צ'יפס 🍟", "המבורגר 🍔"]},
    {"q": "מה הכי מעצבן אותך?", "o": ["איחורים ⏰", "רעש 🔊", "אי-סדר 🗃️", "הודעות קוליות 🎙️"]},
    {"q": "אם היית גיבור/ת סרט – מה הסגנון?", "o": ["אקשן הירואי ⚔️", "רומנטי קומי 💝", "מסתורין ופשע 🕵️", "פנטזיה ☄️"]},
    {"q": "מה כוח העל האמיתי שלך?", "o": ["אינטליגנציה רגשית 💛", "כושר גופני 💪", "יצירתיות 🎨", "כאריזמה ✨"]},
    {"q": "איפה הייתם גרים אם לא בישראל?", "o": ["ניו יורק 🗽", "פריז 🗼", "טוקיו 🏯", "ברצלונה 🌞"]},
    {"q": "מה הייתם מוחקים מהעולם?", "o": ["פקקים 🚗", "מוזיקת מעליות 🎹", "שיחות וספאם 📞", "יתושים 🦟"]},
    {"q": "איזה מקצוע היית בוחר/ת בעולם אחר?", "o": ["שף 👨‍🍳", "אסטרונאוט 🚀", "מוזיקאי/ת 🎼", "ספורטאי/ת 🏅"]},
    {"q": "מה הכי מרגש אותך?", "o": ["הצלחות קטנות ✨", "הפתעות 🎁", "רגעים שקטים 🌙", "אנשים חדשים 🤝"]},
    {"q": "מה הייתם רוצים שהשני/ה יעשה יותר?", "o": ["לומר מחמאות 💬", "לחבק 🤗", "לבשל ביחד 🍳", "לצאת להרפתקאות 🗺️"]},
    {"q": "איזה אמוג'י הכי מתאר אותך?", "o": ["😂 צוחק/ת", "😎 קול", "🥺 רגיש/ה", "🔥 נלהב/ת"]},
    {"q": "מה הייתם שומעים לפני שינה?", "o": ["פודקאסט 🎙️", "מוזיקה שקטה 🎵", "סדרה ברקע 📺", "שקט מוחלט 🤫"]},
    {"q": "מה הדבר הראשון שאתה/ת עושה/ה בבוקר?", "o": ["טלפון 📱", "שירותים 🚽", "קפה ☕", "מקלחת 🚿"]},
    {"q": "מה גורם לך להרגיש שסוף השבוע התחיל?", "o": ["לישון מאוחר 💤", "לצאת לברים 🍻", "ספורט בבוקר 🏃", "ארוחת שישי 👨‍👩‍👧"]},
    {"q": "איזו מציאות חלופית היית בוחר/ת?", "o": ["חיים לפני הטלפון 📵", "לחיות בלי להזדקן 🌱", "לא צריך שעות שינה 🌀", "קיץ תמידי ☀️"]},
    {"q": "מה הגהינום הפרטי שלך?", "o": ["ישיבות ארוכות 😴", "לחכות בתור ⌛", "קבוצות וואטסאפ מיותרות 📱", "לחפש חנייה 🚗"]},
    {"q": "מה הרגש שאתה/ת הכי קשה להסתיר אותו?", "o": ["עצב 😢", "כעס 😤", "שמחה 😄", "בושה 😳"]},
    {"q": "איך אתה/ת מעדיף/ה לפתור ויכוח?", "o": ["לדבר מיד 🗣️", "להתקרר ואחר כך לדבר ❄️", "לכתוב הודעה ✉️", "לשכוח ולהמשיך הלאה 🙃"]},
    {"q": "אם הייתם נעולים יחד שבוע בבית, מה היית עושה?", "o": ["בינג' סדרות 📺", "להתחיל פרויקט ביחד 🔨", "לבשל כל דבר בעולם 🍲", "לישון ולנוח 😴"]},
    {"q": "איזה חוויה יחד הכי חשובה לך?", "o": ['טיול לחו"ל ✈️', "ארוחת ערב רומנטית 🕯️", "הרפתקה בטבע 🏕️", "ערב שקט בבית 🛋️"]},
    {"q": "מה הייתם עושים עם יום חופש פתאומי ולבד?", "o": ["לטייל לבד 🚶", "לישון כל היום 😴", "לצאת לחברים 🎉", "לעסוק בתחביב 🎨"]},
    {"q": "איזה ריח הכי מרגיע אותך?", "o": ["קפה ☕", "גשם 🌧️", "אוכל מהתנור 🍞", "ים 🌊"]},
    {"q": "מתי אתה/ת בשיאך?", "o": ["בוקר מוקדם 🌅", "צהריים ☀️", "ערב 🌆", "לילה 🌙"]},
    {"q": "מה יכול להרוס לך ערב מושלם?", "o": ["ויכוח 🔥", "רעש 🔊", "שינוי תוכנית ברגע האחרון 🔄", "אינטרנט איטי 📡"]},
    {"q": "איזה סגנון תקשורת הכי מתאר אותך?", "o": ["ישיר ולעניין 🎯", "דיפלומטי ורגיש 🤝", "הומוריסטי 😂", "שקט ומאזין 🎧"]},
    {"q": "מה הייתם שואלים אדם חדש שאתם פוגשים?", "o": ["מה אתה עובד? 💼", "מה אתה אוהב לעשות? 🎭", "מאיפה אתה? 🗺️", "מה הסרט האחרון שראית? 🎬"]},
    {"q": "אם הייתם חיים בעידן אחר, איזה היה?", "o": ["הרומאים הקדמונים 🏛️", "מסע בין כוכבי עתידי 🚀", "שנות ה-80 🕹️", "המאה ה-19 🎩"]},
    {"q": "מה הדבר שאתה/ת הכי גאה בו?", "o": ["הישג אישי 🏆", "מערכת יחסים 💛", "ערך שדבקת בו 🌟", "כישרון מסוים 🎸"]},
    {"q": "איך אתה/ת מגיב/ה לביקורת?", "o": ["לוקח/ת ללב 💔", "מנתח/ת לעומק 🧠", "מגן/ה על עצמי 🛡️", "מתעלם/ת ומתקדם/ת 🚀"]},
    {"q": "מה מרגיש לך כמו ביזבוז זמן?", "o": ["ישיבות מיותרות 😑", "גלילה בסושיאל 📱", "תקועים בפקק 🚗", "סדרה שלא אהבת 📺"]},
    {"q": "איזה ילד/ה היית?", "o": ["שקט/ה ומסתגר/ת 📚", "שובב/ה ואנרגטי/ת 🏃", "אמנותי/ת ויצירתי/ת 🎨", "מנהיג/ה חברתי/ת 👑"]},
    {"q": "מה הדבר הראשון שאתה/ת שם/ה לב אליו באדם חדש?", "o": ["עיניים 👀", "חיוך 😊", "אופן הדיבור 🗣️", "שפת גוף 🤷"]},
    {"q": "מה יכול להחזיר לך אנרגיה אחרי יום קשה?", "o": ["שינה 😴", "אוכל טוב 🍕", "שיחה עם מישהו קרוב 📞", "בדידות ושקט 🧘"]},
    {"q": "אם היית כותב/ת ספר על חייך, איך הוא היה מתחיל?", "o": ["בהרפתקה 🌍", "ברגע מכונן 🔑", "בהומור 😂", "בתיאור מקום אהוב 🏡"]},
    {"q": "מה הדבר שאתה/ת הכי פוחד/ת ממנו?", "o": ["בדידות 🌑", "כישלון 📉", "מחלה 🏥", "לאכזב אחרים 😞"]},
    {"q": "מה מגדיר/ה אותך יותר מכל?", "o": ["המשפחה שלי 👨‍👩‍👧", "העבודה שלי 💼", "הערכים שלי 🌟", "החיוך שלי 😊"]},
]

# ── STATE ──
rooms = {}        # code -> GameRoom
connections = {}  # WebSocket -> {room_code, player_num}


class GameRoom:
    def __init__(self, code):
        self.code = code
        self.ws = {}           # {1: ws, 2: ws}
        self.players = {}      # {1: {name, gender, score}, 2: {...}}
        self.mode = None
        self.stage = 0
        self.q = 0
        self.intro_acked = False
        self.questions = {}    # {s1: [...10 items], s2: [...], s3: [...], s4: [...]}
        self.s1_ans = {}       # {q: {p1, p1_ts, p2, p2_ts}}
        self.s2_state = {}     # {q: {buzz_ts_1, buzz_ts_2, buzzer, result}}
        self.s3_ans = {}       # {q: {p1, p1_ts, p2, p2_ts}}
        self.s4_state = {}     # {q: {p1, p2, g1, g1_ts, g2, g2_ts}}

    async def send(self, pnum, msg):
        ws = self.ws.get(pnum)
        if ws:
            try:
                await ws.send_json(msg)
            except:
                pass

    async def broadcast(self, msg):
        for pnum in [1, 2]:
            await self.send(pnum, msg)


# ── HELPERS ──
def gen_code():
    while True:
        code = str(random.randint(1000, 9999))
        if code not in rooms:
            return code


def sample_questions():
    return {
        's1': random.sample(S1_BANK, min(10, len(S1_BANK))),
        's2': random.sample(S2_BANK, min(10, len(S2_BANK))),
        's3': random.sample(S3_BANK, min(10, len(S3_BANK))),
        's4': random.sample(S4_BANK, min(10, len(S4_BANK))),
    }


def get_room_and_pnum(ws):
    info = connections.get(ws)
    if not info:
        return None, None
    room = rooms.get(info['room_code'])
    return room, info['player_num']


# ── SCORING ──
def score_s1(qd):
    match = qd.get('p1') == qd.get('p2')
    if match:
        first = 1 if qd.get('p1_ts', 0) <= qd.get('p2_ts', 0) else 2
        pts1, pts2 = (2, 1) if first == 1 else (1, 2)
        return pts1, pts2, True
    return 0, 0, False


def score_s3(v1, v2, ts1, ts2):
    diff = abs(v1 - v2)
    base = [3, 1, 0, -1, -2][min(diff, 4)]
    speed = [2, 1, 0, -1, -2][min(diff, 4)]
    pts1, pts2 = base, base
    if ts1 <= ts2:
        pts1 += speed
    else:
        pts2 += speed
    return max(0, pts1), max(0, pts2), diff, base, speed, (1 if ts1 <= ts2 else 2)


def score_s4(qd):
    g1ok = qd.get('g1') == qd.get('p2')
    g2ok = qd.get('g2') == qd.get('p1')
    gt1 = qd.get('g1_ts', float('inf'))
    gt2 = qd.get('g2_ts', float('inf'))
    pts1, pts2 = 0, 0
    if g1ok and g2ok:
        if gt1 <= gt2:
            pts1, pts2 = 2, 1
        else:
            pts1, pts2 = 1, 2
    elif g1ok:
        pts1 = 2 if gt1 <= gt2 else 1
    elif g2ok:
        pts2 = 2 if gt2 <= gt1 else 1
    return pts1, pts2, g1ok, g2ok


async def update_scores(room, pts1, pts2):
    room.players[1]['score'] += pts1
    room.players[2]['score'] += pts2


def scores_payload(room):
    return {'p1': room.players[1]['score'], 'p2': room.players[2]['score']}


def next_stage_for_mode(mode, current_stage):
    if mode == 'full':
        return current_stage + 1
    return 5  # single stage mode goes straight to final


# ── HANDLERS ──
async def handle_create_room(ws, data):
    name = data.get('name', '').strip()
    gender = data.get('gender', 'm')
    if not name:
        await ws.send_json({'type': 'error', 'message': 'נדרש שם'})
        return
    code = gen_code()
    room = GameRoom(code)
    room.players[1] = {'name': name, 'gender': gender, 'score': 0}
    room.ws[1] = ws
    room.questions = sample_questions()
    rooms[code] = room
    connections[ws] = {'room_code': code, 'player_num': 1}
    await ws.send_json({'type': 'room_created', 'code': code})


async def handle_join_room(ws, data):
    name = data.get('name', '').strip()
    gender = data.get('gender', 'm')
    code = str(data.get('code', ''))
    if not name or len(code) != 4:
        await ws.send_json({'type': 'error', 'message': 'פרטים לא תקינים'})
        return
    room = rooms.get(code)
    if not room:
        await ws.send_json({'type': 'error', 'message': 'חדר לא נמצא!'})
        return
    if 2 in room.players:
        await ws.send_json({'type': 'error', 'message': 'החדר מלא'})
        return
    room.players[2] = {'name': name, 'gender': gender, 'score': 0}
    room.ws[2] = ws
    connections[ws] = {'room_code': code, 'player_num': 2}
    await room.broadcast({
        'type': 'player_joined',
        'p1': room.players[1],
        'p2': room.players[2],
        'questions': room.questions
    })


async def handle_choose_mode(ws, data):
    room, pnum = get_room_and_pnum(ws)
    if not room or pnum != 1:
        return
    mode = str(data.get('mode', 'full'))
    room.mode = mode
    await room.broadcast({'type': 'mode_announced', 'mode': mode})


async def handle_start_game(ws, data):
    room, pnum = get_room_and_pnum(ws)
    if not room or pnum != 1 or not room.mode:
        return
    start_stage = 1 if room.mode == 'full' else int(room.mode)
    room.stage = start_stage
    room.q = 0
    room.intro_acked = False
    await room.broadcast({'type': 'stage_intro', 'stage': start_stage})


async def handle_start_stage(ws, data):
    room, pnum = get_room_and_pnum(ws)
    if not room or pnum != 1:
        return
    room.intro_acked = True
    await room.broadcast({'type': 'countdown_done', 'stage': room.stage})
    await send_question(room, room.stage, 0)


async def send_question(room, stage, q):
    room.q = q
    room.s2_state.setdefault(q, {})
    qs = room.questions[f's{stage}']
    if q >= len(qs):
        return
    qdata = qs[q]
    await room.broadcast({
        'type': 'question',
        'stage': stage,
        'q': q,
        'total': len(qs),
        'qdata': qdata,
        'scores': scores_payload(room)
    })


async def handle_next_question(ws, data):
    room, pnum = get_room_and_pnum(ws)
    if not room or pnum != 1:
        return
    stage = room.stage
    qs = room.questions[f's{stage}']
    nq = room.q + 1
    if nq >= len(qs):
        next_stage = next_stage_for_mode(room.mode, stage)
        room.stage = next_stage
        room.q = 0
        room.intro_acked = False
        if next_stage >= 5:
            await render_final(room)
        else:
            await room.broadcast({'type': 'stage_intro', 'stage': next_stage})
    else:
        await send_question(room, stage, nq)


async def render_final(room):
    s1 = room.players[1]['score']
    s2 = room.players[2]['score']
    winner = 1 if s1 > s2 else (2 if s2 > s1 else 0)
    await room.broadcast({
        'type': 'game_over',
        'p1': room.players[1],
        'p2': room.players[2],
        'winner': winner,
        'scores': {'p1': s1, 'p2': s2}
    })


# ── STAGE 1 ──
async def handle_answer_s1(ws, data):
    room, pnum = get_room_and_pnum(ws)
    if not room or room.stage != 1:
        return
    q = room.q
    key = 'p1' if pnum == 1 else 'p2'
    qd = room.s1_ans.setdefault(q, {})
    if key in qd:
        return  # already answered
    qd[key] = data.get('answer')
    qd[key + '_ts'] = time.time()
    if 'p1' in qd and 'p2' in qd:
        pts1, pts2, match = score_s1(qd)
        await update_scores(room, pts1, pts2)
        qs = room.questions['s1']
        await room.broadcast({
            'type': 'reveal',
            'stage': 1,
            'q': q,
            'qdata': qs[q],
            'answers': {'p1': qd['p1'], 'p2': qd['p2']},
            'pts1': pts1, 'pts2': pts2,
            'match': match,
            'scores': scores_payload(room)
        })


# ── STAGE 2 ──
async def handle_buzz(ws, data):
    room, pnum = get_room_and_pnum(ws)
    if not room or room.stage != 2:
        return
    q = room.q
    qstate = room.s2_state.setdefault(q, {})
    if 'buzzer' in qstate:
        return
    ts_key = f'buzz_ts_{pnum}'
    qstate[ts_key] = time.monotonic()
    await asyncio.sleep(0.15)
    if 'buzzer' in qstate:
        return
    ts1 = qstate.get('buzz_ts_1', float('inf'))
    ts2 = qstate.get('buzz_ts_2', float('inf'))
    if ts1 == float('inf') and ts2 == float('inf'):
        return
    winner = 1 if ts1 <= ts2 else 2
    qstate['buzzer'] = winner
    await room.broadcast({
        'type': 'buzz_result',
        'buzzer': winner,
        'buzzer_name': room.players[winner]['name'],
        'buzzer_gender': room.players[winner]['gender'],
        'q': q
    })


async def handle_judge_s2(ws, data):
    room, pnum = get_room_and_pnum(ws)
    if not room or room.stage != 2:
        return
    q = room.q
    qstate = room.s2_state.get(q, {})
    buzzer = qstate.get('buzzer')
    if not buzzer:
        return
    correct = bool(data.get('correct'))
    pts1, pts2 = 0, 0
    if correct:
        if buzzer == 1:
            pts1 = 2
        else:
            pts2 = 2
    else:
        if buzzer == 1:
            pts2 = 1
        else:
            pts1 = 1
    await update_scores(room, pts1, pts2)
    qs = room.questions['s2']
    await room.broadcast({
        'type': 's2_result',
        'correct': correct,
        'answer': qs[q]['a'],
        'pts1': pts1, 'pts2': pts2,
        'scores': scores_payload(room)
    })
    await asyncio.sleep(2)
    if room.stage == 2:
        await handle_next_question_internal(room)


async def handle_next_question_internal(room):
    stage = room.stage
    qs = room.questions[f's{stage}']
    nq = room.q + 1
    if nq >= len(qs):
        next_stage = next_stage_for_mode(room.mode, stage)
        room.stage = next_stage
        room.q = 0
        room.intro_acked = False
        if next_stage >= 5:
            await render_final(room)
        else:
            await room.broadcast({'type': 'stage_intro', 'stage': next_stage})
    else:
        await send_question(room, stage, nq)


# ── STAGE 3 ──
async def handle_answer_s3(ws, data):
    room, pnum = get_room_and_pnum(ws)
    if not room or room.stage != 3:
        return
    q = room.q
    key = 'p1' if pnum == 1 else 'p2'
    qd = room.s3_ans.setdefault(q, {})
    if key in qd:
        return
    qd[key] = int(data.get('value', 3))
    qd[key + '_ts'] = time.time()
    if 'p1' in qd and 'p2' in qd:
        v1, v2 = qd['p1'], qd['p2']
        pts1, pts2, diff, base, speed, first = score_s3(v1, v2, qd['p1_ts'], qd['p2_ts'])
        await update_scores(room, pts1, pts2)
        qs = room.questions['s3']
        scale_labels = ['', 'מתנגד/ת בחריפות', 'לא מסכים/ה', 'ניטרלי/ת', 'מסכים/ה', 'מסכים/ה מאוד']
        await room.broadcast({
            'type': 'reveal',
            'stage': 3,
            'q': q,
            'qdata': qs[q],
            'answers': {'p1': v1, 'p2': v2, 'p1_label': scale_labels[v1], 'p2_label': scale_labels[v2]},
            'pts1': pts1, 'pts2': pts2,
            'diff': diff, 'base': base, 'speed': speed, 'first': first,
            'scores': scores_payload(room)
        })


# ── STAGE 4 ──
async def handle_answer_s4(ws, data):
    room, pnum = get_room_and_pnum(ws)
    if not room or room.stage != 4:
        return
    q = room.q
    key = 'p1' if pnum == 1 else 'p2'
    qd = room.s4_state.setdefault(q, {})
    if key in qd:
        return
    qd[key] = int(data.get('idx'))
    # If both have answered self, signal guess phase
    if 'p1' in qd and 'p2' in qd and 'g1' not in qd:
        await room.broadcast({
            'type': 'guess_phase', 'stage': 4, 'q': q,
            'answers': {'p1': qd['p1'], 'p2': qd['p2']},
            'qdata': room.questions['s4'][q]
        })


async def handle_guess_s4(ws, data):
    room, pnum = get_room_and_pnum(ws)
    if not room or room.stage != 4:
        return
    q = room.q
    key = 'g1' if pnum == 1 else 'g2'
    qd = room.s4_state.setdefault(q, {})
    if key in qd:
        return
    qd[key] = int(data.get('idx'))
    qd[key + '_ts'] = time.time()
    if 'g1' in qd and 'g2' in qd:
        pts1, pts2, g1ok, g2ok = score_s4(qd)
        await update_scores(room, pts1, pts2)
        qs = room.questions['s4']
        await room.broadcast({
            'type': 'reveal',
            'stage': 4,
            'q': q,
            'qdata': qs[q],
            'answers': {'p1': qd['p1'], 'p2': qd['p2']},
            'guesses': {'g1': qd['g1'], 'g2': qd['g2'], 'g1ok': g1ok, 'g2ok': g2ok},
            'pts1': pts1, 'pts2': pts2,
            'scores': scores_payload(room)
        })


async def handle_restart(ws, data):
    room, pnum = get_room_and_pnum(ws)
    if not room:
        return
    code = room.code
    for p, w in room.ws.items():
        connections.pop(w, None)
    rooms.pop(code, None)
    await ws.send_json({'type': 'restarted'})


# ── DISCONNECT ──
async def handle_disconnect(ws):
    info = connections.pop(ws, None)
    if not info:
        return
    room = rooms.get(info['room_code'])
    if not room:
        return
    other = 2 if info['player_num'] == 1 else 1
    await room.send(other, {'type': 'error', 'message': 'השחקן השני התנתק מהמשחק'})
    code = room.code
    for w in list(room.ws.values()):
        connections.pop(w, None)
    rooms.pop(code, None)


# ── MAIN WEBSOCKET ──
HANDLERS = {
    'create_room': handle_create_room,
    'join_room': handle_join_room,
    'choose_mode': handle_choose_mode,
    'start_game': handle_start_game,
    'start_stage': handle_start_stage,
    'next_question': handle_next_question,
    'answer_s1': handle_answer_s1,
    'buzz': handle_buzz,
    'judge_s2': handle_judge_s2,
    'answer_s3': handle_answer_s3,
    'answer_s4': handle_answer_s4,
    'guess_s4': handle_guess_s4,
    'restart': handle_restart,
}


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_json()
            handler = HANDLERS.get(data.get('type'))
            if handler:
                await handler(ws, data)
            else:
                await ws.send_json({'type': 'error', 'message': f'unknown action: {data.get("type")}'})
    except WebSocketDisconnect:
        await handle_disconnect(ws)
    except Exception as e:
        try:
            await ws.send_json({'type': 'error', 'message': str(e)})
        except:
            pass
        await handle_disconnect(ws)


@app.get("/")
async def root():
    return FileResponse("static/index.html")


app.mount("/static", StaticFiles(directory="static"), name="static")
