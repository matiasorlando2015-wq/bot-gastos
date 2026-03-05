from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from gastos import cargar_gasto, resumen_mes_actual


TOKEN = "8442795480:AAEIJt3bWL3_EX4MRtdKcv4UGy2ZKiNuOLY"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot de contabilidad activo\n"
        "Comandos:\n"
        "cargar: /c\n"
        "Ver datos: /d\n"
        "Ver archivos: /b"
    )

async def datos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resumen = resumen_mes_actual()
    await update.message.reply_text(resumen)

async def gasto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    # 1. cantidad de argumentos
    if len(args) != 3:
        await update.message.reply_text(
            "❌ Formato incorrecto\n"
            "Usá: /gasto monto categoria medio\n"
            "Ej: /gasto 2500 comida mp"
        )
        return

    # 2. monto válido
    try:
        monto = int(args[0])
        if monto <= 0:
            raise ValueError
    except ValueError:
        await update.message.reply_text("❌ El monto debe ser un número mayor a 0")
        return

    categoria = args[1].lower()
    medio = args[2].lower()

    # 3. ejecutar lógica
    try:
        cargar_gasto(monto, categoria, medio)
    except ValueError as e:
        await update.message.reply_text(f"❌ {str(e)}")
        return

    # 4. OK
    await update.message.reply_text(
        f"✅ Gasto cargado\n"
        f"${monto} – {categoria} – {medio}"
    )

async def backup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    with open("datos.json", "rb") as f:
        await update.message.reply_document(f)

    with open("Gastos.txt", "rb") as f:
        await update.message.reply_document(f)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("d", datos))
app.add_handler(CommandHandler("c", gasto))
app.add_handler(CommandHandler("b", backup))

print("🤖 Bot corriendo...")
app.run_polling()

# python bot.py