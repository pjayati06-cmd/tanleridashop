const fs = require('fs');
const path = require('path');

// Re-use tool call logic from index.js but run it directly for local CLI sync
const indexCode = require('./index.js'); // Wait, we can't require it easily because it runs readline.
// Let's implement a standalone sync script that reads .env and pushes files to Shopify API (or simulates it)

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

const STORE_DOMAIN = process.env.SHOPIFY_STORE_DOMAIN || 'tan-lerida.myshopify.com';
const THEME_ID = process.env.SHOPIFY_THEME_ID || '197507121233';
const ACCESS_TOKEN = process.env.SHOPIFY_ADMIN_API_ACCESS_TOKEN;

const isSimulation = !ACCESS_TOKEN || ACCESS_TOKEN === 'shpat_your_token_here' || ACCESS_TOKEN.startsWith('shpat_internal');

console.log(`[Shopify Sync] Mode: ${isSimulation ? 'SIMULATION (Local)' : 'LIVE (Shopify)'}`);
console.log(`[Shopify Sync] Store Domain: ${STORE_DOMAIN}`);
console.log(`[Shopify Sync] Theme ID: ${THEME_ID}`);

const sourceDir = path.join(__dirname, '..', 'Tan Lerida', 'Shopify-Theme');
const simDir = path.join(__dirname, '..', 'simulated_shopify');

if (!fs.existsSync(sourceDir)) {
  console.error(`Error: Source directory not found: ${sourceDir}`);
  process.exit(1);
}

const filesToSync = [
  { src: 'sections/atelier-hero.liquid', dest: 'sections/atelier-hero.liquid' },
  { src: 'layout/theme.liquid', dest: 'layout/theme.liquid' },
  { src: 'templates/index.json', dest: 'templates/index.json' },
  { src: 'assets/tan-lerida-custom.css', dest: 'assets/tan-lerida-custom.css' },
  { src: 'sections/care-guide.liquid', dest: 'sections/care-guide.liquid' },
  { src: 'templates/page.care-guide.json', dest: 'templates/page.care-guide.json' },
  { src: 'assets/leather_new_grain.png', dest: 'assets/leather_new_grain.png' },
  { src: 'assets/leather_patina_grain.png', dest: 'assets/leather_patina_grain.png' },
  { src: 'assets/care_water_wipe.png', dest: 'assets/care_water_wipe.png' },
  { src: 'assets/care_storage_dustbag.png', dest: 'assets/care_storage_dustbag.png' },
  { src: 'assets/care_conditioner_wax.png', dest: 'assets/care_conditioner_wax.png' },
  { src: 'sections/commitment.liquid', dest: 'sections/commitment.liquid' },
  { src: 'templates/page.commitment.json', dest: 'templates/page.commitment.json' },
  { src: 'assets/care_workshop_detail.png', dest: 'assets/care_workshop_detail.png' },
  { src: 'assets/tannery_drums.png', dest: 'assets/tannery_drums.png' },
  { src: 'assets/stitching_detail.png', dest: 'assets/stitching_detail.png' },
  { src: 'assets/heritage_tools.png', dest: 'assets/heritage_tools.png' }
];

async function syncFile(file) {
  const srcPath = path.join(sourceDir, file.src);
  if (!fs.existsSync(srcPath)) {
    console.warn(`Warning: File not found: ${srcPath}, skipping.`);
    return;
  }
  
  const isBinary = file.src.endsWith('.png') || file.src.endsWith('.jpg') || file.src.endsWith('.jpeg');
  
  if (isSimulation) {
    const destPath = path.join(simDir, file.dest);
    fs.mkdirSync(path.dirname(destPath), { recursive: true });
    if (isBinary) {
      const content = fs.readFileSync(srcPath);
      fs.writeFileSync(destPath, content);
      console.log(`[Simulation] Synced local binary file to: simulated_shopify/${file.dest} (${content.length} bytes)`);
    } else {
      const content = fs.readFileSync(srcPath, 'utf-8');
      fs.writeFileSync(destPath, content, 'utf-8');
      console.log(`[Simulation] Synced local file to: simulated_shopify/${file.dest} (${content.length} bytes)`);
    }
  } else {
    let domain = STORE_DOMAIN;
    if (!domain.includes('.')) {
      domain = `${domain}.myshopify.com`;
    }
    const url = `https://${domain}/admin/api/2024-01/themes/${THEME_ID}/assets.json`;
    const headers = {
      "X-Shopify-Access-Token": ACCESS_TOKEN,
      "Content-Type": "application/json"
    };
    
    let assetPayload = { key: file.dest };
    let size = 0;
    if (isBinary) {
      const content = fs.readFileSync(srcPath);
      assetPayload.attachment = content.toString('base64');
      size = content.length;
    } else {
      const content = fs.readFileSync(srcPath, 'utf-8');
      assetPayload.value = content;
      size = content.length;
    }
    
    try {
      const res = await fetch(url, {
        method: 'PUT',
        headers,
        body: JSON.stringify({ asset: assetPayload })
      });
      
      if (!res.ok) {
        const errText = await res.text();
        throw new Error(`Shopify API response (${res.status}): ${errText}`);
      }
      
      console.log(`[Live] Successfully pushed to Shopify: ${file.dest} (${size} bytes)`);
    } catch (err) {
      console.error(`[Live] Failed to push ${file.dest}: ${err.message}`);
    }
  }
}

async function run() {
  for (const file of filesToSync) {
    await syncFile(file);
  }
  console.log("[Shopify Sync] Finished.");
}

run();
