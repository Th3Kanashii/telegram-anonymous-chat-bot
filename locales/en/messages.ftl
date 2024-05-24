welcome = 🥰 <b>Welcome to the anonymous chat, { $name }!
          ❤️ Here you can freely express your thoughts and share emotions.
          🌟 Brighten up your day by discussing something interesting here!

          ❓ Full bot functionality: /help
          (clickable command)</b>

help = 😍 <b>{ $name }, commands:

        🌐 /language | <code>language</code> ❯ change language
        👤 /profile | <code>profile</code> ❯ check your profile
        🔗 /link | <code>link</code> ❯ send a link to your profile
        🔍 /search | <code>search</code> ❯ search for a conversation partner
        ➡️ /next | <code>next</code> ❯ next conversation partner
        🛑 /stop | <code>stop</code> ❯ stop searching
        💌 /chan | <code>chan</code> ❯ get a cute picture
        🎲 /dice | <code>dice</code> ❯ roll the dice
        🏆 /top | <code>top</code> ❯ user ranking

        🔗 Project link: <a href='https://github.com/Th3Kanashii/telegram-anonymous-chat-bot'>GitHub</a></b>

language = 🌐 <b>{ $name }, what language would you like me to speak?</b>

profile = 👤 <b>{ $name }, <u>Your</u> profile:
          🆔 ❯ <code>{ $id }</code>

          💰 Balance: { $balance } cookies

          📆 Registration Date: { DATETIME($date) }</b>

dice = 🎲 <b><u>Your</u> roll: <code>{ $number }</code>
       💰 Your balance: <code>{ $balance }</code>

       🪑 Your position in top: { $position }</b>

top = 🍪 { $name }, top cookie earners 🍪

      { $tops }
      ❤️ Total users: { $users }
      🪑 Your position in top: { $position }

command-language = 🌐 Change language
command-profile = 👤 Your profile
command-link = 🔗 Send you're profile link a companion
command-search = 🔍 Search for conversation partner
command-next = ➡️ Next conversation partner
command-stop = 🛑 Stop search or dialogue
command-chan = 💌 Send chan
command-dice = 🎲 Roll the dice
command-top = 🏆 Top cookie earners

search-btn = ☕ Search companion
cancel-btn = ⏹️ End dialogue
stop-btn = 🛑 Cancel search
next-btn = ➡️ Next companion
profile-btn = 🔓 Open profile
close-profile-btn = 🔒 Close profile

search-not-started = 🔍 <b>Start searching for a conversation partner!</b>
looking-for-a-companion= 🔍 <b>Already looking for <u>you</u> a conversation partner...</b>
search-companion = 🔍 <b>Searching for <u>you</u> a conversation partner...</b>
next-companion = 🔍 <b>Searching for <u>you</u> a new conversation partner...</b>
stop-companion = 😔 <b>That's it.. I won't look for anyone else!</b>
block-companion = 😔 <b>Oops! It seems the interlocutor has blocked the bot</b>
profile-opened = 🔓 Profile opened
profile-closed = 🔒 Profile closed

found-companion = 🎁 <b>Found <u>you</u> a conversation partner, enjoy chatting!</b>
chat-with-companion = 💬 <b>You already have a conversation partner!</b>

send-link = 🔗 <b>Your conversation partner has sent a link to their profile!</b>
companion-linked = 🔗 <b>Link to your profile sent!</b>

you-leave = 🕊 <b><u>You</u> left the chat!</b>
companion-leave = 🕊 <b>Your conversation partner left the chat!
                  🔍 Searching for <u>you</u> a new conversation partner...</b>

not-enough-balance = 😔 <b>{ $name }, insufficient cookies
                     💸 Needed: 999 cookies
                     🍪 Balance: { $balance } cookies

                     🎲 Play dice (/dice) to earn cookies</b> 🍪

chans-info =
    { NUMBER($chan) ->
        [0] <b>Hello, my darling! 💖🌟 I'm Orumiru, your unique companion in the world of refined emotions and elegant passion. My lips promise sweet moments, and my expressive eyes will take you beyond the ordinary. Ready to experience the heat of our shared adventures? 💋✨ Let's embark on a journey of unforgettable experiences together! #OrumiruChan #EmotionalElevation #SharedPath</b>
        [1] <b>Hello, my enchanter! 💫💋 I'm Neko, your mysterious companion in the world of secrets and open allure. My fiery eyes will tell you many stories, and my grace will enchant your heart. Ready to delve into a world of mysteries and unforgettable experiences? 🔥💖 Let's deepen the charms together! #NekoChan #MysteriousGrace #SharedAdventures</b>
        *[other] <b>Hello, my sweetie! 💋🌟 I'm Kuro, your special magic in the world of the finest delights. My eyes sparkle, awaiting you, and fragments of my smile will lead you to the edge of exquisite pleasure. Let's make every moment together special, filled with magic and tenderness. 💖✨ Ready to take my hand and embark on a journey of unforgettable experiences? 🔥🌹 #KuroChan #YourSweetPleasure #SharedJourney</b>
    }
