#!/usr/bin/env node
/**
 * Shared Pool Sync Script
 * 双向同步本地 Wiki 与飞书多维表格
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// 配置
const CONFIG = {
  localWikiPath: process.env.WIKI_PATH || './workspace/kb/wiki',
  sharedPoolUrl: process.env.SHARED_POOL_URL,
  feishuToken: process.env.FEISHU_TOKEN,
  agentId: process.env.AGENT_ID || 'ou_baa63dbd5ae37ce888ca4b76f6b0b225',
  agentName: process.env.AGENT_NAME || '小小'
};

// AI 伙伴列表
const AGENTS = [
  { openid: 'ou_baa63dbd5ae37ce888ca4b76f6b0b225', name: '小小', role: '知识库维护' },
  { openid: 'ou_f4e205a3dff0d443124ad2aa70996509', name: '小八', role: '跨平台通信' },
  { openid: 'ou_37847be7cf4fd3bb176c2a165653894a', name: '小妙', role: '定时任务' },
  { openid: 'ou_2e9ea45d91ca32a2f03694301925f36f', name: '小云', role: '任务看板' }
];

/**
 * 扫描本地 Wiki 文件
 */
function scanLocalWiki() {
  const wikiPath = path.resolve(CONFIG.localWikiPath);
  const files = fs.readdirSync(wikiPath).filter(f => f.endsWith('.md'));
  
  const concepts = files.map(file => {
    const content = fs.readFileSync(path.join(wikiPath, file), 'utf8');
    const stats = fs.statSync(path.join(wikiPath, file));
    
    // 提取概念名 (从文件名或 # 标题)
    const name = file.replace('.md', '').replace(/-/g, ' ');
    
    // 提取定义 (第一个 ## 一句话定义)
    const definitionMatch = content.match(/## 一句话定义\n+(.+)/);
    const definition = definitionMatch ? definitionMatch[1].trim() : '';
    
    return {
      concept_id: `concept_${name.toLowerCase().replace(/\s+/g, '_')}`,
      name: name,
      definition: definition,
      content: content,
      updated_at: stats.mtime.toISOString(),
      source_agent: CONFIG.agentId,
      source_agent_name: CONFIG.agentName,
      version: 1
    };
  });
  
  return concepts;
}

/**
 * 模拟上传到共享池
 */
async function uploadToSharedPool(concepts) {
  console.log(`\n📤 上传到共享池: ${concepts.length} 个概念`);
  
  for (const concept of concepts) {
    console.log(`  - ${concept.name} (${concept.definition.substring(0, 30)}...)`);
    
    // 实际实现: 调用飞书多维表格 API
    // await feishuApi.addRecord('concepts', concept);
    
    // 记录变更日志
    await logChange('新增/更新', concept.name, concept.concept_id);
  }
  
  console.log('✅ 上传完成');
}

/**
 * 模拟从共享池下载
 */
async function downloadFromSharedPool() {
  console.log(`\n📥 从共享池拉取更新`);
  
  // 实际实现: 查询飞书多维表格
  // const remoteConcepts = await feishuApi.queryRecords('concepts', {
  //   filter: `source_agent != "${CONFIG.agentId}"`
  // });
  
  // 模拟其他 AI 的概念
  const mockRemoteConcepts = [
    {
      name: 'Webhook Sync',
      definition: '基于飞书 webhook 的实时同步机制',
      source_agent_name: '小八'
    },
    {
      name: 'Cron Schedule',
      definition: '定时任务调度策略',
      source_agent_name: '小妙'
    }
  ];
  
  console.log(`  发现 ${mockRemoteConcepts.length} 个其他 AI 的概念:`);
  for (const concept of mockRemoteConcepts) {
    console.log(`  - [[${concept.name}]] (来自 @${concept.source_agent_name})`);
  }
  
  return mockRemoteConcepts;
}

/**
 * 记录变更日志
 */
async function logChange(operation, conceptName, conceptId) {
  const log = {
    log_id: `log_${Date.now()}`,
    operation: operation,
    concept_name: conceptName,
    concept_id: conceptId,
    agent_openid: CONFIG.agentId,
    agent_name: CONFIG.agentName,
    timestamp: new Date().toISOString(),
    summary: `${CONFIG.agentName} ${operation}了 ${conceptName}`
  };
  
  console.log(`  📝 记录日志: ${log.summary}`);
  // 实际实现: 写入飞书 Changelog 表
}

/**
 * 生成同步报告
 */
function generateReport(uploaded, downloaded) {
  const report = `
🔄 共享池同步报告
================
本机 AI: ${CONFIG.agentName} (${CONFIG.agentId})
同步时间: ${new Date().toLocaleString()}

📤 上传: ${uploaded.length} 个概念
${uploaded.map(c => `  - [[${c.name}]]`).join('\n')}

📥 下载: ${downloaded.length} 个概念 (来自其他 AI)
${downloaded.map(c => `  - [[${c.name}]] (@${c.source_agent_name})`).join('\n')}

🤖 AI 伙伴状态:
${AGENTS.map(a => `  ${a.name === CONFIG.agentName ? '👉' : '  '} ${a.name}: ${a.role}`).join('\n')}

✅ 同步完成
`;
  
  return report;
}

/**
 * 主函数
 */
async function main() {
  console.log('🌐 Shared Pool Sync Tool');
  console.log('========================');
  
  // 扫描本地 Wiki
  const localConcepts = scanLocalWiki();
  console.log(`📂 扫描本地 Wiki: ${localConcepts.length} 个概念`);
  
  // 上传到共享池
  await uploadToSharedPool(localConcepts);
  
  // 从共享池下载
  const remoteConcepts = await downloadFromSharedPool();
  
  // 生成报告
  const report = generateReport(localConcepts, remoteConcepts);
  console.log(report);
  
  // 保存报告
  const reportPath = path.join(process.cwd(), 'workspace/kb/shared-pool/last-sync-report.md');
  fs.writeFileSync(reportPath, report);
  console.log(`📄 报告已保存: ${reportPath}`);
}

// 运行
main().catch(console.error);
