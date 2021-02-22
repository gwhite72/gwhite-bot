const Discord = require('discord.js');
const { token } = require('./token.json');
const client = new Discord.Client();

// 連上線時的事件
client.on('ready', () => {
    console.log(`Logged in as ${client.user.tag}!`);
});

// 當 Bot 接收到訊息時的事件
client.on('message', msg => {
    // 如果訊息的內容是 'ping'
    if (msg.content === 'G白好可愛') {
        // 則 Bot 回應 'Pong'
        msg.reply('我他喵喵的不可愛啦ヽ(#`Д´)ﾉ');
    }
	if (msg.content === 'G白好好吃') {
        // 則 Bot 回應 'Pong'
        msg.reply('我不好吃！OAQ');
    }
	if (msg.content === 'G白好好吃~') {
        // 則 Bot 回應 'Pong'
        msg.reply('我不好吃！OAQ');
    }
	if (msg.content === 'G白好好吃~~') {
        // 則 Bot 回應 'Pong'
        msg.reply('我不好吃！OAQ');
    }
	if (msg.content === 'G白好好吃~~~') {
        // 則 Bot 回應 'Pong'
        msg.reply('我不好吃！然後不要再加波浪弧了啦');
    }
	if (msg.content === 'G白好可愛~') {
        // 則 Bot 回應 'Pong'
        msg.reply('我就說我不可愛了齁！(#`Д´)ﾉ');
    }
	if (msg.content === 'G白好可愛~~') {
        // 則 Bot 回應 'Pong'
        msg.reply('不要一直加波浪弧啦！OAQQ');
    }
	if (msg.content === '晚安') {
        // 則 Bot 回應 'Pong'
        msg.reply('晚安晚安~OuO');
    }
	if (msg.content === '晚安~') {
        // 則 Bot 回應 'Pong'
        msg.reply('晚安祝你睡得好(*´∀`)~♥');
    }
	if (msg.content === '晚安晚安') {
        // 則 Bot 回應 'Pong'
        msg.reply('晚安~記得要刷牙再睡哦♥(´∀` )人');
    }
	if (msg.content === '你們好奇怪') {
        // 則 Bot 回應 'Pong'
        msg.reply('對啊！除了你以外的人都好奇怪(´・ω・`)');
    }
	if (msg.content === '居白好可愛') {
        // 則 Bot 回應 'Pong'
        msg.reply('我他喵喵喵的不可愛啦ヽ(#`Д´)ﾉ');
    }
	if (msg.content === '居白') {
        // 則 Bot 回應 'Pong'
        msg.reply('好可愛(ﾟ∀ﾟ)');
    }
	if (msg.content === 'G白') {
        // 則 Bot 回應 'Pong'
        msg.reply('好可愛(ﾟ∀ﾟ)');
    }
	if (msg.content === '居白好可愛~') {
        // 則 Bot 回應 'Pong'
        msg.reply('他也很受哦~(ﾟ∀。)');
    }

});

client.login(token);
