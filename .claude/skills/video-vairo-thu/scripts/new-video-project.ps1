[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)]
  [string]$ProjectPath,

  [string]$Title = 'Video vairo thú'
)

$ErrorActionPreference = 'Stop'
$fullProjectPath = [IO.Path]::GetFullPath($ProjectPath)
$pathRoot = [IO.Path]::GetPathRoot($fullProjectPath)
if ($fullProjectPath.TrimEnd('\', '/') -eq $pathRoot.TrimEnd('\', '/')) {
  throw 'ProjectPath không được là thư mục gốc của ổ đĩa.'
}

if (Test-Path -LiteralPath $fullProjectPath) {
  $existing = Get-ChildItem -LiteralPath $fullProjectPath -Force -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($existing) { throw "Thư mục dự án đã có dữ liệu: $fullProjectPath" }
}

$skillRoot = Split-Path -Parent $PSScriptRoot
$templateRoot = Join-Path $skillRoot 'assets\project-template'
if (-not (Test-Path -LiteralPath $templateRoot)) { throw "Thiếu template: $templateRoot" }

@('images', 'flow', 'audio', 'work', 'qa') | ForEach-Object {
  New-Item -ItemType Directory -Path (Join-Path $fullProjectPath $_) -Force | Out-Null
}

$rootTemplates = @('BRIEF.md', 'SCRIPT.md', 'STORYBOARD.md', 'flow-prompts.md', 'takes.json', 'timeline.json')
foreach ($name in $rootTemplates) {
  $content = Get-Content -LiteralPath (Join-Path $templateRoot $name) -Raw
  $content = $content.Replace('{{TITLE}}', $Title)
  Set-Content -LiteralPath (Join-Path $fullProjectPath $name) -Value $content -Encoding utf8
}

$captionContent = Get-Content -LiteralPath (Join-Path $templateRoot 'captions.ass') -Raw
$captionContent = $captionContent.Replace('{{TITLE}}', $Title)
Set-Content -LiteralPath (Join-Path $fullProjectPath 'work\captions.ass') -Value $captionContent -Encoding utf8

Write-Output "Đã tạo dự án: $fullProjectPath"
Write-Output 'Tiếp theo: điền brief/kịch bản/storyboard, tạo ảnh, clip Flow, thoại và timeline.'

