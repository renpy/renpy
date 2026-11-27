# Windows development

`run.ps1` is the Windows equivalent of `run.sh`. Set up these two things first:

- **llvm-mingw.** Download an `llvm-mingw-*-ucrt` ZIP from the
  [llvm-mingw releases](https://github.com/mstorsjo/llvm-mingw/releases),
  extract it, and add its `bin` directory to `PATH`.
- **windev.** If `lib\py3-windows-x86_64\dev` does not exist, download
  `renpy-*-windev.zip` and extract it into the repository root, which creates
  that directory. Take it from
  `https://nightly.renpy.org/current-8`, or from
  `https://nightly.renpy.org/current-8-fix/` on the `fix` branch. Never mix
  master and fix archives. If compilation fails, replace it with the latest
  windev archive for your branch.
