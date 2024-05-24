welcome = 🥰 <b>匿名チャットへようこそ、{ $name }さん！
          ❤️ ここでは自由に考えを表現し、感情を共有することができます。
          🌟 何か面白いことを話して、日々を輝かせましょう！

          ❓ ボットの完全な機能：/help
          (クリック可能なコマンド)</b>

help = 😍 <b>{ $name }さん、コマンド:

        🌐 /language | <code>言語</code> ❯ 言語を変更する
        👤 /profile | <code>プロフィール</code> ❯ 自分のプロフィールをチェックする
        🔗 /link | <code>リンク</code> ❯ 自分のプロフィールへのリンクを送信する
        🔍 /search | <code>検索</code> ❯ 会話相手を検索する
        ➡️ /next | <code>次へ</code> ❯ 次の会話相手に移動する
        🛑 /stop | <code>停止</code> ❯ 検索を停止する
        💌 /chan | <code>ちゃん</code> ❯ かわいい画像を受け取る
        🎲 /dice | <code>サイコロ</code> ❯ サイコロを振る
        🏆 /top | <code>トップ</code> ❯ ユーザーのランキング

        🔗 プロジェクトのリンク： <a href='https://github.com/Th3Kanashii/telegram-anonymous-chat-bot'>GitHub</a></b>

language = 🌐 <b>{ $name }、私はどの言語で話すことを望みますか？</b>

profile = 👤 <b>{ $name }, <u>あなたの</u>プロフィール:
          🆔 ❯ <code>{ $id }</code>

          💰 バランス: { $balance } クッキー

          📆 登録日: { DATETIME($date) }</b>

dice = 🎲 <b><u>あなた</u>の出目: <code>{ $number }</code>
       💰 あなたのバランス: <code>{ $balance }</code>

       🪑 トップでのあなたの位置: { $position }</b>

top = 🍪 { $name }, クッキーのトップ 🍪

      { $tops }
      ❤️ 総ユーザー数: { $users }
      🪑 トップでのあなたの位置: { $position }

command-language = 🌐 言語を変更
command-profile = 👤 あなたのプロフィール
command-link = 🔗 あなたのプロフィールへのリンクを会話相手に送信
command-search = 🔍 会話相手を検索
command-next = ➡️ 次の会話相手
command-stop = 🛑 検索または対話を停止
command-chan = 💌 ひよこを送る
command-dice = 🎲 サイコロを振る
command-top = 🏆 クッキーのトップ

search-btn = ☕ 対話者を検索する
cancel-btn = ⏹️ 対話をやめてください
stop-btn = 🛑 検索をキャンセルする
next-btn = ➡️ 次の対談者は
profile-btn = 🔓 プロフィールを開く
close-profile-btn = 🔒 プロフィールを閉じる

search-not-started = 🔍 <b>相手を検索していません。</b>
looking-for-a-companion= 🔍 <b>すでに相手を探しています。</b>
search-companion = 🔍 <b>相手を探しています。</b>
next-companion = 🔍 <b>新しい相手を探しています...</b>
stop-companion = 😔 <b>以上です。誰も探さないよ！</b>
block-companion = 😔 <b>おっと！相手がボットをブロックしたようです</b>
profile-opened = 🔓 プロフィールが公開されています
profile-closed = 🔒 プロフィールは閉じられました

found-companion = 🎁 <b>相手が見つかりました。楽しい会話を!</b>
chat-with-companion = 💬 <b>すでに相手がいます。</b>

send-link = 🔗 <b>相手がプロフィールのリンクを送信しました!</b>
companion-linked = 🔗 <b>プロフィールのリンクが送信されました!</b>

you-leave = 🕊 <b>チャットを退出しました!</b>
companion-leave = 🕊 <b>相手がチャットを退出しました。
                  🔍 新しい相手を探しています...</b>

not-enough-balance = 😔 <b>{ $name }、クッキーが不足しています
                     💸 必要数: 999 クッキー
                     🍪 口座残高: { $balance } クッキー

                     🎲 サイコロ (/dice) をプレイして、 クッキー</b> を獲得します 🍪

chans-info =
    { NUMBER($chan) ->
        [0] <b>こんにちは、私のかわいい人！ 💖🌟 私はオルミル、洗練された感情とエレガントな情熱の世界であなたのユニークな仲間です。私の唇は甘い瞬間を約束し、鮮明な目はあなたを普通の範囲を超えさせます。私たちの共有冒険の熱を感じる準備ができていますか？ 💋✨ 一緒に忘れられない体験の世界に旅立ちましょう！ #オルミルちゃん #感情の高揚 #共有の道</b>
        [1] <b>こんにちは、私の魔法使い！ 💫💋 私はネコ、秘密と開かれた魅力の世界であなたの神秘的な仲間です。私の火のような目がたくさんの物語を語り、私の優雅さがあなたの心を魅了します。謎と忘れられない体験の世界に没頭する準備はできていますか？ 🔥💖 魅力を一緒に深めましょう！ #ネコちゃん #神秘的な優雅さ #共有の冒険</b>
        *[other] <b>こんにちは、私の甘い人！ 💋🌟 私はクロ、最高の喜びの世界であなたの特別な魔法です。私の目はあなたを待って輝き、私の笑顔のかけらがあなたを洗練された喜びの果てに導きます。一緒に、特別で魔法的、優しさに満ちた瞬間を作りましょう。 💖✨ 私の手を取って、忘れられない体験の旅に出かける準備はできていますか？ 🔥🌹 #クロちゃん #あなたの甘い喜び #共有の旅</b>
    }
