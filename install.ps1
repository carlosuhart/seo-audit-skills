$SkillsDir = "$env:USERPROFILE\.claude\skills"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

if (-not (Test-Path $SkillsDir)) {
    New-Item -ItemType Directory -Path $SkillsDir | Out-Null
}

# Copies each skill folder in full (SKILL.md, references/, scripts/), skipping downloaded
# third-party binaries (vendor/) and Python caches. Existing local files that are not in the
# repo (for example a private references/casos-privados.md) are left untouched.
$count = 0
Get-ChildItem -Path "$ScriptDir\skills" -Directory | ForEach-Object {
    $skillName = $_.Name
    $srcDir = $_.FullName
    if (Test-Path (Join-Path $srcDir "SKILL.md")) {
        $destDir = Join-Path $SkillsDir $skillName
        Get-ChildItem -Path $srcDir -Recurse -File | Where-Object {
            $_.FullName -notmatch '\\(vendor|__pycache__)\\'
        } | ForEach-Object {
            $rel = $_.FullName.Substring($srcDir.Length).TrimStart('\')
            $dest = Join-Path $destDir $rel
            $parent = Split-Path -Parent $dest
            if (-not (Test-Path $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
            Copy-Item -Path $_.FullName -Destination $dest -Force
        }
        Write-Host "Installed: $skillName"
        $count++
    }
}

Write-Host "Done. $count skills installed to $SkillsDir"
Write-Host "Skills that need a third-party download (e.g. accesibilidad-wcag) explain it in their SKILL.md."
