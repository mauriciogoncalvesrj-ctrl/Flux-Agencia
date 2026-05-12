const puppeteer = require('puppeteer');
const fs = require('fs');

async function renderPDF(htmlFile, pdfFile) {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  const html = fs.readFileSync(htmlFile, 'utf8');
  await page.setContent(html, { waitUntil: 'networkidle0' });
  await page.pdf({
    path: pdfFile,
    format: 'A4',
    margin: { top: '15mm', bottom: '15mm', left: '12mm', right: '12mm' },
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: '<div style="font-size:8px;color:#999;text-align:right;width:100%;padding-right:10px;padding-top:5px;"><span class="date"></span></div>',
    footerTemplate: '<div style="font-size:8px;color:#999;text-align:center;width:100%;border-top:1px solid #e0e0e0;padding-top:5px;">Flux Agência — Relatório Meta Ads — Página <span class="pageNumber"></span></div>'
  });
  await browser.close();
  console.log(`PDF gerado: ${pdfFile}`);
}

const [,, htmlFile, pdfFile] = process.argv;
if (!htmlFile || !pdfFile) {
  console.error('Uso: node render_pdf.js <input.html> <output.pdf>');
  process.exit(1);
}
renderPDF(htmlFile, pdfFile).catch(err => { console.error(err); process.exit(1); });