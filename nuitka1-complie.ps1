$start_time = Get-Uptime
Write-Output $start_time
python3.8.exe -m nuitka --jobs=24 --clang --lto=no --mingw64 --show-memory --show-progress --output-dir=build/nuitka1 --include-data-dir=./configs=./configs --include-data-dir=./libs/fonts=./libs/fonts --include-data-dir=./textures=./textures --include-data-dir=./libs/pyglet=./pyglet --enable-plugin=numpy --nofollow-import-to=objprint,numpy,pillow,cffi,PIL,pyglet --standalone $args .\DR.py
$end_time = Get-Uptime
$out = $end_time.TotalMilliseconds - $start_time.TotalMilliseconds
Write-Output $end_time.TotalSeconds $start_time.TotalSeconds $out s
Write-Output $start_time $end_time
Write-Output "--jobs=24 --clang --mingw64 --lto=no and ($args)"
# --include-data-dir=./libs/pyglet=./pyglet
# --run
# --disable-ccache
