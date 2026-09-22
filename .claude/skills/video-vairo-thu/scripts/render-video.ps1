[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)]
  [string]$ProjectPath,

  [string]$TimelineFile = 'timeline.json',
  [string]$OutputName = 'final.mp4'
)

$ErrorActionPreference = 'Stop'
foreach ($commandName in @('ffmpeg', 'ffprobe')) {
  if (-not (Get-Command $commandName -ErrorAction SilentlyContinue)) {
    throw "$commandName chưa có trong PATH."
  }
}

$projectRoot = [IO.Path]::GetFullPath($ProjectPath)
$timelinePath = Join-Path $projectRoot $TimelineFile
$captionPath = Join-Path $projectRoot 'work\captions.ass'
$flowRoot = Join-Path $projectRoot 'flow'
$workRoot = Join-Path $projectRoot 'work'
$outputPath = if ([IO.Path]::IsPathRooted($OutputName)) {
  [IO.Path]::GetFullPath($OutputName)
} else {
  Join-Path $projectRoot $OutputName
}

if (-not (Test-Path -LiteralPath $timelinePath)) { throw "Không tìm thấy $timelinePath" }
if (-not (Test-Path -LiteralPath $captionPath)) { throw "Không tìm thấy $captionPath" }
New-Item -ItemType Directory -Path $workRoot -Force | Out-Null

$timeline = Get-Content -LiteralPath $timelinePath -Raw | ConvertFrom-Json
$targetDuration = [double]$timeline.target_duration
$sceneDurations = @($timeline.scene_durations | ForEach-Object { [double]$_ })
$sceneFiles = @(Get-ChildItem -LiteralPath $flowRoot -File -Filter 'scene-*.mp4' | Sort-Object Name)
if ($sceneFiles.Count -eq 0) { throw 'Không có clip flow/scene-*.mp4.' }
if ($sceneFiles.Count -ne $sceneDurations.Count) {
  throw "Số clip ($($sceneFiles.Count)) khác số scene_durations ($($sceneDurations.Count))."
}
$durationSum = ($sceneDurations | Measure-Object -Sum).Sum
if ([math]::Abs($durationSum - $targetDuration) -gt 0.01) {
  throw "Tổng scene_durations ($durationSum) khác target_duration ($targetDuration)."
}

$culture = [Globalization.CultureInfo]::InvariantCulture
$videoBase = Join-Path $workRoot 'video-base.mp4'
$videoArgs = @('-y', '-loglevel', 'error')
foreach ($scene in $sceneFiles) { $videoArgs += @('-i', $scene.FullName) }
$videoFilters = @()
$concatLabels = ''
for ($i = 0; $i -lt $sceneFiles.Count; $i++) {
  $durationText = $sceneDurations[$i].ToString('0.###', $culture)
  $videoFilters += "[$i`:v]trim=duration=$durationText,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1,fps=30[v$i]"
  $concatLabels += "[v$i]"
}
$videoFilters += "$concatLabels`concat=n=$($sceneFiles.Count):v=1:a=0[v]"
$videoArgs += @(
  '-filter_complex', ($videoFilters -join ';'),
  '-map', '[v]', '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
  '-pix_fmt', 'yuv420p', '-movflags', '+faststart', $videoBase
)
& ffmpeg @videoArgs
if ($LASTEXITCODE -ne 0) { throw 'Dựng video nền thất bại.' }

$tracks = @($timeline.audio_tracks)
$hasBgm = $timeline.bgm -and -not [string]::IsNullOrWhiteSpace([string]$timeline.bgm.file)
if ($tracks.Count -eq 0 -and -not $hasBgm) { throw 'timeline.json chưa có audio_tracks hoặc bgm.' }

$audioRaw = Join-Path $workRoot 'audio-raw.wav'
$audioMix = Join-Path $workRoot 'audio-mix.wav'
$audioArgs = @('-y', '-loglevel', 'error')
$audioFilters = @()
$audioLabels = @()
$audioIndex = 0

