
// pdf_render_engine.js - Precision Print Stylesheet & Fixed-Page Layout Engine
// Enforces 8.5in x 11in page geometry, inner gutter margins, and clean break boundaries

const PRINT_CSS = `
@media print {
  @page {
    size: letter portrait;
    margin: 0.75in 0.5in 0.75in 0.75in; /* 0.75in inner binding gutter */
  }

  body {
    background: #ffffff !important;
    color: #000000 !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.45;
    margin: 0 !important;
    padding: 0 !important;
  }

  /* Structural Page Container */
  .pdf-page-container {
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    box-sizing: border-box;
  }

  /* Page Break Management */
  .page-break-after {
    page-break-after: always;
    break-after: page;
  }

  .avoid-break, table, tr, figure, blockquote, .signature-block, .exhibit-panel {
    page-break-inside: avoid !important;
    break-inside: avoid !important;
  }

  /* Table Grid Cleanliness */
  table.print-table {
    width: 100% !important;
    border-collapse: collapse !important;
    margin-top: 12pt;
    margin-bottom: 12pt;
  }

  table.print-table th, table.print-table td {
    border: 1px solid #1e293b !important;
    padding: 6pt 8pt !important;
    font-size: 9pt !important;
    text-align: left;
  }

  table.print-table th {
    background-color: #f1f5f9 !important;
    color: #0f172a !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    font-size: 8pt !important;
  }

  /* Legal Monospace Staging */
  pre.legal-mono {
    font-family: "Courier New", Courier, monospace !important;
    font-size: 8.5pt !important;
    line-height: 1.35 !important;
    white-space: pre-wrap !important;
    word-break: break-all !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
  }

  /* Header & Footer Anchors */
  .running-header {
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 4pt;
    margin-bottom: 12pt;
    font-size: 8pt;
    color: #64748b;
    text-transform: uppercase;
    display: flex;
    justify-content: space-between;
  }

  .running-footer {
    border-top: 1px solid #cbd5e1;
    padding-top: 4pt;
    margin-top: 16pt;
    font-size: 8pt;
    color: #64748b;
    display: flex;
    justify-content: space-between;
  }

  /* Hide Web UI Chrome */
  nav, button, .no-print, #nav-compliance-btn, #complianceHubModal, #marketingModal {
    display: none !important;
  }
}
`;

function injectPrintStyles() {
  if (document.getElementById('pdf-print-stylesheet')) return;
  const style = document.createElement('style');
  style.id = 'pdf-print-stylesheet';
  style.textContent = PRINT_CSS;
  document.head.appendChild(style);
}

// Universal formatted print window generator
function openFormattedPdfPrintWindow(title, subtitle, bodyHtml, isMonospace = false) {
  injectPrintStyles();

  const printWindow = window.open('', '_blank');
  if (!printWindow) {
    alert('Pop-up blocked. Please allow pop-ups for this domain to generate PDFs.');
    return;
  }

  const timestamp = new Date().toLocaleString();
  const documentHtml = `
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>${title}</title>
      <style>${PRINT_CSS}</style>
      <style>
        /* Screen preview styling matching physical print paper */
        body {
          background-color: #0f172a;
          padding: 24px;
          display: flex;
          justify-content: center;
        }
        .page-sheet {
          background: #ffffff;
          width: 8.5in;
          min-height: 11in;
          padding: 0.75in 0.5in 0.75in 0.75in;
          box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
          box-sizing: border-box;
          color: #000000;
          font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }
        @media print {
          body { background: transparent; padding: 0; }
          .page-sheet { width: 100%; min-height: auto; box-shadow: none; padding: 0; }
        }
      </style>
    </head>
    <body>
      <div class="page-sheet">
        <div class="running-header">
          <span>Section 8 Rentals and More LLC • Statutory Compliance Record</span>
          <span>${title}</span>
        </div>

        <div style="margin-bottom: 14pt;">
          <h1 style="font-size: 14pt; margin: 0; font-weight: 800; text-transform: uppercase;">${title}</h1>
          <p style="font-size: 9pt; color: #475569; margin: 2pt 0 0 0;">${subtitle}</p>
        </div>

        ${isMonospace 
          ? `<pre class="legal-mono">${bodyHtml}</pre>` 
          : `<div class="pdf-page-container">${bodyHtml}</div>`
        }

        <div class="running-footer avoid-break">
          <span>Certified Record Token: [SEC8-DOC-${Date.now().toString().slice(-8)}]</span>
          <span>Rendered: ${timestamp}</span>
        </div>
      </div>

      <script>
        window.addEventListener('load', () => {
          setTimeout(() => {
            window.print();
          }, 250);
        });
      </script>
    </body>
    </html>
  `;

  printWindow.document.open();
  printWindow.document.write(documentHtml);
  printWindow.document.close();
}

window.injectPrintStyles = injectPrintStyles;
window.openFormattedPdfPrintWindow = openFormattedPdfPrintWindow;
