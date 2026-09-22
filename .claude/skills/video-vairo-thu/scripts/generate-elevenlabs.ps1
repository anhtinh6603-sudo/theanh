[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)]
  [string]$ProjectPath,

  [string]$TakesFile = 'takes.json',
  [string]$ApiKeyEnv = 'ELEVENLABS_API_KEY',
  [string]$ModelId = 'eleven_v3',
  [string]$LanguageCode = 'vi',
  [string]$OutputFormat = 'mp3_44100_128'
)

$ErrorActionPreference = 'Stop'
$projectRoot = [IO.Path]::GetFullPath($ProjectPath)
$takesPath = Join-Path $projectRoot $TakesFile
$audioRoot = Join-Path $projectRoot 'audio'
if (-not (Test-Path -LiteralPath $takesPath)) { throw "Không tìm thấy $takesPath" }
New-Item -ItemType Directory -Path $audioRoot -Force | Out-Null

$apiKey = [Environment]::GetEnvironmentVariable($ApiKeyEnv)
if ([string]::IsNullOrWhiteSpace($apiKey)) {
  throw "Chưa cấu hình biến môi trường $ApiKeyEnv"
}

$takes = Get-Content -LiteralPath $takesPath -Raw | ConvertFrom-Json
if (-not $takes -or $takes.Count -eq 0) { throw 'takes.json chưa có lượt thoại.' }
$headers = @{ 'xi-api-key' = $apiKey; 'Content-Type' = 'application/json' }

foreach ($take in $takes) {
  $voiceId = $take.voice_id
  if ([string]::IsNullOrWhiteSpace($voiceId) -and $take.voice_env) {
    $voiceId = [Environment]::GetEnvironmentVariable([string]$take.voice_env)
  }
  if ([string]::IsNullOrWhiteSpace($voiceId)) {
    throw "Thiếu voice ID cho take $($take.file)."
  }
  if ([string]::IsNullOrWhiteSpace([string]$take.text)) {
    throw "Thiếu text cho take $($take.file)."
  }

  $uri = "https://api.elevenlabs.io/v1/text-to-speech/$voiceId/with-timestamps?output_format=$OutputFormat"
  $payload = @{
    text = [string]$take.text
    model_id = $ModelId
    language_code = $LanguageCode
    voice_settings = @{
      stability = 0.5
      similarity_boost = 0.78
      style = 0.30
      use_speaker_boost = $true
    }
  } | ConvertTo-Json -Depth 6

  $response = Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -Body $payload
  $mediaPath = Join-Path $audioRoot "$($take.file).mp3"
  [IO.File]::WriteAllBytes($mediaPath, [Convert]::FromBase64String($response.audio_base64))
  $alignment = if ($response.normalized_alignment) { $response.normalized_alignment } else { $response.alignment }
  $alignment | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $audioRoot "$($take.file)-alignment.json") -Encoding utf8
  Write-Output "Đã tạo $($take.file).mp3"
}

