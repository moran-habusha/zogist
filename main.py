from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json, random, time, asyncio

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET"])

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
    {"m": "אתה נוטה לשמור טינה לאחר ויכוחים", "f": "את נוטה לשמור טינה לאחר ויכוחים", "wo": False},
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
    {"m": "אתה מעדיף חיות מחמד קטנות על גדולות", "f": "את מעדיפה חיות מחמד קטנות על גדולות", "wo": False},
    {"m": "אתה חולם לנסוע לסיבוב מסביב לעולם", "f": "את חולמת לנסוע לסיבוב מסביב לעולם", "wo": False},
    {"m": "אתה אוהב לבלות בצפייה בסדרות", "f": "את אוהבת לבלות בצפייה בסדרות", "wo": False},
    {"m": "אתה מרגיש בנוח עם שתיקות", "f": "את מרגישה בנוח עם שתיקות", "wo": False},
    {"m": "אתה שומר כסף בצד כל חודש", "f": "את שומרת כסף בצד כל חודש", "wo": False},
    {"m": "אתה מתגעגע לתקופת הילדות", "f": "את מתגעגעת לתקופת הילדות", "wo": False},
    {"m": "אתה מעדיף להיות הראשון שמגיע לאירועים", "f": "את מעדיפה להיות הראשונה שמגיעה לאירועים", "wo": False},
    {"m": "אתה אוהב מקלחת חמה גם בקיץ", "f": "את אוהבת מקלחת חמה גם בקיץ", "wo": False},
    {"m": "אתה נוטה לשחק הרבה בטלפון", "f": "את נוטה לשחק הרבה בטלפון", "wo": False},
    {"m": "אתה מחפש תמיד את הפתרון הקל ביותר", "f": "את מחפשת תמיד את הפתרון הקל ביותר", "wo": False},
    {"m": "אתה אוהב כשמפתיעים אותך", "f": "את אוהבת כשמפתיעים אותך", "wo": False},
    {"m": "אתה מרגיש טוב יותר אחרי ספורט", "f": "את מרגישה טוב יותר אחרי ספורט", "wo": False},
    {"m": "אתה אוהב לתכנן טיולים", "f": "את אוהבת לתכנן טיולים", "wo": False},
    {"m": "אתה קונה דברים אימפולסיבית", "f": "את קונה דברים אימפולסיבית", "wo": False},
    {"m": "אתה אוהב לדון בנושאים עמוקים", "f": "את אוהבת לדון בנושאים עמוקים", "wo": False},
    {"m": "אתה מעדיף שיחה פנים אל פנים על הודעה", "f": "את מעדיפה שיחה פנים אל פנים על הודעה", "wo": False},
    {"m": "אתה סובל מקור", "f": "את סובלת מקור", "wo": False},
    {"m": "אתה אוהב ריח של דלק", "f": "את אוהבת ריח של דלק", "wo": False},
    {"m": "אתה מרגיש שאתה אדם אופטימי", "f": "את מרגישה שאת אדם אופטימית", "wo": False},
    {"m": "האם מצחיק אותך סרטונים של אנשים נופלים", "f": "האם מצחיק אותך סרטונים של אנשים נופלים", "wo": False},
]

