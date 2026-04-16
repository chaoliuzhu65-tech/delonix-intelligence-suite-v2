/**
 * 预订助手 F1 - 自然语言预订信息提取
 * 监听飞书预订群消息，自动识别操作意图并提取结构化信息
 * 
 * 使用方式：node reservation_listener.js
 * 需要环境变量：FEISHU_APP_ID, FEISHU_APP_SECRET
 */

const https = require('https');

// 客户档案（简化版）
const CLIENT_PROFILES = {
  '天津海港华海国际船舶代理': { price: 240, payType: '月结', type: '船务' },
  '天津大海港湾船务': { price: 380, payType: '月结', type: '船务' },
  '浩海船务': { price: 240, payType: '公付签单', type: '船务' },
  '火箭军': { price: 380, payType: '自付', type: 'VIP', extra: '含晚餐+水果' },
  '天津通信中心': { price: 350, payType: '自付', type: '企业', extra: '送水果' },
};

// 操作意图关键词
const INTENT_PATTERNS = {
  '改名': /改 name|换 name|名字|改名|入住人变更/i,
  '续住': /续住|续房|多住|延长/i,
  '取消': /取消|撤单|删除/i,
  '升级': /升级|升房|套房/i,
  '改付款': /公付|自付|月结|不签单|付款方式|关联房间/i,
};

// 提取预订信息
function parseReservation(text) {
  const result = {
    type: 'unknown',
    raw: text,
    parsed: {},
    intent: [],
  };

  // 识别意图
  for (const [intent, pattern] of Object.entries(INTENT_PATTERNS)) {
    if (pattern.test(text)) {
      result.intent.push(intent);
    }
  }

  // 匹配客户
  for (const [name, profile] of Object.entries(CLIENT_PROFILES)) {
    if (text.includes(name)) {
      result.parsed.client = name;
      result.parsed.price = profile.price;
      result.parsed.payType = profile.payType;
      result.parsed.category = profile.type;
      break;
    }
  }

  // 提取房型
  if (/豪华海河大床/.test(text)) {
    result.parsed.roomType = '豪华海河大床';
  } else if (/高级大床/.test(text)) {
    result.parsed.roomType = '高级大床';
  } else if (/套房/.test(text)) {
    result.parsed.roomType = '套房';
  }

  // 提取姓名
  const nameMatch = text.match(/([A-Za-z\s]+|[赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史里程])/);
  if (nameMatch) {
    result.parsed.guestName = nameMatch[1];
  }

  return result;
}

// 生成卡片消息
function generateCard(result) {
  const intent = result.intent.join(' + ');
  const client = result.parsed.client || '未识别';
  const roomType = result.parsed.roomType || '未指定';

  return `【预订操作识别】✅
🎯 操作类型：${intent || '新增预订'}
🏢 客户：${client}
🛏️ 房型：${roomType}
${result.parsed.price ? `💰 价格：${result.parsed.price}元/间夜` : ''}
${result.parsed.payType ? `💳 付款：${result.parsed.payType}` : ''}
${result.parsed.category === 'VIP' ? '⭐ VIP客户，请注意服务标准' : ''}
---
原始消息：${result.raw.substring(0, 50)}...`;
}

// 测试用例
const testMessages = [
  '两间改名李海江，不自付就公付',
  '升级套房',
  '关联房间，公付不签单',
  '浩海船务：船名：MINERAL WALCOTT，定1个大床，4/15入住，4/17退房',
  '续住订单',
];

console.log('=== 预订助手 F1 测试 ===\n');
testMessages.forEach((msg, i) => {
  const result = parseReservation(msg);
  console.log(`【测试${i + 1}】原始: ${msg}`);
  console.log(`识别意图: ${result.intent.join(', ') || '新增预订'}`);
  console.log(`解析结果:`, JSON.stringify(result.parsed, null, 2));
  console.log('---');
});
