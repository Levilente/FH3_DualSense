# Publishing a release

The release must contain **only the DLL** as an asset.

1. Build (see the README): the result is `build/DualSense.dll`.
2. Test the DLL in game once, **without** hot reload: the platform's `fh3-mods\platform.log` should show the mod's lines (with `Log=1`) without errors; plug in a DualSense, drive, open the menus.
3. Make sure the version in `CMakeLists.txt` (`project(... VERSION x.y.z)`), `CHANGELOG.md` and the tag agree (current: `1.4.0`). The platform's update check compares the GitHub release tag (a leading `v` is ignored) with the version the mod registers. It only works for a public repository.
4. Tag and publish:

```sh
git tag v1.4.0
git push origin v1.4.0
gh release create v1.4.0 build/DualSense.dll --title "DualSense for FH3 1.4.0" --notes-file release-notes.md
```

`release-notes.md` can be the matching section of [CHANGELOG.md](CHANGELOG.md) plus the requirements line from the README (FH3 Mod Platform 1.1.1 or newer). Do not attach source archives, ini files or anything else.

The DLL is build output and is listed in `.gitignore`; it is never committed.
