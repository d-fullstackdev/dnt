/**
 * Puppeteer Stealth Fetcher
 * Designed for Celios 9 Danantara Monitor
 * Bypasses Cloudflare, Akamai, and Datadome bot detection on media & ratings sites.
 */

const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const fs = require('fs');
const path = require('path');

// Apply stealth plugin
puppeteer.use(StealthPlugin());

// System Chrome path if available
const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const executablePath = fs.existsSync(CHROME_PATH) ? CHROME_PATH : undefined;

async function fetchWithStealth(url, outputPath = null, headless = 'new') {
    const isHeadless = headless === 'true' || headless === 'new' || headless === true;
    
    // Persistent user data dir to maintain verified Cloudflare session cookies
    const userDataDir = path.join(__dirname, '..', '..', 'cache', 'puppeteer_profile');
    if (!fs.existsSync(userDataDir)) {
        fs.mkdirSync(userDataDir, { recursive: true });
    }

    const launchOptions = {
        headless: isHeadless ? 'new' : false,
        executablePath: executablePath,
        userDataDir: userDataDir,
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-infobars',
            '--window-size=1920,1080',
            '--disable-blink-features=AutomationControlled',
            '--disable-features=IsolateOrigins,site-per-process'
        ],
        defaultViewport: {
            width: 1920,
            height: 1080
        }
    };

    let browser;
    try {
        browser = await puppeteer.launch(launchOptions);
        const page = await browser.newPage();

        // Realistic Desktop User-Agent
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36');
        
        // Add extra headers
        await page.setExtraHTTPHeaders({
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'Upgrade-Insecure-Requests': '1'
        });

        // Navigate
        const response = await page.goto(url, {
            waitUntil: 'networkidle2',
            timeout: 45000
        });

        // Wait slightly if Cloudflare challenge is active
        const title = await page.title();
        if (title.toLowerCase().includes('just a moment') || title.toLowerCase().includes('cloudflare')) {
            console.error('⚠️ Cloudflare challenge detected, waiting for clearance...');
            await new Promise(r => setTimeout(r, 6000));
        }

        // Extract metadata and content
        const pageData = await page.evaluate(() => {
            // Remove scripts, styles, and unwanted noise
            const clone = document.cloneNode(true);
            const scripts = clone.querySelectorAll('script, style, noscript, iframe, svg');
            scripts.forEach(s => s.remove());

            return {
                title: document.title,
                url: window.location.href,
                innerText: document.body ? document.body.innerText : '',
                html: document.documentElement.outerHTML
            };
        });

        const result = {
            success: true,
            status: response ? response.status() : 200,
            url: pageData.url,
            original_url: url,
            title: pageData.title,
            text_length: pageData.innerText.length,
            text: pageData.innerText,
            html: pageData.html,
            timestamp: new Date().toISOString()
        };

        if (outputPath) {
            const dir = path.dirname(outputPath);
            if (!fs.existsSync(dir)) {
                fs.mkdirSync(dir, { recursive: true });
            }
            fs.writeFileSync(outputPath, JSON.stringify(result, null, 2), 'utf-8');
            console.log(`✓ Fetched & saved to: ${outputPath} (${result.text_length} chars)`);
        } else {
            console.log(JSON.stringify(result));
        }

        return result;

    } catch (err) {
        console.error(`❌ Puppeteer error for ${url}:`, err.message);
        const errResult = {
            success: false,
            url: url,
            error: err.message,
            timestamp: new Date().toISOString()
        };
        if (outputPath) {
            fs.writeFileSync(outputPath, JSON.stringify(errResult, null, 2), 'utf-8');
        }
        return errResult;
    } finally {
        if (browser) {
            await browser.close();
        }
    }
}

// CLI Execution support
if (require.main === module) {
    const args = process.argv.slice(2);
    if (args.length === 0) {
        console.log("Usage: node stealth_fetcher.js <url> [output_file.json] [--headless true/false]");
        process.exit(1);
    }
    const targetUrl = args[0];
    const outputFile = args[1] && !args[1].startsWith('--') ? args[1] : null;
    const headless = args.includes('--headless=false') || args.includes('--headless false') ? false : 'new';
    
    fetchWithStealth(targetUrl, outputFile, headless);
}

module.exports = { fetchWithStealth };