S2_BANK = [
    {"q": "איזה צבעים מופיעים בדגל איטליה?", "a": "ירוק, לבן, אדום", "h": "3 פסים אנכיים"},
    {"q": "כמה שחקנים יש בקבוצת כדורגל?", "a": "11", "h": "לא כולל שחקני החלפה"},
    {"q": "מה הבירה של אוסטרליה?", "a": "קנברה", "h": "לא סידני ולא מלבורן!"},
    {"q": "כמה שניות יש בשעה?", "a": "3,600", "h": "60×60"},
    {"q": "מה הנהר הארוך בעולם?", "a": "הנילוס", "h": "עובר דרך מצרים"},
    {"q": "כמה פיאות יש לקובייה?", "a": "6", "h": "אחת לכל מספר"},
    {"q": "מה הבירה של ברזיל?", "a": "ברזיליה", "h": "לא ריו ולא סאו פאולו!"},
    {"q": "מה השם הנוסף של איטליה?", "a": "מדינת המגף", "h": "הצורה הגיאוגרפית שלה"},
    {"q": "מה הנוסחה הכימית של מים?", "a": "H₂O", "h": "שני מימן אחד חמצן"},
    {"q": "כמה שחקנים יש בקבוצת כדורסל?", "a": "5", "h": "הרבה פחות מכדורגל"},
    {"q": "מה הבירה של קנדה?", "a": "אוטווה", "h": "לא טורונטו!"},
    {"q": "כמה גרם יש בקילוגרם?", "a": "1,000", "h": "מה המשמעות של קילו ביוונית?"},
    {"q": "מה הכוכב הקרוב ביותר לכדור הארץ?", "a": "השמש", "h": "זה למה רואים אותו רוב היממה"},
    {"q": "כמה ימים יש בשנה מעוברת?", "a": "366", "h": "בשנה רגילה יש אחד פחות"},
    {"q": "באיזו יבשת נמצאת ישראל?", "a": "אסיה", "h": "המזרח התיכון"},
    {"q": "מה הצבע שנוצר מערבוב כחול וצהוב?", "a": "ירוק", "h": "צבע הטבע"},
    {'q': 'כמה אותיות יש בא"ב העברי?', "a": "22", "h": "מאלף עד תו"},
    {"q": "מה כוכב הלכת הגדול ביותר במערכת השמש?", "a": "צדק", "h": "האישה תמיד ______"},
    {"q": "כמה צלעות יש לחמשושה?", "a": "5", "h": "כמו כוכב ים"},
    {"q": "מה הבירה של ספרד?", "a": "מדריד", "h": "לא ברצלונה!"},
    {"q": "מה הים הגדול בעולם?", "a": "האוקיינוס השקט", "h": "גדול מכל היבשות יחד"},
    {"q": "כמה שעות יש ביממה?", "a": "24", "h": "חצי עם אור וחצי עם חושך"},
    {'q': 'כמה ק"ג יש בטון?', "a": "1,000", "h": "מה המשמעות של קילו ביוונית?"},
    {"q": "מה הבירה של יפן?", "a": "טוקיו", "h": "אחת הערים הגדולות בעולם"},
    {"q": "מה הצבע שנוצר מערבוב אדום וצהוב?", "a": "כתום", "h": "באנגלית זה גם שם של פרי"},
    {"q": "איזה כיוון השמש שוקעת?", "a": "מערב", "h": "הנגדי למזרח"},
    {"q": "כמה זמן לוקח לאור מהשמש להגיע לכדור הארץ?", "a": "כ-8 דקות", "h": 'מהירות האור 300,000 ק"מ/שנייה'},
    {"q": "מה שם היבשת שבה נמצאות ברזיל וארגנטינה?", "a": "אמריקה הדרומית", "h": "תשובה מלאה בשתי מילים"},
    {"q": "כמה מחזורי דם יש ללב?", "a": "2", "h": "ימנית ושמאלית"},
    {"q": "מה קורה למים ב-100 מעלות צלזיוס?", "a": "רותחים", "h": "גבול בין נוזל לגז"},
    {"q": "כמה עצמות יש בגוף האדם הבוגר?", "a": "206", "h": "תינוק נולד עם יותר"},
    {"q": "מה שם הכוח שמושך חפצים לכדור הארץ?", "a": "כבידה", "h": "ניוטון גילה אותו"},
    {"q": "כמה שעות שינה מומלץ לבוגר בלילה?", "a": "8", "h": "שליש מהיממה"},
    {"q": "מה הקשר המשפחתי של אריה, פנתר וקרקל?", "a": "חתוליים", "h": "כולם שונאים עכברים"},
    {"q": "מה השיא של יוסין בולט בריצת 100 מטר?", "a": "~10 שניות (9.58)", "h": "סופרים אחורה בסילבסטר"},
    {"q": "איזה גז מהווה את רוב האטמוספירה?", "a": "חנקן (78%)", "h": "לא חמצן!"},
    {"q": "כמה מדינות גובלות בישראל?", "a": "4", "h": "גם מספר חברי הביטלס וצבי הנינג'ה"},
    {"q": "מה קורה לנפח של מים כשהם קופאים?", "a": "הם מתרחבים", "h": "לכן בקבוקים מתפוצצים"},
    {"q": "כמה סוגי דם יש?", "a": "שמונה", "h": "לא לשכוח שיש גם + ו-"},
    {"q": "מה שם הגדר הגדולה שנבנתה בסין?", "a": "החומה הגדולה של סין", "h": "נמתחת אלפי קילומטרים"},
    {"q": "מה הבירה של איטליה?", "a": "רומא", "h": "לא מילאנו ולא נאפולי!"},
    {"q": "מה עיר הבירה של פורטוגל?", "a": "ליסבון", "h": "לא פורטו!"},
    {"q": "כמה אצבעות יש לבני אדם בסך הכל?", "a": "20", "h": "ידיים ורגליים"},
    {"q": "איך קוראים לים שנמצא בין ישראל לירדן?", "a": "ים המלח", "h": "אי אפשר לשקוע בו"},
    {"q": "מה האוקיינוס שבין ישראל להודו?", "a": "האוקיינוס ההודי", "h": "שלישי בגודלו"},
    {"q": "איך קוראים לכוכב הכי בוהק בשמיים?", "a": "כוכב הצפון", "h": "רוחות השמיים"},
    {"q": "כמה דקות יש בשעה?", "a": "60", "h": "אותו מספר כמו שניות בדקה"},
    {"q": "מה השפה הנפוצה ביותר בעולם?", "a": "מנדרינית", "h": "שפת סין"},
    {"q": "כמה צלעות יש לאוקטגון?", "a": "8", "h": "זה לא מזכיר לך שם של חיה?"},
    {"q": "באיזה שנה נחנך מגדל אייפל?", "a": "1889", "h": "זה לפני 1900.."},
    {"q": "כמה שחקנים צריך בשביל משחק כדורעף?", "a": "12", "h": "ב-2 קבוצות"},
    {"q": "מה הצבע שנוצר מערבוב לבן ואדום?", "a": "ורוד", "h": "צבע אהבה קלאסי"},
    {"q": "מה המדינה עם הכי הרבה תושבים?", "a": "הודו", "h": "עקפה את סין לאחרונה"},
    {"q": "כמה צלעות יש למשולש?", "a": "3", "h": "כמו הספרה"},
    {"q": "מה הבירה של גרמניה?", "a": "ברלין", "h": "לא מינכן!"},
    {"q": "מה הספורט הפופולרי ביותר בעולם?", "a": "כדורגל", "h": "מונדיאל"},
    {"q": "כמה שנים חוגגים בחתונת כסף?", "a": "25", "h": "1/4 ממאה"},
    {"q": "מה המדינה הגדולה ביותר בעולם?", "a": "רוסיה", "h": "גובלת בכמעט הכל"},
    {"q": "איפה מוצגת המונה ליזה?", "a": "הלובר", "h": "נמצא בפריז"},
    {"q": "כמה צבעים יש בקשת בענן?", "a": "7", "h": "מספר טיפולוגי"},
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
    "חייב לגור ביחד לפני נישואין",
    "עדיף חבר אחד טוב מעשרה מכרים",
    "ריב קטן בריא לזוגיות",
    "צריך לדעת לבשל לפני שנכנסים לזוגיות",
    "עדיף לתת כסף כמתנה מאשר משהו אישי",
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
    "הראשון שמתנצל בויכוח הוא החלש יותר",
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
    "אנשים שלא רוצים ילדים הם אנוכיים",
    "עדיף לגור בשכירות מאשר לקנות דירה",
    "אפשר להיות חבר טוב של ההורים שלך",
    "ספורטאים מרוויחים יותר מדי",
    "מי שלא אוהב קפה לא מתאים לי",
    "סוף טוב בסרט הופך אותו למוצלח",
    "עדיף לעבוד לבד מאשר לעבוד בצוות",
    "אם שניכם עובדים אין סיבה שאחד יבצע יותר מטלות בית",
    "הגיל הוא רק מספר",
    "חשוב לשמור על קשר עם האקסים של ילדיך",
    "חינוך הוא האחריות הכי גדולה של הורים",
    "אפשר לאהוב מישהו ולא להסתדר איתו",
    "שתי שפות הן מינימום לאדם משכיל",
    "הכסף לא קובע את האושר אבל הוא עוזר",
    "אנשים שמגיעים באיחור מעצבנים",
    "ביקורת בונה היא מתנה",
    "מותר לגלות סודות של אחרים לבן/ת הזוג שלי",
    "לגדל חיית מחמד זה כמעט כמו לגדל ילד",
    "הטלפון הוא הדבר שהכי הורס זוגיות",
    "כל אחד יכול להשתנות עם מספיק רצון",
]

