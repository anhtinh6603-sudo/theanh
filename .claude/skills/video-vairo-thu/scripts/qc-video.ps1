[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)]
  [string]$VideoPath,

  [double]$ExpectedDuration = 0
)

$ErrorActionPreference = 'Stop'
foreach ($commandName in @('ffmpeg', 'ffprobe')) {
  if (-not (Get-Command $commandName -ErrorAction SilentlyContinue)) {
    throw "$commandName chưa có trong PATH."
  }
}

$fullVideoPath = [IO.Path]::GetFullPath($VideoPath)
if (-not (Test-Path -LiteralPath $fullVideoPath)) { throw "Không tìm thấy $fullVideoPath" }
$projectRoot = Split-Path -Parent $fullVideoPath
$qaRoot = Join-Path $projectRoot 'qa'
New-Item -ItemType Directory -Path $qaRoot -Force | Out-Null

$probe = (& ffprobe -v error -show_entries 'format=duration,bit_rate:stream=index,codec_name,codec_type,width,height,r_frame_rate,pix_fmt,sample_rate,channels' -of json $fullVideoPath | Out-String) | ConvertFrom-Json
$videoStream = $probe.streams | Where-Object { $_.codec_type -eq 'video' } | Select-Object -First 1
$audioStream = $probe.streams | Where-Object { $_.codec_type -eq 'audio' } | Select-Object -First 1
$duration = [double]$probe.format.duration

$nullSink = if ($IsWindows) { 'NUL' } else { '/dev/null' }
$decodeOutput = (& ffmpeg -v error -i $fullVideoPath -f null $nullSink 2>&1 | Out-String).Trim()
$decodeOk = [string]::IsNullOrWhiteSpace($decodeOutput)

$audioAnalysis = (& ffmpeg -hide_banner -nostats -i $fullVideoPath -map 0:a:0 -af 'ebur128=peak=true' -f null $nullSink 2>&1 | Out-String)
$loudnessMatches = [regex]::Matches($audioAnalysis, 'I:\s+(-?\d+(?:\.\d+)?)\s+LUFS')
$peakMatches = [regex]::Matches($audioAnalysis, 'Peak:\s+(-?\d+(?:\.\d+)?)\s+dBFS')
$loudness = if ($loudnessMatches.Count) { [double]$loudnessMatches[$loudnessMatches.Count - 1].Groups[1].Value } else { $null }
$truePeak = if ($peakMatches.Count) { [double]$peakMatches[$peakMatches.Count - 1].Groups[1].Value } else { $null }

$contactSheet = Join-Path $qaRoot 'final-contact-sheet.jpg'
$durationText = $duration.ToString('0.###', [Globalization.CultureInfo]::InvariantCulture)
& ffmpeg -y -loglevel error -i $fullVideoPath -vf "fps=12/$durationText,scale=270:480,tile=4x3:padding=6:margin=6" -frames:v 1 $contactSheet
if ($LASTEXITCODE -ne 0) { throw 'Không tạo được contact sheet.' }

$durationOk = if ($ExpectedDuration -gt 0) { [math]::Abs($duration - $ExpectedDuration) -le 0.2 } else { $true }
$formatOk = (
  $videoStream.codec_name -eq 'h264' -and
  [int]$videoStream.width -eq 1080 -and
  [int]$videoStream.height -eq 1920 -and
  $videoStream.r_frame_rate -eq '30/1' -and
  $audioStream.codec_name -eq 'aac' -and
  [int]$audioStream.sample_rate -eq 48000
)
$audioOk = ($null -ne $loudness -and $loudness -ge -16.5 -and $loudness -le -13.5 -and $null -ne $truePeak -and $truePeak -le -1.5)
$status = if ($durationOk -and $formatOk -and $decodeOk -and $audioOk) { 'PASS' } else { 'FAIL' }

$report = [ordered]@{
  status = $status
  video = $fullVideoPath
  duration = [math]::Round($duration, 3)
  expected_duration = if ($ExpectedDuration -gt 0) { $ExpectedDuration } else { $null }
  video_codec = $videoStream.codec_name
  width = [int]$videoStream.width
  height = [int]$videoStream.height
  fps = $videoStream.r_frame_rate
  pixel_format = $videoStream.pix_fmt
  audio_codec = $audioStream.codec_name
  sample_rate = [int]$audioStream.sample_rate
  channels = [int]$audioStream.channels
  integrated_lufs = $loudness
  true_peak_dbfs = $truePeak
  decode_ok = $decodeOk
  decode_errors = $decodeOutput
  contact_sheet = $contactSheet
  visual_review_required = $true
}

$reportPath = Join-Path $qaRoot 'qc-report.json'
$report | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $reportPath -Encoding utf8
$report | ConvertTo-Json -Depth 5
Write-Output "Báo cáo: $reportPath"
Write-Output 'Hãy mở contact sheet và xem toàn bộ video bằng mắt/tai trước khi giao.'

