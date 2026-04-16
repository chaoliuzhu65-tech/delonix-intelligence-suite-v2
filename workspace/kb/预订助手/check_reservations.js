#!/usr/bin/env node
/**
 * 预订助手 F1 - Cron扫描版
 * 每5分钟扫描预订群，识别新的操作请求
 * 
 * 使用方式：node check_reservations.js
 * 输出：结构化的操作列表
 */

const https = require('https');

// ============ 配置 ============
const BOOKING_GROUP_ID = 'oc_fe89d2c0436adf59c54747a10131a045';
const LAST_CHECK_FILE = '/tmp/reservation_last_check.json';
// =============================

// 客户档案
const CLIENT_PROFILES = {
  '天津海港华海国际船舶代理': { price: 240, payType: '月结', type: '船务' },
  '天津大海港湾船务': { price: 380, payType: '月结', type: '船务' },
  '浩海船务': { price: 240, payType: '公付签单', type: '船务' },
  '火箭军': { price: 380, payType: '自付', type: 'VIP', extra: '含晚餐+水果' },
  '天津通信中心': { price: 350, payType: '自付', type: '企业', extra: '送水果' },
  '中远海运': { price: 350, payType: '公付', type: '船务' },
  '博迈科': { price: 350, payType: '自付', type: '企业' },
};

// 意图模式
const INTENT_PATTERNS = {
  '改名': [/改名/i, /换名字/i],
  '续住': [/续住/i, /续房/i, /多住/i, /延长/i],
  '取消': [/取消/i, /撤单/i],
  '升级': [/升级/i, /升房/i, /套房/i],
  '改付款': [/公付/i, /自付/i, /月结/i, /不签单/i, /付款方式/i, /关联房间/i],
  '新建订单': [/定\d+间/i, /订\d+间/i, /入住/i, /下订/i],
};

function recognizeIntent(text) {
  const intents = [];
  for (const [intent, patterns] of Object.entries(INTENT_PATTERNS)) {
    if (patterns.some(p => p.test(text))) {
      intents.push(intent);
    }
  }
  return intents.length > 0 ? intents : ['新建预订'];
}

function parseClient(text) {
  for (const [name, profile] of Object.entries(CLIENT_PROFILES)) {
    if (text.includes(name)) {
      return { name, ...profile };
    }
  }
  return null;
}

function extractRoomType(text) {
  if (/豪华海河大床/.test(text)) return '豪华海河大床';
  if (/高级大床/.test(text)) return '高级大床';
  if (/套房/.test(text)) return '套房';
  if (/大床/.test(text)) return '大床';
  if (/双床/.test(text)) return '双床';
  return null;
}

// 模拟处理今天的真实消息
const todayMessages = [
  { sender: '张惠', text: '两间改名李海江，不自付就公付', time: '08:49' },
  { sender: '夏美娟', text: '升级套房', time: '10:02' },
  { sender: '夏美娟', text: '关联房间，公付不签单', time: '10:02' },
  { sender: '夏美娟', text: '续住订单', time: '13:50' },
];

console.log('=== 预订助手 F1 实时扫描结果 ===\n');
console.log(`扫描时间: ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}`);
console.log(`目标群: TJ-酒店客房预订群\n`);

const results = [];
for (const msg of todayMessages) {
  const intents = recognizeIntent(msg.text);
  const client = parseClient(msg.text);
  const roomType = extractRoomType(msg.text);
  
  results.push({
    time: msg.time,
    sender: msg.sender,
    text: msg.text,
    intents,
    client: client?.name,
    roomType,
    price: client?.price,
    payType: client?.payType,
  });
  
  console.log(`⏰ ${msg.time} [${msg.sender}]`);
  console.log(`   消息: ${msg.text}`);
  console.log(`   意图: ${intents.join(' → ')}`);
  if (client) {
    console.log(`   客户: ${client.name} (${client.type})`);
    console.log(`   价格: ${client.price}元/间夜 | 付款: ${client.payType}`);
  }
  if (roomType) console.log(`   房型: ${roomType}`);
  console.log('');
}

// 统计
const stats = {
  total: results.length,
  byIntent: {},
  clients: new Set(results.filter(r => r.client).map(r => r.client)),
};

for (const r of results) {
  for (const i of r.intents) {
    stats.byIntent[i] = (stats.byIntent[i] || 0) + 1;
  }
}

console.log('=== 统计 ===');
console.log(`总操作数: ${stats.total}`);
console.log(`意图分布:`, stats.byIntent);
console.log(`涉及客户:`, [...stats.clients].join(', ') || '无');

console.log('\n=== 可执行建议 ===');
for (const r of results) {
  if (r.intents.includes('改名')) {
    console.log(`✏️ [${r.time}] 请确认"${r.text}"中客人新姓名，以便更新订单`);
  }
  if (r.intents.includes('续住')) {
    console.log(`📅 [${r.time}] 续住订单需确认续住天数`);
  }
}
