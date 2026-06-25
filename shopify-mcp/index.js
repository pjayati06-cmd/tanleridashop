const fs = require('fs');
const path = require('path');
const readline = require('readline');

// Load environment variables from .env files
function loadEnv() {
  const paths = [
    path.join(__dirname, '.env'),
    path.join(__dirname, '..', '.env'),
    path.join(__dirname, '..', '.env.local')
  ];
  for (const p of paths) {
    if (fs.existsSync(p)) {
      const content = fs.readFileSync(p, 'utf-8');
      for (const line of content.split('\n')) {
        const trimmed = line.trim();
        if (trimmed && !trimmed.startsWith('#')) {
          const parts = trimmed.split('=');
          if (parts.length >= 2) {
            const key = parts[0].trim();
            const val = parts.slice(1).join('=').trim().replace(/^['"]|['"]$/g, '');
            process.env[key] = val;
          }
        }
      }
    }
  }
}
loadEnv();

// Logging to stderr so it doesn't mess up stdout (which is for JSON-RPC only)
function log(msg) {
  process.stderr.write(`[Shopify MCP] ${msg}\n`);
}

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false
});

rl.on('line', (line) => {
  if (!line.trim()) return;
  try {
    const request = JSON.parse(line);
    handleRequest(request);
  } catch (err) {
    sendError(null, -32700, "Parse error");
  }
});

function sendResponse(id, result) {
  console.log(JSON.stringify({
    jsonrpc: "2.0",
    id,
    result
  }));
}

function sendError(id, code, message, data) {
  console.log(JSON.stringify({
    jsonrpc: "2.0",
    id,
    error: { code, message, data }
  }));
}

async function handleRequest(req) {
  const { id, method, params } = req;
  
  if (method === 'initialize') {
    sendResponse(id, {
      protocolVersion: "2024-11-05",
      capabilities: {
        tools: {}
      },
      serverInfo: {
        name: "shopify-mcp",
        version: "1.0.0"
      }
    });
    return;
  }
  
  if (method === 'notifications/initialized') {
    return;
  }
  
  if (method === 'ping') {
    sendResponse(id, {});
    return;
  }
  
  if (method === 'tools/list') {
    sendResponse(id, {
      tools: [
        {
          name: "get_theme_files",
          description: "List all asset files in the Shopify theme",
          inputSchema: {
            type: "object",
            properties: {}
          }
        },
        {
          name: "get_theme_file",
          description: "Get the content of a specific asset file in the Shopify theme",
          inputSchema: {
            type: "object",
            properties: {
              asset_key: {
                type: "string",
                description: "The key of the asset (e.g. 'sections/atelier-hero.liquid')"
              }
            },
            required: ["asset_key"]
          }
        },
        {
          name: "update_theme_file",
          description: "Create or update an asset file in the Shopify theme",
          inputSchema: {
            type: "object",
            properties: {
              asset_key: {
                type: "string",
                description: "The key of the asset (e.g. 'sections/atelier-hero.liquid')"
              },
              value: {
                type: "string",
                description: "The content of the asset file"
              }
            },
            required: ["asset_key", "value"]
          }
        },
        {
          name: "delete_theme_file",
          description: "Delete an asset file from the Shopify theme",
          inputSchema: {
            type: "object",
            properties: {
              asset_key: {
                type: "string",
                description: "The key of the asset to delete"
              }
            },
            required: ["asset_key"]
          }
        }
      ]
    });
    return;
  }
  
  if (method === 'tools/call') {
    const { name, arguments: args } = params;
    try {
      const result = await callTool(name, args);
      sendResponse(id, result);
    } catch (err) {
      sendError(id, -32603, err.message);
    }
    return;
  }
  
  sendError(id, -32601, `Method not found: ${method}`);
}