S4_BANK = [
    {"q": "מה היית מעדיף/ה לאכול עכשיו?", "o": ["פיצה 🍕", "סושי 🍣", "המבורגר 🍔", "גלידה 🍦"]},
    {"q": "איזה חופשה הכי מושכת אותך?", "o": ["חוף ים 🏖️", "הרים ⛰️", "עיר גדולה 🌆", "לראות נטפליקס בבית 🛋️"]},
    {"q": "איזה ז'אנר סרטים את/ה הכי אוהב/ת?", "o": ["אקשן 💥", "רומנטיקה 💕", "קומדיה 😂", "אימה 👻"]},
    {"q": "מה הכי חשוב בזוגיות?", "o": ["הומור 😂", "כימיה 💫", "ערכים משותפים 🤝", "ביטחון כלכלי 💰"]},
    {"q": "איך נראה הדייט המושלם?", "o": ["מסעדה יוקרתית 🍽️", "טיול בטבע 🌿", "מסיבה עם חברים 🎉", "בישול ביחד 👨‍🍳"]},
    {"q": "איזה בעל חיים היית רוצה להיות?", "o": ["אריה 🦁", "דולפין 🐬", "נשר 🦅", "חתול 🐱"]},
    {"q": "איזה כוח-על היית בוחר/ת?", "o": ["לעוף ✈️", "לקרוא מחשבות 🧠", "לעצור את הזמן ⏸️", "להתחקות ממקום למקום 🌀"]},
    {"q": "איזה ז'אנר מוזיקה את/ה הכי אוהב/ת?", "o": ["פופ 🎤", "ראפ 🎧", "רוק 🎸", "מזרחית 🎵"]},
    {"q": "מה הופך סוף שבוע למושלם?", "o": ["נסיעה ספונטנית 🚗", "פיקניק בפארק 🌳", "ספא וסדרות 🛁", "מסיבה עם חברים 🎊"]},
    {"q": "מה התכונה הכי חשובה בבן/בת זוג?", "o": ["הומור 😄", "יושר 💎", "שאפתנות 🚀", "רגישות 💞"]},
    {"q": "מה הייתם קונים עם מיליון שקל?", "o": ["דירה 🏠", "טיול בעולם ✈️", "רכב יוקרה 🚗", "השקעות 📈"]},
    {"q": "איזה ארוחת בוקר את/ה הכי אוהב/ת?", "o": ["שקשוקה 🍳", "טוסט עם ממרח 🍞", "חביתה עם ירקות 🥗", "קפה ודי ☕"]},
    {"q": "איזה תחביב היית רוצה לפתח?", "o": ["לנגן 🎸", "לצייר ✏️", "לבשל ולאפות 🍰", "לצלם 📸"]},
    {"q": "מה הופך יום חופש למושלם?", "o": ["לישון עד מאוחר 😴", "לצאת לטבע או לים 🌊", "להיות עם האנשים הנכונים 👫", "אוכל טוב וקניות 🛍️"]},
    {"q": "איזה קינוח את/ה הכי אוהב/ת?", "o": ["שוקולד 🍫", "גלידה 🍦", "עוגה 🎂", "פירות טריים 🍓"]},
    {"q": "אם מחר היית מתחיל/ה דיאטה, מה הדבר שהיית אוכל/ת אחרון?", "o": ["פיצה 🍕", "שוקולד 🍫", "צ'יפס 🍟", "המבורגר 🍔"]},
    {"q": "מה הכי מעצבן אותך?", "o": ["איחורים ⏰", "רעש 🔊", "אי-סדר 🗃️", "הודעות קוליות 🎙️"]},
    {"q": "אם היית גיבור/ת סרט – איזה ז'אנר הוא היה?", "o": ["אקשן הירואי ⚔️", "רומנטי קומי 💝", "מסתורין ופשע 🕵️", "פנטזיה ☄️"]},
    {"q": "מה כוח העל האמיתי שלך?", "o": ["אינטליגנציה רגשית 💛", "כושר גופני 💪", "יצירתיות 🎨", "כריזמה ✨"]},
    {"q": "איפה הייתם גרים אם לא בישראל?", "o": ["ניו יורק 🗽", "פריז 🗼", "טוקיו 🏯", "ברצלונה 🌞"]},
    {"q": "מה הייתם מוחקים מהעולם?", "o": ["פקקים 🚗", "מוזיקת מעליות 🎹", "שיחות ספאם 📞", "יתושים 🦟"]},
    {"q": "איזה מקצוע היית בוחר/ת בעולם אחר?", "o": ["שף 👨‍🍳", "אסטרונאוט 🚀", "מוזיקאי/ת 🎼", "ספורטאי/ת 🏅"]},
    {"q": "מה הכי מרגש אותך?", "o": ["הצלחות קטנות ✨", "הפתעות 🎁", "רגעים שקטים 🌙", "אנשים חדשים 🤝"]},
    {"q": "מה הייתם רוצים שהשני/ה יעשה יותר?", "o": ["לומר מחמאות 💬", "לחבק 🤗", "לבשל ביחד 🍳", "לצאת להרפתקאות 🗺️"]},
    {"q": "איזה אמוג'י הכי מתאר אותך?", "o": ["צוחק/ת 😂", "קול 😎", "רגיש/ה 🥺", "נלהב/ת 🔥"]},
    {"q": "מה הייתם שומעים לפני שינה?", "o": ["פודקאסט 🎙️", "מוזיקה שקטה 🎵", "סדרה ברקע 📺", "שקט מוחלט 🤫"]},
    {"q": "מה הדבר הראשון שאת/ה עושה/ה בבוקר?", "o": ["טלפון 📱", "שירותים 🚽", "קפה ☕", "מקלחת 🚿"]},
    {"q": "מה גורם לך להרגיש שסוף השבוע התחיל?", "o": ["לישון מאוחר 💤", "לצאת לברים 🍻", "ספורט בבוקר 🏃", "ארוחת שישי 👨‍👩‍👧"]},
    {"q": "איזו מציאות חלופית היית בוחר/ת?", "o": ["חיים לפני הטלפון 📵", "לחיות בלי להזדקן 🌱", "לא צריך שעות שינה 🌀", "קיץ תמידי ☀️"]},
    {"q": "מה הגהינום הפרטי שלך?", "o": ["ישיבות עבודה ארוכות 😴", "לחכות בתור ⌛", "קבוצות וואטסאפ מיותרות 📱", "לחפש חנייה 🚗"]},
    {"q": "מה הרגש שהכי קשה לך להסתיר?", "o": ["עצב 😢", "כעס 😤", "שמחה 😄", "בושה 😳"]},
    {"q": "איך את/ה מעדיף/ה לפתור ויכוח?", "o": ["לדבר מיד 🗣️", "להתקרר ואחר כך לדבר ❄️", "לכתוב הודעה ✉️", "לשכוח ולהמשיך הלאה 🙃"]},
    {"q": "אם הייתם נעולים יחד שבוע בבית, מה היית עושה?", "o": ["בינג' סדרות 📺", "להתחיל פרויקט ביחד 🔨", "לבשל כל דבר בעולם 🍲", "לישון ולנוח 😴"]},
    {"q": "איזה חוויה יחד הכי חשובה לך?", "o": ['טיול לחו"ל ✈️', "ארוחת ערב רומנטית 🕯️", "הרפתקה בטבע 🏕️", "ערב שקט בבית 🛋️"]},
    {"q": "איך הייתם ממלאים יום שלם בלי אף אחד?", "o": ["יוצא/ת לטייל 🚶", "הולך/ת לישון 😴", "מפתח/ת את התחביבים שלי 🎨", "פשוט משתגע/ת 🤪"]},
    {"q": "איזה ריח הכי מרגיע אותך?", "o": ["קפה ☕", "גשם 🌧️", "אוכל מהתנור 🍞", "ים 🌊"]},
    {"q": "מתי את/ה בשיאך?", "o": ["בוקר מוקדם 🌅", "צהריים ☀️", "ערב 🌆", "לילה 🌙"]},
    {"q": "מה יכול להרוס לך ערב מושלם?", "o": ["ויכוח 🔥", "רעש 🔊", "שינוי תוכניות ברגע האחרון 🔄", "אוכל מבאס במסעדה 🍽️"]},
    {"q": "איזה סגנון תקשורת הכי מתאר אותך?", "o": ["ישיר ולעניין 🎯", "דיפלומטי ורגיש 🤝", "הומוריסטי 😂", "שקט ומאזין 🎧"]},
    {"q": "מה הייתם שואלים אדם חדש שאתם פוגשים?", "o": ["במה אתה עובד? 💼", "מה התחביבים שלך? 🎭", "מאיפה אתה? 🗺️", "מה אתה אוהב לאכול? 🍕"]},
    {"q": "אם הייתם יכולים לחיות בעידן אחר – הייתם בוחרים ב...", "o": ["הרומאים הקדמונים 🏛️", "מסע בין כוכבי עתידי 🚀", "שנות ה-80 🕹️", "המאה ה-19 🎩"]},
    {"q": "מה הדבר שאת/ה הכי גאה בו?", "o": ["הישג אישי 🏆", "מערכת יחסים 💛", "ערך שדבקת בו 🌟", "כישרון מסוים 🎸"]},
    {"q": "איך את/ה מגיב/ה לביקורת?", "o": ["לוקח/ת ללב 💔", "מנתח/ת לעומק 🧠", "מגן/ה על עצמי 🛡️", "מתעלם/ת ומתקדם/ת 🚀"]},
    {"q": "מה מרגיש לך כמו ביזבוז זמן?", "o": ["ישיבות ארוכות שיכלו להיות אימייל 📧", "גלילה בסושיאל 📱", "להיתקע בפקק 🚗", "סרט/סדרה עם סוף גרוע 😑"]},
    {"q": "איזה ילד/ה היית?", "o": ["שקט/ה ומסתגר/ת 📚", "שובב/ה ואנרגטי/ת 🏃", "אמנותי/ת ויצירתי/ת 🎨", "מנהיג/ה חברתי/ת 👑"]},
    {"q": "מה הדבר הראשון שאת/ה שם/ה לב אליו באדם חדש?", "o": ["עיניים 👀", "חיוך 😊", "אופן הדיבור 🗣️", "שפת גוף 🤷"]},
    {"q": "מה יכול להחזיר לך אנרגיה אחרי יום קשה?", "o": ["שינה 😴", "אוכל טוב 🍕", "שיחה עם מישהו קרוב 📞", "בדידות ושקט 🧘"]},
    {"q": "אם היית כותב/ת ספר על חייך, איך הוא היה מתחיל?", "o": ["בהרפתקה 🌍", "ברגע מכונן 🔑", "בהומור 😂", "בתיאור מקום אהוב 🏡"]},
    {"q": "מה הדבר שאת/ה הכי פוחד/ת ממנו?", "o": ["בדידות 🌑", "כישלון 📉", "מחלה 🏥", "לאכזב אחרים 😞"]},
    {"q": "מה מגדיר/ה אותך יותר מכל?", "o": ["המשפחה שלי 👨‍👩‍👧", "העבודה שלי 💼", "הערכים שלי 🌟", "ההישגים שלי 🏆"]},
    {"q": "מה הייתם לובשים לדייט ראשון?", "o": ["חולצה מכופתרת 👔", "ג'ינס וחולצה 👕", "שמלה/חליפה 👗", "מה שנוח 😌"]},
    {"q": "איפה הייתם ישנים בטיול?", "o": ["מלון מפנק 🏨", "אוהל בטבע ⛺", "Airbnb מקומי 🏡", "כל מקום שיש"]},
    {"q": "מה הייתם אוכלים בשישי בבוקר?", "o": ["ארוחת בוקר ישראלית 🥗", "פנקייק 🥞", "אבוקדו טוסט 🥑", "שאריות מאתמול 🍕"]},
    {"q": "מה הייתם עושים עם פרס כספי?", "o": ["טיול חלומות ✈️", "לחסוך 💰", "לתת לצדקה 💝", "לשדרג את הבית 🏠"]},
    {"q": "מה מעצבן אתכם בנסיעה?", "o": ["פקקים 🚗", "גשם/ערפל 🌧️", "צפירות 📯", "רמזורים אדומים 🔴"]},
    {"q": "איזה אפליקציה לא תוכלו לוותר עליה?", "o": ["וואטסאפ 💬", "אינסטגרם 📸", "יוטיוב ▶️", "ספוטיפיי 🎵"]},
    {"q": "מה הייתם עושים עם יום חופש בהפתעה מהעבודה?", "o": ["משלימים שעות שינה 😴", "יום סידורים 📋", "יוצאים לנשום אוויר בטבע 🌿", "נפגשים עם אנשים 🤝"]},
    {"q": "מה הייתם לוקחים לאי בודד?", "o": ["ספר 📚", "גיטרה 🎸", "מצלמה 📷", "אוכל טעים 🍔"]},
    {"q": "מה אתם עושים בדרך כלל כשאתם מחכים בתור למשהו?", "o": ["משחקים בטלפון 🎮", "מסתכלים מסביב 👀", "מדברים עם מישהו 🗣️", "רק מחכים שייגמר 😑"]},
    {"q": "איך אתם ישנים?", "o": ["על הצד ⬅️", "על הגב 🔝", "על הבטן 👇", "בכל תנוחה 🌀"]},
    {"q": "אילו הייתה לכם מכונת זמן – לאן הייתם נוסעים?", "o": ["לעתיד 🚀", "לעבר ההיסטורי 🏛️", "לתקן טעות אישית 🔄", "לראות את הסוף 🔮"]},
    {"q": "מה סגנון הבית שלכם?", "o": ["מינימליסטי 🤍", "צבעוני ומלא 🌈", "וינטג' 🪑", "מודרני ונקי 🏢"]},
    {"q": "איך תגיבו לביקורת על עבודה שלכם?", "o": ["תלמדו ממנה 📝", "תגנו על עצמכם 🛡️", "תכעסו 😤", "תתעלמו 🙃"]},
    {"q": "מה הייתם מזמינים בסוף ארוחה?", "o": ["קפה ☕", "קינוח 🍰", "עוד מנה ראשונה 🍕", "שום דבר, אני כנראה שבע/ה 😌"]},
    {"q": "מה הייתם עושים אחרי ויכוח?", "o": ["מתנצלים מיד 🙏", "מצטננים לבד ❄️", "מדברים 🗣️", "ממשיכים כאילו כלום 😶"]},
    {"q": "איפה הייתם מעדיפים לגור?", "o": ["מרכז עיר 🏙️", "שכונה שקטה 🌳", "כפר 🌾", "חוף ים 🌊"]},
    {"q": "מה הדבר הראשון שאת/ה עושה כשאת/ה מגיע/ה הביתה?", "o": ["מחליף/ת בגדים 👕", "פותח את המקרר 🧊", "מדליק/ה טלוויזיה 📺", "שוכב/ת על הספה 🛋️"]},
    {"q": "מה אתם בדרך כלל קוראים?", "o": ["חדשות 📰", "ספרים 📖", "משהו מקצועי 💼", "לא קוראים הרבה 🙃"]},
    {"q": "איך הייתם מבלים ערב ביחד בבית?", "o": ["סדרה ביחד 📺", "משחק קופסה 🎲", "שיחה ארוכה 💬", "כל אחד בעצמו 🙃"]},
    {"q": "מה הייתם רוצים שבן/בת הזוג ישפר/תשפר?", "o": ["זמן איכות ⏱️", "תקשורת 💬", "רומנטיקה 💕", "עצמאות 🚀"]},
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
        self.s1_streak = 0          # positive = agreement streak, negative = disagreement streak
        self.s1_history = []        # list of {m, f, matched}
        self.s2_history = []        # list of {q, correct, buzzer}
        self.s3_history = []        # list of {q, diff, v1, v2}
        self.s4_history = []        # list of {q, g1ok, g2ok}
        self.pending_next = None    # next stage to go to after summary ack
        self.ll_results = {}       # {1: {receiving:[...], giving:[...]}, 2: {...}}

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
        pts1 = 2
    elif g2ok:
        pts2 = 2
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
    room.pending_next = None
    room.s1_ans = {}
    room.s2_state = {}
    room.s3_ans = {}
    room.s4_state = {}
    room.s1_history = []
    room.s2_history = []
    room.s3_history = []
    room.s4_history = []
    room.s1_streak = 0
    room.players[1]['score'] = 0
    room.players[2]['score'] = 0
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
    if room.pending_next is not None:
        return  # already transitioning to next stage, ignore duplicate
    stage = room.stage
    qs = room.questions[f's{stage}']
    nq = room.q + 1
    if nq >= len(qs):
        next_stage = next_stage_for_mode(room.mode, stage)
        if next_stage >= 5:
            await send_stage_summary(room, stage, next_stage)
        else:
            await send_stage_summary(room, stage, next_stage)
    else:
        await send_question(room, stage, nq)


async def send_stage_summary(room, stage, next_stage):
    room.pending_next = next_stage
    data = build_stage_summary(room, stage)
    await room.broadcast({
        'type': 'stage_summary',
        'stage': stage,
        'next_stage': next_stage,
        **data
    })


def build_stage_summary(room, stage):
    p1n = room.players[1]['name']
    p2n = room.players[2]['name']
    sc = scores_payload(room)

    if stage == 1:
        h = room.s1_history
        total = len(h)
        agreed = sum(1 for x in h if x['matched'])
        if total == 0: return {'stats': '', 'comment': ''}
        pct = round(agreed / total * 100)
        stats = f"{agreed} הסכמות מתוך {total} שאלות ({pct}%)"
        if pct == 100: comment = "הסכמתם על הכל – אחד מכם בטח שיקר 😂"
        elif pct >= 80: comment = f"כמעט זהים. מפחיד קצת, לא? 😏"
        elif pct >= 60: comment = "הסכמתם יותר ממה שחשבתם – ביחד עדיף מלבד 🤝"
        elif pct >= 40: comment = "חצי חצי – זה בדיוק מה שהופך זוגיות למעניינת 😅"
        elif pct >= 20: comment = "הפכים נמשכים? בואו נקוות שכן 😬"
        else: comment = "וואו. זה... מיוחד. שמרו על הניגודים! 🤣"
        return {'stats': stats, 'comment': comment, 'scores': sc}

    elif stage == 2:
        h = room.s2_history
        total = len(h)
        if total == 0: return {'stats': '', 'comment': ''}
        p1_correct = sum(1 for x in h if x['buzzer'] == 1 and x['correct'])
        p2_correct = sum(1 for x in h if x['buzzer'] == 2 and x['correct'])
        p1_buzz = sum(1 for x in h if x['buzzer'] == 1)
        p2_buzz = sum(1 for x in h if x['buzzer'] == 2)
        stats = f"{p1n}: {p1_buzz} לחיצות, {p1_correct} נכון | {p2n}: {p2_buzz} לחיצות, {p2_correct} נכון"
        total_correct = p1_correct + p2_correct
        if total_correct == total: comment = "כל תשובה נכונה! אתם יחד צוות קוויז מנצח 🏆"
        elif total_correct >= total * 0.7: comment = "רוב התשובות היו נכונות – הידע כאן! 💡"
        elif p1_buzz > p2_buzz * 2: comment = f"{p1n} לחץ/ה על הכפתור מהר מדי – לפעמים שתיקה זה ניצחון 😂"
        elif p2_buzz > p1_buzz * 2: comment = f"{p2n} השתלט/ה על הכפתור – מרשים, גם אם לא תמיד צדק/ה 😂"
        else: comment = "המאבק על הכפתור היה שווה – הקרב ממשיך 🔥"
        return {'stats': stats, 'comment': comment, 'scores': sc}

    elif stage == 3:
        h = room.s3_history
        total = len(h)
        if total == 0: return {'stats': '', 'comment': ''}
        bulls = sum(1 for x in h if x['diff'] == 0)
        close = sum(1 for x in h if x['diff'] == 1)
        far = sum(1 for x in h if x['diff'] >= 3)
        stats = f"פגיעה בול: {bulls} | קרוב (מרחק 1): {close} | רחוק (מרחק 3+): {far} מתוך {total}"
        if bulls >= total * 0.6: comment = "אתם חושבים ממש אותו דבר – מי מחשיב מי? 😂"
        elif bulls + close >= total * 0.7: comment = "דעות דומות, עם כמה ניואנסים – בדיוק כמו שצריך 😏"
        elif far >= total * 0.5: comment = "הדעות שלכם... שונות. לגמרי. ועדיין כאן. 🤣"
        else: comment = "יש לכם דעות משלכם, וזה בסדר גמור 😏"
        return {'stats': stats, 'comment': comment, 'scores': sc}

    elif stage == 4:
        h = room.s4_history
        total = len(h)
        if total == 0: return {'stats': '', 'comment': ''}
        g1_right = sum(1 for x in h if x['g1ok'])
        g2_right = sum(1 for x in h if x['g2ok'])
        stats = f"{p1n} ניחש/ה נכון {g1_right} פעמים | {p2n} ניחש/ה נכון {g2_right} פעמים"
        total_right = g1_right + g2_right
        if total_right >= total * 1.5: comment = "אתם מכירים אחד את השני מצוין! 💞"
        elif total_right >= total: comment = "לא רע – חצי הדרך להכרות אמיתית 😄"
        else: comment = "עוד הרבה לגלות אחד על השני – הרפתקה לפניכם 🤷"
        return {'stats': stats, 'comment': comment, 'scores': sc}

    return {'stats': '', 'comment': '', 'scores': scores_payload(room)}


def calc_compatibility(room):
    pcts = []
    if room.s1_history:
        agreed = sum(1 for h in room.s1_history if h['matched'])
        pcts.append(agreed / len(room.s1_history) * 100)
    if room.s3_history:
        close = sum(1 for h in room.s3_history if h['diff'] <= 1)
        pcts.append(close / len(room.s3_history) * 100)
    if room.s4_history:
        correct = sum((1 if h['g1ok'] else 0) + (1 if h['g2ok'] else 0) for h in room.s4_history)
        pcts.append(correct / (len(room.s4_history) * 2) * 100)
    return round(sum(pcts) / len(pcts)) if pcts else 50


def build_final_summary(room, compat, winner):
    p1 = room.players[1]
    p2 = room.players[2]
    lines = []
    # compatibility line
    if compat >= 80: lines.append(f"רמת התאמה {compat}% – שניכם ממש אחד. מפחיד, בצורה הטובה.")
    elif compat >= 65: lines.append(f"רמת התאמה {compat}% – לא תאומים, אבל גם לא מדינות שונות.")
    elif compat >= 50: lines.append(f"רמת התאמה {compat}% – בדיוק מספיק כדי להפוך כל שיחה לעניינית.")
    elif compat >= 35: lines.append(f"רמת התאמה {compat}% – הניגוד ביניכם הוא הדבר הכי מרתק בחדר.")
    else: lines.append(f"רמת התאמה {compat}% – בינתיים. יש עוד הרבה גילויים בדרך.")
    # score line
    s1, s2 = p1['score'], p2['score']
    gap = abs(s1 - s2)
    wn = p1['name'] if winner == 1 else p2['name']
    ln = p2['name'] if winner == 1 else p1['name']
    if winner == 0: lines.append("הניקוד יצא תיקו מושלם – שניכם שווים בדיוק, ומישהו צריך לנצח בפעם הבאה.")
    elif gap <= 3: lines.append(f"{wn} ניצח/ה בהפרש קטן – {ln} כנראה כבר מתכנן/ת נקמה.")
    else: lines.append(f"{wn} ניצח/ה בפרש ניכר – {ln}, יש לנו כמה שאלות.")
    # notable question
    if room.s1_history:
        disagreed = [h for h in room.s1_history if not h['matched']]
        agreed_all = [h for h in room.s1_history if h['matched']]
        if disagreed:
            q = disagreed[0]
            qt = q['m'][:28]
            lines.append(f'על "{qt}..." לא הסכמתם – נושא טוב לשיחה הבאה.')
        elif agreed_all and len(agreed_all) == len(room.s1_history):
            lines.append("הסכמתם על כל שאלה בשלב הראשון. אחד מכם בטח שיקר.")
    elif room.s3_history:
        worst = max(room.s3_history, key=lambda h: h['diff'])
        if worst['diff'] >= 3:
            qt = worst['q'][:28]
            lines.append(f'על "{qt}..." הייתה הדעה הכי שונה – כדאי לשמור לשיחת ערב.')
    # closing
    closings = ["בסך הכל? מומלץ לשחק שוב. עם יין.", "ועכשיו אתם יודעים. ממש יודעים.", "המשחק גמר – הזוגיות ממשיכה. בהצלחה 💑", "המסקנה? שניכם מעניינים. ממש."]
    lines.append(random.choice(closings))
    return lines


def get_highlights(room):
    highlights = {}
    # Most agreed S1
    agreed = [h for h in room.s1_history if h['matched']]
    if agreed:
        highlights['agreed'] = agreed[0]['m'][:40]
    # Most disputed S3
    if room.s3_history:
        worst = max(room.s3_history, key=lambda h: h['diff'])
        if worst['diff'] >= 2:
            highlights['disputed'] = worst['q'][:40]
    # Most disputed S1
    if 'disputed' not in highlights:
        dis = [h for h in room.s1_history if not h['matched']]
        if dis:
            highlights['disputed'] = dis[0]['m'][:40]
    return highlights


async def render_final(room):
    s1 = room.players[1]['score']
    s2 = room.players[2]['score']
    winner = 1 if s1 > s2 else (2 if s2 > s1 else 0)
    compat = calc_compatibility(room)
    summary_lines = build_final_summary(room, compat, winner)
    highlights = get_highlights(room)
    await room.broadcast({
        'type': 'game_over',
        'p1': room.players[1],
        'p2': room.players[2],
        'winner': winner,
        'scores': {'p1': s1, 'p2': s2},
        'compatibility': compat,
        'summary_lines': summary_lines,
        'highlights': highlights
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
        # Track streak
        if match:
            room.s1_streak = max(0, room.s1_streak) + 1
        else:
            room.s1_streak = min(0, room.s1_streak) - 1
        # Track history
        qitem = qs[q]
        room.s1_history.append({'m': qitem['m'], 'f': qitem['f'], 'matched': match})
        # Streak message
        streak_msg = None
        sk = room.s1_streak
        if sk >= 5: streak_msg = "5 הסכמות ברצף! 🏆 כמעט מפחיד כמה אתם דומים"
        elif sk >= 4: streak_msg = "4 ברצף! אתם ממש על אותו גל 💞"
        elif sk >= 3: streak_msg = "3 הסכמות ברצף! 🔥 אתם כאילו חשבתם יחד"
        elif sk <= -5: streak_msg = "5 אי-הסכמות ברצף 😅 אולי כדאי לדבר קצת?"
        elif sk <= -4: streak_msg = "4 ברצף... אחד מכם צריך לוותר 🤔"
        elif sk <= -3: streak_msg = "3 אי-הסכמות ברצף 😬 הניגודים נמשכים?"
        await room.broadcast({
            'type': 'reveal',
            'stage': 1,
            'q': q,
            'qdata': qs[q],
            'answers': {'p1': qd['p1'], 'p2': qd['p2']},
            'pts1': pts1, 'pts2': pts2,
            'match': match,
            'scores': scores_payload(room),
            'streak': room.s1_streak,
            'streak_msg': streak_msg
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
    both_buzzed = 'buzz_ts_1' in qstate and 'buzz_ts_2' in qstate
    time_diff = None
    if both_buzzed:
        time_diff = round(abs(qstate['buzz_ts_1'] - qstate['buzz_ts_2']), 2)
    await room.broadcast({
        'type': 'buzz_result',
        'buzzer': winner,
        'buzzer_name': room.players[winner]['name'],
        'buzzer_gender': room.players[winner]['gender'],
        'q': q,
        'both_buzzed': both_buzzed,
        'time_diff': time_diff
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
    qs = room.questions['s2']
    qs_item = qs[q]
    room.s2_history.append({'q': qs_item['q'], 'correct': correct, 'buzzer': buzzer})
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
        await send_stage_summary(room, stage, next_stage)
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
        room.s3_history.append({'q': qs[q], 'diff': diff, 'v1': v1, 'v2': v2})
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
    # Send guess_phase immediately to this player only (don't wait for partner)
    await ws.send_json({
        'type': 'guess_phase', 'stage': 4, 'q': q,
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
        room.s4_history.append({'q': qs[q]['q'], 'g1ok': g1ok, 'g2ok': g2ok})
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


async def handle_ack_summary(ws, data):
    room, pnum = get_room_and_pnum(ws)
    if not room or pnum != 1:
        return
    next_s = room.pending_next
    if next_s is None:
        return
    room.pending_next = None
    if next_s >= 5:
        await render_final(room)
    else:
        room.stage = next_s
        room.q = 0
        room.intro_acked = False
        await room.broadcast({'type': 'stage_intro', 'stage': next_s})


async def handle_choose_experience(ws, data):
    room, pnum = get_room_and_pnum(ws)
    if not room or pnum != 1:
        return
    experience = data.get('experience', 'zogist')
    if experience == 'love_languages':
        room.ll_results = {}
    await room.broadcast({'type': 'experience_chosen', 'experience': experience})


async def handle_ll_done(ws, data):
    room, pnum = get_room_and_pnum(ws)
    if not room:
        return
    room.ll_results[pnum] = data.get('results', {})
    if len(room.ll_results) == 2:
        await room.broadcast({
            'type': 'll_results',
            'p1': room.ll_results.get(1, {}),
            'p2': room.ll_results.get(2, {}),
            'names': {'p1': room.players[1]['name'], 'p2': room.players[2]['name']}
        })
    # else: first to finish — just wait, no message to partner


async def handle_start_zogist_after_ll(ws, data):
    room, pnum = get_room_and_pnum(ws)
    if not room or pnum != 1:
        return
    await room.broadcast({'type': 'experience_chosen', 'experience': 'zogist'})


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
    'choose_experience': handle_choose_experience,
    'll_done': handle_ll_done,
    'start_zogist_after_ll': handle_start_zogist_after_ll,
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
    'ack_summary': handle_ack_summary,
    'ping': lambda ws, data: None,
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


@app.get("/ping")
async def ping():
    return JSONResponse({"ok": True})

@app.get("/")
async def root():
    return FileResponse("static/index.html")


app.mount("/static", StaticFiles(directory="static"), name="static")
