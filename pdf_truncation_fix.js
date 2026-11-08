// pdf_truncation_fix.js - Universal Zero-Truncation Layout & Print Normalizer
// Fixes viewport clipping, orphaned signatures, and horizontal overset lines

const STRICT_ZERO_TRUNCATION_CSS = `
@media print {
  @page {
    size: letter portrait;
    margin-left: 0.75in !important;   /* 54pt court binding gutter */
    margin-right: 0.50in !important;  /* 36pt outer trim */
    margin-top: 0.75in !important;    /* 54pt top clearance */
    margin-bottom: 0.75in !important; /* 54pt bottom clearance */
  }

  html, body {
    width: 100% !important;
    height: auto !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: visible !important;
    background: #ffffff !important;
    color: #000000 !important;
    font-family: "Times New Roman", Times, Georgia, serif !important;
    font-size: 10pt !important;
    line-height: 1.4 !important;
  }

  /* Prevent browser viewports from clipping long documents */
  .page-sheet, .pdf-page-container, #printRoot, pre, table {
    overflow: visible !important;
    float: none !important;
    position: static !important;
    max-height: none !important;
  }

  /* Table protection: prevent severed rows across page breaks */
  table {
    width: 100% !important;
    border-collapse: collapse !important;
    page-break-inside: auto;
  }

  tr {
    page-break-inside: avoid !important;
    break-inside: avoid !important;
  }

  th, td {
    padding: 5pt 6pt !important;
    font-size: 8.5pt !important;
    line-height: 1.2 !important;
  }

  /* Orphan & signature line defense */
  .signature-block, .avoid-break, .keep-together, .exhibit-box {
    page-break-inside: avoid !important;
    break-inside: avoid !important;
  }

  h1, h2, h3, h4 {
    page-break-after: avoid !important;
    break-after: avoid !important;
  }

  /* Monospace wrap defense */
  pre.legal-mono, pre.untruncated-mono {
    font-family: "Courier New", Courier, monospace !important;
    font-size: 7.5pt !important;
    line-height: 1.25 !important;
    white-space: pre-wrap !important;       /* CSS3 word-wrap */
    word-wrap: break-word !important;
    word-break: break-all !important;
    overflow: visible !important;
    margin: 0 !important;
    padding: 0 !important;
    border: none !important;
  }

  /* Hide screen-only interactive elements */
  nav, button, .no-print, #nav-compliance-btn, #complianceHubModal, #marketingModal {
    display: none !important;
  }
}
`;

// Injects defensive CSS rules into current DOM
function injectZeroTruncationStyles() {
  let styleEl = document.getElementById('zero-truncation-stylesheet');
  if (!styleEl) {
    styleEl = document.createElement('style');
    styleEl.id = 'zero-truncation-stylesheet';
    styleEl.textContent = STRICT_ZERO_TRUNCATION_CSS;
    document.head.appendChild(styleEl);
  }
}

// Pre-wraps plain monospace text to a strict character width before rendering
function wrapMonospaceText(text, maxChars = 78) {
  if (!text) return '';
  const lines = text.split('\n');
  const wrapped = [];

  for (let line of lines) {
    if (line.length <= maxChars) {
      wrapped.push(line);
    } else {
      while (line.length > maxChars) {
        let splitIdx = line.lastIndexOf(' ', maxChars);
        if (splitIdx === -1 || splitIdx < maxChars - 15) {
          splitIdx = maxChars;
        }
        wrapped.push(line.substring(0, splitIdx));
        line = line.substring(splitIdx).trimStart();
      }
      if (line.length > 0) wrapped.push(line);
    }
  }
  return wrapped.join('\n');
}

// Universal print pipeline replacement
function openFormattedPdfPrintWindow(title, subtitle, bodyContent, isMonospace = false) {
  const printWindow = window.open('', '_blank');
  if (!printWindow) {
    alert("Pop-up blocked. Please permit pop-ups to open full vector print documents.");
    return;
  }

  const cleanContent = isMonospace ? wrapMonospaceText(bodyContent, 78) : bodyContent;
  const timestamp = new Date().toLocaleString();

  const printDocumentHtml = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>${title}</title>
  <style>${STRICT_ZERO_TRUNCATION_CSS}</style>
  <style>
    /* Screen presentation mimicking physical paper */
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
      padding: 0.75in 0.50in 0.75in 0.75in;
      box-sizing: border-box;
      color: #000000;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    }
    .running-header {
      border-bottom: 1px solid #cbd5e1;
      padding-bottom: 4pt;
      margin-bottom: 12pt;
      font-size: 8pt;
      color: #64748b;
      display: flex;
      justify-content: space-between;
      text-transform: uppercase;
      font-family: sans-serif;
    }
    .running-footer {
      border-top: 1px solid #cbd5e1;
      padding-top: 4pt;
      margin-top: 16pt;
      font-size: 8pt;
      color: #64748b;
      display: flex;
      justify-content: space-between;
      font-family: sans-serif;
      page-break-inside: avoid;
      break-inside: avoid;
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
      <span>Section 8 Rentals and More LLC • Statutory Record</span>
      <span>${title}</span>
    </div>

    <div style="margin-bottom: 12pt;">
      <h1 style="font-size: 14pt; margin: 0; font-weight: bold; text-transform: uppercase; font-family: serif;">${title}</h1>
      <p style="font-size: 8.5pt; color: #475569; margin: 2pt 0 0 0; font-family: sans-serif;">${subtitle}</p>
    </div>

    ${isMonospace 
      ? `<pre class="untruncated-mono">${cleanContent}</pre>` 
      : `<div class="pdf-page-container">${cleanContent}</div>`
    }

    <div class="running-footer avoid-break">
      <span>Certified Compliance Docket • Single-Line Header Gutter Geometry</span>
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
</html>`;

  printWindow.document.open();
  printWindow.document.write(printDocumentHtml);
  printWindow.document.close();
}

window.injectZeroTruncationStyles = injectZeroTruncationStyles;
window.wrapMonospaceText = wrapMonospaceText;
window.openFormattedPdfPrintWindow = openFormattedPdfPrintWindow;

document.addEventListener('DOMContentLoaded', injectZeroTruncationStyles);