async function callTool(name, args) {
  loadEnv();
  
  const storeDomain = process.env.SHOPIFY_STORE_DOMAIN || 'tan-lerida.myshopify.com';
  const themeId = process.env.SHOPIFY_THEME_ID || '197507121233';
  const accessToken = process.env.SHOPIFY_ADMIN_API_ACCESS_TOKEN;
  
  if (!accessToken || accessToken === 'shpat_your_token_here') {
    throw new Error("Shopify Admin API Access Token is not set in environment or .env file. Please configure the token.");
  }
  
  const isSimulation = accessToken.startsWith('shpat_internal') || accessToken.startsWith('shpss_');
  
  if (isSimulation) {
    return handleSimulation(name, args);
  }
  
  // Real Shopify API integration
  const headers = {
    "X-Shopify-Access-Token": accessToken,
    "Content-Type": "application/json"
  };
  
  let domain = storeDomain;
  if (!domain.includes('.')) {
    domain = `${domain}.myshopify.com`;
  }
  
  const baseUrl = `https://${domain}/admin/api/2024-01/themes/${themeId}/assets.json`;
  
  if (name === 'get_theme_files') {
    log("Fetching list of files in theme...");
    const res = await fetch(baseUrl, { headers });
    if (!res.ok) {
      const errText = await res.text();
      throw new Error(`Shopify API error (${res.status}): ${errText}`);
    }
    const data = await res.json();
    return {
      content: [{ type: "text", text: JSON.stringify(data.assets || [], null, 2) }]
    };
  }
  
  if (name === 'get_theme_file') {
    const key = args.asset_key;
    log(`Fetching file content for key: ${key}`);
    const url = `${baseUrl}?asset[key]=${encodeURIComponent(key)}`;
    const res = await fetch(url, { headers });
    if (!res.ok) {
      const errText = await res.text();
      throw new Error(`Shopify API error (${res.status}): ${errText}`);
    }
    const data = await res.json();
    return {
      content: [{ type: "text", text: JSON.stringify(data.asset || {}, null, 2) }]
    };
  }
  
  if (name === 'update_theme_file') {
    const key = args.asset_key;
    const val = args.value;
    log(`Updating file content for key: ${key}`);
    const res = await fetch(baseUrl, {
      method: 'PUT',
      headers,
      body: JSON.stringify({ asset: { key, value: val } })
    });
    if (!res.ok) {
      const errText = await res.text();
      throw new Error(`Shopify API error (${res.status}): ${errText}`);
    }
    const data = await res.json();
    return {
      content: [{ type: "text", text: JSON.stringify(data.asset || {}, null, 2) }]
    };
  }
  
  if (name === 'delete_theme_file') {
    const key = args.asset_key;
    log(`Deleting file: ${key}`);
    const url = `${baseUrl}?asset[key]=${encodeURIComponent(key)}`;
    const res = await fetch(url, { method: 'DELETE', headers });
    if (!res.ok) {
      const errText = await res.text();
      throw new Error(`Shopify API error (${res.status}): ${errText}`);
    }
    const data = await res.json();
    return {
      content: [{ type: "text", text: JSON.stringify(data || {}, null, 2) }]
    };
  }
  
  throw new Error(`Tool not found: ${name}`);
}

// Handles local simulation of the Shopify theme repository
function handleSimulation(name, args) {
  const simDir = path.join('c:/Open code AI', 'simulated_shopify');
  fs.mkdirSync(simDir, { recursive: true });
  
  log(`[Simulation Mode] Executing tool: ${name}`);
  
  if (name === 'get_theme_files') {
    const files = [];
    function scan(dir, base = '') {
      if (!fs.existsSync(dir)) return;
      const items = fs.readdirSync(dir);
      for (const item of items) {
        const fullPath = path.join(dir, item);
        const relativeKey = base ? `${base}/${item}` : item;
        const stat = fs.statSync(fullPath);
        if (stat.isDirectory()) {
          scan(fullPath, relativeKey);
        } else {
          files.push({
            key: relativeKey.replace(/\\/g, '/'),
            public_url: null,
            created_at: stat.birthtime.toISOString(),
            updated_at: stat.mtime.toISOString(),
            content_type: relativeKey.endsWith('.css') ? 'text/css' : 'text/plain',
            size: stat.size
          });
        }
      }
    }
    scan(simDir);
    
    // Fallback default assets if directory is empty
    if (files.length === 0) {
      files.push({ key: "layout/theme.liquid", size: 1000 });
      files.push({ key: "sections/header.liquid", size: 500 });
    }
    
    return {
      content: [{ type: "text", text: JSON.stringify(files, null, 2) }]
    };
  }
  
  if (name === 'get_theme_file') {
    const key = args.asset_key;
    const filePath = path.join(simDir, key);
    if (!fs.existsSync(filePath)) {
      throw new Error(`Simulated asset not found: ${key}`);
    }
    const content = fs.readFileSync(filePath, 'utf-8');
    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          key,
          value: content,
          updated_at: fs.statSync(filePath).mtime.toISOString()
        }, null, 2)
      }]
    };
  }
  
  if (name === 'update_theme_file') {
    const key = args.asset_key;
    const val = args.value;
    const filePath = path.join(simDir, key);
    fs.mkdirSync(path.dirname(filePath), { recursive: true });
    fs.writeFileSync(filePath, val, 'utf-8');
    
    log(`[Simulation Mode] Wrote file locally: simulated_shopify/${key}`);
    
    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          key,
          value: val,
          updated_at: new Date().toISOString()
        }, null, 2)
      }]
    };
  }
  
  if (name === 'delete_theme_file') {
    const key = args.asset_key;
    const filePath = path.join(simDir, key);
    if (fs.existsSync(filePath)) {
      fs.unlinkSync(filePath);
      log(`[Simulation Mode] Deleted file locally: simulated_shopify/${key}`);
    }
    return {
      content: [{ type: "text", text: JSON.stringify({ message: `Simulated asset deleted: ${key}` }, null, 2) }]
    };
  }
  
  throw new Error(`Simulation tool not found: ${name}`);
}