foreach ($track in $tracks) {
  $trackPath = Join-Path $projectRoot ([string]$track.file)
  if (-not (Test-Path -LiteralPath $trackPath)) { throw "Thiếu audio: $trackPath" }
  $audioArgs += @('-i', $trackPath)
  $startMs = [int]$track.start_ms
  $volume = if ($null -eq $track.volume) { 1.0 } else { [double]$track.volume }
  $volumeText = $volume.ToString('0.###', $culture)
  $label = "a$audioIndex"
  $audioFilters += "[$audioIndex`:a]adelay=$startMs`:all=1,volume=$volumeText[$label]"
  $audioLabels += "[$label]"
  $audioIndex++
}

if ($hasBgm) {
  $bgmPath = Join-Path $projectRoot ([string]$timeline.bgm.file)
  if (-not (Test-Path -LiteralPath $bgmPath)) { throw "Thiếu BGM: $bgmPath" }
  $audioArgs += @('-stream_loop', '-1', '-i', $bgmPath)
  $bgmVolume = if ($null -eq $timeline.bgm.volume) { 0.10 } else { [double]$timeline.bgm.volume }
  $bgmVolumeText = $bgmVolume.ToString('0.###', $culture)
  $targetText = $targetDuration.ToString('0.###', $culture)
  $fadeOutStart = [math]::Max(0, $targetDuration - 2).ToString('0.###', $culture)
  $audioFilters += "[$audioIndex`:a]atrim=duration=$targetText,asetpts=PTS-STARTPTS,volume=$bgmVolumeText,afade=t=in:st=0:d=1.2,afade=t=out:st=$fadeOutStart`:d=2[bgm]"
  $audioLabels += '[bgm]'
}

$targetText = $targetDuration.ToString('0.###', $culture)
$audioFilters += "$($audioLabels -join '')amix=inputs=$($audioLabels.Count):duration=longest:dropout_transition=0,apad=pad_dur=$targetText,atrim=duration=$targetText,aresample=48000[raw]"
$audioArgs += @(
  '-filter_complex', ($audioFilters -join ';'), '-map', '[raw]',
  '-ac', '2', '-ar', '48000', '-c:a', 'pcm_s16le', $audioRaw
)
& ffmpeg @audioArgs
if ($LASTEXITCODE -ne 0) { throw 'Phối audio thô thất bại.' }

$nullSink = if ($IsWindows) { 'NUL' } else { '/dev/null' }
$analysis = (& ffmpeg -hide_banner -nostats -i $audioRaw -map 0:a:0 -af 'ebur128=peak=true' -f null $nullSink 2>&1 | Out-String)
$matches = [regex]::Matches($analysis, 'I:\s+(-?\d+(?:\.\d+)?)\s+LUFS')
if ($matches.Count -eq 0) { throw 'Không đo được loudness của audio.' }
$integrated = [double]::Parse($matches[$matches.Count - 1].Groups[1].Value, $culture)
$gainDb = -15.0 - $integrated
$gainText = $gainDb.ToString('0.###', $culture)
& ffmpeg -y -loglevel error -i $audioRaw -af "volume=$gainText`dB,alimiter=limit=0.84" -ac 2 -ar 48000 -c:a pcm_s16le $audioMix
if ($LASTEXITCODE -ne 0) { throw 'Chuẩn hóa loudness thất bại.' }

Push-Location $projectRoot
try {
  & ffmpeg -y -loglevel error -i 'work/video-base.mp4' -i 'work/audio-mix.wav' -vf "subtitles='work/captions.ass'" -map 0:v:0 -map 1:a:0 -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -t $targetText -movflags +faststart $outputPath
  if ($LASTEXITCODE -ne 0) { throw 'Xuất final MP4 thất bại.' }
} finally {
  Pop-Location
}

Write-Output "Đã xuất: $outputPath"
& ffprobe -v error -show_entries 'format=duration:stream=codec_name,codec_type,width,height,r_frame_rate,sample_rate,channels' -of json $outputPath

