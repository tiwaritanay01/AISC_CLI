/**
 * Netlify Function: raw.js
 * Serves raw PowerShell delivery script from a compressed stateless URL:
 * /r?f=<filename>&d=<compressed_code>
 */

const zlib = require('zlib');

exports.handler = async (event) => {
  const params = event.queryStringParameters || {};
  const filename = (params.f || 'experiment.py').replace(/[^\w\.\-_]/g, '_');
  const data = params.d;

  if (!data) {
    return {
      statusCode: 400,
      headers: {
        'Content-Type': 'text/plain; charset=utf-8',
        'Access-Control-Allow-Origin': '*'
      },
      body: 'Write-Error "Missing data parameter (d)."'
    };
  }

  try {
    let base64 = data.replace(/-/g, '+').replace(/_/g, '/');
    while (base64.length % 4) {
      base64 += '=';
    }
    const buf = Buffer.from(base64, 'base64');
    let decoded;
    try {
      decoded = zlib.gunzipSync(buf).toString('utf-8');
    } catch (e) {
      decoded = buf.toString('utf-8');
    }

    let script;
    if (decoded.includes('$target') && decoded.includes('Set-Content')) {
      script = decoded;
    } else {
      script = `# LabX Remote - Custom Experiment Delivery
$filename = "${filename}"
$code = @'
${decoded}
'@
$target = Join-Path $PWD $filename
Set-Content -Path $target -Value $code -Encoding utf8
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " [OK] Experiment code saved to: $filename" -ForegroundColor Green
Write-Host " Theory is embedded after line 50. Ready to execute!" -ForegroundColor White
Write-Host " Run: py $filename" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
`;
    }

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'text/plain; charset=utf-8',
        'Cache-Control': 'public, max-age=86400',
        'Access-Control-Allow-Origin': '*'
      },
      body: script
    };
  } catch (err) {
    return {
      statusCode: 500,
      headers: {
        'Content-Type': 'text/plain; charset=utf-8',
        'Access-Control-Allow-Origin': '*'
      },
      body: `Write-Error "Failed to process delivery script: ${err.message}"`
    };
  }
};

